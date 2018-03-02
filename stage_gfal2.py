#!/usr/bin/env python
""" Attempt to stage a file throug a given SURL. """

import gfal2
import sys

__author__ = 'Frits Sweijen'
__version__ = '1.0.0'
__maintainer__ = 'Frits Sweijen'
__email__ = 'sweijen <at> strw.leidenuniv.nl'
__status__ = 'Development'

def stage(surl, wait=False, verbose=True):
    """ Attempt to stage the given SURL.
    Args:
        surl (str): SURL pointing to the file to stage.
        wait (bool): wait for the staging to succeed or fail before returning.
        verbose (bool): be verbose or not.
    Returns:
        success (bool): boolean indicating if staging succeeded or failed.
    """
    context = gfal2.creat_context()
    try:
        if verbose:
            print('Attempting to stage {:s}'.format(surl.split('/')[-1]))
        # bring_online(surl, pintime, timeout, async)
        # Set the pintime (in seconds) to 7 days (as the LTA).
        # Put in an asynchronous request so it doesn't block.
        (status, token) = context.bring_online(surl, 604800, 60, True)
        # Wait for a result if wanted.
        if wait:
            import time
            # Status 0 = queued, >0 = pinned, <0 = error.
            while status == 0:
                print status
                status = context.bring_online_poll(surl, token)
                # Sleep for 100ms to avoid excessive CPU load.
                time.sleep(0.1)
        success = True
    except gfal2.GError, e:
        success = False
        if verbose:
            print('Staging failed with error code'),
            print(e.code)
            print(e.message)
    return success

if __name__ == '__main__':
    surl = sys.argv[1]
    stage(surl)
