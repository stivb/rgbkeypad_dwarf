import time
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

class NoteBasher:
    
    def __init__(self, midi, defVelocity=100, defDuration=.5):
        self.noteQueue=[]
        self.midi = midi
        self.duration=defDuration
        self.velocity=defVelocity
        self.last=0
        
    def noteOn(self,note):
        #clear previous - use this if not using tidyUp() for the noteoffs
        
        noteOffs = [tup for tup in self.noteQueue]
        for index, tup in enumerate(noteOffs):
            self.midi.send(NoteOn(tup[0], 0))
            print ("noteOff on", tup[0]);
        self.noteQueue=[]
        ##################################
        noteTuple=tuple([note,time.monotonic()])
        self.noteQueue.append(noteTuple)
        #monitor.statusUpdate(str(noteTuple[0]))
        self.midi.send(NoteOn(note, self.velocity))
        
    def queueLength(self):
        return len(self.noteQueue)
        
    def tidyUp(self):
        if len(self.noteQueue)==0: return
        noteOffs = [tup for tup in self.noteQueue if time.monotonic()-tup[1]> .09]
        for index, tup in enumerate(noteOffs):
            self.midi.send(NoteOn(tup[0], 0))
            print ("noteOff on", tup[0]);
        self.noteQueue = [x for x in self.noteQueue if x not in noteOffs]
