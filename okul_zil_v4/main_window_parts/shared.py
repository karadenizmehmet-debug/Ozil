# Auto-generated shared imports for V4 modular split
import os
import sys
import json
import random
import datetime
import socket
import platform
import traceback
import pygame
import threading
from gtts import gTTS
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSystemTrayIcon, QMenu, QAction, QStyle, QApplication,
                             QMessageBox, QInputDialog, QLineEdit, QGridLayout)
from PyQt5.QtCore import Qt, QTimer, QTime, QDate
from PyQt5.QtGui import QFont, QPixmap, QIcon

from config import GUNLER, AYLAR, SOZLER, MODERN_TEMA, MUZIK_KLASORU, ZIL_KLASORU, BASE_DIR, ANONS_KLASORU, AYARLAR_DOSYASI, AYARLAR_TEMP, IKON_DOSYASI, yolu_normalize_et
from utils import pencere_ortala, log_yaz
from web_server import WebSunucuThread, flask_app
from ui_components import ClickableSlider, SarkiSecPenceresi
from settings_window import AyarlarPenceresi
from firebase_dinleyici import FirebaseDinleyici
