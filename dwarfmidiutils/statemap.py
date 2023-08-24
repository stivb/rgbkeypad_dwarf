
from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange

class StateMap:
    
    def __init__(self, stateMapItems):
        self.stateMapItems = stateMapItems
        self.pos = 0

    def next(self)
        if self.pos+1>=len(stateMapItems):
            self.pos=0
        else
            self.pos+=1
        print("Now going to state", self.name)

    def allCols(self)
        return list(map((lambda x: x.col), self.stateMapItems))

    def currCol(self)
        return self.stateMapItems[self.pos].col

    def goto(self, newpos)
        self.pos = newpos


    def currMidiCmd(self)
        if self.stateMap.currMidiCmd()==None: return None
        if self.stateMap.midiCmdVal()==None: return None
        return ControlChange(self.stateMapItems[self.pos].midiCmdNum(),self.stateMapItems[self.pos].midiCmdVal())

    
class StateMapItem

def __init__(self, name, col, midiCmdNum , midiCmdVal):
        self.name=name
        self.fx = fx
        self.col= col
        self.midiCmdNum = midiCmdNum
        self.midiCmdVal = midiCmdVal

    
    
        