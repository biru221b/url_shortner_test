from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .utils import base62_encode, BASE62_SALT


class ShortURL(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    long_url = models.URLField()
    short_key = models.CharField(max_length=16, unique=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    click_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_key} -> {self.long_url}"

    def clean(self):
        parsed = urlparse(self.long_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValidationError({"long_url": "Only http/https URLs are allowed."})

    @property
    def is_expired(self):
        return self.expires_at is not None and self.expires_at <= timezone.now()

    def _generate_short_key(self):
        i = 0
        while True:
            candidate = base62_encode(self.id + BASE62_SALT + i)
            if not ShortURL.objects.filter(short_key=candidate).exists():
                return candidate
            i += 1

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)
        if creating and not self.short_key:
            self.short_key = self._generate_short_key()
            super().save(update_fields=["short_key"])
