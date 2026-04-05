# reports/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid


class Report(models.Model):

    ## Status choices
    STATUS_OPEN = 'open'
    STATUS_PENDING = 'pending'
    STATUS_CLEARED = 'cleared'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_CLEARED, 'Cleared'),
    ]

    ## Waste type choices
    WASTE_HOUSEHOLD = 'household'
    WASTE_FURNITURE = 'furniture'
    WASTE_TYRES = 'tyres'
    WASTE_CONSTRUCTION = 'construction'
    WASTE_OTHER = 'other'
    WASTE_CHOICES = [
        (WASTE_HOUSEHOLD, 'Household'),
        (WASTE_FURNITURE, 'Furniture'),
        (WASTE_TYRES, 'Tyres'),
        (WASTE_CONSTRUCTION, 'Construction'),
        (WASTE_OTHER, 'Other'),
    ]

    ## Size choices
    SIZE_SMALL = 'small'
    SIZE_MEDIUM = 'medium'
    SIZE_LARGE = 'large'
    SIZE_CHOICES = [
        (SIZE_SMALL, 'Small'),
        (SIZE_MEDIUM, 'Medium'),
        (SIZE_LARGE, 'Large'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports')

    ## Location
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=10, blank=True)

    ## Council routing
    council_name = models.CharField(max_length=255, blank=True)
    council_email = models.EmailField(blank=True)
    council_notified = models.BooleanField(default=False)
    council_notified_at = models.DateTimeField(null=True, blank=True)

    ## Report details
    waste_type = models.CharField(max_length=20, choices=WASTE_CHOICES, default=WASTE_OTHER)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default=SIZE_SMALL)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN)

    ## Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cleared_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.waste_type} - {self.postcode} ({self.status})"


class ReportPhoto(models.Model):
    ## Separate model so each report can have multiple photos
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.report.id}"