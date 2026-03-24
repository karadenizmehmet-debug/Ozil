import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# audio_manager
write_file("core/audio_manager.py", """import pygame
import winsound

class AudioManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.ok = True
        except:
            self.ok = False

    def play(self, path):
        if self.ok:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        else:
            winsound.PlaySound(path, winsound.SND_FILENAME)
""")

# scheduler
write_file("core/scheduler.py", """from datetime import timedelta

class Scheduler:
    def __init__(self, get_program, audio_manager):
        self.get_program = get_program
        self.audio = audio_manager
        self.son_calinan = None

    def kontrol_et(self, now):
        program = self.get_program()

        for zil in program:
            saat = zil.get("saat")
            ses = zil.get("ses")

            if not saat or not ses:
                continue

            if self._calinmali(now, saat):
                dakika_key = f"{now.hour}:{now.minute}"

                if self.son_calinan != dakika_key:
                    self.audio.play(ses)
                    self.son_calinan = dakika_key

    def _calinmali(self, now, hedef):
        return now >= hedef and now <= hedef + timedelta(seconds=30)
""")

print("Patch başarıyla uygulandı 🚀")