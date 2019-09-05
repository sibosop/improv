#!/usr/bin/env python
import os
import random
import parser
import sys
import time
import argparse
import datetime
import signal



home = os.environ['HOME']

proj = "%s/%s"%(home,"GitProjects")
mod = "%s/%s"%(proj,"improv")
specDir = "%s/%s"%(mod,"specs")
sys.path.append(mod+"/sibcommon")
defaultSpecFile = "%s/%s"%(specDir,"improv.json")
import config
from utils import print_dbg
from utils import setDebug

from controller import Controller

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

def service_shutdown(signum, frame):
    print_dbg('Caught signal %d' % signum)
    raise ServiceExit


signal.signal(signal.SIGTERM, service_shutdown)
signal.signal(signal.SIGINT, service_shutdown)
controller = None
if __name__ == '__main__':
  try:
    random.seed()
    pname = sys.argv[0]
    os.environ['DISPLAY']=":0.0"
    os.chdir(os.path.dirname(sys.argv[0]))
    print_dbg(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))  
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--spec', nargs=1, help='specify spec file', default=[defaultSpecFile])
    parser.add_argument('-v','--verbose', action = 'store_true',help='set verbose mode')
    args = parser.parse_args()
    setDebug(args.verbose)
    specFile = args.spec[0]
    print_dbg("using spec: %s"%specFile)
    specs = config.load(specFile)
    controller = Controller(specs["inPort"],specs["outPort"],specs)
    while True:
      event = controller.getEvent()
      print_dbg("event: %s"%event)
  except ServiceExit:
    print("Service exit received")
  except Exception, e:
    print("%s: error %s"%(pname,e))
  if controller:
    controller.close()
