#!/usr/bin/env python
"""Primary namespace for all BigSense LtSense Code.
   LtSense is the client used to transmit sensor data to
   the BigSense Web Service"""


exit_all_threads = False
"""Field to be checked by all threads at the beginning of their loop
   to see if the LtSense program should continue to run. This is
   typically set by a signal handler."""
