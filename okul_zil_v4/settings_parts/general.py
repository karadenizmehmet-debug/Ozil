from .general_layout2 import SettingsGeneralLayoutMixin
from .general_network2 import SettingsGeneralNetworkMixin
from .general_logging2 import SettingsGeneralLoggingMixin
from .general_security2 import SettingsGeneralSecurityMixin

class SettingsGeneralMixin(
    SettingsGeneralLayoutMixin,
    SettingsGeneralNetworkMixin,
    SettingsGeneralLoggingMixin,
    SettingsGeneralSecurityMixin,
):
    pass
