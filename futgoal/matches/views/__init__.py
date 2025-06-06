from .match_views import (
    MatchListView,
    MatchDetailView,
    MatchCreateView,
    MatchUpdateView,
    MatchDeleteView
)
from .match_note_views import (
    MatchNoteListView,
    MatchNoteDetailView,
    MatchNoteCreateView,
    MatchNoteUpdateView,
    MatchNoteDeleteView,
    delete_match_note_ajax
)

__all__ = [
    'MatchListView',
    'MatchDetailView',
    'MatchCreateView',
    'MatchUpdateView',
    'MatchDeleteView',
    'MatchNoteListView',
    'MatchNoteDetailView',
    'MatchNoteCreateView',
    'MatchNoteUpdateView',
    'MatchNoteDeleteView',
    'delete_match_note_ajax'
]
