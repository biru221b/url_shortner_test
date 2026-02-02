from django import forms
from django.utils import timezone

from .models import ShortURL


class ShortURLForm(forms.ModelForm):
    expires_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = ShortURL
        fields = ["long_url", "expires_at", "is_active"]

    def clean_expires_at(self):
        expires_at = self.cleaned_data.get("expires_at")
        if expires_at and expires_at <= timezone.now():
            raise forms.ValidationError("Expiration must be in the future.")
        return expires_at
