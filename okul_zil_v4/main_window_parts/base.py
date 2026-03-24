from .base_init import MainWindowBaseInitMixin
from .base_storage import MainWindowBaseStorageMixin
from .base_network2 import MainWindowBaseNetworkMixin

class MainWindowBaseMixin(
    MainWindowBaseInitMixin,
    MainWindowBaseStorageMixin,
    MainWindowBaseNetworkMixin,
):
    pass
