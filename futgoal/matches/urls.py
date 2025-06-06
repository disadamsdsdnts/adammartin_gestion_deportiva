from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('', views.MatchListView.as_view(), name='match_list'),
    path('create/', views.MatchCreateView.as_view(), name='match_create'),
    path('<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),
    path('<int:pk>/edit/', views.MatchUpdateView.as_view(), name='match_update'),
    path('<int:pk>/delete/', views.MatchDeleteView.as_view(), name='match_delete'),
]
