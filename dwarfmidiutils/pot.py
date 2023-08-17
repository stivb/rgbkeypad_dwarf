from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange
from analogio import AnalogIn

class Pot:
    def __init__(self, midi, nId, pin, callback=None):
        self.midi = midi
        self.nId = nId
        self.prevVoltage = 0
        self.pin=pin
        self.analogue = AnalogIn(pin)
        self.callback = callback
        self.currVoltage=0.0
        
    def get_voltage(self, voltage):
        return int((voltage * 127) / 65536)
    
    def check(self):

        currVoltage = self.get_voltage(self.analogue.value)
        if abs(self.prevVoltage-currVoltage)>3:
            self.midi.send(ControlChange(self.nId, currVoltage))
            self.prevVoltage=currVoltage
            if self.callback!=None:
                self.callback(self.nId, currVoltage)