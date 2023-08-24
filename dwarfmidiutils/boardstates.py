import time

class BoardState:
    
    def __init__(self, fx=-1, loops=None):
        self.fx = fx
        self.loops = loops
        self.status()
        
    def setFx(self, fx):
        self.fx = fx
        
    def setLoops(self, loops):
        self.loops = loops
        
    def status(self):
        print(self.fx)
        print(self.loops)
    
        
class BoardStates:
    
    def __init__(self, nStates, callback):
        self.states = [None]*nStates
        self.pos = 0
        self.callback = callback
        
    def setState(self, state):        
        self.states[self.pos] = state
        self.pos = self.pos+1
        if self.pos>=len(self.states):
            self.pos=0
        self.callback(self.states[self.pos],False)
        self.status()
            
    def gotoState(self,pos):
        if self.pos==pos: return
        currState = self.pos
        filteredList = list(filter(lambda item: item is not None, self.states))
        if pos >=len(filteredList):
            self.pos=0
        else:self.pos=pos
        self.callback(self.states[self.pos],True)
        self.status()
        
    def nextState(self):
        self.gotoState(self.pos+1)
          
    def prevState(self):
        self.gotoState(self.pos-1)
        
    def getState(self):
        return self.states[self.pos]
        
    def status(self):
        filteredList = list(filter(lambda item: item is not None, self.states))
        print ("self.pos is ", self.pos, " out of ", len(filteredList), " populated items")
        