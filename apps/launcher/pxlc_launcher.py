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

import os
import sys
import subprocess

# Add path to Qt shim to sys.path, or comment out next line if Qt shim is already available
#
sys.path.append('../../../../thirdparty_lib/python27/Qt.py-1.2.0.b2')
 
from Qt import QtCore, QtWidgets, QtGui
 
from pxlc_launcher_UI_for_Qt_shim import Ui_MainWindow


class ActualMainWindow( QtWidgets.QMainWindow ):

    def __init__(self):

        super(ActualMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connect_ui_actions()
        self._adjust_ui()

    def _adjust_ui(self):

        self.ui.textBrowser.setHtml("The <i>quick</i> brown <span style='color: red;'>fox</span> ran " \
                                    "up the water spout. 1lIO0GQqg")
        self.ui.label.setProperty('cls', 'Title')

    def _connect_ui_actions(self):

        self.ui.pushButton.clicked.connect(self.launch_app)
        self.ui.pushButton_2.clicked.connect(self.launch_command_shell)

    def launch_app(self):

        self.ui.statusbar.showMessage(':: Launching super cool application ...')
        subprocess.Popen([r'C:\Program Files\Blender Foundation\Blender\blender.exe'])

    def launch_command_shell(self):

        self.ui.statusbar.showMessage(':: Launching command shell console ...')
        os.system('START cmd.exe')


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    # Need to create QtGui.QFontDatabase BEFORE setting style sheet that contains
    # fonts from the system
    #
    font_db = QtGui.QFontDatabase()
    orig_font_fam_list = font_db.families()[:]

    # Add Title font
    font_db.addApplicationFont( 'fonts/Merriweather_Sans/MerriweatherSans-Regular.ttf' );
    font_db.addApplicationFont( 'fonts/Merriweather_Sans/MerriweatherSans-Bold.ttf' );

    # Add Body Text font
    font_db.addApplicationFont( 'fonts/Open_Sans/OpenSans-Regular.ttf' );
    font_db.addApplicationFont( 'fonts/Open_Sans/OpenSans-Italic.ttf' );
    font_db.addApplicationFont( 'fonts/Open_Sans/OpenSans-Bold.ttf' );
    font_db.addApplicationFont( 'fonts/Open_Sans/OpenSans-BoldItalic.ttf' );

    # Add Optional Body Text font
    font_db.addApplicationFont( 'fonts/Montserrat/Montserrat-Regular.ttf' );
    font_db.addApplicationFont( 'fonts/Montserrat/Montserrat-Italic.ttf' );
    font_db.addApplicationFont( 'fonts/Montserrat/Montserrat-Bold.ttf' );
    font_db.addApplicationFont( 'fonts/Montserrat/Montserrat-BoldItalic.ttf' );

    # Add Fixed space font
    font_db.addApplicationFont( 'fonts/Roboto_Mono/RobotoMono-Regular.ttf' );
    font_db.addApplicationFont( 'fonts/Roboto_Mono/RobotoMono-Bold.ttf' );

    added_font_fam_list = []
    full_font_fam_list = font_db.families()
    for f in full_font_fam_list:
        if f in orig_font_fam_list:
            continue
        added_font_fam_list.append( f )

    for added_font in added_font_fam_list:
        print( '{} ...'.format( added_font ) )
        style_list = font_db.styles( added_font )
        for style in style_list:
            print('    {}'.format( style ))

    with open('pxlc_launcher.qt.css', 'r') as fp:
        app.setStyleSheet( fp.read() )

    my_window = ActualMainWindow()
    my_window.show()

    sys.exit(app.exec_())


