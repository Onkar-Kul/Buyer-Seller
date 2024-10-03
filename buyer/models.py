from django.db import models

from accounts.models import User


# Create your models here.
class PurchaseRequest(models.Model):
    STATUS_CHOICES = (('In-Process', 'In-Process'),
                      ('Approved', 'Approved'),
                      ('Rejected', 'Rejected'))
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_requests', null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_requests', null=True, blank=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES, default='In-Process')
    description = models.TextField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


