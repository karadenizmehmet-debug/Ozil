from .shared import *
from .bootstrap import SettingsBootstrapMixin
from .security_flow import SettingsSecurityFlowMixin
from .file_ops import SettingsFileOpsMixin
from .schedule_ui import SettingsScheduleUiMixin
from .schedule_ops import SettingsScheduleOpsMixin
from .special import SettingsSpecialMixin
from .general_system import SettingsGeneralSystemMixin
from .general_remote import SettingsGeneralRemoteMixin
from .general_logs import SettingsGeneralLogsMixin
from .backup_ops import SettingsBackupOpsMixin
from .backup_firebase import SettingsBackupFirebaseMixin
from .about_page import SettingsAboutMixin

class AyarlarPenceresi(SettingsBootstrapMixin, SettingsSecurityFlowMixin,
                       SettingsFileOpsMixin, SettingsScheduleUiMixin,
                       SettingsScheduleOpsMixin, SettingsSpecialMixin,
                       SettingsGeneralSystemMixin, SettingsGeneralRemoteMixin,
                       SettingsGeneralLogsMixin, SettingsBackupOpsMixin,
                       SettingsBackupFirebaseMixin, SettingsAboutMixin, QDialog):
    pass
