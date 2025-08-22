from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapping_list_create, name='mapping-list-create'),
    path('<int:patient_id>/', views.patient_doctors, name='patient-doctors'),
    path('delete/<int:pk>/', views.mapping_delete, name='mapping-delete'),
]