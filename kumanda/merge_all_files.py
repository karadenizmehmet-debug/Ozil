#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kumanda klasöründeki tüm dosyaları tek bir text dosyasında birleştirir
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def merge_files_in_folder(folder_path, output_filename="kumanda_all_files.txt"):
    """
    Belirtilen klasördeki tüm dosyaları tek bir text dosyasında birleştirir
    
    Args:
        folder_path (str): Dosyaların bulunduğu klasör yolu
        output_filename (str): Çıktı dosyasının adı
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"❌ Klasör bulunamadı: {folder_path}")
        return False
    
    output_path = folder_path / output_filename
    
    # Tüm dosyaları al (klasörler hariç, Python cache hariç)
    files = sorted([
        f for f in folder_path.iterdir() 
        if f.is_file() and f.name != output_filename and not f.name.startswith('.')
    ])
    
    if not files:
        print(f"❌ {folder_path} klasöründe dosya bulunamadı")
        return False
    
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            # Başlık
            output_file.write("=" * 80 + "\n")
            output_file.write(f"KUMANDA KLASÖRÜ - TÜM DOSYALAR\n")
            output_file.write(f"Oluşturulma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
            output_file.write(f"Toplam Dosya Sayısı: {len(files)}\n")
            output_file.write("=" * 80 + "\n\n")
            
            # Dosya listesi
            output_file.write("DOSYA LİSTESİ:\n")
            output_file.write("-" * 80 + "\n")
            for idx, file_path in enumerate(files, 1):
                file_size = file_path.stat().st_size
                output_file.write(f"{idx}. {file_path.name} ({file_size:,} bytes)\n")
            output_file.write("-" * 80 + "\n\n")
            
            # Dosya içerikleri
            for idx, file_path in enumerate(files, 1):
                output_file.write("\n")
                output_file.write("=" * 80 + "\n")
                output_file.write(f"DOSYA {idx}/{len(files)}: {file_path.name}\n")
                output_file.write("=" * 80 + "\n")
                output_file.write(f"Boyut: {file_path.stat().st_size:,} bytes\n")
                output_file.write(f"Yol: {file_path}\n")
                output_file.write("-" * 80 + "\n\n")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        output_file.write(content)
                except Exception as e:
                    output_file.write(f"❌ Dosya okunamadı: {str(e)}\n")
                
                output_file.write("\n\n")
        
        file_size = output_path.stat().st_size
        print(f"✅ Başarıyla birleştirildi!")
        print(f"📄 Çıktı dosyası: {output_path}")
        print(f"📊 Toplam boyut: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
        print(f"📁 Birleştirilen dosya sayısı: {len(files)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        return False

if __name__ == "__main__":
    # Varsayılan olarak script dosyasının bulunduğu dizini kullan
    script_dir = Path(__file__).parent
    merge_files_in_folder(script_dir)
