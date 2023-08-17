import time
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange

class StateBtn:

    def __init__(self, nId, btn, midi, callback=None, states=None, colors=None, cmdVals=None, ctrlChangeChn=None):
        self.id = nId
        self.btn=btn
        self.midi = midi
        self.state=0
        self.lastPressed=0
        self.callback=callback
        if states==None:
            self.states = [0,0]
        else:
            self.states=states
        if colors==None:
            self.colors = [(0,0,255),(255,0,0)]
        else:
            self.colors=colors
            
        if ctrlChangeChn==None:
            self.ctrlChangeChn=nId
        else:
            self.ctrlChangeChn=ctrlChangeChn
            
        if cmdVals==None:
            self.cmdVals=[1,96]
        else:
            self.cmdVals=cmdVals;
        self.btn.set_led(*self.colors[self.state])
            
 
    def check(self):
        if self.btn.pressed:
            self.wasPressed()
    
    def setCtrlChangeChn(self,ctrlChangeChn):
        self.ctrlChangeChn=ctrlChangeChn
        
    def checkState(self):
        if self.state==len(self.states):
            self.state=0
            
    def wasPressed(self):
        now = time.monotonic()
        if now-self.lastPressed >.2 :
            print("state button", self.id)
            self.upState()
            self.lastPressed=now
            if self.callback!=None:
                self.callback(self.id, self.state)
   
    def upState(self):
        self.state+=1
        self.checkState()
        self.enactState()
        
    def setState(self, state):
        print ("setting self.state, currently ", self.state, " to ", state)
        if state==self.state:
            return
        self.state=state
        self.checkState()
        self.enactState()
        
    def getState(self):
        return self.state
    
    def enactState(self):        
        self.btn.set_led(*self.colors[self.state])
        if self.midi==None: return
        self.midi.send(ControlChange(self.id+40, self.cmdVals[self.state]))
