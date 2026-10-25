import unicodedata

from django import forms
from django.forms import BaseFormSet, formset_factory

from .models import Poll, PollOption


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ("question", "description")
        labels = {"question": "Sorun", "description": "Açıklama (isteğe bağlı)"}
        widgets = {
            "question": forms.TextInput(
                attrs={
                    "placeholder": "Örn. Bu akşam sinemaya mı gitsem, evde mi kalsam?",
                    "maxlength": 180,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "maxlength": 500,
                    "placeholder": "İstersen biraz daha bağlam ekle.",
                }
            ),
        }

    def clean_question(self):
        question = " ".join(self.cleaned_data["question"].split())
        if len(question) < 12:
            raise forms.ValidationError("Soru en az 12 karakter olmalı.")
        return question

    def clean_description(self):
        return self.cleaned_data["description"].strip()


class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ("text",)
        labels = {"text": "Seçenek"}
        widgets = {
            "text": forms.TextInput(
                attrs={"maxlength": 80, "placeholder": "Seçeneğini yaz"}
            )
        }

    def clean_text(self):
        text = " ".join(self.cleaned_data["text"].split())
        if len(text) < 2:
            raise forms.ValidationError("Seçenek en az 2 karakter olmalı.")
        return text


class BasePollOptionFormSet(BaseFormSet):
    default_error_messages = {
        "too_few_forms": "Bir ankette en az 2, en fazla 5 seçenek olmalı.",
        "too_many_forms": "Bir ankette en az 2, en fazla 5 seçenek olmalı.",
        "missing_management_form": "Seçenek formu bilgileri eksik veya değiştirilmiş.",
    }

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        option_texts = []
        for form in self.forms:
            text = form.cleaned_data.get("text", "").strip()
            if text:
                option_texts.append(text)

        if not 2 <= len(option_texts) <= 5:
            raise forms.ValidationError("Bir ankette en az 2, en fazla 5 seçenek olmalı.")

        normalized = [unicodedata.normalize("NFKC", text).casefold() for text in option_texts]
        if len(normalized) != len(set(normalized)):
            raise forms.ValidationError("Aynı seçenek bir ankette birden fazla kez kullanılamaz.")


PollOptionFormSet = formset_factory(
    PollOptionForm,
    formset=BasePollOptionFormSet,
    extra=0,
    min_num=2,
    max_num=5,
    validate_min=True,
    validate_max=True,
)
