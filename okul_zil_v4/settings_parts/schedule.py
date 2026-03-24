from .schedule_layout2 import SettingsScheduleLayoutMixin
from .schedule_table_ops3 import SettingsScheduleTableOpsMixin
from .schedule_switching2 import SettingsScheduleSwitchMixin

class SettingsScheduleMixin(
    SettingsScheduleLayoutMixin,
    SettingsScheduleTableOpsMixin,
    SettingsScheduleSwitchMixin,
):
    pass
