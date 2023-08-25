import time

class DrumBtn:
    
    def __init__(self, nId, btn, midi, note, debounce, callback=None):
        self.id=nId
        self.note=note
        self.midi = midi
        self.velocity=100
        self.btn=btn
        self.justPressed=False
        self.color=(255,255,255)
        self.lastPressed=0
        self.debounce = debounce
        self.callback = callback
        btn.set_led(*self.color)
        #self.btn.led_off()
        
    def noteOn(self):
        self.btn.led_on()
        if self.callback!=None:
                self.callback(self.id, self.note)
        self.btn.led_off()
        
    def check(self):
        if self.btn.pressed:
            self.wasPressed()
  
    def wasPressed(self):
        print(self.id, " ", self.btn)
        now = time.monotonic()
        if now-self.lastPressed > self.debounce :
            self.noteOn()
            self.lastPressed=now
            