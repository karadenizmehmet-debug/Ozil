from .audio_dialogs import MainWindowAudioDialogsMixin
from .audio_playback import MainWindowAudioPlaybackMixin
from .audio_announcements import MainWindowAudioAnnouncementMixin
from .audio_playlist import MainWindowAudioPlaylistMixin

class MainWindowAudioMixin(
    MainWindowAudioDialogsMixin,
    MainWindowAudioPlaybackMixin,
    MainWindowAudioAnnouncementMixin,
    MainWindowAudioPlaylistMixin,
):
    pass
