import os
import sys
from typing import Optional

from PyQt5.QtCore import QMargins, QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QPushButton, QSizePolicy, QStackedLayout, QVBoxLayout, QWidget

zones = [
    {
        'name': 'The Waking Shore',
        'path': 'gallery/thewakingshores.jpg',
    },
    {
        'name': 'Ohn’ahran Plains',
        'path': 'gallery/plainsofohnahra.merged.jpg',
    },
    {
        'name': 'The Azure Span',
        'path': 'gallery/theazurespan.merged.jpg',
    },
    {
        'name': 'Thaldraszus',
        'path': 'gallery/thaldraszus.merged.jpg',
    },
    {
        'name': 'Valdrakken',
        'path': 'gallery/valdrakken.jpg',
    },
    {
        'name': 'The Forbidden Reach',
        'path': 'gallery/theforbiddenreach.merged.jpg',
    },
    {
        'name': 'Dragon Isles',
        'path': 'gallery/dragonisles.jpg',
    }
]


def resourcePath(relative):
    return os.path.join(
        getattr(sys, '_MEIPASS', os.path.abspath(".")),
        relative
    )


class ZoneMapWidget(QLabel):
    def __init__(self, parentLayout):
        super().__init__()
        self.parentLayout = parentLayout

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.parentLayout.setCurrentIndex(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WoW Beta Map')
        self.setWindowOpacity(0.6)
        self.resize(QSize(720, 480))

        windowFlags = self.windowFlags()
        windowFlags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(windowFlags)

        mainLayout = QStackedLayout()
        self.mainLayout = mainLayout

        galleryLayout = QGridLayout()
        for i in range(len(zones)):
            zone = zones[i]
            button = self.createZoneButton(zone['name'])
            button.clicked.connect(self.createShowZoneMapHandler(i))
            galleryLayout.addWidget(button, i // 4, i % 4)
        galleryPage = QWidget()
        galleryPage.setLayout(galleryLayout)
        mainLayout.addWidget(galleryPage)

        self.currentZone = -1
        self.currentPixmap: Optional[QPixmap] = None

        zoneMapWidget = ZoneMapWidget(mainLayout)
        zoneMapWidget.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored))
        self.zoneMapWidget = zoneMapWidget
        mainLayout.addWidget(zoneMapWidget)
        mainLayout.setCurrentIndex(0)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

    def resizeZoneMap(self):
        if self.currentPixmap == None:
            return
        width = self.size().width()
        height = self.size().height()
        if height < width * 2 / 3:
            expectedWidth = int(height * 3 / 2)
            marginLeft = (width - expectedWidth) // 2
            marginRight = width - expectedWidth - marginLeft
            self.zoneMapWidget.setContentsMargins(
                QMargins(marginLeft, 0, marginRight, 0))
        else:
            expectedHeight = int(width * 2 / 3)
            marginTop = (height - expectedHeight) // 2
            marginBottom = height - expectedHeight - marginTop
            self.zoneMapWidget.setContentsMargins(
                QMargins(0, marginTop, 0, marginBottom))

    def resizeEvent(self, event):
        self.resizeZoneMap()

    def createShowZoneMapHandler(self, i):
        def showZoneMapHandler():
            self.mainLayout.setCurrentIndex(1)
            if self.currentZone == i:
                return
            pix = QPixmap(resourcePath(zones[i]['path']))
            self.currentPixmap = pix
            self.zoneMapWidget.setPixmap(pix)
            self.zoneMapWidget.setScaledContents(True)
            self.resizeZoneMap()
            self.currentZone = i
        return showZoneMapHandler

    @staticmethod
    def createZoneButton(zoneName):
        button = QPushButton()
        button.setText(zoneName)
        button.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))
        return button


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
