
import logging
import shutil

from pwui.WorkerOpBase import WorkerOpBase


class CmdWorkerOp( WorkerOpBase ):

    def __init__( self, central_wdg, params, parent=None ):
        WorkerOpBase.__init__( self, parent )
        self.central_wdg = central_wdg
        self.params = params
        self.count = 0

    def prep( self, data ):
        data.update( {} )

    def incremental_op( self, data, update_info ):
        # return True to keep going with incremental_op() calls, return False to end run
        ret_bool = True
        self.count += 1
        num_files = self.params.get('num_files', 0)

        if num_files:
            src_fpath = self.params.get('src_filepath','')
            dst_fpath = '{}/SOMEFILE.{}.jpg'.format( self.params.get('dst_dirpath',''), str(self.count).zfill(4) )
            shutil.copy2( src_fpath, dst_fpath )
            data['percent'] = float(self.count) / float(num_files)
        else:
            ret_bool = False

        if self.count == self.params.get('num_files', 0):
            ret_bool = False

        return ret_bool

    def cancel_cleanup( self, data ):
        sys.stdout.write('\n**** CALLED cancel_cleanup() ****\n')
        sys.stdout.flush()


__IGNORE__ = '''
def execute_cmd( params ):

    logging.debug('')
    logging.debug('>> params: {}'.format( params ))

    keys = params.keys()
    keys.sort()

    logging.debug('')

    for k in keys:
        v = params.get(k)
        if type(v) is str or type(v) is unicode:
            logging.debug( '    {} = "{}"'.format( k, params.get(k) ))
        else:
            logging.debug( '    {} = {}'.format( k, params.get(k) ))

    logging.debug('')
'''

