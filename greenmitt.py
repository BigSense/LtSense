#!/usr/bin/env python

from greenstation.controller import DefaultController
from greenstation.data import SQLiteDataHandler
import ConfigParser


if __name__ == '__main__':
  
    config = ConfigParser.ConfigParser()
    config.readfp(open('gm.config'))
  
    controller = DefaultController(config)
    controller.set_data_handler(SQLiteDataHandler(config))

