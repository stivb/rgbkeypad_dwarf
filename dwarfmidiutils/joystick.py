import time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull


class JoyStick:
    def __init__(self, midi, nId, vPin, hPin, btnPin, callback=None):
        self.midi = midi
        self.nId = nId
        self.vAnalog = AnalogIn(vPin)
        self.hAnalog = AnalogIn(hPin)
        self.switch = DigitalInOut(btnPin)
        self.switch.direction = Direction.INPUT
        self.switch.pull = Pull.UP
        self.callback = callback
        self.lastMoved = time.monotonic()
        self.notches = [4,24,64,104,124]
        self.notchMap = [-2,-1,0,1,2]
        
    def get_voltage(self, voltage):
        return int((voltage * 127) / 65536)
        
    def check(self):
        now = time.monotonic()
        
        v = self.get_voltage(self.vAnalog.value)
        h = self.get_voltage(self.hAnalog.value)
        b = not self.switch.value
        
        #print(b,self.lastMoved)
        
        if b and (now -self.lastMoved)> .2: 
            self.lastMoved = now
            self.callback(0,0,b)
            return
        
        if (v==0 and h==0): return
        
        if h==0:
            if (now-self.lastMoved)<.5: return
        else:
            if (now-self.lastMoved)<.2: return
        
        nearestV = min(range(len(self.notches)), key=lambda i: abs(self.notches[i]-v))
        nearestH = min(range(len(self.notches)), key=lambda i: abs(self.notches[i]-h))  
   
   
        if self.callback!=None:
                self.lastMoved = now
                self.callback(self.notchMap[nearestV],self.notchMap[nearestH],b)

