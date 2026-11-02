# -*- coding: utf-8 -*-

# # put this at top of each app file:
# ------------------------------------------
if __name__ == "__main__":
    import main
    main.main()

# ---- imports

#import  sys
#import  glob
import os
import sys
from functools import partial

import exifread  # a pip install
from   qtpy import QtWidgets, QtCore, QtGui
from   app_global import AppGlobal
# from wx.lib.pubsub import setuparg1
# from wx.lib.pubsub import pub as Publisher
from   pubsub import pub
import photo_triag

import file_info  # useful file information on files to view
# import photo_triag  # the controller

# https://stackoverflow.com/questions/5374451/importerror-cannot-import-name-publisher

# this is for publish and subscribe pattern, with an update
# from wx.lib.pubsub import Publisher

# and replace any occurrence of "Publisher()." by "Publisher."

# from wx.lib.pubsub import Publisher as pub


class GUI( QtWidgets.QMainWindow ):

    def __init__( self,  ):
        """
        Constructor
        """
        self.controller     = AppGlobal.controller
        self.parameters     = AppGlobal.parameters

        existing_qt_app     = QtWidgets.QApplication.instance()
        self.wx_app         = existing_qt_app if existing_qt_app else QtWidgets.QApplication( sys.argv )
                                # attribute kept named wx_app -- AppGlobal.wx_app is a shared name
                                # used by sibling stuffdb projects, holds the QApplication now

        AppGlobal.wx_app    = self.wx_app
        AppGlobal.gui       = self

        QtWidgets.QMainWindow.__init__( self )    # ?? title?
        self.setWindowTitle( "" )

        self.folderPath     = ""
        #self.fileInfo      = None
        self.position       = ( self.parameters.xPosition   , self.parameters.yPosition )

        # Publisher.subscribe(self.resizeFrame, ("resize"))
        pub.subscribe( self.resizeFrame, "resize" )  # for new pubsub

        self.viewer_ix_max      = self.parameters.viewers   # ?? move to parameters
        self.viewers            = []

        self._build_gui( )


        #self.s

    #----------------------------------------------------------------------
    def _build_gui( self ):
        """
        _build_gui
        build add n image viewers
        seems fine
        separate function for tool bar
        """
        self.central_widget = QtWidgets.QWidget( self )
        self.setCentralWidget( self.central_widget )
        self.sizer           = QtWidgets.QHBoxLayout( self.central_widget )

        for ix in range( self.viewer_ix_max ):
            print( f"ix for viewers = {ix}")
            self.viewers.append( ViewerPanel( self ) )
            self.sizer.addWidget( self.viewers[ix], 1 )

        self._build_toolbar()
        self._build_menu()

        self.show()
        self.adjustSize()
        self._center()

    #----------------------------------------------------------------------
    def _center( self ):
        """
        center on the primary screen, qtpy has no built in Center() like wx did
        """
        screen_geom  = QtWidgets.QApplication.primaryScreen().availableGeometry()
        frame_geom   = self.frameGeometry()
        frame_geom.moveCenter( screen_geom.center() )
        self.move( frame_geom.topLeft() )

    #----------------------------------------------------------------------
    def _build_toolbar(self):
        """
        build the toolbar
        """
        self.toolbar    = self.addToolBar( "main" )
        self.toolbar.setIconSize( QtCore.QSize(16,16) )

        # where do icons come from open_ic0:
#        wxWidgets: wxArtProvider Class Reference
#        http://docs.wxwidgets.org/3.1/classwx_art_provider.html
        # qtpy note: wx.ArtProvider has no qtpy equivalent, using QStyle standard icons instead

        x_ico           = self.style().standardIcon( QtWidgets.QStyle.SP_MessageBoxInformation )

        # !! looks like some dead code
        # 2024 fix: Use :meth:`AddTool` instead.
        # but got  arguments did not match any overloaded call:
        # wx.ToolBar.AddTool(self, id, label, bitmap,
        # bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp=””,
        # longHelp=””, clientData=None)

        # ----
        open_ico        = self.style().standardIcon( QtWidgets.QStyle.SP_DialogOpenButton )
        self.openTool   = self.toolbar.addAction( open_ico, 'iod' )
        self.openTool.setToolTip( "Open Image Directory" )
        self.openTool.triggered.connect( self.onOpenDirectory )

        # # xxxTool         = self.toolbar.AddTool( wx.ID_ANY, x_ico, "xxxx", "xxx" )
        # xxxTool         = self.toolbar.AddTool(
        #                         13,     # id  !!
        #                         label        = 'xxx',
        #                         bitmap       = x_ico,    # wx.Bitmap( an_image ),
        #                         bmpDisabled  = x_ico,    # wx.Bitmap( an_image ),
        #                         kind         = wx.ITEM_RADIO,
        #                         shortHelp    = "XXX tool, what?" )



    #----------------------------------------------------------------------
    def _build_menu(self):
        """
        what it says, read
        """
        # Create the menu bar
        menu_bar   = self.menuBar()
        #menu_bar.Append(menu_1, "tx_menu_1")
        # menu_bar.Append(menu_2, "tx_menu_2")

        menu_1      = menu_bar.addMenu( "Configuration" )

        action      = menu_1.addAction( "Show Parameters" )
        #self.Bind(wx.EVT_MENU, self.menu_function, widget  )
        # self.Bind( wx.EVT_MENU, AppGlobal.os_open_txt_file, "parameters.py" )

        partial_function = partial( self.menu_open_txt_file, file_name = "parameters.py" )
        action.triggered.connect( partial_function )

        #----
        action    = menu_1.addAction( "Edit Readme" )
        partial_function = partial( self.menu_open_txt_file, file_name = "readme_rsh.txt" )
        action.triggered.connect( partial_function )

        #----
        action    = menu_1.addAction( "Edit Log File" )
        partial_function = partial( self.menu_open_txt_file, file_name = self.parameters.pylogging_fn  )
        action.triggered.connect( partial_function )

        # ----
        menu_2      = menu_bar.addMenu( "Help" )

        #----
        action    = menu_2.addAction( "Help Info" )
        partial_function = partial( self.menu_open_txt_file, file_name = "help.txt"  )
        action.triggered.connect( partial_function )

        #----
        action    = menu_2.addAction( "Technical Information" )
        partial_function = partial( self.menu_open_txt_file, file_name = "technical.txt"  )
        action.triggered.connect( partial_function )

        # help_function    = partial( AppGlobal.os_open_txt_file, "./help/technical.txt" )
        # a_menu.add_command( label   = "Show Technical Information",

        #----
        action    = menu_2.addAction( "About" )
        partial_function = partial( self.menu_open_txt_file, file_name = "about.txt"  )
        action.triggered.connect( partial_function )

        # a_menu.add_command( label   = "Show Parameters",
        #                     command = self.show_parms )

    #----------------------------------------------------------------------
    def menu_open_txt_file( self, event, file_name ):
        """
        use partial
        partial_function   = self.menu_open_txt_file
        partial_function   = value_from_hundreds = partial(         partial_function   = , units = 2, tens = 1 )
        partial_function = partial( self.menu_open_txt_file, file_name = "parameters.py" )

       Args:
            event (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        #rint( f"menu_open_txt_file event     >{event}<")
        #rint( f"menu_open_txt_file file_name >{file_name}<")
        AppGlobal.os_open_txt_file( file_name )

    #----------------------------------------------------------------------
    def menu_function( self, event ):
        # Function to handle menu events .. from chat gpt
        """
        chat gpt does not seem to work
        """
        print( f"menu_function event {event}")
        action    = self.sender()
        if action is None:
            print("Invalid menu action")
        else:
            print(f"Menu command executed: {action.text()}")


    #----------------------------------------------------------------------
    def setSizePosition(self, ):
        """

        """
        self.move( *self.position )     # flags=SIZE_USE_EXISTING)
        self.show()

    #----------------------------------------------------------------------
    def resizeFrame( self, ):
        """
        associate with gui "resize"
        pub.sendMessage(  "resize", arg1=123  ) #  2024 api update  still ng
        """
        self.adjustSize()


    #----------------------------------------------------------------------
    def onOpenDirectory(self, event):
        """
        Opens a DirDialog to allow the user to open a folder with pictures
        """
        # content moved to controller

        self.controller.updateImages( "junk" )   # delete junk and dead code

     #----------------------------------------------------------------------
    def deletAdd(self,):
        """
        test on rearranging image containing widgets
        """
        #rint("deleteAdd")
        self.sizer.removeWidget( self.viewers[2] )
        #ret = self.sizer.Remove( self.viewers[2] )
        self.sizer.addWidget( self.viewers[2], 1 )


        self.sizer.update()
        self.adjustSize()
        self._center()
        self.show()

    #----------------------------------------------------------------------
    def blow_up( self, viewer, action ):
        """
        think unreachabe and maybe incompatible
        consider moving to gui
        make larger than normal so that
        a smaller number of pictures may be examined.
        may center on the viewer
        """
        print( "blow_up" )
        self.blown_up       = True

    #----------------------------------------------------------------------
    def blow_down( self, ):
        """
        restore size and position after blow up
        """
        print( "blow_down" )

        for i_viewer in self.viewers:
            i_viewer.blow_down()

        self.sizer.update()
        self.adjustSize()      # !! was self.sizer.Fit( self.myGui ) in wx version; self.myGui was undefined

        #self.setSizePosition

        self.controller.blown_up       = False

#----------------------------------------------------------------------
class ViewerPanel( QtWidgets.QFrame ):
    """
    all the viewers one instance for each picture

    """
    #----------------------------------------------------------------------
    def __init__( self, parent ):
        """
        Constructor
        style=wx.RAISED_BORDER)
        """

        QtWidgets.QFrame.__init__(self, parent)
        self.setFrameStyle( QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised )

        screen_geom         = QtWidgets.QApplication.primaryScreen().size()
        width, height       = screen_geom.width(), screen_geom.height()
        self.picPaths       = []          # list of all file, may be obsolete as may be some of this other stuff
        self.currentPicture = 0
        self.totalPictures  = 0

#        self.controller     = self.GetParent( ).myController
#        self.parameters     = self.GetParent( ).myParameters   # better get from controller

        self.controller     = AppGlobal.controller
        self.parameters     = AppGlobal.parameters   # better get from controller


        # ??make parameter
        #  self.photoMaxSize = height - self.parameters.photoMaxSizeAdj  # may want in parameters

        # problems march 2024 may now need ints so make ints

        self.photoMaxSizeDn     = int( height - self.parameters.photoMaxSizeAdj )  # Normal size may want in parameters

        self.photoMaxSizeUp     = int( self.photoMaxSizeDn * 2  ) # during blow up

        self.fileInfo           = None

        #Publisher.subscribe(self.updateImages, ("update images"))

        #self.slideTimer = wx.Timer(None)
        #self.slideTimer.Bind(wx.EVT_TIMER, self.update)

        self.layout()

        #self.Cursor
        #self.SetCursor

    #----------------------------------------------------------------------
    def layout(self):
        """
        Layout the widgets on the panel
        """

        self.mainSizer = QtWidgets.QVBoxLayout()
        #btnSizer = wx.BoxSizer( wx.HORIZONTAL )
        btnSizer = QtWidgets.QGridLayout()
        btnSizer.setSpacing( 1 )

        # ========= IMAGE WAS ABOVE HERE

#==============================================================================
#         btnData = [("Previous",   btnSizer, self.onPrevious),
#                    ("Slide Show", btnSizer, self.onSlideShow),
#                    ("Next",       btnSizer, self.onNext),
#                    ("del",        btnSizer, self.deleteImage) ]
#==============================================================================

        btnData = [ (self.parameters.butZeroLabel,   btnSizer,  self.onZero),
                    (self.parameters.butOneLabel,    btnSizer,  self.onOne ),
                    (self.parameters.butTwoLabel,    btnSizer,  self.onTwo ),
                    ("RR" ,    btnSizer,  self.rr      ),
                    ("RL" ,    btnSizer,  self.rl      ),
                    ("USD" ,   btnSizer,  self.usd      ),
                    # ("Tst" ,   btnSizer,  self.tst      ),  # for testing new functions
                   ]

        for ix, data in enumerate( btnData ):
            label, sizer, handler = data
            self.btnBuilder(label, sizer, handler, ix )

        self.mainSizer.addLayout( btnSizer )
        self.mainSizer.setAlignment( btnSizer, QtCore.Qt.AlignCenter )

        #----------- MOVE IMAGE HERE
        # 2024 update
        #img = wx.EmptyImage(self.photoMaxSizeDn,self.photoMaxSizeDn )
        blank_pixmap = QtGui.QPixmap( self.photoMaxSizeDn, self.photoMaxSizeDn )
        blank_pixmap.fill( QtCore.Qt.transparent )

        # 2024 update
        #self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
        #                                 wx.BitmapFromImage(img))
        self.imageCtrl = QtWidgets.QLabel( self )
        self.imageCtrl.setFixedSize( self.photoMaxSizeDn, self.photoMaxSizeDn )   # freeze size so layout never shifts
        self.imageCtrl.setAlignment( QtCore.Qt.AlignCenter )                      # center smaller/odd-aspect images in the fixed box
        self.imageCtrl.setPixmap( blank_pixmap )


        self.mainSizer.addWidget( self.imageCtrl, 0, QtCore.Qt.AlignCenter )
        self.imageLabel = QtWidgets.QLabel( "", self )
        self.mainSizer.addWidget( self.imageLabel, 0, QtCore.Qt.AlignCenter )

        # ------------------

        self.setLayout( self.mainSizer )

    #----------------------------------------------------------------------
    def btnBuilder(self, label, sizer, handler, ix ):
        """
        Builds a button, binds it to an event handler and adds it to a sizer

        """
        btn = QtWidgets.QPushButton( label, self )
        btn.clicked.connect( handler )

        #sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)   # for box
        row, col = divmod( ix, 3 )
        sizer.addWidget( btn, row, col )   # for grid?

    #----------------------------------------------------------------------
    def loadImage(self, image):
        """
        """
        # for re scaling later may want to keep unscaled image in memory
        # or keep a large size and a small size

        image_name = os.path.basename(image)
        img        = QtGui.QImage( image )
        # scale the image, preserving the aspect ratio
        W = img.width()
        H = img.height()
        # MAR 2024 seem to need ints
        if W > H:
            NewW = int( self.photoMaxSizeDn )
            NewH = int( self.photoMaxSizeDn * H / W )
        else:
            NewH = int( self.photoMaxSizeDn )
            NewW = int( self.photoMaxSizeDn * W / H )
        # see also  http://ubuntuforums.org/showthread.php?t=1188248

        img = img.scaled( NewW, NewH, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation )

        # 2024 update Call to deprecated item BitmapFromImage.
        # Use :class:`wx.Bitmap` instead
        #self.imageCtrl.SetBitmap( wx.BitmapFromImage(img) )
        self.imageCtrl.setPixmap( QtGui.QPixmap.fromImage( img ) )
        self.imageLabel.setText( image_name )
        self.update()

        #Publisher.sendMessage( "resize",  )  # who gets this message, look at gui and controller
        #Publisher.sendMessage( ( "resize", "what" ) )  # who gets this message, look at gui and controller
        #Publisher.sendMessage(  "resize", "what"  )  # who gets this message, look at gui and controller
        #pub.sendMessage(  "resize", arg1=123  ) #  2024 api update  still ng
        #pub.sendMessage(  "resize",   )
        pub.sendMessage( photo_triag.RESIZE_TOPIC )
        # anObj = dict(a=456, b='abc')
        # pub.sendMessage('rootTopic', arg1=123, arg2=anObj)


    #----------------------------------------------------------------------
    def blow_down( self, ):
        """
        restore size and position after blow up
        """
        print( "viewer.blow_down" )

     #----------------------------------------------------------------------
    def blow_up( self, ):
        """
        restore size and position after blow up
        """
        print( "viewer.blow_up" )

    #----------------------------------------------------------------------
    def setFileInfo( self, fileInfo ):

        """
        sets the fileInfo and displays the image
        ?? move loadImage here?
        """
        self.fileInfo    = fileInfo
        self.loadImage( self.fileInfo.fullname )

        # new for extended attributes in test

        if self.parameters.read_exif_flag:
            self.readExif( fileInfo )

    #----------------------------------------------------------------------
    def readExif( self, fileInfo ):
        """
        read other data in the image file
        and print it ( change to log it )
        should not be in gui.
        """
        print( "" )
        print( f"readExif fileInfo.fullname = {fileInfo.fullname}",  )

#        print "gui.py  readExif early return so no file info show"
#        return

        f = open( fileInfo.fullname, 'rb')

        # Return Exif tags
        tags = exifread.process_file( f )
        #Note: To use this library in your project as a Git sub module, you should: from <submodule_folder> import exifread
        #Returned tags will be a dictionary mapping names of Exif tags to their values in the file named by path_name.
        #You can process the tags as you wish. In particular, you can iterate through all the tags with:
        f.close()
        for tag in list(tags.keys()):
            if tag not in ('JPEGThumbnail', 'TIFFThumbnailxx', 'Filenamexx', 'EXIF MakerNotexx'):
                print(( "Key: %s, value %s" % (tag, tags[tag] ) ))


    #----------------------------------------------------------------------
    def updateImagesxxxxx(self, msg):
        """
        Updates the picPaths list to contain the current folder's images
        called by publish/subscribe
        """
        #print "gui.py just got the message"
        self.picPaths = msg.data
        self.totalPictures = len(self.picPaths)
        #self.loadImage(self.picPaths[0])

    #----------------------------------------------------------------------
    def deleteImagexxxx(self, event):
        """
        dead code now, probably forever
        """
        self.controller.deleteImage( self )

    #----------------------------------------------------------------------
    def onZero( self, event ):
        """

        """
        self.controller.classify( self, 0 )

    def onOne( self, event ):
        """

        """
        self.controller.classify( self, 1 )

    def onTwo( self, event ):
        """

        """
        self.controller.classify( self, 2 )

    #----------------------------------------------------------------------
    def rr( self, event ):
        """
        rotate right
        """
        #rint self
        #rint self.fileInfo
        self.controller.rotate( self, "rr" )

    #----------------------------------------------------------------------
    def rl( self, event ):
        """
        rotate left
        """
        self.controller.rotate( self, "rl" )

    #----------------------------------------------------------------------
    def usd( self, event ):
        """
        rotate up side down
        """
        self.controller.rotate( self, "usd" )

    #----------------------------------------------------------------------
    def tst( self, event ):
        """
        rotate up side down
        """
        self.controller.tst( self, event )

# ---- eof ================================

