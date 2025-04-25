from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class IPOListing(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    company_name = models.CharField(max_length=200)
    symbol = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Z0-9]+$',
                message='Symbol must contain only uppercase letters and numbers'
            )
        ]
    )
    issue_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    lot_size = models.PositiveIntegerField()
    total_issue_size = models.PositiveIntegerField()
    subscription_start = models.DateTimeField()
    subscription_end = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.symbol})"

    def clean(self):
        if self.subscription_end <= self.subscription_start:
            raise ValidationError("Subscription end date must be after start date")

    class Meta:
        ordering = ['-subscription_start']
        verbose_name = 'IPO Listing'
        verbose_name_plural = 'IPO Listings'

class IPOApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    ipo = models.ForeignKey(
        IPOListing,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    lots_applied = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    application_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.ipo.company_name}"

    def clean(self):
        if self.lots_applied > self.ipo.total_issue_size:
            raise ValidationError("Lots applied cannot exceed total issue size")

    class Meta:
        ordering = ['-application_date']
        verbose_name = 'IPO Application'
        verbose_name_plural = 'IPO Applications'
        unique_together = ['user', 'ipo'] 