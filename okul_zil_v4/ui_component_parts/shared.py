import os
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QDialog, QMessageBox, QSlider, QListWidget,
                             QFrame, QApplication)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from config import MODERN_TEMA, MUZIK_KLASORU, AYARLAR_DOSYASI
from utils import pencere_ortala
