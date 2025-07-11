from django.utils import timezone
from django.db import models

class CompatibilityResult(models.Model):
    name1 = models.CharField(max_length=255)
    name2 = models.CharField(max_length=255)
    compatibility_score = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)  # Store latitude
    longitude = models.FloatField(null=True, blank=True)  # Store longitude
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name1} & {self.name2}: {self.compatibility_score}%"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('compatibility_result_detail', kwargs={'id': self.id})

class SubscriptionUser(models.Model):
    PLATFORM_CHOICES = (
        ('apple', 'Apple'),
        ('google', 'Google'),
    )

    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    unique_subscription_id = models.CharField(max_length=255, unique=True)  # original_transaction_id or purchaseToken
    product_id = models.CharField(max_length=255)
    expiration_date = models.DateTimeField(null=True, blank=True)
    auto_renewing = models.BooleanField(default=False)
    last_validated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    limit = models.IntegerField(default=3)
    status = models.CharField(max_length=255, default='active')

    def __str__(self):
        return f"{self.platform} - {self.unique_subscription_id}"

    def is_expired(self):
        return timezone.now() > self.expiration_date