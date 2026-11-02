# -*- coding: utf-8 -*-

"""
Overview:
    This program is designed to help the user quickly sort images into 3 classes,
    typically keep, keep as duplicated, and delete.
    Since incorrect rotation is so often a issue you can also rotate either left
    right or upside down.
    Details:

    *>text     D:/Russ/0000/python00/python3/_projects/image_edit/Ver6/readme_rsh.txt

"""

# # put this at top of each app file:
# ------------------------------------------
if __name__ == "__main__":
    import main
    main.main()

# # ------------------------------------------
# ---- imports

import datetime
import glob
import logging
import os
import os.path
import shutil
import subprocess
import sys
import time
from pprint import pprint

from app_global import AppGlobal
from PIL import Image, PngImagePlugin
#from wx.lib.pubsub import setuparg1    # needed to make next work ???
# from wx.lib.pubsub import pub as Publisher
from pubsub import pub
from qtpy import QtCore, QtGui, QtWidgets

# --------  local imports
import file_info
import gui
import parameters

# https://stackoverflow.com/questions/5374451/importerror-cannot-import-name-publisher
# from wx.lib.pubsub import Publisher
# and replace any occurrence of "Publisher()." by "Publisher."

RESIZE_TOPIC   = "resize"   # and makes more searchable  image_files.

JPEG_EXTS      = ( ".jpg", ".jpeg" )

# checked against "exiftran -h", exiftran 2012 vintage, mint 22.2
EXIFTRAN_FLAGS = { "rr"  : "-9",     # rotate right, 90 clockwise
                   "rl"  : "-2",     # rotate left,  270 clockwise
                   }                 # anything else: "-1", 180

PIL_ROTATIONS  = { "rr"  : Image.ROTATE_270,   # pil rotates counter clockwise
                   "rl"  : Image.ROTATE_90,
                   }                           # anything else: ROTATE_180

class App:

    def __init__(self,  ):

        self.myName             = "App for image_edit"

        self.titlePrefix        = "Image Triage, "    # Triage
        self.version            = "Ver11 2025 07 13.0"
        self.titlePrefix        = f"{self.titlePrefix} {self.version}: "

        AppGlobal.controller    = self
        self.parameters         = parameters.Parameters( ) # open early may effect other

        self.logger_id          = self.parameters.logger_id
        self.logger             = self.__config_logger( )

        self.imageIx            = 0
        self.maxImageIx         = 0   # for the array of fileInfos

        self.fileInfoEof        = file_info.FileInfo( "eof.jpg"  )
        self.fileInfoEof.ixfilelist  = -1    # -1 indicated not in sorted directory list
        self.fileInfoEof.ixSort      = -1

        self.blown_up       = False

        self.fileInfos      = None     # list of all files, in sort order

        self.folderPath     = None     # directory for images  ?? may not be needed at object level
        self.picPaths       = None     # list images or pictures  ?
            # ?? may not be needed at object level
        self.dirOne         = None     # directory for next best
        self.dirTwo         = None     # directory for "delete"

        self.dirBack        = None     # directory for backup when editing
        self.ixMaxImage     = None     # index of the right most picture

        self.prog_info()

        #Publisher.subscribe( self.updateImages, ( "update images" ) )   #subscribe for event
        pub.subscribe( self.updateImages, ( "update images" ) )  # api update

        self.gui            = gui.GUI(  )

        self.wx_app         = AppGlobal.wx_app

        #self.gui.SetTitle( self.titlePrefix + "no directory selected" )

        self.allEof( )

        self.wx_app.exec_()

    # ----------------------------------------------------------------------
    def allEof( self, ):
        """
        initial all Eof.jpg in the viewer

        """
        # 2024 update deprecated class. Use Cursor instead.
        #self.waitCursor     = wx.StockCursor( wx.CURSOR_WAIT )
        self.normCursor     = self.gui.cursor()
        self.waitCursor     = QtGui.QCursor( QtCore.Qt.WaitCursor )
        self.gui.setCursor( self.waitCursor   )
        for ixViewer in ( list(range( self.gui.viewer_ix_max)) ):
            self.gui.viewers[ixViewer].setFileInfo( self.fileInfoEof )
        self.gui.setCursor( self.normCursor   )

    # ----------------------------------------------------------------------
    def showIntImage( self, ):
        """
        initial display left to right after a directory is chosen
        still in use - yes
        """
        #rint "showIntImage"
        for ixViewer in ( list(range( self.gui.viewer_ix_max)) ):
            #rint("showIntImage", ixViewer)
            ixImage = ixViewer

            if  ixImage < len( self.fileInfos ):
                fileInfo            = self.fileInfos[ ixImage ]
                self.ixMaxImage     = ixImage

            else:
                fileInfo            = self.fileInfoEof
                self.ixMaxImage     = -1

            fileInfo.ixfilelist     = ixImage   # what does this do, does this var exist??
            self.gui.viewers[ixViewer].setFileInfo( fileInfo )

    # ----------------------------------------------------------------------
    def makeDir( self, a_dir ):
        #result_dir   = r"d:\temp\delete_me"
        if not os.path.exists( a_dir ):
            #rint "make it"
            os.makedirs( a_dir )
        #else:
            #rint "dir exists"

    #----------------------------------------------------------------------
    def updateImages( self, msg ):
        """
        Updates the picPaths list to contain the current folder's images as list
        will build the master list and sort
        this is a subscriber -- may drop and call from gui
        from gui.onOpenDirectory
        """
        # qtpy has no modal exec()/ID_OK dance, getExistingDirectory returns "" on cancel
        if self.folderPath is None:
            default_dir     = self.parameters.first_open_dir   # first open of the session
        else:
            default_dir     = ""                               # "" = default dialog behaviour

        folder_path     = QtWidgets.QFileDialog.getExistingDirectory( self.gui, "Choose a directory for pictures", default_dir )

        if folder_path:
            self.folderPath = folder_path
            msg  = "user opened folderPath " + self.folderPath
            self.logger.info( msg )
            # can we extend to more file types, need to i think
            # caps and / vs \ in Linux
            # this is a mess to get all types, caps, perhaps I should just iterate myself
            file_list       = []

            a_glob          = glob.glob( self.folderPath + "/*.jpg")
            file_list.extend( a_glob )

            a_glob          = glob.glob( self.folderPath + "/*.JPG")
            file_list.extend( a_glob )

            a_glob          = glob.glob( self.folderPath + "/*.png")
            file_list.extend( a_glob )

            a_glob          = glob.glob( self.folderPath + "/*.PNG")
            file_list.extend( a_glob )

            file_list       = list( set( file_list) ) # de dup

            self.picPaths   = file_list

            print(  f"selected files,  self.picPaths {self.picPaths}"   )
                  # this is a mess of all files matching above line in dir user chooses.
        else:
            return
        # next may be wrong if user did not pick a directory

        self.gui.setCursor( self.waitCursor   )   # self.waitCursor

        self.gui.setWindowTitle( self.titlePrefix + self.folderPath )

        self.fileInfos = []
        for item in self.picPaths:
            self.fileInfos.append( file_info.FileInfo( item ) )
                # build the list we are going to use
            #rint item
            #rint self.fileInfos[ -1 ]
        # sort by some criteria, now say size just as a test
        self.fileInfos.sort( key = self.getKey  )
        pprint( self.fileInfos )

        #lf.maxImageIx     = 0
        # put in sort order do not have to maintain until new directory
        for ix, ifileInfo in enumerate( self.fileInfos ):
            ifileInfo.ixSort = ix

        self.dirOne      = os.path.join( self.folderPath, self.parameters.subOne, ""  )
        self.makeDir( self.dirOne )

        self.dirTwo      = os.path.join( self.folderPath, self.parameters.subTwo, ""  )
        self.makeDir( self.dirTwo )

        self.dirBack     = os.path.join( self.folderPath, self.parameters.subBack, "" )
        self.makeDir( self.dirBack )

        self.showIntImage()

        self.gui.setSizePosition()
        self.gui.setCursor( self.normCursor   )

    #----------------------------------------------------------------------
    def getKey( self, item ):
        """
        key for sort, this is kind of basic
        item returned will be the sort key
        """
        #return item.size
        return  item.fullname

    #----------------------------------------------------------------------
    def findNextImage( self, prior ):
        """
        prior is ix of the prior fileInfos
        return ix of next valid fileInfos or -1 if no valid ix
        this is overdone because I currently do not back up just go forward
        """
        ix         = -1
        ixImage    = prior
        done       = False   # break might do as well
        if ixImage == -1:     # already past end -- may need a before end flag as well
            return ixImage

        while done == False:
            ixImage  += 1
            # may have a variable that keeps the length ??
            if ixImage >= len( self.fileInfos ):
                done   = True
                ix     = -1
            elif not self.fileInfos[ixImage].processed:
                done   = True
                ix     = ixImage
        return ix

    # #----------------------------------------------------------------------
    # def showNextImage( self, ignore ):
    #     print("!! showNextImage is dead??")

    #     #ixImage = self.imageIx   # try next ( could get a few from next controls )

    #     for ix_viewer in reversed( list(range( self.gui.viewer_ix_max)) ):

    #         ixImage  = self.findNextImage( self.gui.viewers[ix_viewer].file_info.ixfilelist )
    #         if ixImage != -1:
    #             file_info             = self.fileInfos[ ixImage ]
    #             # file_info.ixfilelist  = ixImage
    #             self.gui.viewers[ix_viewer].setFileInfo( file_info )
    #         else:
    #             self.gui.viewers[ix_viewer].setFileInfo( self.fileInfoEof )

    #         return

    #----------------------------------------------------------------------
    def getViewerIx( self, viewer ):
        """
        determine the index of the viewer
        may need update for moving viewers
        """
        for ixViewer in ( list(range( self.gui.viewer_ix_max)) ):

            if self.gui.viewers[ ixViewer ]  ==  viewer:
                #rint " viewer is", ixViewer
                break

        return ixViewer

    #----------------------------------------------------------------------
    def rotate( self, viewer, action ):
        """
        rotate the image, replace file
        make a backup unless already made
        **manage dates  ?? test looks like done

        jpeg goes through exiftran, lossless, no decode and no re-encode,
        all the metadata is carried over.  png is already a lossless format
        so pillow is fine for the pixels, but pillow drops every ancillary
        chunk on save so we hand them back ourselves.
        """
        # should have any sizing position stuff as aspect may change??
        #print "rotate"

        #ixViewer  = self.getViewerIx( viewer )   # we have the viewer do we need the ix
        #viewer    = self.gui.viewers[ ixViewer ]  # do not need
        fileInfo  = viewer.fileInfo

        if fileInfo.ixSort == -1:   # no rotation for eof
            return

        fn        = fileInfo.fullname
        a_ext     = os.path.splitext( fn )[1].lower()
        a_is_jpeg = a_ext in JPEG_EXTS
        exiftran  = shutil.which( "exiftran" )

        # refuse rather than fall back to a lossy pillow save, better to do
        # nothing than to quietly re-encode the original and lose the exif
        if a_is_jpeg and ( exiftran is None ):
            msg   = ( "exiftran is not installed, so this jpeg cannot be "
                      "rotated without re-encoding it and losing both image "
                      "quality and the exif data.\n\n"
                      "install it with:    sudo apt install exiftran\n\n"
                      "the file has not been changed." )
            self.complain( "Cannot rotate jpeg", msg )
            return

        self.gui.setCursor( self.waitCursor   )

        #.wxBeginBusyCursor( cursor   )   #Cursor *cursor = wxHOURGLASS_CURSOR)

        fbn       = os.path.basename( fn )
        dest      = os.path.join( self.dirBack, fbn )
        print(time.time(), fileInfo.modify_date)

        # copy2 not move, exiftran rotates in place so the file has to stay
        # put, and copy2 carries the modify date onto the backup for us
        if not os.path.isfile( dest ):
            shutil.copy2( fn, dest )

        if a_is_jpeg:
            a_ok  = self.rotate_jpeg( fn, action, exiftran )
        else:
            a_ok  = self.rotate_pillow( fn, action )

        if not a_ok:
            self.gui.setCursor( self.normCursor   )
            return

        viewer.setFileInfo( fileInfo  )  # resetting same one to reload

        os.utime( fn, ( time.time(), fileInfo.modify_date ))   # (accesstime, modifiedtime).

        self.gui.setCursor( self.normCursor   )

    #----------------------------------------------------------------------
    def rotate_jpeg( self, fn, action, exiftran ):
        """
        lossless rotate in place, exiftran shuffles the dct blocks and copies
        every marker, it also fixes up the exif orientation tag and the
        embedded thumbnail which a hand rolled copy would get wrong
        ret: True if the file was rotated
        """
        a_flag    = EXIFTRAN_FLAGS.get( action, "-1" )
        a_cmd     = [ exiftran, a_flag, "-i", fn ]

        a_result  = subprocess.run( a_cmd, capture_output = True, text = True )

        if a_result.returncode != 0:
            msg   = ( f"exiftran could not rotate\n\n{fn}\n\n"
                      f"{a_result.stderr.strip()}\n\n"
                      f"the original is in {self.parameters.subBack}" )
            self.complain( "Rotate failed", msg )
            return False

        return True

    #----------------------------------------------------------------------
    def rotate_pillow( self, fn, action ):
        """
        png ( and anything else non jpeg ), the pixels survive a round trip
        untouched, the metadata does not unless we put it back by hand
        ret: True if the file was rotated
        """
        a_rotation  = PIL_ROTATIONS.get( action, Image.ROTATE_180 )

        try:
            im          = Image.open( fn )
            im.load()                       # so we are not holding the file open

            a_info      = dict( im.info )
            a_text      = dict( getattr( im, "text", {} ) )
                          # transpose does not carry text chunks, unlike jpeg
                          # exif, so they have to come off the original
            a_rotated   = im.transpose( a_rotation )
            im.close()

            a_pnginfo   = PngImagePlugin.PngInfo()
            for i_key, i_value in a_text.items():
                a_pnginfo.add_text( i_key, i_value )

            a_kwargs    = { "pnginfo" : a_pnginfo }
            for i_key in ( "exif", "icc_profile", "dpi", "transparency" ):
                if i_key in a_info:
                    a_kwargs[ i_key ] = a_info[ i_key ]

            a_rotated.save( fn, **a_kwargs )

        except OSError as a_exception:
            msg   = ( f"could not rotate\n\n{fn}\n\n{a_exception}\n\n"
                      f"the original is in {self.parameters.subBack}" )
            self.complain( "Rotate failed", msg )
            return False

        return True

    #----------------------------------------------------------------------
    def complain( self, a_title, a_msg ):
        """
        loud failure, we would rather stop and say so than silently do
        something lossy to the user's originals
        """
        self.logger.error( f"{a_title}: {a_msg}" )
        QtWidgets.QMessageBox.critical( self.gui, a_title, a_msg )

   #----------------------------------------------------------------------
    #def tst( self, viewer, event ):
    def tst( self, from_menu_bar ):
        """
        place for test routine

        """
        print(" tst ... ")
        print( from_menu_bar )

    #----------------------------------------------------------------------
    def classify( self, viewer, action ):
        """
        the user has "classified a picture" which is
        then processed, and we go on to the next image
        now new classify
        and move to next pic

        """
        #rint " classify"
        fileInfo = viewer.fileInfo

        if fileInfo.ixSort == -1:   # no processing for eof
            return

        self.gui.setCursor( self.waitCursor   )

        # use this guy to process the file related to this viewer
        src   = fileInfo.fullname
        # need to extract name from full name then build dest
        dest   = os.path.basename( src )

        #action determines if needs to be copied and if so where
        if   action == 0:
            #fileInfo.processed   = True
            destDir              = self.folderPath

        elif action == 1:
            destDir              = self.dirOne

        else:
            destDir              = self.dirTwo

        dest   = os.path.join( destDir, dest )
        fileInfo.processed   = True
        fileInfo.newname     = dest

        if action != 0:
            shutil.move( src, dest )

        # ========= move deleted to the end and reload

        #print "deleteAdd"
        self.gui.sizer.removeWidget( viewer )
        #ret = self.sizer.Remove( self.viewers[2] )
        #Add( self.viewers[2], 1, wx.EXPAND )
        self.gui.sizer.addWidget( viewer, 1 )

        #self.Show()
        # some of this might go over to the gui
        self.gui.sizer.update( )
        self.gui.adjustSize( )
        #self.gui.Center()
        #self.gui.Show()

        ix_next  = self.findNextImage( self.ixMaxImage )
        self.ixMaxImage  = ix_next
        if ix_next >= 0:
            viewer.setFileInfo( self.fileInfos[ ix_next ] )
        else:
            viewer.setFileInfo( self.fileInfoEof )

        self.gui.setCursor( self.normCursor   )

        self.gui.setSizePosition()   # Sept 2017 changed to correct call

    #----------------------------------------------------------------------
    def zeroTwoxxxxx( self, viewer, action ):
        """
        replaced By classify this loads all the picks to add one new at end
        sort the file into correct directory
        delete from viewer and bring in the next, supersedes show next
        image? no
        viewer the Viewer whose button was pressed
        action 0....2

        """
        # need to find the viewer ?
        #rint("zeroTwo")
        ixViewer  = self.getViewerIx( viewer )   # DO WE    need this?

        # need to work on dates still need to check
        fileInfo = self.gui.viewers[ ixViewer ].fileInfo   # could directly get from viewer

        if fileInfo.ixSort == -1:   # no processing for eof
            return

        # use this guy to process the file related to this viewer
        src   = fileInfo.fullname

        dest   = os.path.basename( src )

        #action determines if it needs to be copied and if so where
        if   action == 0:
            destDir              = self.folderPath

        elif action == 1:
            destDir              = self.dirOne

        else:
            destDir              = self.dirTwo

        dest                 = os.path.join( destDir, dest )
        fileInfo.processed   = True
        fileInfo.newname     = dest

        if action != 0:
            shutil.move( src, dest )

        # now manage the gui to bring up the next image -- could be done in the gui??
        ixLowViewer = ixViewer
        for ixViewer in ( list(range( ixLowViewer, self.gui.viewer_ix_max)) ):

            ix_next  = self.findNextImage( self.gui.viewers[ixViewer].fileInfo.ixSort )
            self.ixMaxImage = ix_next
            if ix_next >= 0:
                self.gui.viewers[ixViewer].setFileInfo( self.fileInfos[ ix_next ] )
            else:
                self.gui.viewers[ixViewer].setFileInfo( self.fileInfoEof )

    #----------------------------------------------------------------------
    def prog_info( self ):
        """
        log info about program and its argument/environment
        nice to have system time and date
        """
        self.logit( "" )
        self.logit( "============================" )
        self.logit( "" )

        self.logit( "Running image_edit version = " + self.version  )
        self.logit( "" )
        #  data_dir=russ_data  graph_type=graph_tot
        if len( sys.argv ) == 0:
            self.logit( "no command line arg " )
        else:
            ix_arg = 0
            for aArg in  sys.argv:

                self.logit( "command line arg " + str( ix_arg ) + " = " + sys.argv[ix_arg])
                ix_arg += 1

        self.logger.info(  "current directory " +  os.getcwd() )
        self.logger.info(  "COMPUTERNAME "      +  str( os.getenv( "COMPUTERNAME" ) ) )
            # may not exist in Linux

        start_ts     = time.time()
        dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
        string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info( "Time now: " + string_rep )

    # --------------------------------------------------------
    def __config_logger( self, ):
        """
        configure the logger in usual way using the current parameters

        args: zip
        ret:  the logger
        """
        logger = logging.getLogger( self.logger_id  )

        logger.handlers = []
        logger.setLevel( self.parameters.logging_level )
            # DEBUG , INFO	WARNING	ERROR	CRITICAL

        fh        = logging.FileHandler(   self.parameters.pylogging_fn )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info( "Done __config_logger__" ) #  .debug   .info    .warn    .error

        return logger

    # ----------------------------------------------------------------------
    def logit( self, adata ):
        """
        for compatibility with old code
        # self.logit( str( self.task_tick )  )   # self.logit( "msg"  )
        """
        self.log( adata, "logit" )

    # ----------------------------------------------------------------------
    def log( self, adata, ato ):
        """
        just a call to logger
        is this needed/used, can component
        call directly?

        """
        self.logger.info( "log() " + adata ) #  .debug   .info    .warn    .error

        return

