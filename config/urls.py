from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from django.conf import settings
from django.views.static import serve
import os

from inventory.models import Item, SellRecord


@login_required
def dashboard_view(request):
    # Only this user's items
    qs_items = Item.objects.filter(is_active=True, created_by=request.user)
    qs_sales = SellRecord.objects.filter(user=request.user)

    total_items = qs_items.count()
    low_stock_items = qs_items.filter(quantity__lt=5).count()
    total_value = qs_items.aggregate(
        total=models.Sum(models.F("quantity") * models.F("unit_price"))
    )["total"] or 0

    totals = qs_sales.aggregate(
        invested=models.Sum(models.F("quantity") * models.F("item__unit_price")),
        revenue=models.Sum(models.F("quantity") * models.F("sell_price")),
    )
    money_invested = totals["invested"] or 0
    revenue = totals["revenue"] or 0
    profit = revenue - money_invested

    context = {
        "total_items": total_items,
        "low_stock_items": low_stock_items,
        "total_value": total_value,
        "money_invested": money_invested,
        "revenue": revenue,
        "profit": profit,
    }
    return render(request, "dashboard.html", context)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("inventory/", include("inventory.urls")),
    path("", dashboard_view, name="dashboard"),
]

# Serve static files from STATIC_ROOT during local development (HTTPS dev server)
if os.environ.get("DEV_SERVE_STATIC", "1") == "1":
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
