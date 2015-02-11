#!/usr/bin/env python
"""
Copyright [2014] [http://bigsense.io]

This file is part of LtSense.

LtSense is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LtSense is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LtSense.  If not, see <http://www.gnu.org/licenses/>.
"""
from optparse import OptionParser
import sys
import logging
import ltsense
from ltsense.config import BootStrap
import datetime
import signal
from os.path import basename
from os import getpid


#exit program signal
def signal_break_handler(signal, frame):
  print('Interurpt Detected. Killing threads')
  ltsense.exit_all_threads = True
  sys.exit(0)

signal.signal(signal.SIGINT, signal_break_handler)


def logfile_arg():
  def func(option,opt_str,value,parser): #@IndentOk
    if parser.rargs and not parser.rargs[0].startswith('-'):
      val=parser.rargs[0]
      parser.rargs.pop(0)
    else:
      #defaults to program_name_YYYY-MM-DD_HHMMSS.log
      val = 'var/log/' + basename(sys.argv[0]) + '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + '.log'
    setattr(parser.values,option.dest,val)
  return func


def main():
  """ltsense entry point."""
  parser = OptionParser(usage="%prog [-dvq] [-l <logfile>] [-c config ]",
                         description="%prog sensor relay service.\n", version="%prog {}".format(ltsense.sense_version()), epilog='Copyright 2011-2014 Sumit Khanna. http://BigSense.io')
  parser.add_option('-d','--debug',action='store_true',help='show additional debugging output')
  parser.add_option('-l','--logfile',action='callback',callback=logfile_arg(),help='store output to logfile [default: var/log/%s_yyyy-mm-dd-hhmmss.log]' % basename(sys.argv[0]),metavar='FILE',dest='logfile')
  parser.add_option('-c','--config',action='store',dest='config',help='configuration file [default: %default]',default='etc/gm.config')
  parser.add_option('-p','--pid',action='store',help='location to store PID', dest='pidfile')
  parser.set_defaults(verbose=True)
  parser.add_option('-v', action='store_true', dest='verbose', help='verbose output (default, combine with -d for additional information)')
  parser.add_option('-q', action='store_false', dest='verbose', help='run silent')

  (options, args) = parser.parse_args()

  #pid file
  if options.pidfile is not None:
    with(open(options.pidfile,'w')) as pid_fd:
      pid_fd.write( "%d\n" % getpid())

  #-d option
  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.INFO)

  #logger setup
  if options.verbose is True:
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
    logging.getLogger('').addHandler(console)

  if options.logfile is not None:
    logfile = logging.FileHandler(options.logfile)
    logfile.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(logfile)


  BootStrap(options.config)
  #ltsense.loader.load_config(options.config)
  #controller = ltsense.loader.get_class('Controller')
  #pause for Ctrl+C Signal Handler
  signal.pause()

if __name__ == '__main__':
  main()
