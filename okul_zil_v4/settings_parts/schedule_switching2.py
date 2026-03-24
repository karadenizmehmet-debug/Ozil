from .shared import *

class SettingsScheduleSwitchMixin:
        def hafta_ici_gun_degisti(self, y):
                self.gecici_veri[self.tablo_ici_eski_gun] = self.tablodan_veriyi_al(
                    self.tablo_ici)
                self.tablo_ici_eski_gun = y
                self.tabloyu_doldur(self.tablo_ici, y)

        def hafta_sonu_gun_degisti(self, y):
                self.gecici_veri[self.tablo_sonu_eski_gun] = self.tablodan_veriyi_al(
                    self.tablo_sonu)
                self.tablo_sonu_eski_gun = y
                self.tabloyu_doldur(self.tablo_sonu, y)

