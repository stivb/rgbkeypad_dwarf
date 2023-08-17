from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange
from digitalio import DigitalInOut, Direction, Pull


class FootSwitch:
    def __init__(self, midi, nId, pin, callback=None):
        self.midi = midi
        self.nId = nId
        self.prevVoltage = 0
        self.pin=pin
        self.state=0
        self.lastPressed=0
        self.btn = digitalio.DigitalInOut(pin)
        self.btn.direction = digitalio.Direction.INPUT
        self.btn.pull = digitalio.Pull.DOWN
        self.callback=callback
    
    def check(self):
        if self.btn.value:
            print(self.nId)
      
    def wasPressed(self):
            now = time.monotonic
            if now-lastPressed >.2 :
                changeState()
                self.lastPressed=now
                enactState()
                self.callback(nId, self.state)
            
    def changeState(self):
        if self.state==0: self.state=1
        else: self.state=0
        
    def enactState(self):
        self.midi.send(nId, 1+self.state*96)