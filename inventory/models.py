from django.db import models
from django.conf import settings


class Item(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50)  # per-user unique via Meta
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="items_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items_updated",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    class Meta:
        # same SKU allowed for different users, but not repeated for one user
        unique_together = ("created_by", "sku")


class SellRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sell_records",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="sales",
    )
    quantity = models.PositiveIntegerField()
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def revenue(self):
        return self.quantity * self.sell_price

    @property
    def cost(self):
        return self.quantity * self.item.unit_price

    @property
    def profit(self):
        return self.revenue - self.cost
