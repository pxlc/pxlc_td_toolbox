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

import sqlite3
import types

import logging


class BackEnd( object ):

    def __init__( self, db_server, db_type ):

        self.db_server = db_server
        self.db_type = db_type


    def find( self, table, filters=[], fields=[], order_by=None ):

        con = sqlite3.connect( self.db_server )
        c = con.cursor()

        field_list_str = '*'
        if fields:
            field_list_str = ', '.join( fields )

        where_clause = ''
        if filters:
            # for now assume all clauses must be true (use AND)
            wc_arr = []
            for f in filters:
                comp_value = f[2]
                if type(comp_value) in types.StringTypes:
                    comp_value = "'{}'".format( str(comp_value) )
                wc_arr.append( """{} {} {}""".format( f[0], f[1], comp_value ) )
            if wc_arr:
                where_clause = ' WHERE {}'.format( ' AND '.join( wc_arr ) )

        order_by_str = ''
        if order_by:
            # assume order is a tuple ... (<field_name>, <direction>) where direction is 'asc' or 'desc'
            order_by_str = ' ORDER BY {field} {direction}'.format( field=order_by[0], direction=order_by[1].upper() )

        select_stmt = 'SELECT {fl_str} FROM {t}{w}{o};'.format( fl_str=field_list_str, t=table,
                                                                w=where_clause, o=order_by_str )
        logging.debug( select_stmt )

        c.execute( select_stmt )
        results = c.fetchall()

        con.close()

        if results:
            return results[:]
        return []


if __name__ == '__main__':

    db = BackEnd( sys.argv[1], 'sqlite3' )

    logging.debug('')
    logging.debug('')

    res = db.find( 'sequence', [], [], order_by=('id','asc') )
    for r in res:
        logging.debug('    {}'.format( r ))

    logging.debug('')
    logging.debug('')


