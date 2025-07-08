from django.urls import path
from . import views

urlpatterns = [
    path('metrics/', views.metrics_view, name='metrics'),
    path('download_metrics/<int:year>/', views.download_metrics_report, name='download_metrics_report'),
    path('download_metrics_pdf/', views.download_metrics_pdf, name='download_metrics_pdf'),
    path('download_user_report/<int:user_id>/', views.download_user_report_pdf, name='download_user_report_pdf'),
    path('download_intern_report/', views.download_intern_report_pdf, name='download_intern_report_pdf'),
]
