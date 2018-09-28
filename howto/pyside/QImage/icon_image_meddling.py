# -------------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2018 pxlc@github
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -------------------------------------------------------------------------------

import sys
from PySide import QtCore, QtGui

ICONS_ROOT = '../../../res/icons'


class IconButton(QtGui.QPushButton):

    def __init__(self, icon_image_filepath, bright_factor=1.5, dark_factor=0.75, parent=None):
        super(IconButton, self).__init__(parent)

        img = QtGui.QImage()
        img.load(icon_image_filepath)

        img_bright = self._get_brighter_image(img, bright_factor)
        img_dark = self._get_darker_image(img, dark_factor)

        self.icon_normal = QtGui.QIcon()
        self.icon_normal.addPixmap(QtGui.QPixmap.fromImage(img))

        self.icon_hover = QtGui.QIcon()
        self.icon_hover.addPixmap(QtGui.QPixmap.fromImage(img_bright))

        self.icon_press = QtGui.QIcon()
        self.icon_press.addPixmap(QtGui.QPixmap.fromImage(img_dark))

        self.setIcon(self.icon_normal)

        self.mouse_btn_pressed = False
        self.mouse_hover_on = False

    def enterEvent(self, evt):
        self.mouse_hover_on = True
        if not self.mouse_btn_pressed:
            self.setIcon(self.icon_hover)

    def leaveEvent(self, evt):
        self.mouse_hover_on = False
        if not self.mouse_btn_pressed:
            self.setIcon(self.icon_normal)

    def mousePressEvent(self, evt):
        self.mouse_btn_pressed = True
        self.setIcon(self.icon_press)

    def mouseReleaseEvent(self, evt):
        self.mouse_btn_pressed = False
        if self.mouse_hover_on:
            self.setIcon(self.icon_hover)
        else:
            self.setIcon(self.icon_normal)

    def _get_brighter_image(self, q_image, bright_factor):

        img = q_image.copy(0, 0, q_image.height(), q_image.width())

        for y in range(img.height()):
            for x in range(img.width()):
                color = img.pixel(x, y)
                r = (float(QtGui.qRed(color)) / 255.0) * bright_factor
                g = (float(QtGui.qGreen(color)) / 255.0) * bright_factor
                b = (float(QtGui.qBlue(color)) / 255.0) * bright_factor
                a = float(QtGui.qAlpha(color) / 255.0)
                if r > 1.0:
                    r = 1.0
                if g > 1.0:
                    g = 1.0
                if b > 1.0:
                    b = 1.0
                # -----------------------------------------------------------------------
                # this is weird because color in the system is an index to color tables
                # so in this following line you need to call the .rgba() method of QColor
                # which returns a long int for the index to color table
                # -----------------------------------------------------------------------
                img.setPixel(x, y, QtGui.QColor.fromRgbF(r, g, b, a).rgba())
        return img

    def _get_darker_image(self, q_image, dark_factor):

        img = q_image.copy(0, 0, q_image.height(), q_image.width())

        for y in range(img.height()):
            for x in range(img.width()):
                color = img.pixel(x, y)
                r = (float(QtGui.qRed(color)) / 255.0) * dark_factor
                g = (float(QtGui.qGreen(color)) / 255.0) * dark_factor
                b = (float(QtGui.qBlue(color)) / 255.0) * dark_factor
                a = float(QtGui.qAlpha(color) / 255.0)
                img.setPixel(x, y, QtGui.QColor.fromRgbF(r, g, b, a).rgba())
        return img


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = IconButton('{iroot}/Icons8_color/png_48/modern_art-48.png'.format(iroot=ICONS_ROOT),
                         bright_factor=1.6, dark_factor=0.65,
                         parent=self)

        btn.setMinimumSize(QtCore.QSize(128, 128))
        btn.setMaximumSize(QtCore.QSize(128, 128))
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setText("")

        btn.setIconSize(QtCore.QSize(96, 96))

        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setObjectName("pushButton")

        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)       
        btn.setText("")
        
        self.setGeometry(300, 300, 250, 300)
        self.setWindowTitle('Tooltips')    
        self.show()
        

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
