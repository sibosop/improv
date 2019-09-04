#!/usr/bin/env python
import os
import sys
import mido
home = os.environ['HOME']
proj = "%s/%s"%(home,"GitProjects")
mod = "%s/%s"%(proj,"improv")
specDir = "%s/%s"%(mod,"specs")
sys.path.append(mod+"/sibcommon")
import singleton
from utils import print_dbg

class Controller(object):
  _metaclass_ = singleton.Singleton
  
  def __init__(self,inPort,outPort):
    mido.set_backend('mido.backends.rtmidi')
    self.midiIn = mido.open_input(inPort,callback=self.eventHandler)
    self.midiOut = mido.open_output(outPort)
      
  def eventHandler(self,msg):
    print_dbg("%s"%(msg))
    
  def close():
    self.midiIn.close()
    self.midiOut.close()

