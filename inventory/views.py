from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction

from .models import Item, SellRecord, UserProfile
from .forms import ItemForm, SellRecordForm, UserProfileForm
from audit.utils import create_audit_log
from audit.models import AuditLog


@login_required
def item_list(request):

    items = Item.objects.filter(
        is_active=True,
        created_by=request.user,
    )

    search_query = request.GET.get("search")

    if search_query:
        items = items.filter(sku__icontains=search_query)

    return render(
        request,
        "inventory/item_list.html",
        {
            "items": items,
        },
    )


@login_required
def item_create(request):

    if request.method == "POST":

        form = ItemForm(request.POST)

        if form.is_valid():

            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            messages.success(request, "Item created successfully.")

            create_audit_log(
                request,
                AuditLog.Action.CREATE,
                "Item",
                item.pk,
                description=f"Created item {item.name}",
            )

            return redirect("inventory_list")

    else:
        form = ItemForm()

    return render(
        request,
        "inventory/item_form.html",
        {"form": form},
    )


@login_required
def item_update(request, pk):

    item = get_object_or_404(
        Item,
        pk=pk,
        is_active=True,
        created_by=request.user,
    )

    if request.method == "POST":

        form = ItemForm(request.POST, instance=item)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()

            messages.success(request, "Item updated successfully.")

            create_audit_log(
                request,
                AuditLog.Action.UPDATE,
                "Item",
                obj.pk,
                description=f"Updated item {obj.name}",
            )

            return redirect("inventory_list")

    else:
        form = ItemForm(instance=item)

    return render(
        request,
        "inventory/item_form.html",
        {
            "form": form,
            "item": item,
        },
    )


@login_required
def item_delete(request, pk):

    item = get_object_or_404(
        Item,
        pk=pk,
        is_active=True,
        created_by=request.user,
    )

    if request.method == "POST":

        item.is_active = False
        item.save()

        messages.success(request, "Item deleted successfully.")

        create_audit_log(
            request,
            AuditLog.Action.DELETE,
            "Item",
            item.pk,
            description=f"Soft-deleted item {item.name}",
        )

        return redirect("inventory_list")

    return render(
        request,
        "inventory/item_confirm_delete.html",
        {"item": item},
    )


@login_required
def item_sell(request, pk):

    item = get_object_or_404(
        Item,
        pk=pk,
        is_active=True,
        created_by=request.user,
    )

    if request.method == "POST":

        form = SellRecordForm(request.POST)

        if form.is_valid():

            sell = form.save(commit=False)
            sell.user = request.user
            sell.item = item

            if sell.quantity > item.quantity:

                form.add_error(
                    "quantity",
                    "Not enough stock."
                )

            else:

                item.quantity -= sell.quantity
                item.save()

                sell.save()

                messages.success(
                    request,
                    "Sell recorded successfully."
                )

                create_audit_log(
                    request,
                    AuditLog.Action.OTHER,
                    "SellRecord",
                    sell.pk,
                    description=f"Sold {sell.quantity} of {item.name} at {sell.sell_price}",
                )

                return redirect("inventory_list")

    else:
        form = SellRecordForm()

    return render(
        request,
        "inventory/item_sell.html",
        {
            "form": form,
            "item": item,
        },
    )


@login_required
@require_POST
@transaction.atomic
def reset_inventory(request):

    SellRecord.objects.filter(
        user=request.user
    ).delete()

    Item.objects.filter(
        created_by=request.user
    ).delete()

    messages.success(
        request,
        "All your inventory data has been reset."
    )

    return redirect("dashboard")


@login_required
def sales_report(request):
    sales = (
        SellRecord.objects
        .filter(user=request.user)
        .select_related("item")
        .order_by("-created_at")
    )

    total_revenue = sum(sale.revenue for sale in sales)
    total_profit = sum(sale.profit for sale in sales)

    avg_profit = 0

    if sales.count() > 0:
        avg_profit = total_profit / sales.count()

    context = {
        "sales": sales,
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "avg_profit": avg_profit,
    }

    return render(request, "inventory/sales_report.html", context)


@login_required
def setting(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            saved_profile = form.save(commit=False)
            saved_profile.user = request.user
            saved_profile.save()
            messages.success(request, "Settings saved successfully!")
            return redirect("settings")
    else:
        form = UserProfileForm(instance=profile)

    return render(
        request,
        "inventory/setting.html",
        {"form": form},
    )