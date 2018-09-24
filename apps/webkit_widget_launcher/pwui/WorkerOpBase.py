
import os
import sys
import time

from PySide import QtCore, QtGui

# from QtCore: Signal, QObject, QThread


class _WorkerOpSignal( QtCore.QObject ):

    sig = QtCore.Signal( dict )


class WorkerOpBase( QtCore.QThread ):

    def __init__( self, parent=None ):

        QtCore.QThread.__init__( self, parent )

        self.exiting = False
        self.signal = _WorkerOpSignal()

        self.data = {'percent': 0.0}

        self.__reset()


    def __reset( self ):
        self.__last_percent = 0.0
        self.__is_prepped = False
        self.__was_cancelled = False


    def set_callback( self, callback_fn ):
        self.signal.sig.connect( callback_fn )


    def callback( self, callback_data ):
        self.signal.sig.emit( callback_data )


    def cancel( self ):
        if not self.isRunning():
            return
        self.__was_cancelled = True
        self.exiting = True

        self.__wait_on_cancel()


    def __wait_on_cancel( self ):
        while self.isRunning():
            time.sleep(0.01)
            continue


    def start( self ):
        if self.isRunning() or self.exiting:
            # only allow to start if worker is stopped and *not* running
            return False

        self.__reset()
        self.exiting = False
        super(WorkerOpBase, self).start()  # now execute the QThread ".start()" method

        while not self.isRunning():
            time.sleep(0.01)
            continue
        return True


    def prep( self, data ):
        # NOTE: override this method in sub-class.
        pass


    def incremental_op( self, data ):
        # NOTE: override this method in sub-class.
        # returns True if more work to be done, otherwise False if operation completed
        pass


    def cancel_cleanup( self, data ):
        # NOTE: override this method in sub-class.
        pass


    def run( self ):
        #
        # NOTE: setting the thread instance member variable ".exiting" to True will stop the thread
        #
        while not self.exiting:
            if not self.__is_prepped:
                self.prep( self.data )
                self.__is_prepped = True
                self.callback( {'action': 'prep', 'status': 'completed'} )
                continue
            update_info = {}
            continue_run = self.incremental_op( self.data, update_info )
            if self.data.get('percent', 0.0) > self.__last_percent or update_info.get('force_update', False):
                self.callback( { 'action': 'percent_update', 'percent': self.data.get('percent', 0.0),
                                    'update_info': update_info } )
            if not continue_run:
                self.exiting = True

        if self.__was_cancelled:
            self.cancel_cleanup( self.data )
            self.callback( {'action': 'end_run', 'status': 'cancelled'} )
            self.__was_cancelled = False
        else:
            self.callback( {'action': 'end_run', 'status': 'completed'} )

        self.exiting = False


