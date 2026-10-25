from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from polls.models import Poll, PollOption, Vote


DEMO_POLLS = [
    {
        "username": "elifkarar",
        "question": "Bu hafta sonu deniz kenarına mı gitsek, ormana mı?",
        "description": "Hava ikisi için de güzel görünüyor; kısa bir kaçamak yapacağız.",
        "options": ["Deniz kenarı", "Orman yürüyüşü"],
        "votes": [0, 1, 0, 0, 1],
    },
    {
        "username": "mertdusunuyor",
        "question": "Yeni çalışma masam için hangi rengi seçmeliyim?",
        "description": "Oda açık renkli ve gün boyunca bol ışık alıyor.",
        "options": ["Doğal ahşap", "Mat beyaz", "Antrasit"],
        "votes": [0, 0, 1, 0, 2, 0],
    },
    {
        "username": "zeynepsoruyor",
        "question": "Arkadaş buluşmasında hangi tatlıyı hazırlayayım?",
        "description": "Sekiz kişiyiz; kolay paylaşılabilen bir şey olsun.",
        "options": ["San Sebastian", "Brownie", "Tiramisu", "Magnolia"],
        "votes": [1, 1, 2, 0, 1, 2, 1],
    },
    {
        "username": "cansecemedi",
        "question": "Akşam evde film mi izleyelim, dışarı mı çıkalım?",
        "description": "Yoğun bir haftanın ardından sakinlik ve eğlence arasında kaldık.",
        "options": ["Evde film gecesi", "Dışarı çıkalım"],
        "votes": [0, 1, 1, 1],
    },
    {
        "username": "selinfikir",
        "question": "Bir sonraki kısa tatil için hangi şehri seçelim?",
        "description": "Tarih, yemek ve yürüyerek keşfedilecek sokaklar önceliğimiz.",
        "options": ["Eskişehir", "İzmir", "Mardin", "Kapadokya", "Antalya"],
        "votes": [2, 1, 2, 2, 3, 1, 0, 2],
    },
    {
        "username": "burakkarar",
        "question": "Sabah rutinine spor mu, kitap mı eklemek daha iyi?",
        "description": "İkisine birden vakit ayıramıyorum; birini düzenli hale getirmek istiyorum.",
        "options": ["20 dakika spor", "30 dakika kitap", "Günlere böl"],
        "votes": [0, 2, 2, 1, 2],
    },
]


class Command(BaseCommand):
    help = "Yerel önizleme için farklı kullanıcılara ait örnek anketler oluşturur."

    def handle(self, *args, **options):
        if connection.vendor != "sqlite":
            raise CommandError(
                "Güvenlik nedeniyle demo verisi yalnızca TEST_SQLITE=1 ile SQLite üzerinde oluşturulur."
            )

        User = get_user_model()
        authors = {}
        voters = []

        with transaction.atomic():
            for poll_data in DEMO_POLLS:
                username = poll_data["username"]
                author, created = User.objects.get_or_create(
                    username=username,
                    defaults={"email": f"{username}@example.invalid"},
                )
                if created:
                    author.set_unusable_password()
                    author.save(update_fields=["password"])
                authors[username] = author

            for number in range(1, 9):
                username = f"demo_oycu_{number}"
                voter, created = User.objects.get_or_create(
                    username=username,
                    defaults={"email": f"{username}@example.invalid"},
                )
                if created:
                    voter.set_unusable_password()
                    voter.save(update_fields=["password"])
                voters.append(voter)

            for poll_data in DEMO_POLLS:
                poll, _ = Poll.objects.update_or_create(
                    author=authors[poll_data["username"]],
                    question=poll_data["question"],
                    defaults={
                        "description": poll_data["description"],
                        "is_published": True,
                    },
                )
                poll_options = []
                for position, text in enumerate(poll_data["options"], start=1):
                    option, _ = PollOption.objects.update_or_create(
                        poll=poll,
                        position=position,
                        defaults={"text": text},
                    )
                    poll_options.append(option)

                for voter, option_index in zip(voters, poll_data["votes"]):
                    Vote.objects.update_or_create(
                        poll=poll,
                        user=voter,
                        defaults={"option": poll_options[option_index], "guest_id": None},
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo hazır: {len(DEMO_POLLS)} anket, "
                f"{Poll.objects.filter(author__in=authors.values()).count()} yayınlanmış kayıt."
            )
        )
