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

import jinja2
import json

import pprint
import logging

from PySide import QtGui, QtCore, QtWebKit

# --- local imports
import pwui


class WebPageWithConsoleLogger( QtWebKit.QWebPage ):
    """
    Makes it possible to use a Python logger to print javascript console messages
    """
    def __init__(self, parent=None):
        super(WebPageWithConsoleLogger, self).__init__(parent)

    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):

        console_msg_str = "JS({}:{}): {}".format( sourceID, lineNumber, msg )
        logging.info( console_msg_str )


class OutputCapture( QtCore.QObject ):
    """
    Makes it possible to capture stdout and stderr messages in order to write them
    out to a PySide QtWidget for display within the UI (and not in a console)
    """

    outputWritten = QtCore.Signal(object, object)

    def __init__( self, parent, is_error_msg=False ):

        QtCore.QObject.__init__(self, parent)
        if is_error_msg:
            self._stream = sys.stderr
            sys.stderr = self
        else:
            self._stream = sys.stdout
            sys.stdout = self
        self._is_error_msg = is_error_msg

    def write( self, msg_str ):
        self._stream.write( msg_str )
        self.outputWritten.emit( msg_str, self._is_error_msg)

    def __getattr__(self, name):
        return getattr(self._stream, name)

    def __del__(self):
        try:
            if self._is_error_msg:
                sys.stderr = self._stream
            else:
                sys.stdout = self._stream
        except AttributeError:
            pass


class CentralWidget( QtGui.QWidget ):

    def __init__( self, app_window, html_template_file, app_config, display_log_to_console=False ):

        super(CentralWidget, self).__init__()

        self.unique_id_next = 1

        self.app_window = app_window
        self.app_config = app_config

        self.app_dir_path = self.app_config.get('APP_DIR_PATH','')

        self.user_cache_path = pwui.util.expand_path( self.app_config.get("USER_CACHE_PATH",""),
                                                      force_forward_slash=True )
        self.app_config["USER_CACHE_PATH"] = self.user_cache_path
        if not os.path.isdir( self.user_cache_path ):
            os.makedirs( self.user_cache_path )

        self.user_session_dirpath = '{}/sessions/{}'.format( self.user_cache_path,
                                                             pwui.util.get_timestamp_str( include_mills=True,
                                                                                          delims={
                                                                                              'date': '-',
                                                                                              'gap': '_',
                                                                                              'time': '.',
                                                                                              'mills': '.'
                                                                                            } ) )
        if not os.path.isdir( self.user_session_dirpath ):
            os.makedirs( self.user_session_dirpath )

        self.session_log_filepath = '{}/_session.log'.format( self.user_session_dirpath )

        fmt_str = '%(asctime)s [%(levelname)s] %(message)s'
        logging.basicConfig( filename=self.session_log_filepath, filemode='a',
                             # format='%(asctime)s [%(levelname)s] %(message)s',
                             format=fmt_str,
                             datefmt='%Y-%m-%d %H:%M:%S',
                             level=logging.DEBUG )

        #--- write to stdout and stderr also
        console_handler = logging.StreamHandler()
        console_handler.setFormatter( logging.Formatter( fmt_str ) )
        logging.getLogger().addHandler( console_handler )
        #---

        env_cfg_file = '{}/example_configs/example_env_config.json'.format( self.app_dir_path )
        app_cfg_file = '{}/example_configs/example_app_path_config.json'.format( self.app_dir_path )

        self.env_mgr = pwui.EnvManager()
        self.env_mgr.add_env_config_file( "my_env", env_cfg_file, apply_now=True )
        self.env_mgr.add_app_config_file( "my_app_paths", app_cfg_file, apply_now=True )

        self.j2_template_env = jinja2.Environment( loader=jinja2.FileSystemLoader(
                                                    searchpath=[
                                                        '{}'.format(self.app_dir_path),
                                                        '{}/cmd'.format(self.app_dir_path),
                                                    ] ) )
        file_sys_protocol = 'file:///' if sys.platform == 'win32' else 'file://'
        template_vars = {
            'FPRE': file_sys_protocol,
            'AL': '{{', 'AR': '}}',
            'APP_DIR_PATH': self.app_dir_path,
            'ICON_DIR_PATH': self.app_config.get('PATHS',{}).get('ICON_DIR',''),
            'WEB_LIB_PATH': self.app_config.get('PATHS',{}).get('WEB_LIB',''),
            'APP_THEME': 'dark',
        }
        self.base_template_vars = template_vars.copy()

        pp = pprint.PrettyPrinter( indent=4 )

        cmd_scripts_html_arr = []
        cmd_list = self._get_cmd_list()

        for cmd in cmd_list:
            cmd_script_line = '<script src="{fpre}{app_path}/cmd/{c}/{c}.js"></script>'.format(
                                    fpre=file_sys_protocol, app_path=self.app_dir_path, c=cmd )
            cmd_scripts_html_arr.append( cmd_script_line )

        template_vars.update( {
            'CMD_SCRIPTS': '\n'.join( cmd_scripts_html_arr ),
        } )

        html_to_load = self.j2_template_env.get_template( html_template_file ).render( template_vars )

        DEBUG_HTML = False
        if DEBUG_HTML:
            open("_generated_page.html","w").write( "{}\n".format( html_to_load ) )

        self.webkit_viewer = QtWebKit.QWebView()
        self.webkit_viewer.setPage( WebPageWithConsoleLogger() )
        self.webkit_viewer.setHtml( html_to_load )

        self.webkit_view_frame = self.webkit_viewer.page().mainFrame()

        # Add hooks to allow executing python functionality from within JavaScript
        #
        self.webkit_view_frame.addToJavaScriptWindowObject( 'pyAppWin', self.app_window )
        self.webkit_view_frame.addToJavaScriptWindowObject( 'pyCentralWdg', self )

        # self.webkit_view_frame.setScrollBarPolicy( QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff )
        # self.webkit_view_frame.setScrollBarPolicy( QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff )

        self.output_log_wdg = QtGui.QTextBrowser( self )

        main_wdg_layout = QtGui.QVBoxLayout()

        main_wdg_layout.setSpacing(0)
        main_wdg_layout.setContentsMargins(0, 0, 0, 0)

        main_wdg_layout.addWidget( self.webkit_viewer )
        main_wdg_layout.addWidget( self.output_log_wdg )

        self.setLayout( main_wdg_layout )

        # hook up capture of stdout and stderr ...
        #
        self.stdout_capture = OutputCapture( self, is_error_msg=False )
        self.stdout_capture.outputWritten.connect( self.capture_output_to_log )

        self.stderr_capture = OutputCapture( self, is_error_msg=True )
        self.stderr_capture.outputWritten.connect( self.capture_output_to_log )

        # --- worker operations
        self.worker_op = None


    def generate_cmd_panel_html( self, cmd ):

        cmd_template_vars  = self.base_template_vars.copy()

        cmd_opts = json.loads( open('{path}/cmd/{c}/{c}.json'.format( path=self.app_dir_path, c=cmd ), 'r').read() )

        cmd_template_vars["CMD_TITLE"] = cmd_opts.get('CMD_TITLE', cmd)
        cmd_template_vars["CMD_NAME"] = cmd

        filler_d = self.get_cmd_fillers( cmd_opts.get('FILLERS',[]) )
        cmd_template_vars.update( filler_d )

        id_gen_list = cmd_opts.get('ID_GENERATE_LIST',[])
        for id_gen in id_gen_list:
            cmd_template_vars[ id_gen ] = '{}_{}'.format( id_gen, str(self.unique_id_next).zfill(8) )
            self.unique_id_next += 1

        html_tmpl = '{c}/{c}.TEMPLATE.html'.format( c=cmd )
        cmd_html = self.j2_template_env.get_template( html_tmpl ).render( cmd_template_vars )

        return cmd_html


    def get_cmd_fillers( self, filler_info_list ):

        logging.debug('')
        logging.debug(':: FILLER_INFO_LIST: {}'.format( filler_info_list ))

        filler_d = {}

        for filler_info in filler_info_list:
            filler_type = filler_info.get('filler_type','')
            if filler_type == 'data_list':
                query = filler_info.get('query_info',{})
                db = pwui.BackEnd( query.get('backend_server',''), query.get('backend_type','') )
                f_list = query.get("fields",[])

                query_results = db.find( query.get('entity_type',''), filters=query.get('filters',[]), fields=f_list,
                                            order_by=query.get('order_by',[]) )
                filler_list = []
                for res in query_results:
                    d = {}
                    for i, f in enumerate(f_list):
                        d[ f ] = res[ i ]
                    filler_list.append( d.copy() )

                filler_d[ filler_info.get('template_key','') ] = filler_list[ : ]
            else:
                pass

        return filler_d.copy()


    def capture_output_to_log( self, message_str, is_error_msg ):

        color_str = '#000099'
        if is_error_msg:
            color_str = '#CC0000'

        self.output_log_wdg.insertHtml( '<span style="color: {};">'.format( color_str ) +
                                        message_str.replace('<','&lt;').replace('>','&gt;') +
                                        '</span><br />' )

    def _get_cmd_list( self ):

        cmd_list = []
        item_list = os.listdir( '{}/cmd'.format( self.app_dir_path ) )
        for item in item_list:
            item_path = os.path.join( self.app_dir_path, 'cmd', item )
            if os.path.isdir( item_path ) and item[0] not in ('_','.'):
                cmd_list.append( item )
        return cmd_list


    @QtCore.Slot(str)
    def call_from_js( self, cmd_params_json ):

        cmd_params_map = {}
        try:
            cmd_params_map = json.loads( cmd_params_json )
        except:
            logging.error( 'In call_from_js(): unable to load JSON string with value """{}"""'.format(cmd_params_json))
            return

        if cmd_params_map:
            params = cmd_params_map.get('params')
            cmd_name = cmd_params_map.get('cmd')

            if params.get('_cmd_op_type_', None) == 'WORKER_OP':
                worker_op_module = None
                imp_stmt = 'import cmd.{c}.{c}\nreload( cmd.{c}.{c} )\nworker_op_module = cmd.{c}.{c}'.format(
                                c=cmd_name )
                exec( imp_stmt )
                self.worker_op = worker_op_module.CmdWorkerOp( self, params )

                self.worker_op.started.connect( self.worker_op_started )
                self.worker_op.finished.connect( self.worker_op_finished )
                self.worker_op.terminated.connect( self.worker_op_terminated )

                self.worker_op.set_callback( self.worker_op_callback_fn )

                self.run_js(
'''
var ion_icon_info = {
    'icon_name': 'ion-erlenmeyer-flask',
    'color_str': 'orange'
};

var show_progress = false;
var btn_info_list = [
    {'label': 'OK', 'js_to_exec': 'pwui.popmsg_close();'},
    {'label': 'CANCEL', 'js_to_exec': 'pwui.popmsg_close();'},
];

var body_text = "Testing by copying a src file to many files in destination directory.";
pwui.popmsg_open( "Worker Op Test", body_text, ion_icon_info, show_progress, btn_info_list );
pwui.popmsg_set_progress( 0.0, '0%' );

''' )
                self.worker_op.start()

            elif cmd_name.startswith('op:'):
                cmd_name = cmd_name[3:]
                imp_stmt = 'import op.{c}.{c}\nreload( op.{c}.{c} )'.format( c=cmd_name )
                exec( imp_stmt )
                run_stmt = 'op.{c}.{c}.run_op( params, self, pwui.BackEnd )'.format( c=cmd_name )
                exec( run_stmt )

            else:
                imp_stmt = 'import cmd.{c}.{c}\nreload( cmd.{c}.{c} )'.format( c=cmd_name )
                exec( imp_stmt )
                run_stmt = 'cmd.{c}.{c}.execute_cmd( params )'.format( c=cmd_name )
                exec( run_stmt )


    def worker_op_started( self ):
        pass

    def worker_op_finished( self ):
        pass

    def worker_op_terminated( self ):
        pass

    def worker_op_callback_fn( self, cb_dict ):
        action = cb_dict.get('action','')
        status = cb_dict.get('status','')

        if action == 'percent_update':
            percent_0_to_1 = cb_dict.get('percent', 0.0)
            percent_int = int( percent_0_to_1 * 100.0 + 0.5 )
            self.run_js( "pwui.popmsg_set_progress( {}, '{}%' );".format( percent_0_to_1, percent_int ) )
        else:
            sys.stdout.write('\nGot WorkerOp "{}" callback with status: "{}"\n'.format( action, status ))
            sys.stdout.flush()


    def run_js( self, js_str ):

        self.webkit_view_frame.evaluateJavaScript( js_str )


    def launch_app( self, app_name, params ):

        app_logfile = '{}/{}__{}.log'.format( self.user_session_dirpath, app_name,
                                              pwui.util.get_timestamp_str( filename_friendly=True,
                                                                           include_mills=True ) )

        pid = self.env_mgr.launch_app( app_name, log_filepath=app_logfile,
                                       extra_args_list=params.get('extra_args',[]),
                                       override_cwd=params.get('override_cwd',None) )


    def log_close( self ):

        logging.info( "User selected to EXIT PyWebUI application -- SESSION ENDED." )



class AppWindow( QtGui.QMainWindow ):

    def __init__( self, html_file_path, display_log_to_console=False ):

        super( AppWindow, self ).__init__()

        app_dir_path = os.path.dirname( os.path.realpath( __file__ ) ).replace('\\','/')
        app_config = json.loads( open( '{}/pywebui_config.json'.format( app_dir_path ), 'r' ).read() )

        for path_key, platform_path_info in app_config['PATHS'].iteritems():
            if path_key == '//':
                continue
            path_to_use = pwui.util.expand_path( platform_path_info.get( sys.platform, '' ),
                                                 force_forward_slash=True )
            app_config['PATHS'][ path_key ] = path_to_use

        app_config['APP_DIR_PATH'] = app_dir_path
        sys.path.insert( 0, app_dir_path )

        # --- Directly load IonIcons .ttf into the PySide Font Database ---
        #     NOTE: need to do this so that the IonIcons will show up on Mac OS X
        font_db = QtGui.QFontDatabase()

        orig_font_fam_list = font_db.families()[:]

        font_db.addApplicationFont( '{}/3rdparty/fonts/ionicons.ttf'.format( app_dir_path ) )

        # --- Code / Mono-space font:
        font_db.addApplicationFont( '{}/3rdparty/fonts/DejaVuSansMono.ttf'.format( app_dir_path ) )

        # font_db.addApplicationFont( '{}/3rdparty/fonts/Rubik-Regular.ttf'.format( app_dir_path ) )
        # font_db.addApplicationFont( '{}/3rdparty/fonts/Rubik-Bold.ttf'.format( app_dir_path ) )

        # --- Header and Title font:
        font_db.addApplicationFont( '{}/3rdparty/fonts/MerriweatherSans-Regular.ttf'.format( app_dir_path ) )
        font_db.addApplicationFont( '{}/3rdparty/fonts/MerriweatherSans-Bold.ttf'.format( app_dir_path ) )
        font_db.addApplicationFont( '{}/3rdparty/fonts/MerriweatherSans-ExtraBold.ttf'.format( app_dir_path ) )

        # --- Body text font:
        font_db.addApplicationFont( '{}/3rdparty/fonts/CrimsonText-Roman.ttf'.format( app_dir_path ) )
        font_db.addApplicationFont( '{}/3rdparty/fonts/CrimsonText-Bold.ttf'.format( app_dir_path ) )
        font_db.addApplicationFont( '{}/3rdparty/fonts/CrimsonText-Italic.ttf'.format( app_dir_path ) )
        font_db.addApplicationFont( '{}/3rdparty/fonts/CrimsonText-BoldItalic.ttf'.format( app_dir_path ) )

        full_font_fam_list = font_db.families()

        print('=== Newly loaded fonts ... ===')
        for full_font_fam in full_font_fam_list:
            if full_font_fam in orig_font_fam_list:
                continue
            print('')
            print(':: {} ...'.format( full_font_fam ))
            style_list = font_db.styles( full_font_fam )
            for style in style_list:
                print('      {}'.format( style ))
        print('')

        # setGeometry(x_pos, y_pos, width, height)
        # upper left corner coordinates (x_pos, y_pos)
        self.setGeometry( 300, 100, 600, 700 )

        self.setWindowTitle('PyWebUI')

        # === Tool Bar ===
        self.tool_bar = QtGui.QToolBar( 'Tools', parent=self )
        self.addToolBar( QtCore.Qt.BottomToolBarArea, self.tool_bar )
        self.tool_bar.setMovable( False )
        self.tool_bar.setEnabled( True )  # NOTE: use setEnabled() to disable (False) or enable (True) toolbar

        # === Set up Actions ===
        self.action_info = {}

        # -- Exit Action --
        action = self.create_action( 'Exit', '{}/door_in.png'.format( app_config.get('PATHS',{}).get('ICON_DIR','') ),
                                     # 'Exit Program', add_to_toolbar=False )
                                     'Exit Program', add_to_toolbar=True )

        if sys.platform == 'darwin':
            # use command-Q on Mac OS X
            action.setShortcut('Meta+Q')
        else:
            # use Ctrl-Q for windows and linux
            action.setShortcut('Ctrl+Q')

        action.triggered.connect( self.close )

        # === Menu Bar ===
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu('&File')  # add file menu
        file_menu.addAction( self.action_info.get('Exit') )  # add Exit to file menu

        # === Status Bar ===
        # self.status_bar = self.statusBar()  # does this work?

        # === Set the central widget ===
        self.central_widget = CentralWidget( self, html_file_path, app_config )
        self.setCentralWidget( self.central_widget )


    def create_action( self, action_key, icon_path, tool_tip_str, add_to_toolbar=True ):

        self.action_info[ action_key ] = QtGui.QAction( QtGui.QIcon( icon_path ), tool_tip_str, self )
        if add_to_toolbar:
            self.tool_bar.addAction( self.action_info.get( action_key ) )
        return self.action_info.get( action_key )


    def closeEvent( self, event ):

        self.central_widget.log_close()
        event.accept()


if __name__ == '__main__':

    html_file_path = sys.argv[ 1 ]

    app = QtGui.QApplication([])
    app_window = AppWindow( html_file_path, display_log_to_console=False )
    app_window.show()
    app_window.raise_()
    sys.exit( app.exec_() )


