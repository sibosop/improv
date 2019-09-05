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
    return "event %s num %s value %s"%(self.event,self.num,self.value)

class Controller(object):
  _metaclass_ = singleton.Singleton
  def __init__(self,inPort,outPort,desc):
    mido.set_backend('mido.backends.rtmidi')
    self.midiIn = mido.open_input(inPort)
    self.midiOut = mido.open_output(outPort)
    self.desc = desc
      
  def getEvent(self):
    rval = ControllerEvent()
    msg = self.midiIn.receive();
    print_dbg("type: %s control %d value %d"%(msg.type,msg.control,msg.value))
    for k in self.desc.keys():
      min = self.desc[k][0]
      if len (self.desc[k]) == 2:
        max = self.desc[k][1]
      else:
        max = min
      if msg.control in range(min,max+1):
        rval.event = k
        rval.num = msg.control-min
        rval.value = msg.value
        break
    return rval
      
    
    
  def close(self):
    self.midiIn.close()
    self.midiOut.close()

