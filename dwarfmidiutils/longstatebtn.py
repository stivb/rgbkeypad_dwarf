import time



#needs a concept of a state map
#something with for each state (with midi consequences)
#state 0 - REST, onclick sends 96 on channel 40, PLAYING, onclick sends 96 on channel 41, OFF, onclick sends 0 on channel 40
#which means a state is defined by name,color,channel,value 

class LongStateBtn:
   #LongStateBtn(currKey, keys[exkeys[0]], None, 4, list(colz.values())[0:4], boardStatePressed)
    def __init__(self, nId, btn, adaMidi,stateMap, callback):
        self.id = nId
        self.btn=btn
        self.adaMidi = adaMidi
        self.stateMap=stateMap
        self.callback = callback        
        self.btn.set_led(*self.stateMap.currCol())
        self.lastPressed=0
            
 
    def check(self):
        if self.btn.pressed:
            if self.lastPressed==0:
                self.lastPressed=time.monotonic()
        else:
            if self.lastPressed!=0:
                pressDuration = time.monotonic()-self.lastPressed
                self.lastPressed=0
                self.press(pressDuration>1)

            
           
    def press(self, lp):
        print("state button", self.id, self.stateMap.pos,lp)
        self.stateMap.next()
        self.enactState()
        if self.callback!=None:
            self.callback(self.id, self.stateMap.pos,lp)

        
        
    def setState(self, stateNum):
        print ("setting self.state, of fx button", self.id, " from " , self.stateMap.pos, " to ", stateNum)
        if stateNum==self.stateMap.pos:
            return
        self.stateMap.goto(stateNum)
        self.enactState()
        
    def getState(self):
        return self.stateMap.pos
    
    def enactState(self):      
        if self.adaMidi==None: return
        if self.stateMap.currMidiCmd()==None: return
        self.btn.set_led(*self.stateMap.currCol())
        self.adaMidi.send(self.stateMap.currMidiCmd())
