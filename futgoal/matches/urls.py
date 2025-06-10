from django.urls import path
from . import views
from .views import match_player_stats_views

app_name = 'matches'

urlpatterns = [
    # Matches URLs
    path('', views.AllMatchListView.as_view(), name='match_list'),
    path('all/', views.AllMatchListView.as_view(), name='all_match_list'),
    path('upcoming/', views.UpcomingMatchListView.as_view(), name='upcoming_match_list'),
    path('previous/', views.PreviousMatchListView.as_view(), name='previous_match_list'),
    path('in-progress/', views.InProgressMatchListView.as_view(), name='in_progress_match_list'),
    path('postponed/', views.PostponedMatchListView.as_view(), name='postponed_match_list'),
    path('cancelled/', views.CancelledMatchListView.as_view(), name='cancelled_match_list'),
    path('create/', views.MatchCreateView.as_view(), name='match_create'),
    path('import/', views.MatchImportView.as_view(), name='match_import'),
    path('import/csv-template/', views.MatchImportCSVTemplateView.as_view(), name='match_import_csv_template'),
    path('import/process-csv/', views.MatchProcessCSVView.as_view(), name='match_process_csv'),
    path('bulk-import/', views.MatchBulkDataImportView.as_view(), name='match_bulk_data_import'),
    path('bulk-import/export-data/', views.MatchBulkDataExportView.as_view(), name='match_bulk_data_export'),
    path('bulk-import/process-csv/', views.MatchBulkDataProcessCSVView.as_view(), name='match_bulk_data_process_csv'),
    path('<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),
    path('<int:pk>/edit/', views.MatchUpdateView.as_view(), name='match_update'),
    path('<int:pk>/delete/', views.MatchDeleteView.as_view(), name='match_delete'),

    # Match Notes URLs
    path('notes/', views.MatchNoteListView.as_view(), name='match_note_list'),
    path('<int:match_id>/notes/create/', views.MatchNoteCreateView.as_view(), name='match_note_create'),
    path('notes/<int:pk>/', views.MatchNoteDetailView.as_view(), name='match_note_detail'),
    path('notes/<int:pk>/edit/', views.MatchNoteUpdateView.as_view(), name='match_note_update'),
    path('notes/<int:pk>/delete/', views.MatchNoteDeleteView.as_view(), name='match_note_delete'),
    path('notes/<int:pk>/delete-ajax/', views.delete_match_note_ajax, name='match_note_delete_ajax'),

    # Player Stats URLs
    path('player-stats/', match_player_stats_views.MatchPlayerStatsListView.as_view(), name='player_stats_list'),
    path('player-stats/create/', match_player_stats_views.MatchPlayerStatsCreateView.as_view(), name='player_stats_create'),
    path('player-stats/<int:pk>/', match_player_stats_views.MatchPlayerStatsDetailView.as_view(), name='player_stats_detail'),
    path('player-stats/<int:pk>/edit/', match_player_stats_views.MatchPlayerStatsUpdateView.as_view(), name='player_stats_update'),
    path('player-stats/<int:pk>/delete/', match_player_stats_views.MatchPlayerStatsDeleteView.as_view(), name='player_stats_delete'),
    path('player-stats/summary/', match_player_stats_views.MatchPlayerStatsSummaryView.as_view(), name='player_stats_summary'),
    path('<int:match_id>/player-stats/manage/', match_player_stats_views.MatchPlayerStatsManageView.as_view(), name='player_stats_manage'),
    path('player-stats/quick-add/', match_player_stats_views.MatchPlayerStatsQuickAddView.as_view(), name='player_stats_quick_add'),

    # Player Stats Import URLs
    path('player-stats/import/', match_player_stats_views.MatchPlayerStatsImportView.as_view(), name='player_stats_import'),
    path('player-stats/import/csv-template/', match_player_stats_views.MatchPlayerStatsImportCSVTemplateView.as_view(), name='player_stats_import_csv_template'),
    path('player-stats/import/process-csv/', match_player_stats_views.MatchPlayerStatsProcessCSVView.as_view(), name='player_stats_process_csv'),
    path('player-stats/import/execute/', match_player_stats_views.MatchPlayerStatsImportExecuteView.as_view(), name='player_stats_import_execute'),
]
