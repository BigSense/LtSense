#!/usr/bin/env python
import ConfigParser
import logging

loader_config = ConfigParser.ConfigParser()

loader_classes = {}

#Taken from 
# http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
def load_obj(name):
    components = name.split('.')
    path = '.'.join(components[:-1])
    clss = components[-1:][0]
    mod = __import__(path,globals(),locals(),clss)
    return getattr(mod,clss)()

def load_config(configFile):
  loader_config.readfp(open(configFile,'r'))
  
def get_class(idu):
  if idu in loader_classes: 
    logging.debug('Loading Cached Object ' + idu)
    return loader_classes[idu]

  bean = loader_config.items(idu)
  name = 'greenstation.'+loader_config.get(idu,'class')
  obj = load_obj(name)
  logging.debug('Created Object %s' % name)
  for (key,value) in bean:
    if key == 'class':
      continue
    else:    
      arg = None
      (optype,opt) = value.split('\\')
      if optype == 'class-ref':
        if opt.startswith('{'):
          arg = []
          for c in opt.strip('{}').split(','):
            arg.append(get_class(c))
        else:
          arg = get_class(opt)
      elif optype == 'float':
        arg = float(opt)
      elif optype == 'string': 
        arg = opt

      logging.debug('Setting attribute %s to %s for class %s' % (key,arg,obj))
      getattr(obj,"set_%s" % key)(arg)

  return obj


