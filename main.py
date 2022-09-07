import os
import sys
from typing import Optional

from PyQt5.QtCore import QMargins, QSize, Qt
from PyQt5.QtGui import QKeySequence, QPixmap
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QPushButton, QShortcut, QSizePolicy, QStackedLayout, QWidget

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
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.mainWindow.mainLayout.setCurrentIndex(0)
            self.mainWindow.setTitleDefault()


class TransparentMapWidget(QLabel):
    def __init__(self, mainWindow, title, imagePath, geometry, opacity):
        super().__init__()
        self.mainWindow = mainWindow

        self.setWindowFlags(
            self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)

        self.setWindowTitle(title)
        self.setGeometry(geometry)
        self.setWindowOpacity(opacity)

        zoneMapWidget = self
        zoneMapWidget.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored))
        self.zoneMapWidget = zoneMapWidget

        print(imagePath)
        pix = QPixmap(resourcePath(imagePath))
        self.zoneMapWidget.setPixmap(pix)
        self.zoneMapWidget.setScaledContents(True)
        self.resizeZoneMap()

        mainWindow.hide()
        self.show()

    def closeEvent(self, event) -> None:
        self.mainWindow.show()
        return super().closeEvent(event)

    def resizeZoneMap(self):
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


class ZoneButton(QPushButton):
    def __init__(self, mainWindow, zoneIndex):
        super().__init__()
        self.mainWindow = mainWindow
        self.zoneIndex = zoneIndex

        self.setText(zones[zoneIndex]['name'])
        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))

    def mouseReleaseEvent(self, event) -> None:
        mainWindow = self.mainWindow
        zoneIndex = self.zoneIndex

        if event.button() == Qt.LeftButton:
            mainWindow.mainLayout.setCurrentIndex(1)
            mainWindow.setTitleZoneName(zones[zoneIndex]['name'])
            if mainWindow.currentZone == zoneIndex:
                return
            pix = QPixmap(resourcePath(zones[zoneIndex]['path']))
            mainWindow.currentPixmap = pix
            mainWindow.zoneMapWidget.setPixmap(pix)
            mainWindow.zoneMapWidget.setScaledContents(True)
            mainWindow.resizeZoneMap()
            mainWindow.currentZone = zoneIndex
        elif event.button() == Qt.RightButton:
            TransparentMapWidget(mainWindow, mainWindow.makeTitleTransparentZone(
                zones[zoneIndex]['name']), zones[zoneIndex]['path'], mainWindow.geometry(), mainWindow.mainWindowOpacity)

        return super().mouseReleaseEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windowClass = 'WoW Beta Map'
        self.setTitleDefault()
        self.mainWindowOpacity = 0.6
        self.setWindowOpacity(self.mainWindowOpacity)
        self.resize(QSize(720, 480))

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        mainLayout = QStackedLayout()
        self.mainLayout = mainLayout

        galleryLayout = QGridLayout()
        for i in range(len(zones)):
            button = ZoneButton(self, i)
            # button.clicked.connect(self.createShowZoneMapHandler(i))
            galleryLayout.addWidget(button, i // 4, i % 4)
        galleryPage = QWidget()
        galleryPage.setLayout(galleryLayout)
        mainLayout.addWidget(galleryPage)

        self.currentZone = -1
        self.currentPixmap: Optional[QPixmap] = None

        zoneMapWidget = ZoneMapWidget(self)
        zoneMapWidget.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored))
        self.zoneMapWidget = zoneMapWidget
        mainLayout.addWidget(zoneMapWidget)
        mainLayout.setCurrentIndex(0)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.mainWindowOpacity += 0.05
            if self.mainWindowOpacity > 1:
                self.mainWindowOpacity = 1
        else:
            self.mainWindowOpacity -= 0.05
            if self.mainWindowOpacity < 0.2:
                self.mainWindowOpacity = 0.2
        self.setWindowOpacity(self.mainWindowOpacity)

    def setTitleDefault(self):
        self.setWindowTitle("Zone List – " + self.windowClass)

    def setTitleZoneName(self, name):
        self.setWindowTitle(name + " – " + self.windowClass)

    def makeTitleTransparentZone(self, name):
        return name + " – " + self.windowClass + " (input disabled)"

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


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
