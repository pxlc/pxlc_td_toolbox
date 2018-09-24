
import os
import sys

import json
import traceback
import logging
import types
import subprocess

# --- local imports
import util


class EnvManager( object ):

    def __init__( self ):

        self.env_baseline = os.environ.copy()

        self.env_config_path_by_name = {}
        self.active_env = {}
        self.active_env_name = ""

        self.app_config_path_by_name = {}
        self.active_app_cfg = {}
        self.active_app_cfg_name = ""


    def add_env_config_file( self, env_config_key_name, env_config_filepath, apply_now=False ):

        self.env_config_path_by_name[ env_config_key_name ] = env_config_filepath

        if apply_now:
            self.apply_env_config( env_config_key_name )


    def add_app_config_file( self, app_config_key_name, app_config_filepath, apply_now=False ):

        self.app_config_path_by_name[ app_config_key_name ] = app_config_filepath

        if apply_now:
            self.set_app_config( app_config_key_name )


    def debug_list_env( self ):

        if not self.active_env:
            # TODO: provide error message.
            return

        env_keys = self.active_env.keys()
        env_keys.sort()

        for ek in env_keys:
            ev = self.active_env.get( ek, None )
            logging.debug("    {} ({}) = {} ({})".format( ek, type(ek), ev, type(ev) ))


    def set_app_config( self, app_config_key_name_to_set ):

        if app_config_key_name_to_set not in self.app_config_path_by_name:
            # TODO: provide error message.
            return

        json_filepath = self.app_config_path_by_name.get( app_config_key_name_to_set, "" )
        if not os.path.isfile( json_filepath ):
            # TODO: provide error message.
            return

        try:
            app_info_map = json.loads( open( json_filepath, "r" ).read() )
        except:
            logging.error(">>> EnvManager.set_app_config() EXCEPTION ...")
            logging.error( traceback.format_exc() )
            return

        del app_info_map["//"]

        # for app_name in app_info_map.keys():
        #     app_path = app_info_map.get( app_name ).get( "path", "" )
        #     app_info_map[ app_name ][ "path" ] = util.expand_path( app_path )

        self.active_app_cfg = app_info_map.copy()
        self.active_app_cfg_name = app_config_key_name_to_set


    def apply_env_config( self, config_key_name_to_apply ):

        if config_key_name_to_apply not in self.env_config_path_by_name:
            # TODO: provide error message.
            return

        json_filepath = self.env_config_path_by_name.get( config_key_name_to_apply, "" )
        if not os.path.isfile( json_filepath ):
            # TODO: provide error message.
            return

        try:
            env_info_list = json.loads( open( json_filepath, "r" ).read() )
        except:
            logging.error(">>> EnvManager.apply_env_config() EXCEPTION ...")
            logging.error( traceback.format_exc() )
            return

        env_to_restore = os.environ.copy()
        os.environ.clear()

        # Always start from baseline environment
        os.environ.update( self.env_baseline )

        # Apply environment ...
        for env_info in env_info_list:
            if not env_info:
                continue

            e_var = str( env_info.get("var","") )
            if not e_var:
                continue
            e_value = str( env_info.get("value","") )
            e_type = env_info.get("type","")

            if type(e_value) is types.NoneType:
                # this means remove entry from environment
                del os.environ[ e_var ]
                continue

            if not e_type:
                e_type = "string"

            operation = None
            if '.' in e_type:
                bits = e_type.split('.')
                e_type = bits[0]
                operation = bits[1]

            if e_type == "dir_path":
                assign_path = util.expand_path( e_value )
                if assign_path:
                    os.environ[ e_var ] = assign_path
            elif e_type == "path_list":
                exist_path_list = os.environ.get( e_var, "" ).split( os.path.pathsep )
                assign_path_list = []
                for path in e_value:
                    assign_path = util.expand_path( path )
                    if not assign_path:
                        continue
                    if assign_path in exist_path_list or assign_path in assign_path_list:
                        continue
                    assign_path_list.append( assign_path )

                assign_path_list_str = os.path.pathsep.join( assign_path_list )

                if operation == "prepend":
                    os.environ[ e_var ] = "{}:{}".format( assign_path_list_str, os.getenv( e_var, "" ) )
                elif operation == "replace":
                    os.environ[ e_var ] = assign_path_list_str
                else:
                    # default behaviour is to append
                    os.environ[ e_var ] = "{}:{}".format( os.getenv( e_var, "" ), assign_path_list_str )
            else:
                assign_value = e_value
                if operation != "NO_EXPAND":
                    assign_value = os.path.expandvars( e_value )
                os.environ[ e_var ] = assign_value

        self.active_env = os.environ.copy()

        self.active_env_name = config_key_name_to_apply
        self.active_env["PWUI_ACTIVE_ENV"] = self.active_env_name

        # restore environment
        os.environ.clear()
        os.environ.update( env_to_restore )


    def launch_app( self, app_name, log_filepath=None, extra_args_list=[], override_cwd=None ):

        if not self.active_env:
            # TODO: provide error message.
            return

        if not self.active_app_cfg:
            # TODO: provide error message.
            return

        if app_name not in self.active_app_cfg:
            # TODO: provide error message.
            return

        app_info = self.active_app_cfg.get( app_name, {} ).get( sys.platform, {} )
        if not app_info:
            # TODO: provide error message.
            return

        log_fp = None
        if log_filepath:
            try:
                log_fp = open( log_filepath, 'w' )
            except:
                logging.error("Unable to open app launch log file located here: {}".format( log_filepath ))
                logging.error("Aborting launch of app named '{}'.".format( app_name ))
                return

        env_to_restore = os.environ.copy()
        os.environ.clear()
        os.environ.update( self.active_env )

        exe_path = util.expand_path( app_info.get("path","") )

        # restore environment
        os.environ.clear()
        os.environ.update( env_to_restore )

        cmd_and_args = [ exe_path ] + app_info.get("fixed_args", []) + extra_args_list

        set_cwd = app_info.get("set_cwd", None)
        if override_cwd and os.path.isdir( override_cwd ):
            set_cwd = override_cwd

        creation_flags = None
        cf_str = app_info.get("creation_flags","")
        if cf_str:
            stmt = "creation_flags = {}".format( cf_str )
            exec( stmt )

        pid = 0
        if creation_flags:
            if log_fp:
                pid = subprocess.Popen( cmd_and_args, env=self.active_env.copy(),
                                        creationflags=creation_flags, cwd=set_cwd, stdout=log_fp, stderr=log_fp ).pid
            else:
                pid = subprocess.Popen( cmd_and_args, env=self.active_env.copy(),
                                        creationflags=creation_flags, cwd=set_cwd ).pid
        else:
            if log_fp:
                pid = subprocess.Popen( cmd_and_args, env=self.active_env.copy(), cwd=set_cwd,
                                        stdout=log_fp, stderr=log_fp ).pid
            else:
                pid = subprocess.Popen( cmd_and_args, env=self.active_env.copy(), cwd=set_cwd ).pid

        return pid



if __name__ == "__main__":

    # logging.basicConfig( format='[%(asctime)s %(levelname)s] %(message)s', level=logging.DEBUG )
    logging.basicConfig( format='[%(levelname)s] %(message)s', level=logging.DEBUG )

    # Code to test EnvManager class
    env_config_file = sys.argv[1]
    app_config_file = sys.argv[2]
    app_to_launch = sys.argv[3]

    env_mgr = EnvManager()
    env_mgr.add_env_config_file( "my_env", env_config_file, apply_now=True )
    env_mgr.add_app_config_file( "my_apps", app_config_file, apply_now=True )

    env_mgr.debug_list_env()

    pid = env_mgr.launch_app( app_to_launch )
    logging.info('::')
    logging.info(":: got pid {} for launch of '{}' app".format( pid, app_to_launch ))
    logging.info('::')


