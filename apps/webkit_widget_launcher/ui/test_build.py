
import os
import sys

import jinja2


if __name__ == '__main__':

    app_dir_path = os.path.dirname( os.path.realpath( __file__ ) ).replace('\\','/')
    j2_template_env = jinja2.Environment( loader=jinja2.FileSystemLoader( searchpath=[ app_dir_path ] ) )


