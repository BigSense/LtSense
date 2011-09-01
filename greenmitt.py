#!/usr/bin/env python

from optparse import OptionParser,OptionGroup
import sys
import logging 
import greenstation.loader
import datetime
from os.path import basename

def logfile_arg():
   def func(option,opt_str,value,parser):
      if parser.rargs and not parser.rargs[0].startswith('-'):
         val=parser.rargs[0]
         parser.rargs.pop(0)
      else:
         #defaults to program_name_YYYY-MM-DD_HHMMSS.log
         val = 'var/log/' + basename(sys.argv[0]) + '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + '.log'
      setattr(parser.values,option.dest,val)
   return func

if __name__ == '__main__':

   parser = OptionParser(usage="%prog [-dvq] [-l <logfile>] [-c config ]",
                         description="Greenstation sensor relay service.\n", version="%prog 0.1 alpha", epilog='Copyright 2011 Sumit Khanna. PenguinDreams.org')
   parser.add_option('-d','--debug',action='store_true',help='show additional debugging output')
   parser.add_option('-l','--logfile',action='callback',callback=logfile_arg(),help='store output to logfile [default: var/log/%s_yyyy-mm-dd-hhmmss.log]' % basename(sys.argv[0]),metavar='FILE',dest='logfile')
   parser.add_option('-c','--config',action='store',dest='config',help='configuration file [default: %default]',default='etc/gm.config')
   parser.set_defaults(verbose=True)
   parser.add_option('-v', action='store_true', dest='verbose', help='verbose output (default, combine with -d for additional information)')
   parser.add_option('-q', action='store_false', dest='verbose', help='run silent')

   (options, args) = parser.parse_args()

   #-d option
   if options.debug == True:
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

  
   greenstation.loader.load_config(options.config)
   controller = greenstation.loader.get_class('Controller')
