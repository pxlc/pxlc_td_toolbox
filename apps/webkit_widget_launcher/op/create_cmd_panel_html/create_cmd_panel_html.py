
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


