from .shared import *
from .bootstrap import MainWindowBootstrapMixin
from .config_io import MainWindowConfigIOMixin
from .network_utils import MainWindowNetworkUtilsMixin
from .ui_build import MainWindowUiBuildMixin
from .ui_status import MainWindowUiStatusMixin
from .ui_weather import MainWindowUiWeatherMixin
from .remote import MainWindowRemoteMixin
from .firebase import MainWindowFirebaseMixin
from .audio import MainWindowAudioMixin
from .tray import MainWindowTrayMixin

class OkulZilSistemi(MainWindowBootstrapMixin, MainWindowConfigIOMixin,
                     MainWindowNetworkUtilsMixin, MainWindowUiBuildMixin,
                     MainWindowUiStatusMixin, MainWindowUiWeatherMixin,
                     MainWindowRemoteMixin, MainWindowFirebaseMixin,
                     MainWindowAudioMixin, MainWindowTrayMixin, QWidget):
    pass
