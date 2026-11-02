#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:25:32 2024

@author: russ
"""

import sys


import adjust_path
# # next change used by russ in development
# #sys.path.insert( 1, "../rshlib" )
# sys.path.insert( 1,  "/media/sf_0000/python00/python3/_projects/rshlib" )
# sys.path.insert( 1,  "/mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib" )
# sys.path.insert( 1,  r"D:\Russ\0000\python00\python3\_projects\rshlib" )

# sys.path.insert( 1, r"D:\Russ\0000\python00\python3\_projects\rshlib"   )

print( "Note: main.py may have changed the system path in a way not needed by your installation" )

def main( ):
    import photo_triag

    aApp = photo_triag.App(  )


# --------------------
if __name__ == "__main__":
    # #----- run the full app
    main( )


# # put this at top of each app file:
# # ------------------------------------------
# if __name__ == "__main__":
#     import main
#     main.main()

# ------------------------------------------
