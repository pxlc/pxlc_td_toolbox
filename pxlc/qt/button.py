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

from PySide import QtCore, QtGui


class HoverPressIconButton(QtGui.QPushButton):

    def __init__(self, icon_image_filepath, normal_factor=None, bright_factor=1.25, dark_factor=0.85,
                 btn_w=128, btn_h=128, img_w=None, img_h=None, tooltip='', use_transparent_bkg=False,
                 parent=None):

        super(HoverPressIconButton, self).__init__(parent)

        if img_w is None:
            img_w = btn_w
        if img_h is None:
            img_h = btn_h

        img = QtGui.QImage()
        img.load(icon_image_filepath)

        # if img.width() != img_width or img.height() != img_height:
        #     img = img.scaled(img_width, img_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        img_bright = self._get_adjusted_image(img, bright_factor)
        img_dark = self._get_adjusted_image(img, dark_factor)

        if normal_factor is not None:
            img = self._get_adjusted_image(img, normal_factor)

        self.icon_normal = QtGui.QIcon()
        self.icon_normal.addPixmap(QtGui.QPixmap.fromImage(img))

        self.icon_hover = QtGui.QIcon()
        self.icon_hover.addPixmap(QtGui.QPixmap.fromImage(img_bright))

        self.icon_press = QtGui.QIcon()
        self.icon_press.addPixmap(QtGui.QPixmap.fromImage(img_dark))

        self.setIcon(self.icon_normal)

        self.mouse_btn_pressed = False
        self.mouse_hover_on = False

        self.setMinimumSize(QtCore.QSize(btn_w, btn_h))
        self.setMaximumSize(QtCore.QSize(btn_w, btn_h))
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setText("")

        if use_transparent_bkg:
            self.setStyleSheet("background-color: rgba(0,0,0,0);")

        self.setIconSize(QtCore.QSize(img_w, img_h))
        if tooltip:
            self.setToolTip(tooltip)

        self.click_action_fn = None
        self.click_action_data = None

    def setClickAction(self, click_fn, click_data=None):
        self.click_action_fn = click_fn
        self.click_action_data = click_data

    def enterEvent(self, evt):
        self.mouse_hover_on = True
        if not self.mouse_btn_pressed:
            self.setIcon(self.icon_hover)

    def leaveEvent(self, evt):
        self.mouse_hover_on = False
        if not self.mouse_btn_pressed:
            self.setIcon(self.icon_normal)

    # ------------------------------------------------------------------------------------------
    # NOTE: you do not get "enter" or "leave" events firing between "press" and "release" events
    # ------------------------------------------------------------------------------------------

    def mousePressEvent(self, evt):
        self.mouse_btn_pressed = True
        self.setIcon(self.icon_press)

    def mouseReleaseEvent(self, evt):
        self.mouse_btn_pressed = False
        # self.mouse_hover_on = self.underMouse()  # <-- this does not work
        pos_mouse =  evt.pos()
        if self.rect().contains(pos_mouse):
            self.mouse_hover_on = True
        else:
            self.mouse_hover_on = False

        if self.mouse_hover_on:
            self.setIcon(self.icon_hover)
            if self.click_action_fn:
                if self.click_action_data is None:
                    self.click_action_fn()
                else:
                    self.click_action_fn(self.click_action_data)
        else:
            self.setIcon(self.icon_normal)

    def _get_adjusted_image(self, q_image, mult_factor):

        img = q_image.copy(0, 0, q_image.height(), q_image.width())

        mult_tuple = (1.0, 1.0, 1.0)
        if type(mult_factor) is float:
            mult_tuple = (mult_factor, mult_factor, mult_factor)
        elif type(mult_factor) is tuple:
            mult_tuple = mult_factor

        for y in range(img.height()):
            for x in range(img.width()):
                color = img.pixel(x, y)

                r = (float(QtGui.qRed(color)) / 255.0)
                g = (float(QtGui.qGreen(color)) / 255.0)
                b = (float(QtGui.qBlue(color)) / 255.0)
                a = float(QtGui.qAlpha(color) / 255.0)

                r *= mult_tuple[0] # assume tuple of at least one item!
                if len(mult_tuple) > 1:
                    g *= mult_tuple[1]
                if len(mult_tuple) > 2:
                    b *= mult_tuple[2]

                # now clamp all values to max of 1.0
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

