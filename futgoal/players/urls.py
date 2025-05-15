from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from .views import PlayerList, PlayerCreate, PlayerDetail, PlayerUpdate, PlayerDelete


urlpatterns = [
    # path(
    #     '',
    #     DashboardView.as_view(),
    #     name='dashboard'
    # ),
    path(
        '',
        PlayerList.as_view(),
        name='player_list'
    ),
    path(
        'players/new-player/',
        PlayerCreate.as_view(),
        name='player_create'
    ),
    path(
        'players/<pk>/',
        PlayerDetail.as_view(),
        name='player_detail'
    ),
    path(
        'players/<pk>/update/',
        PlayerUpdate.as_view(),
        name='player_update'
    ),
    path(
        'players/<pk>/delete/',
        PlayerDelete.as_view(),
        name='player_delete'
    ),
]
