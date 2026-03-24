from .backup_layout2 import SettingsBackupLayoutMixin
from .backup_actions3 import SettingsBackupActionsMixin

class SettingsBackupMixin(
    SettingsBackupLayoutMixin,
    SettingsBackupActionsMixin,
):
    pass
