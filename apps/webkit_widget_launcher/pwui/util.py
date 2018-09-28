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

import datetime


# -----------------------------------------------------------------------------------------
#  Path handling functionality
# -----------------------------------------------------------------------------------------

def expand_path( in_path, force_forward_slash=False ):

    if not in_path:
        return in_path

    out_path = os.path.expandvars( os.path.expanduser( in_path ) )

    if force_forward_slash:
        return fo_slash( out_path )

    return os_slash( out_path )


def forward_slash( in_path ):

    if not in_path:
        return in_path

    return in_path.replace('\\','/')


def fo_slash( in_path ):
    return forward_slash( in_path )


def os_slash( in_path ):

    if not in_path:
        return in_path

    sep = os.path.sep
    wrong_sep_by_sep = {'/': '\\', '\\': '/'}

    out_path = in_path.replace( wrong_sep_by_sep.get( sep, '/' ), sep )

    return out_path


# -----------------------------------------------------------------------------------------
#  Timestamp generation functionality
# -----------------------------------------------------------------------------------------

def get_timestamp_str( filename_friendly=False, include_mills=False, delims=None ):

    now_dt = datetime.datetime.now()

    mills = ".{}".format( now_dt.strftime("%f").zfill(6)[:3] )
    ts_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")

    if delims:
        ts_str = ts_str.replace('-', delims.get('date','')).replace(':', delims.get('time','')).replace(' ',
                                                                                                delims.get('gap',''))
        mills = mills.replace('.', delims.get('mills',''))
    elif filename_friendly:
        ts_str = ts_str.replace('-','').replace(':','').replace(' ','_')
        mills = mills.replace('.','')

    if include_mills:
        ts_str += mills

    return ts_str


