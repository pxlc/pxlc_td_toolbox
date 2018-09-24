
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


