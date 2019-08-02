from PyQt5 import QtCore, QtGui, QtWidgets, uic

import os
import glob
import sys
import ntpath

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        self.previewName = 'Артём'
        self.previewSurname = 'Гиндинсон'
        self.previewPioner = QtGui.QPixmap(u'pioner.jpg')

        self.faces = []
        self.dir_path = ""

        uic.loadUi('window.ui', self)

        self.selectMockup = self.findChild(QtWidgets.QPushButton, 'SelectMockup')
        self.selectMockup.clicked.connect(self.selectMockupButtonPressed)

        self.selectNameFont = self.findChild(QtWidgets.QPushButton, 'SelectNameFont')
        self.selectNameFont.clicked.connect(self.selectNameFontButtonPressed)

        self.selectSurnameFont = self.findChild(QtWidgets.QPushButton, 'SelectSurnameFont')
        self.selectSurnameFont.clicked.connect(self.selectSurnameFontButtonPressed)

        self.selectColor = self.findChild(QtWidgets.QPushButton, 'SelectColor')
        self.selectColor.clicked.connect(self.selectColorButtonPressed)

        self.preview = self.findChild(QtWidgets.QLabel, 'Preview')

        self.run = self.findChild(QtWidgets.QPushButton, 'Run')
        self.run.clicked.connect(self.runButtonPressed)

        self.verticalPhotoSlider = self.findChild(QtWidgets.QSlider, 'VerticalPhotoSlider')
        self.horizontalPhotoSlider = self.findChild(QtWidgets.QSlider, 'HorizontalPhotoSlider')
        self.verticalNameSlider = self.findChild(QtWidgets.QSlider, 'VerticalNameSlider')
        self.horizontalNameSlider = self.findChild(QtWidgets.QSlider, 'HorizontalNameSlider')
        self.verticalSurnameSlider = self.findChild(QtWidgets.QSlider, 'VerticalSurnameSlider')
        self.horizontalSurnameSlider = self.findChild(QtWidgets.QSlider, 'HorizontalSurnameSlider')
        self.photoSizeSlider = self.findChild(QtWidgets.QSlider, 'PhotoSizeSlider')

        self.verticalPhotoSlider.valueChanged.connect(self.drawPreviewBadge)
        self.horizontalPhotoSlider.valueChanged.connect(self.drawPreviewBadge)
        self.verticalNameSlider.valueChanged.connect(self.drawPreviewBadge)
        self.horizontalNameSlider.valueChanged.connect(self.drawPreviewBadge)
        self.verticalSurnameSlider.valueChanged.connect(self.drawPreviewBadge)
        self.horizontalSurnameSlider.valueChanged.connect(self.drawPreviewBadge)
        self.photoSizeSlider.valueChanged.connect(self.drawPreviewBadge)

        self.gridLayout = self.findChild(QtWidgets.QGridLayout, 'GridLayout')

        self.mockupFilePath = 'mockup.jpg'
        self.nameFont = QtGui.QFont('Arial', 72, -1, False)
        self.surnameFont = QtGui.QFont('Arial', 72, -1, False)
        self.color = QtGui.QColor()
        self.drawPreviewBadge()

        self.hasFaces = False

        self.show()

    def drawPreviewBadge(self):
        self.drawBadge(self.previewPioner, self.previewName, self.previewSurname)

    def drawBadge(self, photo, name, surname):
        self.previewPioner = photo
        self.previewName = name
        self.previewSurname = surname
        self.pixmap = QtGui.QPixmap(self.mockupFilePath)
        paint = QtGui.QPainter(self.pixmap)
        self.drawPhotoToMockup(photo, paint)
        self.drawTextToMockup(name, surname, paint)
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

    def drawTextToMockup(self, name, surname, paint):
        paint.setFont(self.nameFont)
        paint.setPen(self.color)
        xNamePos = self.horizontalNameSlider.value() / 1000 * self.pixmap.width()
        yNamePos = (1000 - self.verticalNameSlider.value()) / 1000 * self.pixmap.height()
        metrics = QtGui.QFontMetrics(self.nameFont)
        textWidth = metrics.width(name)
        textHeight = metrics.height()
        rect = QtCore.QRect(xNamePos, 
            yNamePos, 
            textWidth, 
            textHeight)
        paint.drawText(rect, QtCore.Qt.TextWordWrap, name)
        paint.setFont(self.surnameFont)
        paint.setPen(self.color)
        xSurnamePos = self.horizontalSurnameSlider.value() / 1000 * self.pixmap.width()
        ySurnamePos = (1000 - self.verticalSurnameSlider.value()) / 1000 * self.pixmap.height()
        metrics = QtGui.QFontMetrics(self.surnameFont)
        textWidth = metrics.width(surname)
        textHeight = metrics.height()
        rect = QtCore.QRect(xSurnamePos, 
            ySurnamePos, 
            textWidth, 
            textHeight)
        paint.drawText(rect, QtCore.Qt.TextWordWrap, surname)

    def updatePreview(self):
        previewPixmap = self.pixmap.scaledToHeight(500)
        self.preview.setPixmap(previewPixmap)
        self.preview.resize(previewPixmap.width(), previewPixmap.height())
        self.setFixedSize(self.gridLayout.sizeHint().width() + 40, self.gridLayout.sizeHint().height() + 40)

    def selectNameFontButtonPressed(self):
        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            self.nameFont = font
            self.drawPreviewBadge()

    def selectSurnameFontButtonPressed(self):
        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            self.surnameFont = font
            self.drawPreviewBadge()

    def selectMockupButtonPressed(self):
        self.mockupFilePath = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл макета')[0]
        self.drawPreviewBadge()

    def selectColorButtonPressed(self):
        self.color = QtWidgets.QColorDialog().getColor()
        self.drawPreviewBadge()

    def runButtonPressed(self):
        if self.hasFaces:
            face = self.faces.pop(0)
            text = os.path.splitext(ntpath.basename(face))[0]
            name = text.split(' ')[0]
            surname = text.split(' ')[1]
            badge_path = os.path.join(self.dir_path, u"Badge " + name + u" " + surname + u".jpg")
            self.pixmap.save(badge_path, 'jpg')
            if len(self.faces) > 0:
                face = self.faces[0]
                text = os.path.splitext(ntpath.basename(face))[0]
                photo = QtGui.QPixmap(face)
                name = text.split(' ')[0]
                surname = text.split(' ')[1]
                self.drawBadge(photo, name, surname)
            else:
                self.hasFaces = False
            
        else:
            self.dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите папку с фотками пионеров')
            self.faces = glob.glob(os.path.join(self.dir_path, u'*.jpg'))
            self.hasFaces = True
            if len(self.faces) > 0:
                self.hasFaces = True

                face = self.faces[0]
                text = os.path.splitext(ntpath.basename(face))[0]
                photo = QtGui.QPixmap(face)
                name = text.split(' ')[0]
                surname = text.split(' ')[1]
                self.drawBadge(photo, name, surname)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()