#!/usr/bin/env python
import os
import sys
import mido
home = os.environ['HOME']
proj = "%s/%s"%(home,"GitProjects")
mod = "%s/%s"%(proj,"/improv")
sys.path.append(mod+"/sibcommon")
import singleton
from utils import print_dbg

class ControllerEvent(object):
  def __init__(self):
    self.event = None
    self.num = 0
    self.value = 0
    
  def __str__(self):
    print("str")
    return "event %s num %s value %s"%(self.event,self.num,self.value)

class Controller(object):
  _metaclass_ = singleton.Singleton
  def __init__(self,inPort,outPort,specs):
    mido.set_backend('mido.backends.rtmidi')
    self.midiIn = mido.open_input(inPort)
    self.midiOut = mido.open_output(outPort)
    self.specs = specs
      
  def getEvent(self):
    rval = ControllerEvent()
    msg = self.midiIn.receive();
    print_dbg("type: %s control %d value %d"%(msg.type,msg.control,msg.value))
    for k in self.specs['nano'].keys():
      min = self.specs['nano'][k][0]
      if len (self.specs['nano'][k]) == 2:
        max = self.specs['nano'][k][1]
      else:
        max = min
      x = range(min,max+1)
      if msg.control in x:
        rval.event = k
        rval.num = msg.control-min
        rval.value = msg.value
    return rval
      
    
    
  def close(self):
    self.midiIn.close()
    self.midiOut.close()

