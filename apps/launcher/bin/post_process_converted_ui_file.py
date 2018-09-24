
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
