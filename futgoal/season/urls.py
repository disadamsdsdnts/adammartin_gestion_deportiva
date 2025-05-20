from django.urls import path
from .views import season_views

app_name = 'season'

urlpatterns = [
    path('', season_views.SeasonListView.as_view(), name='season_list'),
    path('create/', season_views.SeasonCreateView.as_view(), name='season_create'),
    path('<int:pk>/', season_views.SeasonDetailView.as_view(), name='season_detail'),
    path('<int:pk>/update/', season_views.SeasonUpdateView.as_view(), name='season_update'),
    path('<int:pk>/delete/', season_views.SeasonDeleteView.as_view(), name='season_delete'),
]
