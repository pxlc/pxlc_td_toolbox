
import logging


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


