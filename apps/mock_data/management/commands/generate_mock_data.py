import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.mock_data.models import Store, Revenue, Ingredient, Order, OrderItem, RevenueLog


class Command(BaseCommand):
    help = 'Generate mock data for demo purposes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating mock data...')

        # Create stores
        self.create_stores()

        # Create ingredients
        self.create_ingredients()

        # Create revenues
        self.create_revenues()

        # Create orders
        self.create_orders()
        
        # Create some revenue logs
        self.create_revenue_logs()

        self.stdout.write(self.style.SUCCESS(
            'Successfully generated mock data'))

    def create_stores(self):
        """Create mock stores"""
        if Store.objects.exists():
            self.stdout.write('Stores already exist, skipping...')
            return

        stores = [
            {
                'name': '台北信義店',
                'location': '台北市信義區松仁路100號',
                'region': 'taipei',
                'manager_name': '王店長',
                'manager_line_id': 'U123456789abcdef1'
            },
            {
                'name': '台北西門店',
                'location': '台北市萬華區西寧南路120號',
                'region': 'taipei',
                'manager_name': '李店長',
                'manager_line_id': 'U123456789abcdef2'
            },
            {
                'name': '新北板橋店',
                'location': '新北市板橋區文化路一段50號',
                'region': 'new_taipei',
                'manager_name': '張店長',
                'manager_line_id': 'U123456789abcdef3'
            },
            {
                'name': '桃園中壢店',
                'location': '桃園市中壢區中央西路二段30號',
                'region': 'taoyuan',
                'manager_name': '陳店長',
                'manager_line_id': 'U123456789abcdef4'
            },
            {
                'name': '台中西屯店',
                'location': '台中市西屯區河南路二段80號',
                'region': 'taichung',
                'manager_name': '林店長',
                'manager_line_id': 'U123456789abcdef5'
            }
        ]

        for store_data in stores:
            Store.objects.create(**store_data)
            self.stdout.write(f'Created store: {store_data["name"]}')

    def create_ingredients(self):
        """Create mock ingredients"""
        if Ingredient.objects.exists():
            self.stdout.write('Ingredients already exist, skipping...')
            return

        ingredients = [
            # 蔬菜類
            {'name': '高麗菜', 'unit': '顆', 'category': '蔬菜'},
            {'name': '青江菜', 'unit': '把', 'category': '蔬菜'},
            {'name': '小白菜', 'unit': '把', 'category': '蔬菜'},
            {'name': '空心菜', 'unit': '把', 'category': '蔬菜'},
            {'name': '大白菜', 'unit': '顆', 'category': '蔬菜'},

            # 肉類
            {'name': '豬肉片', 'unit': '公斤', 'category': '肉類'},
            {'name': '牛肉片', 'unit': '公斤', 'category': '肉類'},
            {'name': '雞肉片', 'unit': '公斤', 'category': '肉類'},
            {'name': '羊肉片', 'unit': '公斤', 'category': '肉類'},

            # 海鮮類
            {'name': '蝦仁', 'unit': '公斤', 'category': '海鮮'},
            {'name': '花枝丸', 'unit': '包', 'category': '海鮮'},
            {'name': '魚丸', 'unit': '包', 'category': '海鮮'},
            {'name': '蛤蜊', 'unit': '公斤', 'category': '海鮮'},

            # 豆製品
            {'name': '豆腐', 'unit': '盒', 'category': '豆製品'},
            {'name': '豆皮', 'unit': '包', 'category': '豆製品'},
            {'name': '百頁豆腐', 'unit': '包', 'category': '豆製品'},

            # 菇類
            {'name': '金針菇', 'unit': '包', 'category': '菇類'},
            {'name': '香菇', 'unit': '包', 'category': '菇類'},
            {'name': '杏鮑菇', 'unit': '包', 'category': '菇類'},
            {'name': '草菇', 'unit': '包', 'category': '菇類'},

            # 其他
            {'name': '火鍋料', 'unit': '包', 'category': '其他'},
            {'name': '泡麵', 'unit': '包', 'category': '其他'},
            {'name': '烏龍麵', 'unit': '包', 'category': '其他'},
            {'name': '王子麵', 'unit': '包', 'category': '其他'},
        ]

        for ingredient_data in ingredients:
            Ingredient.objects.create(**ingredient_data)
            self.stdout.write(f'Created ingredient: {ingredient_data["name"]}')

    def create_revenues(self):
        """Create mock revenue data for the past 30 days"""
        today = timezone.now().date()
        start_date = today - timedelta(days=30)

        # Get all stores
        stores = Store.objects.all()

        # Delete existing revenues in this date range
        Revenue.objects.filter(date__gte=start_date, date__lte=today).delete()

        # Generate random revenues for each store for each day
        for store in stores:
            # Base revenue for this store (between 30000 and 60000)
            base_revenue = random.randint(30000, 60000)

            # Generate revenue for each day
            for days_ago in range(30, -1, -1):
                date = today - timedelta(days=days_ago)

                # Weekend boost (Fri, Sat, Sun)
                weekend_boost = 1.0
                if date.weekday() >= 4:  # Friday=4, Saturday=5, Sunday=6
                    weekend_boost = 1.2

                # Random daily variation (-10% to +10%)
                daily_variation = random.uniform(0.9, 1.1)

                # Calculate revenue
                revenue_amount = Decimal(
                    base_revenue * weekend_boost * daily_variation)

                # Round to nearest 100
                revenue_amount = round(revenue_amount / 100) * 100

                # Create revenue record
                submitted_at = datetime.combine(date, datetime.min.time(
                )) + timedelta(hours=random.randint(19, 22), minutes=random.randint(0, 59))

                Revenue.objects.create(
                    store=store,
                    date=date,
                    amount=revenue_amount,
                    submitted_at=submitted_at
                )

            self.stdout.write(f'Created revenues for store: {store.name}')

    def create_orders(self):
        """Create mock orders for today"""
        today = timezone.now().date()

        # Get all stores and ingredients
        stores = Store.objects.all()
        ingredients = list(Ingredient.objects.all())

        # Delete existing orders for today
        Order.objects.filter(date=today).delete()

        # Generate orders for each store
        for store in stores:
            # 80% chance of having submitted an order
            if random.random() < 0.8:
                # Create order
                order = Order.objects.create(
                    store=store,
                    date=today,
                    submitted_at=timezone.now() - timedelta(hours=random.randint(1, 5)),
                    is_completed=random.random() < 0.7  # 70% chance of being completed
                )

                # Select random ingredients (between 5 and 15)
                selected_ingredients = random.sample(
                    ingredients, random.randint(5, 15))

                # Create order items
                for ingredient in selected_ingredients:
                    OrderItem.objects.create(
                        order=order,
                        ingredient=ingredient,
                        quantity=random.randint(1, 10)
                    )

                self.stdout.write(
                    f'Created order for store: {store.name} ({"completed" if order.is_completed else "incomplete"})')
            else:
                self.stdout.write(
                    f'No order for store: {store.name} (not submitted)')

    def create_revenue_logs(self):
        """Create some mock revenue change logs"""
        if RevenueLog.objects.exists():
            self.stdout.write('Revenue logs already exist, skipping...')
            return

        # Get some recent revenues to create logs for
        recent_revenues = Revenue.objects.all()[:10]
        
        mock_actions = [
            ('update', '修改營收金額', ['系統管理員', '財務主管', '店長']),
            ('submit', '提交營收', ['店長', '財務主管']),
        ]
        
        for revenue in recent_revenues:
            # Create 1-3 logs per revenue
            num_logs = random.randint(1, 3)
            
            for i in range(num_logs):
                action, action_desc, possible_users = random.choice(mock_actions)
                changed_by = random.choice(possible_users)
                
                # Create different types of changes
                if action == 'update':
                    old_amount = revenue.amount
                    new_amount = old_amount + Decimal(random.randint(-5000, 5000))
                    old_status = random.choice(['pending', 'submitted'])
                    new_status = revenue.status
                    
                    RevenueLog.objects.create(
                        revenue=revenue,
                        store=revenue.store,
                        action=action,
                        old_amount=old_amount,
                        new_amount=new_amount,
                        old_status=old_status,
                        new_status=new_status,
                        date=revenue.date,
                        notes=f'{action_desc}: ${old_amount} → ${new_amount}',
                        changed_by=changed_by,
                        changed_at=revenue.submitted_at + timedelta(
                            hours=random.randint(1, 24)
                        )
                    )
                
                elif action == 'submit':
                    old_status = 'pending'
                    new_status = 'submitted'
                    
                    RevenueLog.objects.create(
                        revenue=revenue,
                        store=revenue.store,
                        action=action,
                        old_status=old_status,
                        new_status=new_status,
                        date=revenue.date,
                        notes=f'{action_desc}: {old_status} → {new_status}',
                        changed_by=changed_by,
                        changed_at=revenue.submitted_at + timedelta(
                            hours=random.randint(1, 48)
                        )
                    )
        
        # Create a few delete logs (for revenues that don't exist anymore)
        stores = Store.objects.all()
        for i in range(3):
            store = random.choice(stores)
            fake_date = timezone.now().date() - timedelta(days=random.randint(1, 30))
            fake_amount = Decimal(random.randint(20000, 80000))
            
            RevenueLog.objects.create(
                store=store,
                action='delete',
                old_amount=fake_amount,
                old_status='pending',
                date=fake_date,
                notes=f'刪除營收記錄: ${fake_amount}',
                changed_by=random.choice(['系統管理員', '財務主管']),
                changed_at=timezone.now() - timedelta(days=random.randint(1, 5))
            )
        
        self.stdout.write(f'Created revenue logs for demonstration')
