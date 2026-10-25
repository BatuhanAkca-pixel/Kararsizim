from django.contrib.auth import get_user_model
from unittest.mock import patch

from django.core import signing
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from .guest_identity import COOKIE_NAME, COOKIE_SALT
from .models import Poll, PollOption, Vote


User = get_user_model()


class PollTestMixin:
    def setUp(self):
        self.user = User.objects.create_user(
            username="yazar",
            email="yazar@example.com",
            password="Guclu-Parola-2026!",
        )

    def create_poll(self, author=None, question="Bu akşam hangi filmi izleyelim?", published=True):
        poll = Poll.objects.create(
            author=author or self.user,
            question=question,
            is_published=published,
        )
        PollOption.objects.create(poll=poll, text="Komedi", position=1)
        PollOption.objects.create(poll=poll, text="Bilim kurgu", position=2)
        return poll

    def form_data(self, options, **poll_fields):
        data = {
            "question": "Bu akşam hangi filmi izleyelim?",
            "description": "Hep birlikte karar verelim.",
            "options-TOTAL_FORMS": str(len(options)),
            "options-INITIAL_FORMS": "0",
            "options-MIN_NUM_FORMS": "2",
            "options-MAX_NUM_FORMS": "5",
        }
        data.update({f"options-{index}-text": text for index, text in enumerate(options)})
        data.update(poll_fields)
        return data


class PollCreationTests(PollTestMixin, TestCase):
    def test_create_page_starts_with_exactly_two_option_rows(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("polls:create"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["option_formset"].total_form_count(), 2)

    def test_guest_is_redirected_to_login(self):
        response = self.client.get(reverse("polls:create"))
        expected = f"{reverse('accounts:login')}?next={reverse('polls:create')}"
        self.assertRedirects(response, expected)

    def test_member_creates_poll_with_two_options_atomically(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("polls:create"), self.form_data(["Sinema", "Restoran"]))

        poll = Poll.objects.get()
        self.assertRedirects(response, reverse("polls:detail", args=[poll.id]))
        self.assertEqual(poll.author, self.user)
        self.assertEqual(list(poll.options.values_list("text", flat=True)), ["Sinema", "Restoran"])

    def test_member_can_create_poll_with_five_options(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("polls:create"),
            self.form_data(["Bir", "İki", "Üç", "Dört", "Beş"]),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PollOption.objects.count(), 5)

    def test_one_or_six_options_are_rejected_without_partial_poll(self):
        self.client.force_login(self.user)
        for options in (["Tek"], ["Bir", "İki", "Üç", "Dört", "Beş", "Altı"]):
            with self.subTest(count=len(options)):
                response = self.client.post(reverse("polls:create"), self.form_data(options))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "en az 2, en fazla 5 seçenek")
                self.assertEqual(Poll.objects.count(), 0)

    def test_blank_and_normalized_duplicate_options_are_rejected(self):
        self.client.force_login(self.user)
        cases = [(["   ", "Geçerli"], "Bu alan zorunludur"), (["Sinema", " sinema "], "birden fazla")]
        for options, message in cases:
            with self.subTest(options=options):
                response = self.client.post(reverse("polls:create"), self.form_data(options))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, message)
                self.assertEqual(Poll.objects.count(), 0)

    def test_failed_form_keeps_safe_values(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("polls:create"),
            self.form_data(["Aynı", " aynı "], question="Korunması gereken soru metni"),
        )
        self.assertContains(response, "Korunması gereken soru metni")
        self.assertContains(response, "Aynı")


class PublicPollTests(PollTestMixin, TestCase):
    def test_public_feed_lists_published_poll_without_email(self):
        poll = self.create_poll()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, poll.question)
        self.assertContains(response, "@yazar")
        self.assertNotContains(response, self.user.email)

    def test_unpublished_poll_is_hidden_and_detail_is_404(self):
        poll = self.create_poll(published=False)
        self.assertNotContains(self.client.get(reverse("home")), poll.question)
        self.assertEqual(self.client.get(reverse("polls:detail", args=[poll.id])).status_code, 404)

    def test_feed_is_newest_first_and_paginated_by_twelve(self):
        for number in range(13):
            self.create_poll(question=f"Karar vermek için yeterli soru {number:02d}?")
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["page_obj"]), 12)
        ids = [poll.id for poll in response.context["page_obj"]]
        expected_ids = list(Poll.objects.filter(is_published=True).values_list("id", flat=True)[:12])
        self.assertEqual(ids, expected_ids)

    def test_detail_escapes_user_supplied_html(self):
        poll = self.create_poll(question="<script>alert('x')</script> güvenli mi?")
        response = self.client.get(reverse("polls:detail", args=[poll.id]))
        self.assertNotContains(response, "<script>alert('x')</script>", html=False)
        self.assertContains(response, "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;", html=False)


class MyPollsTests(PollTestMixin, TestCase):
    def test_my_polls_requires_login_and_only_lists_owner_records(self):
        own_poll = self.create_poll()
        other = User.objects.create_user("diger", "diger@example.com", "Guclu-Parola-2026!")
        other_poll = self.create_poll(author=other, question="Başka kullanıcının yeterince uzun sorusu?")

        anonymous = self.client.get(reverse("polls:mine"))
        self.assertEqual(anonymous.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.get(reverse("polls:mine"))
        self.assertContains(response, own_poll.question)
        self.assertNotContains(response, other_poll.question)


class VoteConstraintTests(PollTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.poll = self.create_poll()
        self.option = self.poll.options.first()

    def test_vote_requires_exactly_one_identity(self):
        invalid_votes = [
            Vote(poll=self.poll, option=self.option),
            Vote(poll=self.poll, option=self.option, user=self.user, guest_id="3bb02d56-c36d-4f85-9496-49b395612f0b"),
        ]
        for vote in invalid_votes:
            with self.subTest(vote=vote):
                with self.assertRaises(IntegrityError), transaction.atomic():
                    Vote.objects.create(
                        poll=vote.poll,
                        option=vote.option,
                        user=vote.user,
                        guest_id=vote.guest_id,
                    )

    def test_database_rejects_duplicate_registered_and_guest_votes(self):
        Vote.objects.create(poll=self.poll, option=self.option, user=self.user)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Vote.objects.create(poll=self.poll, option=self.poll.options.last(), user=self.user)

        guest_id = "3bb02d56-c36d-4f85-9496-49b395612f0b"
        Vote.objects.create(poll=self.poll, option=self.option, guest_id=guest_id)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Vote.objects.create(poll=self.poll, option=self.poll.options.last(), guest_id=guest_id)

    def test_model_validation_rejects_option_from_another_poll(self):
        other_poll = self.create_poll(question="Başka bir ankette hangi seçeneği seçelim?")
        vote = Vote(poll=self.poll, option=other_poll.options.first(), user=self.user)
        with self.assertRaisesMessage(ValidationError, "Seçilen seçenek bu ankete ait değil"):
            vote.full_clean()


class VotingFlowTests(PollTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.poll = self.create_poll()
        self.first_option, self.second_option = self.poll.options.all()
        self.vote_url = reverse("polls:vote", args=[self.poll.id])
        self.detail_url = reverse("polls:detail", args=[self.poll.id])

    def test_guest_can_vote_and_receives_signed_securely_scoped_cookie(self):
        response = self.client.post(self.vote_url, {"option_id": self.first_option.id})

        self.assertRedirects(response, self.detail_url)
        vote = Vote.objects.get()
        self.assertIsNone(vote.user)
        cookie = response.cookies[COOKIE_NAME]
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["samesite"], "Lax")
        self.assertTrue(cookie["secure"])
        decoded = signing.loads(cookie.value, salt=COOKIE_SALT)
        self.assertEqual(decoded, str(vote.guest_id))

        detail = self.client.get(self.detail_url)
        self.assertContains(detail, "100% · 1 oy")
        self.assertContains(detail, "senin oyun")
        self.assertNotContains(detail, "Oyumu gönder")

    def test_detail_assigns_guest_identity_before_vote(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(COOKIE_NAME, response.cookies)
        decoded = signing.loads(response.cookies[COOKIE_NAME].value, salt=COOKIE_SALT)

        self.client.post(self.vote_url, {"option_id": self.first_option.id})
        self.assertEqual(str(Vote.objects.get().guest_id), decoded)

    def test_same_guest_cannot_vote_twice(self):
        self.client.post(self.vote_url, {"option_id": self.first_option.id})
        response = self.client.post(
            self.vote_url,
            {"option_id": self.second_option.id},
            follow=True,
        )
        self.assertEqual(Vote.objects.count(), 1)
        self.assertContains(response, "Bu ankette zaten oy kullandın.")

    def test_registered_user_cannot_vote_twice(self):
        self.client.force_login(self.user)
        self.client.post(self.vote_url, {"option_id": self.first_option.id})
        response = self.client.post(self.vote_url, {"option_id": self.second_option.id}, follow=True)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertContains(response, "Bu ankette zaten oy kullandın.")

    def test_option_from_another_poll_is_rejected(self):
        other_poll = self.create_poll(question="Diğer ankette hangi seçeneği işaretleyelim?")
        response = self.client.post(
            self.vote_url,
            {"option_id": other_poll.options.first().id},
            follow=True,
        )
        self.assertEqual(Vote.objects.count(), 0)
        self.assertContains(response, "Lütfen bu ankete ait bir seçenek seç.")

    def test_missing_option_is_rejected(self):
        response = self.client.post(self.vote_url, {}, follow=True)
        self.assertEqual(Vote.objects.count(), 0)
        self.assertContains(response, "Lütfen bu ankete ait bir seçenek seç.")

    def test_malformed_option_id_is_rejected_without_server_error(self):
        response = self.client.post(self.vote_url, {"option_id": "sayi-degil"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.objects.count(), 0)
        self.assertContains(response, "Lütfen bu ankete ait bir seçenek seç.")

    def test_vote_endpoint_is_post_only(self):
        self.assertEqual(self.client.get(self.vote_url).status_code, 405)

    def test_unpublished_poll_does_not_accept_vote(self):
        self.poll.is_published = False
        self.poll.save(update_fields=["is_published"])
        response = self.client.post(self.vote_url, {"option_id": self.first_option.id})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Vote.objects.count(), 0)

    def test_tampered_cookie_is_replaced_without_error(self):
        self.client.cookies[COOKIE_NAME] = "bozulmus-imza"
        response = self.client.post(self.vote_url, {"option_id": self.first_option.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Vote.objects.count(), 1)
        decoded = signing.loads(response.cookies[COOKIE_NAME].value, salt=COOKIE_SALT)
        self.assertEqual(decoded, str(Vote.objects.get().guest_id))

    def test_integrity_error_from_race_is_shown_as_duplicate_vote(self):
        self.client.force_login(self.user)
        with patch("polls.views.Vote.objects.create", side_effect=IntegrityError):
            response = self.client.post(
                self.vote_url,
                {"option_id": self.first_option.id},
                follow=True,
            )
        self.assertContains(response, "Bu ankette zaten oy kullandın.")
        self.assertEqual(Vote.objects.count(), 0)

    def test_guest_vote_is_not_merged_when_user_logs_in(self):
        self.client.post(self.vote_url, {"option_id": self.first_option.id})
        self.client.force_login(self.user)

        detail = self.client.get(self.detail_url)
        self.assertContains(detail, "Oyumu gönder")

        self.client.post(self.vote_url, {"option_id": self.second_option.id})
        self.assertEqual(Vote.objects.count(), 2)
        self.assertEqual(Vote.objects.filter(user=self.user).count(), 1)

    def test_results_have_correct_counts_and_percentages(self):
        other = User.objects.create_user("oycu", "oycu@example.com", "Guclu-Parola-2026!")
        Vote.objects.create(poll=self.poll, option=self.first_option, user=self.user)
        Vote.objects.create(poll=self.poll, option=self.second_option, user=other)
        self.client.force_login(self.user)

        response = self.client.get(self.detail_url)
        self.assertContains(response, "2 oy")
        self.assertEqual(response.content.decode().count("50% · 1 oy"), 2)

    def test_results_are_hidden_before_voting_but_total_is_public_on_card(self):
        Vote.objects.create(poll=self.poll, option=self.first_option, user=self.user)
        detail = self.client.get(self.detail_url)
        self.assertNotContains(detail, "Sonuçlar")
        self.assertNotContains(detail, "100%")
        self.assertContains(detail, "Oyumu gönder")

        feed = self.client.get(reverse("home"))
        self.assertContains(feed, "1 oy")

    def test_csrf_is_required_for_vote_post(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(self.vote_url, {"option_id": self.first_option.id})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Vote.objects.count(), 0)
