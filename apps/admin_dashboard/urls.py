from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('revenue/', views.RevenueManageView.as_view(), name='revenue'),
    path('orders/', views.OrderManageView.as_view(), name='orders'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    
    # 營收 CRUD 功能
    path('revenue-manage/', views.RevenueCRUDView.as_view(), name='revenue_crud'),
    path('revenue-create/', views.RevenueCreateView.as_view(), name='revenue_create'),
    path('revenue/<int:revenue_id>/', views.RevenueDetailView.as_view(), name='revenue_detail'),
    path('revenue/<int:revenue_id>/delete/', views.RevenueDeleteView.as_view(), name='revenue_delete'),
    path('revenue-logs/', views.RevenueLogView.as_view(), name='revenue_logs'),
    
    # API endpoints
    path('api/export-revenue/', views.export_revenue_report, name='export_revenue'),
    path('api/export-orders/', views.export_orders_report, name='export_orders'),
    path('api/send-notification/', views.send_notification,
         name='send_notification'),
]
