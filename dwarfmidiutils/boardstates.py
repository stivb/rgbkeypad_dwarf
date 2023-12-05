import time
    
        
class BoardStates:
    
    def __init__(self, callback):
        self.states = [None,None,None,None]
        self.pos = 0
        self.callback = callback
        
    def setStates(self, loopsOnArr):        
        self.states[self.pos] = loopsOnArr
        self.pos = -1
            
    def gotoState(self,pos):
        if self.pos==pos || self.pos<0 : 
            return
        filteredList = list(filter(lambda item: item is not None, self.states))
        if pos >=len(filteredList):
            return
        else:self.pos=pos
        self.callback(self.states[self.pos],True)
        
        
    def nextState(self):
        self.gotoState(self.pos+1)
          
    def prevState(self):
        self.gotoState(self.pos-1)
        
    def getState(self):
        return self.states[self.pos]
        
    def status(self):
        filteredList = list(filter(lambda item: item is not None, self.states))
        print ("self.pos is ", self.pos, " out of ", len(filteredList), " populated items")
        i=0
        for bs in filteredList:
            if i==self.pos: print("****************")
            print(bs)
            if i==self.pos: print("****************")
            i=i+1
            