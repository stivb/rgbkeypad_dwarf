class MidiReader:    
    
    def __init__(self, midi, monitor=None):      
        self.midi = midi
        self.line = ""
        self.text = ""
        self.transmissionOn=False
        self.monitor = monitor
        print("Reading from ", self.midi.in_channel)
          
    def displayMidiMessage(self,msg_in):        
        if msg_in is None:
            return
        if isinstance(msg_in, ProgramChange):
            if self.monitor != None:
                self.monitor.update(str(msg_in.patch))
            print(msg_in.patch)
        
        if isinstance(msg_in, NoteOn):
            self.line += chr(msg_in.velocity)
            if msg_in.velocity==60:
                self.transmissionOn=True
            if msg_in.velocity==62:
                self.transmissionOn=False
            if msg_in.velocity==10:
                print(self.txt)
                self.text += self.line
                self.line = ""