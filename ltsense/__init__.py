#!/usr/bin/env python
"""Primary namespace for all BigSense LtSense Code.
   LtSense is the client used to transmit sensor data to
   the BigSense Web Service http://bigsense.io"""

from pkg_resources import get_distribution
from pkg_resources import DistributionNotFound
import os

exit_all_threads = False
"""Field to be checked by all threads at the beginning of their loop
   to see if the LtSense program should continue to run. This is
   typically set by a signal handler."""


def sense_version():

    # FIXME: If we have a package installed and are doing local
    # development, this will probably give us the wrong version
    # It doesn't matter that much though.

    try:
        return get_distribution('ltsense').version
    except DistributionNotFound:
        return os.popen('git describe --dirty').readlines()[0].strip()

