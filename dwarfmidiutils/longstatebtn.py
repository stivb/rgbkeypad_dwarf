import time


class LongStateBtn:
   
    def __init__(self, nId, btn, adaMidi,stateMap, preCmdCallBack, postCmdCallBack):
        self.id = nId
        self.btn=btn
        self.adaMidi = adaMidi
        self.stateMap=stateMap
        self.preCmdCallBack = preCmdCallBack
        self.postCmdCallBack = postCmdCallBack        
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
        if self.preCmdCallBack!=None:
            self.preCmdCallBack(self.id, self.stateMap.pos,lp)
        self.enactState()
        if self.postCmdCallBack!=None:
            self.postCmdCallBack(self.id, self.stateMap.pos,lp)

        
        
    def setState(self, stateNum):
        print ("setting self.state, of fx button", self.id, " from " , self.stateMap.pos, " to ", stateNum)
        if stateNum==self.stateMap.pos:
            return
        self.stateMap.goto(stateNum)
        self.enactState()
        
    def getState(self):
        print("Sourcing the state of button ", self.id)
        return self.stateMap.pos
    
    def enactState(self):
        print(self.adaMidi, self.stateMap.currMidiCmd())
        self.btn.set_led(*self.stateMap.currCol())
        print(*self.stateMap.currCol())
        if self.adaMidi==None: return
        if self.stateMap.currMidiCmd()==None: return        
        self.adaMidi.send(self.stateMap.currMidiCmd())
