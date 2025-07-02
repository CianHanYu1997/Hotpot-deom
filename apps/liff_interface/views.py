from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from apps.mock_data.models import Store, Revenue, Order, OrderItem, Ingredient
from django.conf import settings


class LiffHomeView(View):
    """Home view for LIFF interface"""

    def get(self, request):
        # For demo purposes, we'll use the first store
        store = Store.objects.first()
        if not store:
            # Create a demo store if none exists
            store = Store.objects.create(
                name="台北信義店",
                location="台北市信義區松仁路100號",
                manager_name="王店長",
                manager_line_id="U123456789abcdef"
            )

        context = {
            'store': store,
            'liff_id': settings.LINE_LIFF_ID,
        }
        return render(request, 'liff_interface/home.html', context)


class RevenueReportView(View):
    """Revenue reporting view for store managers"""

    def get(self, request):
        # For demo, we'll use the first store
        store = Store.objects.first()
        today = timezone.now().date()

        # Check if today's revenue already reported
        today_revenue = Revenue.objects.filter(store=store, date=today).first()

        # Get recent revenue history
        recent_revenues = Revenue.objects.filter(
            store=store).order_by('-date')[:7]

        context = {
            'store': store,
            'today': today,
            'today_revenue': today_revenue,
            'recent_revenues': recent_revenues,
            'liff_id': settings.LINE_LIFF_ID,
        }
        return render(request, 'liff_interface/revenue.html', context)


class DailyOrderView(View):
    """Daily ingredient ordering view for store managers"""

    def get(self, request):
        # For demo, we'll use the first store
        store = Store.objects.first()
        today = timezone.now().date()

        # Check if today's order already exists
        today_order = Order.objects.filter(store=store, date=today).first()

        # Get all ingredients grouped by category
        ingredients_by_category = {}
        for ingredient in Ingredient.objects.all():
            if ingredient.category not in ingredients_by_category:
                ingredients_by_category[ingredient.category] = []
            ingredients_by_category[ingredient.category].append(ingredient)

        # If order exists, get quantities
        order_items = {}
        if today_order:
            for item in today_order.items.all():
                order_items[item.ingredient.id] = item.quantity

        context = {
            'store': store,
            'today': today,
            'today_order': today_order,
            'ingredients_by_category': ingredients_by_category,
            'order_items': order_items,
            'liff_id': settings.LINE_LIFF_ID,
        }
        return render(request, 'liff_interface/order.html', context)


class HistoryView(View):
    """View for store managers to see their history"""

    def get(self, request):
        # For demo, we'll use the first store
        store = Store.objects.first()

        # Get recent revenue history
        revenues = Revenue.objects.filter(store=store).order_by('-date')[:30]

        # Get recent order history
        orders = Order.objects.filter(store=store).order_by('-date')[:30]

        context = {
            'store': store,
            'revenues': revenues,
            'orders': orders,
            'liff_id': settings.LINE_LIFF_ID,
        }
        return render(request, 'liff_interface/history.html', context)


@csrf_exempt
@require_POST
def submit_revenue(request):
    """API endpoint for submitting revenue reports"""
    try:
        data = json.loads(request.body)
        store_id = data.get('store_id')
        amount = data.get('amount')
        date = data.get('date', timezone.now().date().isoformat())

        store = get_object_or_404(Store, id=store_id)

        # Create or update revenue for the date
        revenue, created = Revenue.objects.update_or_create(
            store=store,
            date=date,
            defaults={'amount': amount}
        )

        return JsonResponse({
            'success': True,
            'message': '營收回報成功！',
            'created': created
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'錯誤: {str(e)}'
        }, status=400)


@csrf_exempt
@require_POST
def submit_order(request):
    """API endpoint for submitting ingredient orders"""
    try:
        data = json.loads(request.body)
        store_id = data.get('store_id')
        items = data.get('items', [])
        date = data.get('date', timezone.now().date().isoformat())

        store = get_object_or_404(Store, id=store_id)

        # Create or get order for today
        order, created = Order.objects.get_or_create(
            store=store,
            date=date,
            defaults={'is_completed': True}
        )

        # Clear existing items if updating
        if not created:
            order.items.all().delete()

        # Add new items
        for item in items:
            ingredient = get_object_or_404(
                Ingredient, id=item['ingredient_id'])
            OrderItem.objects.create(
                order=order,
                ingredient=ingredient,
                quantity=item['quantity']
            )

        return JsonResponse({
            'success': True,
            'message': '叫菜成功！',
            'created': created
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'錯誤: {str(e)}'
        }, status=400)
