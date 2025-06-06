from django.urls import path
from . import views

app_name = 'rivals'

urlpatterns = [
    path('', views.RivalListView.as_view(), name='rival_list'),
    path('create/', views.RivalCreateView.as_view(), name='rival_create'),
    path('<int:pk>/', views.RivalDetailView.as_view(), name='rival_detail'),
    path('<int:pk>/edit/', views.RivalUpdateView.as_view(), name='rival_update'),
    path('<int:pk>/delete/', views.RivalDeleteView.as_view(), name='rival_delete'),
]
