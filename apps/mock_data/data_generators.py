import random
import datetime
from decimal import Decimal
from django.utils import timezone
from .models import Store, Revenue, Ingredient, Order, OrderItem


def create_mock_stores():
    """Create mock store data"""
    stores = [
        {
            'name': '熱鍋 台北本店',
            'location': '台北市信義區松仁路100號',
            'manager_name': '王大明',
            'manager_line_id': 'wang_manager',
        },
        {
            'name': '熱鍋 新北分店',
            'location': '新北市板橋區民生路50號',
            'manager_name': '李小華',
            'manager_line_id': 'lee_manager',
        },
        {
            'name': '熱鍋 桃園分店',
            'location': '桃園市中壢區中央西路120號',
            'manager_name': '張美玲',
            'manager_line_id': 'chang_manager',
        },
        {
            'name': '熱鍋 台中分店',
            'location': '台中市西區台灣大道200號',
            'manager_name': '林志明',
            'manager_line_id': 'lin_manager',
        },
        {
            'name': '熱鍋 高雄分店',
            'location': '高雄市前鎮區中山路300號',
            'manager_name': '陳小龍',
            'manager_line_id': 'chen_manager',
        },
    ]

    created_stores = []
    for store_data in stores:
        store, created = Store.objects.get_or_create(**store_data)
        created_stores.append(store)

    return created_stores


def create_mock_ingredients():
    """Create mock ingredient data"""
    ingredients = [
        {'name': '高麗菜', 'unit': '顆', 'category': '蔬菜'},
        {'name': '金針菇', 'unit': '包', 'category': '菇類'},
        {'name': '豆皮', 'unit': '片', 'category': '豆製品'},
        {'name': '牛肉片', 'unit': '盒', 'category': '肉類'},
        {'name': '豬肉片', 'unit': '盒', 'category': '肉類'},
        {'name': '雞肉片', 'unit': '盒', 'category': '肉類'},
        {'name': '蝦仁', 'unit': '包', 'category': '海鮮'},
        {'name': '魚丸', 'unit': '包', 'category': '丸類'},
        {'name': '蛋餃', 'unit': '包', 'category': '餃類'},
        {'name': '火鍋湯底', 'unit': '包', 'category': '湯底'},
    ]

    created_ingredients = []
    for ingredient_data in ingredients:
        ingredient, created = Ingredient.objects.get_or_create(
            **ingredient_data)
        created_ingredients.append(ingredient)

    return created_ingredients


def create_mock_revenues(days=30):
    """Create mock revenue data for the past number of days"""
    stores = Store.objects.all()
    if not stores:
        stores = create_mock_stores()

    today = timezone.now().date()
    created_revenues = []

    for store in stores:
        for days_ago in range(days):
            date = today - datetime.timedelta(days=days_ago)

            # Generate random revenue between 20000 and 60000
            amount = Decimal(random.randint(20000, 60000))

            # Weekend boost
            if date.weekday() >= 5:  # Saturday or Sunday
                amount *= Decimal('1.5')

            revenue, created = Revenue.objects.get_or_create(
                store=store,
                date=date,
                defaults={'amount': amount}
            )

            if created:
                created_revenues.append(revenue)

    return created_revenues


def create_mock_orders(days=7):
    """Create mock order data for the past number of days"""
    stores = Store.objects.all()
    if not stores:
        stores = create_mock_stores()

    ingredients = Ingredient.objects.all()
    if not ingredients:
        ingredients = create_mock_ingredients()

    today = timezone.now().date()
    created_orders = []

    for store in stores:
        for days_ago in range(days):
            date = today - datetime.timedelta(days=days_ago)

            # Create order
            order, created = Order.objects.get_or_create(
                store=store,
                date=date,
                defaults={'is_completed': True if days_ago > 0 else False}
            )

            if created:
                # Add random items to order
                num_items = random.randint(3, 8)
                selected_ingredients = random.sample(
                    list(ingredients), num_items)

                for ingredient in selected_ingredients:
                    quantity = random.randint(1, 5)
                    OrderItem.objects.create(
                        order=order,
                        ingredient=ingredient,
                        quantity=quantity
                    )

                created_orders.append(order)

    return created_orders


def generate_all_mock_data():
    """Generate all mock data"""
    stores = create_mock_stores()
    ingredients = create_mock_ingredients()
    revenues = create_mock_revenues()
    orders = create_mock_orders()

    return {
        'stores': len(stores),
        'ingredients': len(ingredients),
        'revenues': len(revenues),
        'orders': len(orders)
    }
