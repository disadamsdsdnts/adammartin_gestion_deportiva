from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('', views.AllMatchListView.as_view(), name='match_list'),
    path('all/', views.AllMatchListView.as_view(), name='all_match_list'),
    path('upcoming/', views.UpcomingMatchListView.as_view(), name='upcoming_match_list'),
    path('previous/', views.PreviousMatchListView.as_view(), name='previous_match_list'),
    path('postponed/', views.PostponedMatchListView.as_view(), name='postponed_match_list'),
    path('cancelled/', views.CancelledMatchListView.as_view(), name='cancelled_match_list'),
    path('create/', views.MatchCreateView.as_view(), name='match_create'),
    path('import/', views.MatchImportView.as_view(), name='match_import'),
    path('import/csv-template/', views.MatchImportCSVTemplateView.as_view(), name='match_import_csv_template'),
    path('import/process-csv/', views.MatchProcessCSVView.as_view(), name='match_process_csv'),
    path('<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),
    path('<int:pk>/edit/', views.MatchUpdateView.as_view(), name='match_update'),
    path('<int:pk>/delete/', views.MatchDeleteView.as_view(), name='match_delete'),
    path('notes/', views.MatchNoteListView.as_view(), name='match_note_list'),
    path('<int:match_id>/notes/create/', views.MatchNoteCreateView.as_view(), name='match_note_create'),
    path('notes/<int:pk>/', views.MatchNoteDetailView.as_view(), name='match_note_detail'),
    path('notes/<int:pk>/edit/', views.MatchNoteUpdateView.as_view(), name='match_note_update'),
    path('notes/<int:pk>/delete/', views.MatchNoteDeleteView.as_view(), name='match_note_delete'),
    path('notes/<int:pk>/delete-ajax/', views.delete_match_note_ajax, name='match_note_delete_ajax'),
]
