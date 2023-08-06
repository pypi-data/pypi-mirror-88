#!/usr/bin/env python

"""
apiparse

Parse API and API groups from sources. List the API occurences from all
directories and sub directories

"""

# Main Routine
if __name__ == "__main__":
    import apicount
    f = apicount.apicount.funcnode()
    f.showapis()

