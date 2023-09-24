import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn


class MidiReader:    
    
    def __init__(self, midi, notify):      
        self.midi = midi
        self.on = True
        self.onAt = time.monotonic()
        self.numbers = []
        self.notify=notify
        print("Reading from ", self.midi.in_channel)
          
#     def displayMidiMessage(self,msg_in):        
#         if msg_in is None:
#             return
#         if isinstance(msg_in, ProgramChange):
#             if self.monitor != None:
#                 self.monitor.update(str(msg_in.patch))
#             print(msg_in.patch)
#         
#         if isinstance(msg_in, NoteOn):
#             self.line += chr(msg_in.velocity)
#             if msg_in.velocity==60:
#                 self.transmissionOn=True
#             if msg_in.velocity==62:
#                 self.transmissionOn=False
#             if msg_in.velocity==10:
#                 print(self.txt)
#                 self.text += self.line
#                 self.line = ""

    def reset(self):
        self.on=True
        self.numbers = []
        
    
    
    def read(self,msg_in):
        if time.monotonic()-self.onAt >2:
            self.on=False
            print("NO MORE WAITING")
            self.notify(self.numbers)
        if msg_in is None:
            return
        if isinstance(msg_in, NoteOn):
            if msg_in.note==127:
                self.on=False
                self.notify(self.numbers)
                return
            else:
                numbers.append(msg_in.note)
                 
             
             