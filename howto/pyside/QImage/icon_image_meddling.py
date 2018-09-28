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

sys.path.append('../../..')
import pxlc

ICONS_ROOT = '../../../res/icons'


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = pxlc.qt.HoverPressIconButton(
                        '{iroot}/Icons8_color/png_48/modern_art-48.png'.format(iroot=ICONS_ROOT),
                        bright_factor=1.6, dark_factor=0.65, parent=self)

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
