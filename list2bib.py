#!/usr/bin/env python3

"""
Take the paperlist and create bib entries ..
"""

import sys
import re
import argparse


def find_meta(text):
    """search for the bibentry items

    Parameters
    ----------
    entry : `str`
        one block from the file

    Returns
    -------
    auth,title,year, month,handle : `str'
        stringd Ready to use in bib entry
    """

    auth = re.compile(r"editor:\s*([\w'`,\- ]+)\n")
    title = re.compile(r"title:\s*(.+)\s*\n")
    handle = re.compile(r"(PSTN-[0-9])+\s*\n")

    # Read the content of the file into a single string
    lines = []
    year = "2020"
    month = "dec"
    auths = ""
    titles = ""
    handles = text[0].strip()

    rset = auth.findall(text[2])
    if (rset):
        auths = rset[0]
    rset = title.findall(text[3])
    if (rset):
        titles = rset[0]

    return auths, titles, year, month, handles




def write_latex_bibentry(auth, title, year, month, handle, fd=sys.stdout):
    """ Write a bibentry based inthe current document
    Parameters
    ----------
    auth : `str``
        Author
    title : `str`
    year  : `str`
    month  : `str`
    handle  : `str`

    """

    print("@DocuShare{{{},".format(handle), file=fd)
    print("   author = {{{}}},".format(auth), file=fd)
    print("    title = {{{}}},".format(title), file=fd)
    print("     year = {},".format(year), file=fd)
    print("    month = {},".format(month), file=fd)
    print("   handle = {{{}}},".format(handle), file=fd)
    print("      url = {{http://{}.lsst.io }} }}".format(handle), file=fd)
    print("\n", file=fd)


def main():
    """Run program and generate bibentry ."""

    filename = "paperList.txt"
    entry = ""
    lines = []
    with open(filename, "r") as fd:
        for line in fd:
            lines.append(line)
            if (not line or len(line) < 4):
                auth, title, year, month, handle = find_meta(lines)
                write_latex_bibentry(auth, title, year, month, handle)
                lines = []



if __name__ == "__main__":
    description = __doc__
    main()
