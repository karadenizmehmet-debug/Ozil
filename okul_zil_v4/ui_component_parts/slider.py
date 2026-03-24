from .shared import *

class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            val = self.minimum() + (
                (self.maximum() - self.minimum()) * event.x()
            ) / self.width()
            self.setValue(int(val))
            event.accept()
        super().mousePressEvent(event)
