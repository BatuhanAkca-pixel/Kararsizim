import uuid

from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.db.models import Q


class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="polls",
        verbose_name="yazar",
    )
    question = models.CharField(
        "soru",
        max_length=180,
        validators=[MinLengthValidator(12)],
    )
    description = models.TextField(
        "açıklama",
        blank=True,
        validators=[MaxLengthValidator(500)],
    )
    created_at = models.DateTimeField("oluşturulma zamanı", auto_now_add=True)
    is_published = models.BooleanField("yayında", default=True)

    class Meta:
        ordering = ("-created_at", "-id")
        verbose_name = "anket"
        verbose_name_plural = "anketler"

    def __str__(self):
        return self.question


class PollOption(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="anket",
    )
    text = models.CharField(
        "seçenek",
        max_length=80,
        validators=[MinLengthValidator(2)],
    )
    position = models.PositiveSmallIntegerField("sıra")

    class Meta:
        ordering = ("position",)
        verbose_name = "anket seçeneği"
        verbose_name_plural = "anket seçenekleri"
        constraints = [
            models.UniqueConstraint(fields=("poll", "position"), name="poll_option_position_unique"),
            models.CheckConstraint(
                condition=Q(position__gte=1, position__lte=5),
                name="poll_option_position_between_1_and_5",
            ),
        ]

    def __str__(self):
        return self.text


class Vote(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="votes",
        verbose_name="anket",
    )
    option = models.ForeignKey(
        PollOption,
        on_delete=models.CASCADE,
        related_name="votes",
        verbose_name="seçenek",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="votes",
        null=True,
        blank=True,
        verbose_name="kullanıcı",
    )
    guest_id = models.UUIDField("misafir kimliği", null=True, blank=True)
    created_at = models.DateTimeField("oy zamanı", auto_now_add=True)

    class Meta:
        verbose_name = "oy"
        verbose_name_plural = "oylar"
        constraints = [
            models.CheckConstraint(
                condition=(
                    (Q(user__isnull=False) & Q(guest_id__isnull=True))
                    | (Q(user__isnull=True) & Q(guest_id__isnull=False))
                ),
                name="vote_exactly_one_voter_identity",
            ),
            models.UniqueConstraint(
                fields=("poll", "user"),
                condition=Q(user__isnull=False),
                name="vote_one_per_registered_user",
            ),
            models.UniqueConstraint(
                fields=("poll", "guest_id"),
                condition=Q(guest_id__isnull=False),
                name="vote_one_per_guest_identity",
            ),
        ]

    def clean(self):
        super().clean()
        if self.option_id and self.poll_id and self.option.poll_id != self.poll_id:
            from django.core.exceptions import ValidationError

            raise ValidationError({"option": "Seçilen seçenek bu ankete ait değil."})

    def __str__(self):
        return f"{self.poll} — {self.option}"
