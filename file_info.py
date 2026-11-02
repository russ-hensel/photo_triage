# -*- coding: utf-8 -*-
# an object for storing file info in large part for sorting
# there is a more official class with almost the same name this
# could become a problem


# ------------------------------------------
if __name__ == "__main__":
    import main
    main.main()

# ---- import

import os


class FileInfo(  ):
    """"""

    def __init__(self,  fullname  ):

        self.create_date   = None
        self.fullname      = fullname
        self.newname       = None
        self.modify_date   = None
        self.processed     = False           # need codes and constants
        self.size          = None
        self.ixSort        = -1              # -1 if not a valid file, else sort order in array from 0

        self.populate()
        #..... add more as needed

    def __str__(self):

            rep   = self.fullname  + "  " +  str( self.size ) # +

            return rep

    def __repr__(self):

            return self.__str__()

    # ---------------
    def populate( self ):
        """
        populate with whateve you decide to support
        """

        if self.fullname != None:
            stats = os.stat( self.fullname )

            #self.size           = stats[ ST_SIZE ]
            #self.modify_date    = stats[ ST_MTIME]

            self.size           = stats.st_size

            self.modify_date    = stats.st_mtime


      # ---------------   looks like a copy mistake
        def __str__(self):

            rep   = self.fullname  + str( self.size )

            return rep

        def __repr__(self):

            return self.__str__()



# =============== eof ===========================



