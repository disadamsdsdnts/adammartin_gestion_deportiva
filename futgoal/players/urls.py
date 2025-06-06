from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from .views import PlayerList, PlayerCreate, PlayerDetail, PlayerUpdate, PlayerDelete, PlayerImportView, PlayerImportCSVTemplateView, PlayerProcessCSVView


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
        'new-player/',
        PlayerCreate.as_view(),
        name='player_create'
    ),
    path(
        'import/',
        PlayerImportView.as_view(),
        name='player_import'
    ),
    path(
        'import/csv-template/',
        PlayerImportCSVTemplateView.as_view(),
        name='player_import_csv_template'
    ),
    path(
        'import/process-csv/',
        PlayerProcessCSVView.as_view(),
        name='player_process_csv'
    ),
    path(
        '<pk>/',
        PlayerDetail.as_view(),
        name='player_detail'
    ),
    path(
        '<pk>/update/',
        PlayerUpdate.as_view(),
        name='player_update'
    ),
    path(
        '<pk>/delete/',
        PlayerDelete.as_view(),
        name='player_delete'
    ),
]
