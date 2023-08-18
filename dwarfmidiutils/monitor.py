#spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
#cs = digitalio.DigitalInOut(board.GP13)
#cs.direction = digitalio.Direction.OUTPUT
#leds = bcddigits.BCDDigits(spi, cs, nDigits=8)

#setting up external foot buttons


#setting up external potentiometers
#analog_A = AnalogIn(board.A0)
#analog_B = AnalogIn(board.A1)
#analog_C = AnalogIn(board.A2)


import displayio
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_st7789 import ST7789

class Monitor:
    

    
    def __init__(self, dizplay):
        self.display = dizplay
        self.kvpScreen = displayio.Group()
        self.txtScreen = displayio.Group()
        self.buffer = ""
        self.status = "Start"
        self.keyAreas = []
        self.valAreas = []
        self.highlight = 0xFFFFFF
        self.dimmed = 0x999999
        self.setupSettingsScreen()
        self.setupContentScreen()
        self.display.show(self.kvpScreen)
        
        
    def setupContentScreen(self):
        self.txt_group = displayio.Group(scale=1, x=10, y=10)
        self.txt_area = label.Label(terminalio.FONT, text="", color=self.highlight)
        self.txt_group.append(self.txt_area)
        self.txtScreen.append(self.txt_group)
    
        
    def setupSettingsScreen(self):        
        self.addKvP("", "", 0, self.highlight)
        self.addKvP("", "", 1, self.dimmed)
        self.addKvP("", "", 2, self.dimmed)
        self.addKvP("", "", 3, self.dimmed)
        self.addKvP("NEXT", "", 4, self.dimmed)
        self.addKvP(self.status, "5", 5, self.dimmed)
        
    def changeScreenIfNecc(self, newScreen):
        if (self.display.root_group!=newScreen):
            self.display.show(newScreen)
    
    #this formats a sequence of kvps from key|value lists    
    def printout(self,isSettingsPage, datastr):
        if not isSettingsPage:
            self.changeScreenIfNecc(self.txtScreen)
            self.txt_area.text = datastr
            print (datastr)
            return
        self.changeScreenIfNecc(self.kvpScreen)
        retval = ""
        lines = datastr.split("\n")
        lines = [x for x in lines if x]
        ct=0
        for line in lines:
            self.printLine(line,ct)
            ct+=1
        for i in range(ct,4):
            self.printLine("",i)
            
    def printContent(self, content):
        print(content)
        

    def printLine(self,line,pos):
        if line=="":
            self.showKvP("","",pos,False)
            return
        key, value = line.split('|')
        if key[0] == "*":  self.showKvP(key[1:],value,pos,True)
        else: self.showKvP(key,value,pos,False)
        
    def showKvP(self, key, val, pos, lit):
        self.keyAreas[pos].text = str(key)
        self.valAreas[pos].text = str(val)
        if lit:
            self.keyAreas[pos].color=self.highlight
            self.valAreas[pos].color=self.highlight
        else:
            self.keyAreas[pos].color=self.dimmed
            self.valAreas[pos].color=self.dimmed
        
    
    def statusUpdate(self, txt):
        self.status= txt
        self.valAreas[5].text = "\n".join(wrap_text_to_lines(self.status, 20))
        
    def statusAppend(self, txt):
        self.status= self.status + txt
        self.valAreas[5].text = "\n".join(wrap_text_to_lines(self.status, 20))
        
    def addKvP(self, key, defValue, pos,col):
        #LEFT column adding KEY placeholder
        key_group = displayio.Group(scale=2, x=0, y=10+(pos*40))
        key_area = label.Label(terminalio.FONT, text=key, color=col)
        self.keyAreas.append(key_area)
        key_group.append(key_area)  # Subgroup for text scaling
        self.kvpScreen.append(key_group)
        #RIGHT column adding VALUE placeholder
        val_group = displayio.Group(scale=2, x=210, y=10+(pos*40))
        val_area = label.Label(terminalio.FONT, text=defValue, color=col)
        self.valAreas.append(val_area)
        val_group.append(val_area)  # Subgroup for text scaling
        self.kvpScreen.append(val_group)
        
        


#