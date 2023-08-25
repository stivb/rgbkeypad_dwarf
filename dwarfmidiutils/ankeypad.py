import time
from analogio import AnalogIn

class AnKeyPad:
    def __init__(self, midi, nId, pin, callback=None):
        self.midi = midi
        self.nId = nId
        self.prevVoltage = 0
        self.pin=pin
        self.analogue = AnalogIn(pin)
        self.callback = callback
        self.currVoltage=0.0
        self.notches = [29,33,40,49,54,57,59,62,69,74,78,83,97,106,115,126]
        self.notchMap=[0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]
        self.velocity=100
        self.lastPressed = time.monotonic()
        
    def get_voltage(self, voltage):
        return int((voltage * 127) / 65536)
    
    def set_notches(self,notches, notchmap):
        self.notches = notches
        self.notchMap = notchmap
    
    def check(self):
        
        now = time.monotonic()
        currVoltage = self.get_voltage(self.analogue.value)
        if currVoltage<25:
            self.prevVoltage=currVoltage
            return    
        
        if  abs(self.prevVoltage-currVoltage)>3 and  now-self.lastPressed >.1:
            
            nearestIdx = min(range(len(self.notches)), key=lambda i: abs(self.notches[i]-currVoltage))            
            self.prevVoltage=currVoltage
            
            self.lastPressed = now
            if self.callback!=None:
                self.callback(self.nId, self.notchMap[nearestIdx]+36)