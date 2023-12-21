import time

class DrumBtn:
    
    def __init__(self, nId, btn, midi, note, debounce, cb_drumPadPressed=None):
        self.id=nId
        self.note=note
        self.midi = midi
        self.velocity=100
        self.btn=btn
        self.justPressed=False
        self.color=(255,255,255)
        self.lastPressed=0
        self.debounce = debounce
        self.cb_drumPadPressed = cb_drumPadPressed
        btn.set_led(*self.color)
        #self.btn.led_off()
        
    def noteOn(self):
        self.btn.led_on()
        if self.cb_drumPadPressed!=None:
                self.cb_drumPadPressed(self.id, self.note)
        self.btn.led_off()
        
    def check(self):
        if self.btn.pressed:
            self.wasPressed()
  
    def wasPressed(self):
        now = time.monotonic()
        if now-self.lastPressed > self.debounce :
            self.noteOn()
            self.lastPressed=now
            