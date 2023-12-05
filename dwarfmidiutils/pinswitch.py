from digitalio import DigitalInOut, Direction, Pull
import time


class PinSwitch:
    def __init__(self, nId, pin, callback=None):
        self.nId = nId
        self.prevVoltage = 0
        self.pin=pin
        self.state=0
        self.lastPressed=0.0
        self.btn = DigitalInOut(pin)
        self.btn.direction = Direction.INPUT
        self.btn.pull = Pull.UP
        self.callback=callback
    
    def check(self):
        if self.btn.value==False:
            self.wasPressed()
      
    def wasPressed(self):
            now = time.monotonic()
            if now-self.lastPressed >.2 :
                self.lastPressed=now
                self.callback(self.nId)
