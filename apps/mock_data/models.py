from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Store(models.Model):
    """Store model representing a restaurant branch"""
    REGION_CHOICES = [
        ('taipei', '台北地區'),
        ('new_taipei', '新北地區'),
        ('taoyuan', '桃園地區'),
        ('taichung', '台中地區'),
        ('tainan', '台南地區'),
        ('kaohsiung', '高雄地區'),
    ]
    
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='taipei')
    manager_name = models.CharField(max_length=100)
    manager_line_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Revenue(models.Model):
    """Daily revenue report for a store"""
    STATUS_CHOICES = [
        ('pending', '未提交'),
        ('submitted', '已提交'),
    ]
    
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='revenues')
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text='備註說明')
    created_by = models.CharField(max_length=100, default='系統')
    updated_by = models.CharField(max_length=100, default='系統')
    updated_at = models.DateTimeField(auto_now=True)
    
    # 保留原有欄位的相容性
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['store', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.store.name} - {self.date} - ${self.amount} ({self.get_status_display()})"


class Ingredient(models.Model):
    """Ingredient that can be ordered by stores"""
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)  # e.g., kg, piece, bag
    # e.g., vegetable, meat, seasoning
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Order(models.Model):
    """Daily ingredient order from a store"""
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='orders')
    date = models.DateField(default=timezone.now)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.store.name} - {self.date}"


class OrderItem(models.Model):
    """Individual item in an order"""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.ingredient.name} x {self.quantity}"


class RevenueLog(models.Model):
    """Log of all revenue changes for audit trail"""
    ACTION_CHOICES = [
        ('create', '新增'),
        ('update', '修改'),
        ('delete', '刪除'),
        ('submit', '提交'),
    ]
    
    revenue = models.ForeignKey(
        Revenue, on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    old_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    new_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    date = models.DateField()
    notes = models.TextField(blank=True, help_text='變更說明')
    changed_by = models.CharField(max_length=100, default='系統')
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-changed_at']
        
    def __str__(self):
        if self.action == 'delete':
            return f"{self.store.name} - {self.date} - {self.get_action_display()} (${self.old_amount})"
        return f"{self.store.name} - {self.date} - {self.get_action_display()}"
