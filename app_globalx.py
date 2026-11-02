# -*- coding: utf-8 -*-

"""
Purpose:
    part of my ( rsh ) library of reusable code
    a library module for multiple applications
	allows any module access to a set of application global values and functions
	typical use:
	from app_global import AppGlobal

    watch out this often uses injected values
    	self.parameters    = AppGlobal.parameters

        app_db    AppDB



"""

import sys
import webbrowser
from   subprocess import Popen
from   pathlib    import Path
import os
import psutil
#from   tkinter    import messagebox
import logging

sys.path.insert(1,  "/mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib" )

import app_global_abc

# ----------------------------------------------
def addLoggingLevel( levelName, levelNum, methodName = None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

     How to add a custom loglevel to Python's logging facility - Stack Overflow
     *>url  https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobbering of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """

    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        #raise AttributeError('{} already defined in logging module'.format(levelName))
        return   # assume already set up ok -- could cause error in contaminated environment

    if hasattr(logging, methodName):
        raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, *args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot )

# # ------------------------
# class NoLoggerLogger( ):
#     """
#     a temporary logger before we have a proper logger
#     implement some of the methods of the logger
#     just some of the protocol not all of this
#     log(level, msg, *args, **kwargs)¶
#     perhaps import module and use its constants which seem not to be
#     CRITICAL 50 ERROR  40   WARNING 30  INFO  20  DEBUG 10 NOTSET 0

#     """
#     __log_later             = []         # tuples for logging after logger is set
#     # ----------------------------------------------
#     @classmethod
#     def info( cls, msg ):
#         """
#         mirror logger.info in limited way
#         """
#         cls.log( logging.INFO, msg )

#     # ----------------------------------------------
#     @classmethod
#     def debug( cls, msg ):
#         """
#         mirror logger.debug in limited way
#         """
#         cls.log( logging.DEBUG, msg )

#     # ----------------------------------------------
#     @classmethod
#     def log( cls, level, msg, *args, **kwargs ):
#         """
#         mirror logger.log in limited way
#         """
#         arg_set  = ( level, msg, )  # not clear how to get rest, for now discard
#         #rint( f"{arg_set[0]} >> {arg_set[1]}" )
#         cls.__log_later.append( arg_set )

#     # ----------------------------------------------
#     @classmethod
#     def log_saved_for_later( cls, logger ):
#         """
#         now have a logger so spit out the saved up stuff if any
#         may or may not print
#         ?? add some indent
#         """
#         for arg_set in cls.__log_later :
#             print( f"log_saved_for_later {arg_set[ 0 ]} {arg_set[ 1 ]}" )
#             logger.log( arg_set[ 0 ], arg_set[ 1 ] )


# # ========================== Begin Class ================================
# class UserCancel( Exception ):
#     """
#     if part way though an operation user wishes to cancel
#     think not used, if is used put in rhslib !!
#     """
#     def __init__(self, arg):
#         # Set some exception information
#         self.msg = arg


NoLoggerLogger  = app_global_abc.NoLoggerLogger
UserCancel      = app_global_abc.UserCancel

OSCall          = app_global_abc.OSCall
# # ------------------------
# class OSCall( app_global_abc.OSCallABC ):
#     """
#     try to call os based on attempts with different utilities
#     in different operating systems
#     """
#     #------------------------
#     def __init__(self, command_list, ):
#         """
#         command list is the list of utilities to try, a list of strings
#         command_aux: like command list but may be a list, a single string, or none, see code

#         """
#         super().__init__( command_list )
#         # self.command_list = []
#         # self.add_command( command_list )

# ------------------------------------------
class AppGlobal( app_global_abc.AppGlobalABC ):
    """
    use at class level ( do not _init_ ) for application globals, similar to but different from parameters
    some global functions
    """
    force_log_level         = 99        # value to force logging, high but not for errors

    # ----------- other important objects typically registered by their inits -- define as none to help document

    controller              = None      # populated by the controller
    parameters              = None      # populated by parameters
    gui                     = None      # populated by the gui
    gui_toolbox             = None      # populated by the controller
    logger                  = None      # populated by the controller
    logger                  = NoLoggerLogger  # can use for now with limited calls, then dumps later ...
    fll                     = force_log_level      #  AppGlobal.fll

    helper                  = None      # populated externally by...
    #helper_thread_id        = None      # set by run in helper thread
    main_thread_id          = None
    logger_id               = None      # populated by the controller
    scheduled_event_list    = None      # populated externally by... -- think dead

    parameter_dicts         = {}        # set up in parameters ????? -- see and example std setup some where

    db_file_name            = None      # initially fetched from controller, later gui may update  this is a bad idea -- drop
    lock_db_file_name       = False     # just an idea, needs functions like check_lock_db_file_name  located where !!
    file_reader             = None
#    live_graph_opt          = 1         # 1 = all in helper                this is just an experiment

    text_editors            =  [ r"D:\apps\Notepad++\notepad++.exe", r"C:\apps\Notepad++\notepad++.exe", "notepad++.exe",
                                 r"gedit", r"xed", r"leafpad", r"mousepad", ]

    file_text_editor        = OSCall( text_editors,  )

    # too soon to call a parameters not defined need to do later
    #file_text_editor.add_command( parameters.ex_editor )

    # add_prog                = AppGlobal.parameters.ex_editor
    # if add_prog is not None:
    #     text_editors        = text_editors + text_editors

    # file_explorers  not in parameters as yet
    file_explorers          = [ r"explorer", "nemo", "xfe", "pcmanfm", ]
    file_explorer           = OSCall( file_explorers ) # !! need linux add and parameters

    # cls not yet defined
    # this gives the name notice to force_log_level... perhaps a better name might be used
    addLoggingLevel( "Notice", force_log_level, methodName=None)

    # self registering when created, not great
    app_file                = None
    app_db                  = None
    app_dir                 = None
    no_video_url            = 4  # AppGlobal.no_video_url

    # ----------------------------------------------
    def __init__(self,  controller  ):

        y  = 1/0    # this guy should not be created and this stops it
        pass



# ======================== eof ======================

