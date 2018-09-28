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

def replace_for_QtWidgets( line ):

    bits = line.split('QtGui.')

    out_line_arr = [ bits[0] ]
    bits = bits[1:]

    for b in bits:
        if b.startswith('QIcon') or b.startswith('QPixmap'):
            out_line_arr += ['QtGui.', b]
        else:
            out_line_arr += ['QtWidgets.', b]

    return ''.join( out_line_arr )


def usage():

    print('')
    print('  Usage: python %s <UI_CONVERTED_TO_PY_FILE> <QT_SHIM_COMPATIBLE_OUTPUT>' %
          os.path.basename(sys.argv[0]))
    print('')


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        usage()
        sys.exit(0)

    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    with open(sys.argv[1], 'r') as in_fp:
        with open(sys.argv[2], 'w') as out_fp:
            for line in in_fp:
                if line.startswith('from PySide import '):
                    out_fp.write( line.replace('PySide', 'Qt').replace('QtGui', 'QtWidgets, QtGui') )
                elif not line.startswith('#') and len(line.strip()) > 0:
                    out_fp.write( replace_for_QtWidgets( line ) )
                else:
                    out_fp.write( line )
