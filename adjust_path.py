#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
Created on Tue Jul 30 15:34:13 2024

@author: russ


import adjust.path
"""
# ---- imports

import os
import socket
import sys

from   pathlib import Path

# adjust according to where I am -- in progress
hostname              = socket.gethostname()
cwd                   = os.getcwd()   # better extract from __file__
adjust_path_file      = __file__

adjust_path_path      = Path( adjust_path_file )
adjust_path_dir_path  = adjust_path_path.parent
adjust_path_dir_name  = str( adjust_path_dir_path )

# ---- PLEASE SET/CHECK THESE
APP_MODULE  = "/photo_triag"
VERBOSE     = 1

if VERBOSE > 20:
    print( "in adust_path")
    print( f"{adjust_path_file = }")
    print( f"{cwd              = }")
    print( f"{hostname         = }\n\n")

try:
    #ix   = cwd.index( "_projects/stuffdb")
    print( f"AdjustPath {APP_MODULE = } {cwd = }")
    ix   = adjust_path_dir_name.index( APP_MODULE )
    print( ix )

    src_root   = adjust_path_dir_name[ : ix   ]
    print( f"in try {src_root = }" )

except ValueError as error:
    # Access the first argument (the message)
    error_message = error.args[0]
    print(f"fallback to 1/0")
    1/0

py3_root            = src_root
proj_root           = f"{py3_root}/_projects"
ex_root             = f"{py3_root}/_examples"


# print( f"{__file__}")

adjust_path_path    = Path( adjust_path_file )
app_dir_path        = adjust_path_path.parent
    # often same as ./
    # directory of the app startup like where main.py is

project_dir_path    = app_dir_path.parent      # ..../_projects
    # one level up where russ keeps all projects
    # probably unique to hei
#rint( f"{hostname              = }")
print( f"{app_dir_path          = }")
print( f"{project_dir_path      = }")



adjust_path_file      = __file__

# # least important at top

sys.path.insert( 1, f"{src_root}/rshlib/in_spect" )
sys.path.insert( 1, f"{src_root}/rshlib/utils" )
sys.path.insert( 1, f"{src_root}/rshlib/rshlib_qt" )
sys.path.insert( 1, f"{src_root}/rshlib" )
sys.path.insert( 1, f"{src_root}/rshlib/app_services" )
sys.path.insert( 1, f"{src_root}/rshlib/rshlib/utils" )

#sys.path.insert( 1, f"{src_root}/_examples" )
# sys.path.insert( 1, f"{src_root}/backup_qt" )


sys.path.insert( 1, f"{src_root}/stuffdb/libs" )

sys.path.insert( 1, f"{src_root}/stuffdb" )
sys.path.insert( 1, "./HTML" )

sys.path.insert( 1, f"{src_root}/stuffdb/py_helpers" )
sys.path.insert( 1, f"{src_root}/stuffdb/data_dict_src" )
sys.path.insert( 1, f"{src_root}/stuffdb/sql" )
sys.path.insert( 1, f"{src_root}/stuffdb/geo_photo" )
sys.path.insert( 1, f"{src_root}/stuffdb/sql" )
sys.path.insert( 1, f"{src_root}/rsh" )


#/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/backup_qt

if VERBOSE >= 10:
    print( "your path has been adjusted"
           "\n    ......" )

if VERBOSE >= 20:
    print( "    path now:" )
    for i_path in sys.path:
        print( "        ", i_path )




