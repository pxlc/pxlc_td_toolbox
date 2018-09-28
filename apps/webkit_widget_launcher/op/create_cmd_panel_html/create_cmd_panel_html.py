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

import pprint
import types
import base64


def run_op( params, central_widget, BackEnd ):

    cmd_name = params.get('cmd_name','')
    js_completion_callback = params.get('js_completion_callback','')
    js_html_base64_var = params.get('js_html_base64_var','')

    try:
        cmd_panel_html = central_widget.generate_cmd_panel_html( cmd_name )
        js_stmt = '{} = "{}";'.format( js_html_base64_var, base64.b64encode( cmd_panel_html ) )
        central_widget.run_js( js_stmt )
    except:
        # TODO: alert or some notice that error occurred!
        return

    central_widget.run_js( js_completion_callback )


