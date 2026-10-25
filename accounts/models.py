from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    username = models.CharField(
        "kullanıcı adı",
        max_length=24,
        unique=True,
        validators=[UnicodeUsernameValidator(), MinLengthValidator(3)],
        help_text="3–24 karakter. Harf, rakam ve @/./+/-/_ kullanılabilir.",
        error_messages={"unique": "Bu kullanıcı adı zaten kullanılıyor."},
    )
    email = models.EmailField(
        "e-posta adresi",
        unique=True,
        error_messages={"unique": "Bu e-posta adresi zaten kullanılıyor."},
    )

    class Meta:
        verbose_name = "kullanıcı"
        verbose_name_plural = "kullanıcılar"
        constraints = [
            models.UniqueConstraint(Lower("username"), name="accounts_user_username_ci_unique"),
            models.UniqueConstraint(Lower("email"), name="accounts_user_email_ci_unique"),
        ]

    def save(self, *args, **kwargs):
        self.username = self.username.strip()
        self.email = self.__class__.objects.normalize_email(self.email).lower()
        super().save(*args, **kwargs)
