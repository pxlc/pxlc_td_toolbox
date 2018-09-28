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
import logging


def run_op( params, central_widget, BackEnd ):

    filler_info = params.get('filler_info',{})

    shot_list = []

    filler_type = filler_info.get('filler_type','')
    if filler_type == 'data_list':
        query = filler_info.get('query_info',{})
        db = BackEnd( query.get('backend_server',''), query.get('backend_type','') )
        f_list = query.get("fields",[])

        query_results = db.find( query.get('entity_type',''), filters=query.get('filters',[]), fields=f_list,
                                    order_by=query.get('order_by',[]) )
        for res in query_results:
            d = {}
            for i, f in enumerate(f_list):
                value = res[ i ]
                if type(value) in types.StringTypes:
                    value = str(value)
                d[ str(f) ] = value
            shot_list.append( d.copy() )

    pp = pprint.PrettyPrinter( indent=2 )

    js_list_name = filler_info.get('target_js_list','')
    for shot in shot_list:
        js_stmt = '''{}.push( {} )'''.format( js_list_name, pp.pformat( shot ) )
        logging.debug('')
        logging.debug('JS: {}'.format( js_stmt ))
        central_widget.run_js( js_stmt )

    js_callback_stmt = filler_info.get('js_completion_stmt','')
    central_widget.run_js( js_callback_stmt )


