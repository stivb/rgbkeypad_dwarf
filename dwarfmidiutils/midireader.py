import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
import math


class MidiReader:
    
# Currently it reads on channel 0 -
# which means you have to set the output channel to 16 on the plugin cos of bug (23/12/23)   
    
    def __init__(self, midi, cb_notify,cb_doLog):      
        self.midi = midi
        self.on = True
        self.startingAt = time.monotonic()
        self.numbers = []
        self.cb_notify=cb_notify
        self.cb_doLog=cb_doLog
        print("Reading from midi channel: ", self.midi.in_channel)
        
    
    def simulate(self):
        note_on_messages = []
        note_values = [48, 56, 60]
        velocities = 100
        for note_value in note_values:
            note_on = NoteOn(note_value, velocity=100)
            note_on_messages.append(note_on)
            time.sleep(0.1)
        for note_on_message in note_on_messages:
            self.read(note_on_message)
            time.sleep(0.1)
        

    def reset(self):
        self.on=True
        self.startingAt = time.monotonic()
        self.numbers = []

    def read(self,msg_in):
        
        
        #after two seconds following initiation
        if time.monotonic()-self.startingAt >2:
            self.on=False
            if (len(self.numbers)>0):
                self.cb_notify(self.numbers)
                self.cb_doLog("In midireader: self.numbers is :" + str(self.numbers))
  
        if msg_in is None:
            return
        
        if isinstance(msg_in, NoteOn):
            self.cb_doLog("*HERE IS A NOTE " + str(msg_in.note))
            self.numbers.append(msg_in.note)
                 
