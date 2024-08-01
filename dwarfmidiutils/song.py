import time
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.control_change import ControlChange

class Song:
    def __init__(self, midi,num=127):
        self.midi = midi
        self.on=False
        self.num=num
        
    def start(self):
        print("Song start")
        if self.on==True:
            return
        self.on=True
        print("Sending note on")
        ControlChange(self.num,127)
        self.midi.send(NoteOn(self.num, 2))
        
        
    def stop(self):
        print("Song stop")
        if not self.on:
            return
        self.on=False
        print("Sending note off")
        ControlChange(self.num,0)
        self.midi.send(NoteOff(self.num, 0))
        
        
        
        
        
    