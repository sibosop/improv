#!/usr/bin/env python
import os
import random
import parser
import sys
import time
import argparse
import datetime


home = os.environ['HOME']

proj = "%s/%s"%(home,"GitProjects")
mod = "%s/%s"%(proj,"improv")
specDir = "%s/%s"%(mod,"specs")
sys.path.append(mod+"/sibcommon")
defaultSpecFile = "%s/%s"%(specDir,"improv.json")
import config

if __name__ == '__main__':
  try:
    random.seed()
    pname = sys.argv[0]
    os.environ['DISPLAY']=":0.0"
    os.chdir(os.path.dirname(sys.argv[0]))
    print(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))  
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--spec', nargs=1, help='specify spec file', default=[defaultSpecFile])
    parser.add_argument('-o','--output', action = 'store_true',help='save session to GardenTakes directory')
    args = parser.parse_args()
    specFile = args.spec[0]
    print "using spec:",specFile
    config.load(specFile)
  except Exception, e:
    print("%s: error %s"%(pname,e))
