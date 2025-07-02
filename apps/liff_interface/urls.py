from django.urls import path
from . import views

app_name = 'liff_interface'

urlpatterns = [
    path('', views.LiffHomeView.as_view(), name='home'),
    path('revenue/', views.RevenueReportView.as_view(), name='revenue'),
    path('order/', views.DailyOrderView.as_view(), name='order'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('api/submit-revenue/', views.submit_revenue, name='submit_revenue'),
    path('api/submit-order/', views.submit_order, name='submit_order'),
]
