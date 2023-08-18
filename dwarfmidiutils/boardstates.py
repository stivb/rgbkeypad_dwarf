import time

class BoardState:
    
    def __init__(self, fx=-1, loops=None):
        self.id=nId
        self.fx = fx
        self.loops = loops
        
    def setFx(self, fx):
        self.fx = fx
        
    def setLoops(self, loops):
        self.loops = loops
        
class BoardStates:
    
    def __init__(self, callback):
        self.states = [None]*3
        self.pos = 0
        self.callback = callback
        
    def setStateAt(self, state,pos):
        if pos>=len(self.states): return
        self.states[pos] = state
        
    def nextState(self)
        currState = self.pos
        filteredList = list(filter(lambda item: item is not None, self.states))
        self.pos = self.pos+1
        if self.pos >=len(filteredList):
            self.pos=0
        if self.pos!=currState:
            self.callback(self.states[self.pos])
          
    def prevState(self)
        currState = self.pos
        filteredList = list(filter(lambda item: item is not None, self.states))
        self.pos = self.pos-1
        if self.pos <=0:
            self.pos=len(filteredList)-1
        if self.pos!=currState:
            self.callback(self.states[self.pos])
        