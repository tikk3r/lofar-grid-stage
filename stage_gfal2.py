#!/usr/bin/env python
""" Attempt to stage a file throug a given SURL. """

import gfal2
import sys

import state_gfal2

__author__ = 'Frits Sweijen'
__version__ = '1.0.0'
__maintainer__ = 'Frits Sweijen'
__email__ = 'sweijen <at> strw.leidenuniv.nl'
__status__ = 'Development'

def stage(surl, async=False, wait=False):
    """ Attempt to stage the given SURL.
    Args:
        surl (str): SURL pointing to the file to stage.
        async (bool): execute the request asynchronously. Prevents blocking, but also prevents exception catching. Use "state_gfal2.py" to check staging status.
        wait (bool): wait for the staging to succeed or fail before returning.
    Returns:
        success (bool): boolean indicating if staging succeeded or failed.
    """
    context = gfal2.creat_context()
    try:
        print('Attempting to stage {:s}'.format(surl.split('/')[-1]))
        status = state_gfal2.check_status(surl)
        if 'ONLINE' in status:
            return True
        # bring_online(surl, pintime, timeout, async)
        # Set the pintime (in seconds) to 7 days (as the LTA).
        # Put in an asynchronous request so it doesn't block.
        (status, token) = context.bring_online(surl, 604800, 60, async)
        # Wait for a result if wanted.
        if wait:
            import time
            # Status 0 = queued, >0 = pinned, <0 = error.
            while status == 0:
                status = context.bring_online_poll(surl, token)
                # Sleep for 100ms to avoid excessive CPU load.
                time.sleep(0.1)
        status = context.bring_online_poll(surl, token)
        if status > 0:
            print('{:s} successfully staged.'.format(surl))
        success = True
    except gfal2.GError, e:
        success = False
        print('Staging failed with error code'),
        print(e.code)
        print(e.message)
    return success

def stage_file(filename, async=False, wait=False):
    """ Attempt to stage SURLS from a file. 
    Args:
        filename (str): file containing one SURL per line.
        async (bool): execute the request asynchronously. Prevents blocking, but also prevents exception catching. Use "state_gfal2.py" to check staging status.
        wait (bool): wait for the staging to succeed or fail before returning.
    Returns:
        None
    """
    with open(filename, 'r') as f:
        for srm in f.readlines():
            stage(srm.strip(), async=async, wait=wait)

if __name__ == '__main__':
    surl = sys.argv[1]
    if surl.startswith('srm://'):
        # Single file.
        stage(surl)
    else:
        # Assume a file list.
        stage_file(surl)
