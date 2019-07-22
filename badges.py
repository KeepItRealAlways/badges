from PyQt5 import QtCore, QtGui, QtWidgets, uic

import os
import glob
import sys
import ntpath

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('window.ui', self)

        self.selectMockup = self.findChild(QtWidgets.QPushButton, 'SelectMockup')
        self.selectMockup.clicked.connect(self.selectMockupButtonPressed)

        self.selectFont = self.findChild(QtWidgets.QPushButton, 'SelectFont')
        self.selectFont.clicked.connect(self.selectFontButtonPressed)

        self.selectColor = self.findChild(QtWidgets.QPushButton, 'SelectColor')
        self.selectColor.clicked.connect(self.selectColorButtonPressed)

        self.preview = self.findChild(QtWidgets.QLabel, 'Preview')

        self.run = self.findChild(QtWidgets.QPushButton, 'Run')
        self.run.clicked.connect(self.runButtonPressed)

        self.verticalPhotoSlider = self.findChild(QtWidgets.QSlider, 'VerticalPhotoSlider')
        self.horizontalPhotoSlider = self.findChild(QtWidgets.QSlider, 'HorizontalPhotoSlider')
        self.verticalTextSlider = self.findChild(QtWidgets.QSlider, 'VerticalTextSlider')
        self.horizontalTextSlider = self.findChild(QtWidgets.QSlider, 'HorizontalTextSlider')
        self.photoSizeSlider = self.findChild(QtWidgets.QSlider, 'PhotoSizeSlider')

        self.verticalPhotoSlider.valueChanged.connect(self.drawPreviewBadge)
        self.horizontalPhotoSlider.valueChanged.connect(self.drawPreviewBadge)
        self.verticalTextSlider.valueChanged.connect(self.drawPreviewBadge)
        self.horizontalTextSlider.valueChanged.connect(self.drawPreviewBadge)
        self.photoSizeSlider.valueChanged.connect(self.drawPreviewBadge)

        self.gridLayout = self.findChild(QtWidgets.QGridLayout, 'GridLayout')

        self.mockupFilePath = 'mockup.jpg'
        self.font = QtGui.QFont()
        self.color = QtGui.QColor()
        self.drawPreviewBadge()

        self.show()

    def drawPreviewBadge(self):
        previewPioner = QtGui.QPixmap(u'pioner.jpg')
        text = 'Артём\nГиндинсон'
        self.drawBadge(previewPioner, text)

    def drawBadge(self, photo, text):
        self.pixmap = QtGui.QPixmap(self.mockupFilePath)
        paint = QtGui.QPainter(self.pixmap)
        self.drawPhotoToMockup(photo, paint)
        self.drawTextToMockup(text, paint)
        self.updatePreview()

    def drawPhotoToMockup(self, photo, paint):
        source = QtCore.QRectF(0, 0, photo.width(), photo.height())
        xPhotoPos = self.horizontalPhotoSlider.value() / 1000 * self.pixmap.width()
        yPhotoPos = (1000 - self.verticalPhotoSlider.value()) / 1000 * self.pixmap.height()
        scaledPhotoWidth = self.photoSizeSlider.value() / 1000 * photo.width()
        scaledPhotoHeight = self.photoSizeSlider.value() / 1000 * photo.height()
        target = QtCore.QRectF(
            xPhotoPos,
            yPhotoPos,
            scaledPhotoWidth,
            scaledPhotoHeight)
        paint.drawPixmap(target, photo, source)

    def drawTextToMockup(self, text, paint):
        paint.setFont(self.font)
        paint.setPen(self.color)
        xTextPos = self.horizontalTextSlider.value() / 1000 * self.pixmap.width()
        yTextPos = (1000 - self.verticalTextSlider.value()) / 1000 * self.pixmap.height()
        metrics = QtGui.QFontMetrics(self.font)
        textWidth = metrics.width(text)
        textHeight = 2 * metrics.height()
        rect = QtCore.QRect(xTextPos, 
            yTextPos, 
            textWidth, 
            textHeight)
        paint.drawText(rect, QtCore.Qt.TextWordWrap, text)

    def updatePreview(self):
        self.preview.setPixmap(self.pixmap)
        self.preview.resize(self.pixmap.width(), self.pixmap.height())
        self.setFixedSize(self.gridLayout.sizeHint().width() + 40, self.gridLayout.sizeHint().height() + 40)

    def selectFontButtonPressed(self):
        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            self.font = font
            self.drawPreviewBadge()

    def selectMockupButtonPressed(self):
        self.mockupFilePath = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл макета')[0]
        self.drawPreviewBadge()

    def selectColorButtonPressed(self):
        self.color = QtWidgets.QColorDialog().getColor()
        self.drawPreviewBadge()

    def runButtonPressed(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите папку с фотками пионеров')
        faces = glob.glob(os.path.join(dir_path, u'*.jpg'))
        for face in faces:
            try:
                name = os.path.splitext(ntpath.basename(face))[0]
                text = name.split(' ')[0] + '\n' + name.split(' ')[1]
                badge_path = os.path.join(dir_path, u"Badge " + name + u".jpg")
                photo = QtGui.QPixmap(face)
                self.drawBadge(photo, text)
                self.pixmap.save(badge_path, 'jpg')
            except IndexError:
                print('Блять, нормально фотки назови, а не ' + name)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()