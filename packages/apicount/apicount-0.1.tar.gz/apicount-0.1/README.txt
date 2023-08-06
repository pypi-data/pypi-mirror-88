
.. sectnum::
.. contents:: Table Of Contents

********
apicount
********

    apicount program lists all apis in given directory or files 

=======
Purpose
=======

    Usecases:
            - Compare API count and API signatures between two sources
            - API Counts to understand the fundamental complexity of program

=====
Usage
=====

    Command Line
    ------------

Usage: python -m apicount

    Usage: apicount [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -a, --showall         Show all apis with signatures
      -f FILENAME, --file=FILENAME
                            filename
      -d DESTNDIR, --destn=DESTNDIR
                            Destination Directory
      -t, --tree            Show All Directory Sources



=========
Examples
=========

    # List funcs for the file
    python -m apicount -f example.c

    # List funcs with signature for the file
    python -m apicount -f example.c -a

    # List Directories and functions
    python -m apicount -t -a   


API
---
.. code-block::        
    import apicount
    f = apicount.apicount.funcnode()
    f.showapis()

