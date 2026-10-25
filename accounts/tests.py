from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class RegistrationTests(TestCase):
    def registration_data(self, **overrides):
        data = {
            "username": "kararsiz",
            "email": "kararsiz@example.com",
            "password1": "Guclu-Bir-Parola-2026!",
            "password2": "Guclu-Bir-Parola-2026!",
        }
        data.update(overrides)
        return data

    def test_register_creates_user_logs_in_and_hides_email_from_home(self):
        response = self.client.post(reverse("accounts:register"), self.registration_data())

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="kararsiz").exists())
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get().pk)

        home = self.client.get(reverse("home"))
        self.assertContains(home, "@kararsiz")
        self.assertNotContains(home, "kararsiz@example.com")

    def test_username_is_unique_ignoring_case(self):
        User.objects.create_user("Kararsiz", "first@example.com", "Guclu-Parola-2026!")
        response = self.client.post(
            reverse("accounts:register"),
            self.registration_data(username="kararsiz", email="second@example.com"),
        )
        self.assertContains(response, "Bu kullanıcı adı zaten kullanılıyor.")
        self.assertEqual(User.objects.count(), 1)

    def test_email_is_unique_ignoring_case(self):
        User.objects.create_user("birinci", "User@Example.com", "Guclu-Parola-2026!")
        response = self.client.post(
            reverse("accounts:register"),
            self.registration_data(username="ikinci", email="user@example.com"),
        )
        self.assertContains(response, "Bu e-posta adresi zaten kullanılıyor.")
        self.assertEqual(User.objects.count(), 1)

    def test_unsafe_next_is_not_used_after_registration(self):
        response = self.client.post(
            reverse("accounts:register") + "?next=https://example.org/steal",
            self.registration_data(),
        )
        self.assertRedirects(response, reverse("home"))


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="deniz",
            email="deniz@example.com",
            password="Guclu-Parola-2026!",
        )

    def test_user_can_log_in_and_session_persists(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "deniz", "password": "Guclu-Parola-2026!"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(self.client.get(reverse("home")).context["user"].is_authenticated)

    def test_logout_requires_post(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)

        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_admin_requires_staff_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)


class PublicHomeTests(TestCase):
    def test_home_is_public_and_shows_phase_one_empty_state(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Şimdilik sessiz buralar")
