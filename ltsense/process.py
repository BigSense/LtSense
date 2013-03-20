from subprocess import Popen,PIPE
import logging
from bigsense import owpy
from Queue import Queue

class ExternalProcessHandler(object):

  def __init__(self):
    object.__init__(self)
    self._process = None
    self.errorLog = '/tmp/process.log'

  def _setup_process(self,procName):
    self._cmd_name = procName
    errFd = open(self.errorLog,'w')

    logging.info('Starting External Process %s' % procName)
    logging.info('Error log %s' % self.errorLog)
    self._process = Popen(procName, shell=False, bufsize=1, stdin=PIPE, stdout=PIPE, stderr=errFd)
    logging.debug('Process Started %s' % procName)

  def read_line(self):
    #TODO: Handle Broken Pipe
    logging.debug('Reading from process %s' % self._cmd_name)
    output = self._process.stdout.readline()
    logging.debug('ReadLine: "%s"' % output.strip())
    return output
    
  def write_line(self,line):
    logging.debug('Writing Statement "%s" to process "%s"' % (line,self._cmd_name))
    #TODO: Handle Broken Pipe
    self._process.stdin.write(line + '\n')
    self._process.stdin.flush()

  command = property(lambda self: self._cmd_name,_setup_process)


class OneWireNativeProcessHandler(object):

  def __init__(self):
    object.__init__(self)
    self._port = None
    self._queue = Queue()


  def _release_port(self):
    owpy.owRelease(self._port)
    self._port = None

  def _init_port(self,port):
    if self._port != None:
      self._release_port()
    self._port = owpy.owAcquireEx(port)

  def __del__(self):
    self._release_port()

  port = property(lambda self: self._port, _init_port)

  def read_line(self):
    return str(self._queue.get())

  def write_line(self,command):

    cmds = command.split(' ')

    if cmds[0] == 'list':
      devs = owpy.owListDevices(self._port)
      self._queue.put(len(devs))
      for d in devs:
        self._queue.put(d)

    elif cmds[0] == 'get' :
      if cmds[1].endswith('10'):
        self._queue.put(owpy.owReadTemperature(self._port,cmds[1]))
      elif cmds[1].endswith('1D'):
        counts = ('%s:%s:%s:%s' % (
            owpy.owReadCounter(self._port,cmds[1],12),
            owpy.owReadCounter(self._port,cmds[1],13),
            owpy.owReadCounter(self._port,cmds[1],14),
            owpy.owReadCounter(self._port,cmds[1],15),
          ))
        self._queue.put(counts)
