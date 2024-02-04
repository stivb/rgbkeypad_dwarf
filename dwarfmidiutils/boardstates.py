import time
  
class BoardStates:
    
    
    def __init__(self, cb_doLog):
        self.states = [None,None,None,None]
        self.index=0
        self.cb_doLog = cb_doLog
        
    def setState(self, loopsOnArr, idx):        
        self.states[idx] = loopsOnArr
        self.cb_doLog("The current loopsOnArr is " + str(loopsOnArr))
        
    def nextState(self):
        """
        Returns the next non-None value from the array.
        If it reaches the end of the array, returns the first non-None value found.
        """
        original_index = self.index
        while True:
            value = self.states[self.index]
            self.index = (self.index + 1) % len(self.states)
            if value is not None:
                return value
            # If no non-None value found, break the loop
            if self.index == original_index:
                break
        # If still no non-None value found, return None (or handle this case as needed)
        return None
            
#     def getState(self,pos):
#         if pos>=len(self.states):
#             return None;
#         else:
#             return self.states[pos]
#         
#     def getNextStateIdx(self,pos):
#         if pos>=len(self.states)-1: return 0
#         if self.states[pos]==None: return 0
#         return pos+1


    
    def clearStates(self):
        self.states = [None,None,None,None]
            