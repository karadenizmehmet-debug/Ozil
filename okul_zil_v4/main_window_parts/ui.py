from .ui_layout2 import MainWindowUiLayoutMixin
from .ui_runtime2 import MainWindowUiRuntimeMixin
from .ui_weather_runtime2 import MainWindowUiWeatherRuntimeMixin

class MainWindowUiMixin(
    MainWindowUiLayoutMixin,
    MainWindowUiRuntimeMixin,
    MainWindowUiWeatherRuntimeMixin,
):
    pass
