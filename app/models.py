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

