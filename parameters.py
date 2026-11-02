# -*- coding: utf-8 -*-
# parameters for image_edit.py

# # put this at top of each app file:
# ------------------------------------------
if __name__ == "__main__":
    import main
    main.main()

# ---- imports

import logging
import os
#import serial
import sys
import time

# local imports
from app_global import AppGlobal


class Parameters( ):
    """
    sets parameter values, globally available thru AppGlobal
    need to look into getter setter value idea
    """

    # -------
    def choose_mode( self ):
        """
        just choose one of the modes below
        this will override some values in default mode
        """
        # ---- ---------- choose ---------
        #self.mode_example()
        self.mode_the_prof()

        # more modes, not currently in existence
        #self.mode_test_1()
        #self.test_photo_db_1()

        # self.mode_test_for_dev_1()
        #self.mode_raw_decade_scan(  )
        pass
        print( self )

    # --------
    def mode_the_prof( self ):
        """
        """
        self.mode               = "mode_the_prof"

        self.xPosition          = 10
        self.yPosition          = 10

        # implementation here is unclear
        self.xSize              = 100
        self.ySize              = 50

        self.photoMaxSizeAdj    = 650.0  # larger no is smaller image

    # -------
    def __init__(self,    ):

        AppGlobal.parameters    = self
        self.controller         = AppGlobal.controller    # save a link to the controller
        self.mode_default()
        self.os_tweaks( )
        self.computer_name_tweaks()

        self.choose_mode()

        self.mode_cull()

    #            self.logger.info(  "current directory " +  os.getcwd() )
    #            self.logger.info(  "COMPUTERNAME "      +
    #                            str( os.getenv( "COMPUTERNAME" ) ) )
                  # may not exist in Linux
    #
    #            start_ts     = time.time()
    #            dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
    #            string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
    #            self.logger.info( "Time now: " + string_rep )
        # automatic, environment

    # -------
    def os_tweaks( self ):
        """
        tweak the default settings of "default_ _mode"
        for particular operating systems
        you may need to mess with this based on your os setup
        """
        if  self.os_win:
            pass
            #self.icon               = r"./clipboard_b.ico"    #  greenhouse this has issues on rasPi
            #self.icon              = None                    #  default gui icon

        else:
            pass

    # -------
    def computer_name_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_mode"
        for particular computers.  Put in settings for you computer if you wish
        these are for my computers, add what you want ( or nothing ) for your computes
        """
        #rint(self.computername, flush=True)

        if self.computername == "smithersxx":
            self.win_geometry       = '1250x1000+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

        elif self.computername == "millhousexx":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"    # russ win 10 millhouse
            self.win_geometry       = '1000x700+250+5'
                # width x height position
                # self.pylogging_fn       = "millhouse_clipboard.py_log"

        elif self.computername == "THEPROF":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
                # russ win 10 millhouse
            self.win_geometry       = '1000x700+250+5'
                # width x height position
#
            self.xPosition          = 10
            self.yPosition          = 10

            # not clear working
            self.xSize              = 50
            self.ySize              = 120

            self.viewers            = 4

            #  implemented   bigger number makes smaller
            self.photoMaxSizeAdj    = 600.0

    # --------
    def mode_cull( self ):
        """
        """
        self.mode  = "mode_cull"

        # name buttons and sub directories
        self.subOne            = r"subDup"
        self.subTwo            = r"subDel"
        self.subBack           = r"subBUp"

        self.butZeroLabel      = r"OK"
        self.butOneLabel       = r"Dup"
        self.butTwoLabel       = r"Del"

    # --------
    def mode_default( self ):
        """
        sets the default mode, should always be called, can
        override settings later
        should populate all required attributes
        app should run
        """
        self.mode  = "mode_default"

        self.computername       = str( os.getenv( "COMPUTERNAME" ) )
        self.start_ts           = time.time()

        # next !! should be replaced by running on

        our_os          = sys.platform

        if our_os == "win32":
            self.os_win = True
        else:
            self.os_win = False

        self.platform           = our_os

        # ---- appearance
        self.viewers            = 4
            # number of photo viewers in the gui -- does work with 1

        self.xPosition          = 10
        self.yPosition          = 10

        # implementation here is unclear
        self.xSize              = 50
        self.ySize              = 50

        # may not be implemented

        self.photoMaxSizeAdj   = 450.0
            # adjustment against the screen size
            # 4, 450 millhouse was good on 4 * 550 on smithers
        self.photoMaxSizeAdj   = 450.0
            # adjustment against the screen size
            # 4, 450 millhouse was good on 4 * 550 on smithers

        #self.photoMaxSizeAdj   = self.viewers * 130  #

        # ---- logging
        self.logger_id         = "image_edit"
        self.logging_level     = logging.DEBUG
        self.pylogging_fn      = "image_edit.py_log"

        # ---- behavior
        self.read_exif_flag    = True      # read and log exif data from the image files

        # ---- first dir
        self.first_open_dir    = r"/mnt/8ball1/first6_root/photos/photos_raw/03"
            # starting directory for the first open-directory dialog of the session
            # "" = stock dialog behavior from the start

        # name buttons and sub directories
        self.subOne            = r"subDup"
        self.subTwo            = r"subDel"
        self.subBack           = r"subBUp"

        self.butZeroLabel      = r"OK"
        self.butOneLabel       = r"Dup"
        self.butTwoLabel       = r"Del"

    # -----------------------------------
    def __str__( self,   ):
        """
        this is informal, just for debugging
        sometimes it is hard to see where values have come out this may help if printed.
        not complete, add as needed -- compare across applications
        this copied from smart_terminal, commented out items might be good to use here or not
        """
        line_begin  ="\n"
        a_str = ""
        a_str = f"{a_str}\n>>>>>>>>>>* Parameters (some) *<<<<<<<<<<<<"
        a_str = f"{a_str}{line_begin}   mode                         {self.mode}"

        # ------------------------------+----------------------------+--------------------

      #  a_str = f"{a_str}{line_begin}   ex_editor                    {self.ex_editor}"
        a_str = f"{a_str}{line_begin}   logger_id                    {self.logger_id}"
        a_str = f"{a_str}{line_begin}   logging_level                {self.logging_level}"
        # ------------------------------+----------------------------+--------------------
        a_str = f"{a_str}{line_begin}   --- appearance ---"

        a_str = f"{a_str}{line_begin}   xPosition                    {self.xPosition}"
        a_str = f"{a_str}{line_begin}   yPosition                    {self.yPosition}"
        a_str = f"{a_str}{line_begin}   photoMaxSizeAdj              {self.photoMaxSizeAdj}"
        a_str = f"{a_str}{line_begin}   viewers                      {self.viewers}"


        a_str = f"{a_str}{line_begin}   --- file name related  ---"

        # ------------------------------+----------------------------+--------------------

        a_str = f"{a_str}\n   and so much more.... \n\n"
        return a_str

# ---- eof ==============================
