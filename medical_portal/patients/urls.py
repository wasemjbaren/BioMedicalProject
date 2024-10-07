# patients/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add this line
    path('register/', views.register, name='register'),
    path('upload/', views.upload_blood_count, name='upload_blood_count'),
    path('blood_counts/', views.view_blood_counts, name='view_blood_counts'),
    path('test-results/', views.test_results, name='test_results'),
    path('blood_counts/<int:blood_count_id>/', views.view_blood_count_file, name='view_blood_count_file'),
    path('blood_counts/<int:blood_count_id>/explanation/', views.file_explanation, name='file_explanation'),
    path('blood_counts/<int:blood_count_id>/analyze/', views.analyze_blood_test, name='analyze_blood_test'),

]





