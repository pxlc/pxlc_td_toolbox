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


class MyButton2(QtGui.QPushButton):

    def __init__(self, parent=None):
        super(MyButton2, self).__init__(parent)

    def enterEvent(self, evt):
        print(':: enter event?')

    def leaveEvent(self, evt):
        print(':: leave event?')


class MyButton(QtGui.QPushButton):

    def __init__(self, q_image_normal, q_image_hover, q_image_press, parent=None):
        super(MyButton, self).__init__(parent)

        self.icon_normal = QtGui.QIcon()
        self.icon_normal.addPixmap(QtGui.QPixmap.fromImage(q_image_normal))

        self.icon_hover = QtGui.QIcon()
        self.icon_hover.addPixmap(QtGui.QPixmap.fromImage(q_image_hover))

        self.icon_press = QtGui.QIcon()
        self.icon_press.addPixmap(QtGui.QPixmap.fromImage(q_image_press))

        self.setIcon(self.icon_normal)

    def enterEvent(self, evt):
        self.setIcon(self.icon_hover)

    def leaveEvent(self, evt):
        self.setIcon(self.icon_normal)


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        

    def _get_brighter_image(self, q_image):

        img = q_image.copy(0, 0, q_image.height(), q_image.width())

        for y in range(img.height()):
            for x in range(img.width()):
                color = img.pixel(x, y)
                r = (float(QtGui.qRed(color)) / 255.0) * 1.25
                g = (float(QtGui.qGreen(color)) / 255.0) * 1.25
                b = (float(QtGui.qBlue(color)) / 255.0) * 1.25
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
                # print('    (%s, %s) is (%s, %s, %s, %s)' % (x, y, r, g, b, a))
        return img


    def _get_darker_image(self, q_image):

        img = q_image.copy(0, 0, q_image.height(), q_image.width())

        for y in range(img.height()):
            for x in range(img.width()):
                color = img.pixel(x, y)
                r = (float(QtGui.qRed(color)) / 255.0) * 0.75
                g = (float(QtGui.qGreen(color)) / 255.0) * 0.75
                b = (float(QtGui.qBlue(color)) / 255.0) * 0.75
                a = float(QtGui.qAlpha(color) / 255.0)
                img.setPixel(x, y, QtGui.QColor.fromRgbF(r, g, b, a).rgba())
                # print('    (%s, %s) is (%s, %s, %s, %s)' % (x, y, r, g, b, a))
        return img


    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')

        img = QtGui.QImage()
        img.load('{iroot}/Icons8_color/png_48/modern_art-48.png'.format(iroot=ICONS_ROOT))

        img_bright = self._get_brighter_image(img)
        img_dark = self._get_darker_image(img)
        
        # btn = MyButton(img, img_bright, img_dark, self)
        btn = MyButton(img, img_dark, img_dark, self)

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
