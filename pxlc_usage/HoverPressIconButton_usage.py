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

sys.path.append('..')
import pxlc

ICONS_ROOT = '../res/icons'
IMAGES_ROOT = '../res/images'


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        
        self.setStyleSheet("background-color: #777777;")

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        btn1 = pxlc.qt.HoverPressIconButton(
                '{iroot}/OfficialSpaceXPhotos/2018-09-20_BFR-in-flight_512x512.png'.format(iroot=IMAGES_ROOT),
                bright_factor=1.25, dark_factor=0.85, btn_w=128, btn_h=128,
                tooltip='<b>HoverPressIconButton</b> example using an <i>image</i>',
                parent=self)

        btn1.setClickAction(self.button_pressed, {'greeting': 'Bonjour!'})
        btn1.setObjectName("pushButton1")
        btn1.move(10, 10)       

        btn2 = pxlc.qt.HoverPressIconButton(
                '{iroot}/material-design-icons-3.0.1/hardware/2x_web/ic_cast_connected_white_48dp.png'.format(
                    iroot=ICONS_ROOT),
                bright_factor=(0.85, 0.85, 0.0), dark_factor=(0.70, 0.70, 0.0), btn_w=128, btn_h=128,
                tooltip='<b>HoverPressIconButton</b> example using a <i>white icon</i> and tinted hover/pressed ' \
                            'color, along with button background color and border radius, with text color ' \
                            'for tooltip',
                parent=self)

        btn2.setStyleSheet("background-color: #010101; color: #999999; border-radius: 12px;")

        btn2.setClickAction(self.button_pressed, {'greeting': 'Hola!'})
        btn2.setObjectName("pushButton2")
        btn2.move(20+128, 10)       

        btn3 = pxlc.qt.HoverPressIconButton(
                '{iroot}/material-design-icons-3.0.1/places/2x_web/ic_pool_white_48dp.png'.format(
                    iroot=ICONS_ROOT),
                bright_factor=(0.85, 0.85, 0.0), dark_factor=(0.70, 0.70, 0.0), btn_w=64, btn_h=64,
                tooltip='<b>HoverPressIconButton</b> example using a <i>white icon</i> and tinted hover/pressed ' \
                            'colors, along with button background color (normal and hover) ' \
                            'and border radius',
                parent=self)

        btn3.setObjectName("pushButton3")
        btn3.setStyleSheet("""
            QPushButton#pushButton3 {
                background-color: #444444; border-radius: 12px;
            }
            QPushButton#pushButton3:hover {
                background-color: #666666; border-radius: 12px;
            }
            QPushButton#pushButton3:pressed {
                background-color: #111111; border-radius: 12px;
            }
        """)  # NOTE: the pressed state above isn't working :-\

        btn3.setClickAction(self.button_pressed, {'greeting': 'Ohaiyo!'})
        btn3.move(30+(128*2), 10)       
        
        btn4 = pxlc.qt.HoverPressIconButton(
                '{iroot}/material-design-icons-3.0.1/editor/2x_web/ic_insert_comment_white_48dp.png'.format(
                    iroot=ICONS_ROOT),
                bright_factor=(0.85, 0.85, 0.0), dark_factor=(0.70, 0.70, 0.0), btn_w=64, btn_h=64,
                use_transparent_bkg=True,
                tooltip='<b>HoverPressIconButton</b> example using a <i>white icon</i> and tint hover color, ' \
                            'along with completely transparent button background',
                parent=self)

        btn4.setClickAction(self.button_pressed, {'greeting': 'Maganda Umaga!'})
        btn4.setObjectName("pushButton4")
        btn4.move(40+(128*2+64), 10)       

        self.setGeometry(300, 300, 600, 200)
        self.setWindowTitle('pxlc HoverPressIconButton usage example')    
        self.show()

    def button_pressed(self, data):

        print('')
        print(':: Got button press with greeting: "{g}"'.format(g=data.get('greeting')))
        print('')
        

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
