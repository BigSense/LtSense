#!/usr/bin/env/python

from Queue import Queue, Empty
import sqlite3
from threading import Lock

class QueueException(Exception):
  pass

class AbstractQueue(object):
  
  def __init__(self):
    object.__init__(self)
    self.queue_timeout = 1.0 #in seconds
    self.size = -1
    
  def dequeue(self):
    "Pulls latest item from queue or returns None"
    raise QueueException("Unimplemented Abstract Queue Function")
  
  def enqueue(self, item):
    "Adds element to queue"
    raise QueueException("Unimplemented Abstract Queue Function")
    
  

class MemoryQueue(AbstractQueue):
  
  def __init__(self):
    AbstractQueue.__init__(self)
    self.__queue = Queue()
    
  def dequeue(self):
    try:
      return self.__queue.get(self.queue_timeout)
    except Empty:
      return None
    
  def enqueue(self,item):
    self.__queue.put(item)
  
  size = property(lambda self: self.__queue.qsize(),lambda self,v:None )


class SQLiteQueue(AbstractQueue):
  
  def __init__(self):
    AbstractQueue.__init__(self)
    self.sqlFile = None
    self.__conn = None
    self.sqlLock = Lock()
    
  def _getDataFile(self):
    return self.sqlFile

  def _setDataFile(self,df):
      self.sqlFile = df  

  dataFile = property(_getDataFile,_setDataFile)  
  
  def __cursor(self):
    if self.__conn == None:
      self.__conn = sqlite3.connect(self.sqlFile,check_same_thread = False)
      cursor = self.__conn.cursor()
      cursor.execute('CREATE TABLE IF NOT EXISTS queue (id INTEGER PRIMARY KEY AUTOINCREMENT,payload TEXT)')
      self.__conn.commit()
      return cursor
    return self.__conn.cursor()
  
  def dequeue(self):
    self.sqlLock.acquire()
    retval = None
    for row in self.__cursor().execute('SELECT id,payload FROM queue ORDER BY id ASC LIMIT 1'):
       self.__cursor().execute('DELETE FROM queue WHERE id = ?', [row[0]])
       self.__conn.commit()
       retval = row[1]
    self.sqlLock.release()
    return retval
    
  def enqueue(self,item):
    self.sqlLock.acquire()
    self.__cursor().execute('INSERT INTO queue(payload) VALUES(?)' , [item] )  
    self.__conn.commit()
    self.sqlLock.release()  
    
  def __qsize(self):
    size = -1
    self.sqlLock.acquire()
    for row in self.__cursor().execute('SELECT COUNT(*) FROM queue'):
      size = int(row[0])
    self.sqlLock.release()   
    return size 
    
  size = property(lambda self: self.__qsize(),lambda self,v:None )
