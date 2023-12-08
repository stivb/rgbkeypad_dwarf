import time
  
class BoardStates:
    
    
    def __init__(self):
        self.states = [None,None,None,None]
        
    def setState(self, loopsOnArr, idx):        
        self.states[idx] = loopsOnArr
            
    def getState(self,pos):
        if pos>=len(self.states):
            return None;
        else:
            return self.states[pos]
        
    def getNextStateIdx(self,pos):
        if pos>=len(self.states)-1: return 0
        if self.states[pos]==None: return 0
        return pos+1
            