# Auto-generated shared imports for V4 modular split
import os
import json
import platform
import traceback
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox,
                             QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
                             QCheckBox, QSpinBox, QTimeEdit, QDialog, QMessageBox,
                             QGridLayout, QTabWidget, QLineEdit, QFileDialog, QWidget, QInputDialog,
                             QProgressBar)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont

from config import (MODERN_TEMA, HAFTA_ICI, HAFTA_SONU, GUNLER,
                    ZIL_KLASORU, MUZIK_KLASORU, LOG_DOSYASI, AYARLAR_DOSYASI, AYARLAR_TEMP)
from utils import pencere_ortala, log_yaz, get_wifi_name, oto_baslat_ayarla
from web_server import flask_app
