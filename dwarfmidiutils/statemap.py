from adafruit_midi.control_change import ControlChange

class StateMap:
    
    def __init__(self, stateMapItems):
        self.stateMapItems = stateMapItems
        self.pos = 0

    def next(self):
        if (self.pos+1)>=len(self.stateMapItems):
            self.pos=0
        else:
            self.pos+=1
        #print("Now at state", self.stateMapItems[self.pos].name, "@",self.pos )

    def allCols(self):
        return list(map((lambda x: x.col), self.stateMapItems))

    def currCol(self):
        return self.stateMapItems[self.pos].col

    def goto(self, newpos):
        self.pos = newpos

    def currMidiCmd(self):
        currItem = self.stateMapItems[self.pos]
        if currItem.midiCmdNum==None: return None
        if currItem.midiCmdVal==None: return None
        return ControlChange(currItem.midiCmdNum,currItem.midiCmdVal)

    
class StateMapItem:

    def __init__(self, name, col, midiCmdNum , midiCmdVal):
        self.name=name
        self.col= col
        self.midiCmdNum = midiCmdNum
        self.midiCmdVal = midiCmdVal

    
    
        