D:\Russ\0000\python00\python3\_projects\image_edit\readme_rsh.txt
ideas to add
transform    -- add quotes at both ends double single



this readme is for my image_edit app

see the help file  when it is written, if ever

something like help.txt

================  s ================

----- install for 2024
from pubsub import pub    pubsub.pub.sendMessage

(py_10) russ@russ-ThinkPad-P72:~$ pip install pypubsub==3.3



 """
Overview:
    This program is designed to help the user quickly sort images into 3 classes,
    typically keep, keep as duplicated, and delete.
    Since incorrect rotation is so often a issue you can also rotate either left
    right or upside down.
    Details:
        Sort Order:

        File handling:
              to be written
        File dates:
              to be written
        Parameters:
              to be written
    Author:  russ_hensel, see:  http:www.opencircuits.com/User:Russ_hensel
    Download:

Environment:
    Tested in:
        OS:        Linux mint
        IDE:       Spyder 5.4.3
        Language:  Python 3.10
     Should run in any Python 3.10 environment on any OS
     this file image_edit.py

Reminders, notes:
    in Spyder kill interpreter after 1 run
    may not run right if started from other than image_edit due to way Publisher works on first call

Status/history:

-------Version 9
    *! add configuration menu and help  ... still needs work
    !! clean up dead code comments
    !! do more on glob for tile types and cap
    !! need about box
    !! author helps ,... look on internet

-------Version 8
    Moving from python 3.7 which worked fine at least under windows ( see version 6 of this app)
    to py_10 python py_10

    *! add configuration menu and help  ... still needs work
    ** seems to work again Linux py_10
    !! do more on glob for tile types and cap
    ** change glob glob for Linux, should  be ok on win
    ** selection of image directory does not work
    ** fix version in title
    ** get edit log, help.... on a menu or something
    ** add main.py....

    for 2024 updates
    ** fix floats
    ** change pubsub imports
    ** fixed deprecation warnings

    apparent a fair amount has changed including some int / float problems
    some deprecation and who know what else see notes in this
    which may be removed as resolved
    !! consider changing name to image_triage.py

--------Version P7
    pretty much skip, some false starts in old


-------Version Older

    working, beta

    enhancements ! = in process, * = done
    ! log exif to log file not print
    * convert to std logger
    ! make into a viewer, run off a file with pic names
    ! too much code in gui
    * resize position coed is a mess and a bit off
    * initial load of eof
    * make sure eof is not processed like a pic
    * can we move the images to make faster  ??
    * rotates
    * better size positron
    ! title with directory displayed
    ! help and about
    ! ini in text file
    !* clean up dead code ??
    ! wait cursor ??
    ! get file name function ? into copy paste
    ! more info function ?
    ! blow up one or two pics ?
    * add border
    * removed simpleApp

"""



--------------------------- scratch --------------




------------------------- gui notes   --------------------





================== old code, reference for awhile =================================

