from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Count, Prefetch
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PollForm, PollOptionFormSet
from .guest_identity import new_guest_identity, read_guest_id, set_guest_cookie
from .models import Poll, PollOption, Vote


def _vote_for_request(request, poll):
    if request.user.is_authenticated:
        return Vote.objects.filter(poll=poll, user=request.user).first()
    guest_id = read_guest_id(request)
    if guest_id:
        return Vote.objects.filter(poll=poll, guest_id=guest_id).first()
    return None


def _poll_with_totals():
    return (
        Poll.objects.select_related("author")
        .prefetch_related(Prefetch("options", queryset=PollOption.objects.order_by("position")))
        .annotate(total_votes=Count("votes"))
    )


def home(request):
    polls = (
        Poll.objects.filter(is_published=True)
        .select_related("author")
        .prefetch_related(Prefetch("options", queryset=PollOption.objects.order_by("position")))
        .annotate(total_votes=Count("votes"))
        .order_by("-created_at", "-id")
    )
    page_obj = Paginator(polls, 12).get_page(request.GET.get("sayfa"))
    return render(request, "polls/feed.html", {"page_obj": page_obj})


def poll_detail(request, poll_id):
    poll = get_object_or_404(
        Poll.objects.select_related("author"),
        pk=poll_id,
        is_published=True,
    )
    signed_guest_value = None
    if request.user.is_authenticated:
        selected_vote = Vote.objects.filter(poll=poll, user=request.user).first()
    else:
        guest_id = read_guest_id(request)
        if guest_id is None:
            guest_id, signed_guest_value = new_guest_identity()
        selected_vote = Vote.objects.filter(poll=poll, guest_id=guest_id).first()
    options = list(poll.options.annotate(vote_count=Count("votes")).order_by("position"))
    total_votes = sum(option.vote_count for option in options)
    if selected_vote:
        for option in options:
            option.percentage = round((option.vote_count / total_votes) * 100) if total_votes else 0

    response = render(
        request,
        "polls/detail.html",
        {
            "poll": poll,
            "options": options,
            "selected_vote": selected_vote,
            "total_votes": total_votes,
        },
    )
    if signed_guest_value is not None:
        set_guest_cookie(response, signed_guest_value)
    return response


def vote(request, poll_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    poll = get_object_or_404(Poll, pk=poll_id, is_published=True)
    option_id = request.POST.get("option_id")
    option = None
    if option_id:
        try:
            option = poll.options.filter(pk=option_id).first()
        except (TypeError, ValueError):
            option = None
    if option is None:
        messages.error(request, "Lütfen bu ankete ait bir seçenek seç.")
        return redirect("polls:detail", poll_id=poll.id)

    existing_vote = _vote_for_request(request, poll)
    if existing_vote:
        messages.info(request, "Bu ankette zaten oy kullandın.")
        return redirect("polls:detail", poll_id=poll.id)

    signed_guest_value = None
    vote_fields = {"poll": poll, "option": option}
    if request.user.is_authenticated:
        vote_fields["user"] = request.user
    else:
        guest_id = read_guest_id(request)
        if guest_id is None:
            guest_id, signed_guest_value = new_guest_identity()
        vote_fields["guest_id"] = guest_id

    try:
        with transaction.atomic():
            Vote.objects.create(**vote_fields)
    except IntegrityError:
        messages.info(request, "Bu ankette zaten oy kullandın.")
    else:
        messages.success(request, "Oyunu aldık! İşte sonuçlar.")

    response = redirect("polls:detail", poll_id=poll.id)
    if signed_guest_value is not None:
        set_guest_cookie(response, signed_guest_value)
    return response


@login_required
def create_poll(request):
    poll_form = PollForm(request.POST or None)
    option_formset = PollOptionFormSet(request.POST or None, prefix="options")

    if request.method == "POST" and poll_form.is_valid() and option_formset.is_valid():
        with transaction.atomic():
            poll = poll_form.save(commit=False)
            poll.author = request.user
            poll.save()
            PollOption.objects.bulk_create(
                [
                    PollOption(poll=poll, text=form.cleaned_data["text"], position=position)
                    for position, form in enumerate(option_formset.forms, start=1)
                    if form.cleaned_data.get("text")
                ]
            )
        messages.success(request, "Anketin yayınlandı!")
        return redirect("polls:detail", poll_id=poll.id)

    return render(
        request,
        "polls/create.html",
        {"poll_form": poll_form, "option_formset": option_formset},
    )


@login_required
def my_polls(request):
    polls = (
        Poll.objects.filter(author=request.user)
        .prefetch_related("options")
        .annotate(total_votes=Count("votes"))
        .order_by("-created_at", "-id")
    )
    page_obj = Paginator(polls, 12).get_page(request.GET.get("sayfa"))
    return render(request, "polls/mine.html", {"page_obj": page_obj})
