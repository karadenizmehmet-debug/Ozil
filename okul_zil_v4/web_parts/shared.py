import os
import secrets
import socket
import platform
from flask import Flask, render_template_string, request, make_response, redirect, session
from PyQt5.QtCore import QThread, pyqtSignal

from config import (
    LOGIN_SABLON, SIFRE_GIRIS_SABLON, HTML_SABLON,
    MOBIL_SARKI_SABLON, SIFRE_SABLON, MUZIK_KLASORU
)
from utils import log_yaz

flask_app = Flask(__name__)
flask_app.mevcut_ses = 100
flask_thread_instance = None
flask_app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

MOBIL_AYARLAR_SABLON = """<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Genel Ayarlar</title>
<style>
  body{font-family:'Segoe UI',sans-serif;background-color:#f1f2f6;text-align:center;padding:20px;}
  h3{color:#2c3e50;}
  .card{background:white;padding:20px;border-radius:12px;box-shadow:0 4px 8px rgba(0,0,0,0.1);
        max-width:400px;margin:0 auto 20px;text-align:left;}
  .row{margin-bottom:15px;display:flex;justify-content:space-between;align-items:center;}
  input[type=range]{width:60%;}
  button{width:100%;padding:12px;background:#0984e3;color:white;border:none;
         border-radius:8px;font-weight:bold;cursor:pointer;}
</style>
</head>
<body>
<h3>⚙️ Genel Sistem Ayarları</h3>
<div class="card">
  <div class="row">
    <span>🔔 Teneffüs Müziği:</span>
    <input type="checkbox" id="ten_aktif" {% if ten_aktif %}checked{% endif %} onchange="guncelle()">
  </div>
  <div class="row">
    <span>📻 Müzik Ses Seviyesi:</span>
    <input type="range" id="muz_ses" min="1" max="100" value="{{ muz_ses }}" onchange="guncelle()">
    <span id="muz_val">%{{ muz_ses }}</span>
  </div>
  <br>
  <button onclick="window.location.href='/'">← Kumandaya Geri Dön</button>
</div>
<script>
function guncelle(){
  let t = document.getElementById('ten_aktif').checked ? 1 : 0;
  let s = document.getElementById('muz_ses').value;
  document.getElementById('muz_val').innerHTML = "%"+s;
  fetch('/mobil_ayar_kaydet/'+t+'/'+s);
}
</script>
</body></html>"""
