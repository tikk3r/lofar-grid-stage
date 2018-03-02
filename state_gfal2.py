#!/usr/bin/env python
""" Check the status of an SRM file to see if it is ONLINE or NEARLINE. """

import gfal2
import sys

__author__ = 'Frits Sweijen'
__version__ = '1.0.0'
__maintainer__ = 'Frits Sweijen'
__email__ = 'sweijen <at> strw.leidenuniv.nl'
__status__ = 'Development'

def check_status(surl, verbose=True):
    """ Obtain the status of a file from the given surl.
    Args:
        surl (str): the SURL pointing to the file.
        verbose (bool): print the status to the terminal.
    Returns:
        status (str): the file status as stored in the 'user.status' attribute.
    """
    context = gfal2.creat_context()
    status = context.getxattr(surl, 'user.status')
    filename = surl.split('/')[-1]
    if verbose:
        print('{:s} is'.format(filename)),
        print(status)
    return status

if __name__ == '__main__':
    surl = sys.argv[1]
    check_status(surl)
