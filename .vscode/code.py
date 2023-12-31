# SPDX-FileCopyrightText: 2021 Sandy Macdonald
#
# SPDX-License-Identifier: MIT

# This example demonstrates how to light keys when pressed.

# Drop the `pmk` folder
# into your `lib` folder on your `CIRCUITPY` drive.


# connctions
# 40->1  (power to 1st pin of display)
# 36->6*_>15  (3.3v to 6th* pin of display, to first pin analog keypad)
# 31->17  (ADC0 to 3rd pin (output of analog keypad))
# 23_>16 (GND to 2nd pin (GND of analog keypad)) - but could use 38 of pi pico
# 
# 
# 
# 
# 18->7 (GND PI TO GND display)
# 17->2 (Chip Select to CS)
# 14->3 (SCK to SCK)
# 15->4 (MOSI)
# 16_>5 (DC)
# see * above
# 
# 
# tft_cs = board.GP13
# tft_dc = board.GP12
# spi_mosi = board.GP11
# spi_clk = board.GP10
################################################

#########NOTES FOR MPC3008###############
#pins on mpc with connections
# 16->3v
# 15->3v
# 14->GND
# 13 SCK   (sck to clk) GP02
# 12 DOUT  (to miso)    GP04
# 11 DIN	 (to mosi)    GP03
# 10 CS    (            GP05
# 9->GND
# # create the spi bus
# spi = busio.SPI(clock=GP02, MISO=GP04, MOSI=board.GP03)
# # create the cs (chip select)
# cs = digitalio.DigitalInOut(board.GP05)
# # create the mcp object
# mcp = MCP.MCP3008(spi, cs)
#might try different mux however
#########################################

from dwarfmidiutils.statebtn import StateBtn
from dwarfmidiutils.longstatebtn import LongStateBtn
from dwarfmidiutils.drumbtn import DrumBtn
from dwarfmidiutils.notebasher import NoteBasher
from dwarfmidiutils.pot import Pot
from dwarfmidiutils.footswitch import FootSwitch
from dwarfmidiutils.ankeypad import AnKeyPad
from dwarfmidiutils.joystick import JoyStick
from dwarfmidiutils.midireader import MidiReader
from dwarfmidiutils.monitor import Monitor
from dwarfmidiutils.settings import Settings
from dwarfmidiutils.boardstates import BoardState,BoardStates
from dwarfmidiutils.statemap import StateMapItem, StateMap

import json
import board
import busio

import terminalio
import displayio
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_st7789 import ST7789
from digitalio import DigitalInOut, Direction, Pull

from adafruit_datetime import datetime
from analogio import AnalogIn
import time
from pmk import PMK
#from pmk.platform.keybow2040 import Keybow2040 as Hardware          # for Keybow 2040
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware  # for Pico RGB Keypad Base

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange



keybow = PMK(Hardware())
keys = keybow.keys

drumNotesPlayed = []

transmissionOn=True

debugging=False

#spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
#cs = digitalio.DigitalInOut(board.GP13)
#cs.direction = digitalio.Direction.OUTPUT
#leds = bcddigits.BCDDigits(spi, cs, nDigits=8)

#setting up external foot buttons


#setting up external potentiometers
#analog_A = AnalogIn(board.A0)
#analog_B = AnalogIn(board.A1)
#analog_C = AnalogIn(board.A2)


#setting up constants

MIDI_MODE_EXCL=0
MIDI_MODE_YOKED=1
MIDI_MODE_LEARN=2

NORTH=0
EAST=3
SOUTH=6
WEST=9

colz = {"RED":(255,0,0),"GREEN":(0,255,0),"BLUE":(0,0,255),
"CYAN":(0,255,255),"VIOLET":(255,0,255),"YELLOW":(255,255,0),
"TEAL":(0,128,128),"PURPLE":(128,0,128),"OLIVE":(128,128,0),
"MAROON":(128,0,0),"LIGHTGREEN":(0,128,0),"NAVY":(0,0,128),
"GRAY":(128,128,128)}

gCurrMidiMode=MIDI_MODE_EXCL

      
class Functions:
    
    def __init__(self):
        self.callCount=0
        self.allowed_funcs =  {"self.SettingsChooseChannel": self.SettingsChooseChannel,
                         "self.SettingsGoBoardSnapshot":self.SettingsGoBoardSnapshot,
                         "self.SettingsSendCCNumVal":self.SettingsSendCCNumVal,
                         "self.SettingsBpm":self.SettingsBpm,
                         "self.SettingsBpb":self.SettingsBpb,
                         "self.SettingsSetBoardChannel":self.SettingsSetBoardChannel,
                         "self.SettingsSetSnapshotChannel":self.SettingsSetSnapshotChannel
                         } 
        
        
    def run_func(self, input_string):
        print(input_string)
        eval(input_string, {"self": self})

    
    def SettingsChooseChannel(self, iput):
        print("Not Yet Implemented", iput)
        
    def SettingsGoBoardSnapshot(self, iput):
        print("Not Yet Implemented", iput)
        
    def SettingsSendCCNumVal(self, iput):
        print("Not Yet Implemented", iput)
        
    def SettingsBpm(self, iput):
        print("Not Yet Implemented", iput)
        
    def SettingsBpb(self, iput):
        print("Not Yet Implemented", iput)
        
    def SettingsSetBoardChannel(self, iput):
        print("Not Yet Implemented", iput)
        
    def SettingsSetSnapshotChannel(self, iput):
        print("Not Yet Implemented", iput)
        
     

#SET UP MIDI CHANNELS TO USE

midi1 = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    midi_out=usb_midi.ports[1],
    in_channel=15,
    out_channel=9,
)
midi2 = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=10)




note = 60
velocity = 127


    
    

def drumBtnPressed(ctrlId,when):
    global drumNotesPlayed
    #notewhen = {"ctrlId":ctrlId, "when":when}
    #drumNotesPlayed.append(notewhen)
    print ("Note played from button ", ctrlId)
    
def joyStickAction(degreeV,degreeH,actioned):
    global settings 
    #settings.handleJoyStick(degreeV,degreeH,actioned)
    
                  
                   
def doNotesOff():
    global drumNotesPlayed
    global Controlz
    currTime = time.monotonic()
    #print(len(drumNotesPlayed))
    for i in range(len(drumNotesPlayed) - 1, -1, -1):
        thisEvtSrc = drumNotesPlayed[i]
        if currTime-thisEvtSrc["when"] > 0.1:
            Controlz[thisEvtSrc["ctrlId"]].noteOff()
            print ("Note off", thisEvtSrc["ctrlId"])
            del drumNotesPlayed[i]
            
 
def fxBtnPressed(id, state): #turning off all the other fx but not the one just turned on
    global fxkeys
    if gCurrMidiMode==MIDI_MODE_EXCL or gCurrMidiMode==MIDI_MODE_YOKED:
        if id in fxkeys:
            for fxkey in fxkeys:
                if fxkey!=id and state==1:
                    Controlz[fxkey].setState(0)
    if gCurrMidiMode==MIDI_MODE_YOKED and state==1:
        if id in loopkeys:
            for fxkey in fxkeys:
                Controlz[fxkey].setState(0)
            Controlz[loopFxTethers[id]].setState(1)
            
    
def footPedalPressed(id, state):
    global debugging
    if debugging: print(id,state)
    
def potMoved(id,state):
    global debugging
    if debugging: print(id,state)
    
def barsPressed(id, state):
    global debugging
    if debugging: print(id,state)
    

        
    
#reset - the toggling of volume and loop handled by midilearn
#when in non-midilearn state, just switches off all loopsand fx
#sets midi back to exclusive mode
def resetPressed(id, state):
    global gCurrMidiMode
    if gCurrMidiMode==MIDI_MODE_LEARN: return
    #turning all loops off (regardless of ending or starting song)
    for loopkey in loopkeys:
        Controlz[loopkey].setState(0)
    #turning all fx off (regardless of ending or starting song)
    for fxkey in fxkeys:
        Controlz[fxkey].setState(0)
    #going to midi mode exclusive (regardless of ending or starting song)
    Controlz[exkeys[0]].setState(MIDI_MODE_EXCL);
    # if restarting turning off the fade state
    if state==1:
        Controlz[exkeys[1]].setState(state);

    
def songChosenPressed(id, value)
    print("song chosen pressed")

def drumPadPressed(id, value):
    global debugging
    global noteBasher
    if debugging: print(id, value)
    noteBasher.noteOn(value)
    
def pagerPressed(id, value):
    global debugging
    global settings
    if debugging: print(id, value)
    if value==2:
        settings.prevItem()
    if value==4:
        settings.nextItem()
    if value==1:
        settings.decrementCurrItem()
    if value==3:
        settings.incrementCurrItem()
    if value==0:
        settings.enactState()
        
def boardStatePressed(id, state, longpress):
    print("boardStatePressed")
    global boardStates
    if longpress:
        boardStates.setState(boardCapture())
    else:
        boardStates.nextState()
        
def setAndEnactBoardState():
    currBoardState = boardCapture()
    nextBoardState = boardStates.getState()
    currBoardState.status()
    nextBoardState.status()
    if currBoardState.fx!=nextBoardState.fx:
        Controlz[nextBoardState.fx].wasPressed()
    currBoardLoops = set(currBoardState.loops)
    nextBoardLoops = set(nextBoardState.loops)
    turnOffs = currBoardLoops-nextBoardLoops
    turnOns = nextBoardLoops-currBoardLoops
    for turnOff in turnOffs:
        Controlz[turnOff].wasPressed()
    for turnOn in turnOns:
        Controlz[turnOn].wasPressed()
    
    

def boardStateUpdated(aBoardState,justNav=True):
    print("Navigation", justNav)
    print(aBoardState)
    if justNav:
        setAndEnactBoardState()
    
def boardCapture():
    #fxBtns = (map((lambda keyNum: Controlz[keyNum]), fxKeys))
    activeFx = list(filter((lambda keyNum: Controlz[keyNum].getState()!=0), fxkeys))[0]
    activeLoops = list(filter((lambda keyNum: Controlz[keyNum].getState()!=0), loopkeys))
    return BoardState(activeFx,activeLoops)

boardStates = BoardStates(boardStateUpdated)

    

keysSouth = {"Drum1":3,"Drum2":2,"Drum3":1,"Drum4":0,
             "Loop1":15,"Loop2":7,"Loop3":6,"Loop4":5,"Loop5":4,
             "Fx1":11,"Fx2":10,"Fx3":9,"Fx4":8,
             "Ex1":14,"Ex2":13,"Ex3":12}
keysWest = {"Drum1":0,"Drum2":4,"Drum3":8,"Drum4":12,
             "Loop1":3,"Loop2":1,"Loop3":5,"Loop4":9,"Loop5":13,
             "Fx1":2,"Fx2":6,"Fx3":10,"Fx4":14,
             "Ex1":7,"Ex2":11,"Ex3":15}
keysNorth = {"Drum1":12,"Drum2":13,"Drum3":14,"Drum4":15,
             "Loop1":0,"Loop2":8,"Loop3":9,"Loop4":10,"Loop5":11,
             "Fx1":4,"Fx2":5,"Fx3":6,"Fx4":7,
             "Ex1":1,"Ex2":2,"Ex3":3}
keysEast =  {"Drum1":15,"Drum2":11,"Drum3":7,"Drum4":3,
             "Loop1":12,"Loop2":13,"Loop3":9,"Loop4":5,"Loop5":1,
             "Fx1":14,"Fx2":10,"Fx3":6,"Fx4":2,
             "Ex1":8,"Ex2":4,"Ex3":0}
    
ks = keysNorth
ksInv = {v: k for k, v in ks.items()}

drumkeys = [ks["Drum1"],ks["Drum2"],ks["Drum3"],ks["Drum4"]]
loopkeys  = [ks["Loop1"],ks["Loop2"],ks["Loop3"],ks["Loop4"],ks["Loop5"]]
fxkeys = [ks["Fx1"],ks["Fx2"],ks["Fx3"],ks["Fx4"]]
exkeys = [ks["Ex1"],ks["Ex2"],ks["Ex3"]]
loopFxTethers = {ks["Loop2"]:ks["Fx1"],ks["Loop3"]:ks["Fx2"],ks["Loop4"]:ks["Fx3"],ks["Loop5"]:ks["Fx4"]}





    

print(drumkeys)

#footPedalPins = [board.GP20,board.GP21]
#analoguePins = [board.A0,board.A1]



#utility singleton classes
noteBasher = NoteBasher(midi1, 100, .1)
midiReader = MidiReader(midi1)


Controlz = {}
ct=0
gmDrums = [36,37,38,39]
for keynum in drumkeys:
    Controlz[ct]=DrumBtn(keynum, keys[keynum], midi1, [gmDrums[ct]], .2, drumPadPressed)
    ct=ct+1
    
for keynum in fxkeys:
    fxKeyStateMap = [StateMapItem("FxOn".ct-4, colz["GREEN"], 40+ct, 1 ),
                     StateMapItem("FxOff".ct-4, colz["RED"], 40+ct, 96 )]
    Controlz[ct]=LongStateBtn(40+ct, keys[keynum], midi1,fxKeyStateMap, fxBtnPressed)
    ct=ct+1
    
for keynum in loopkeys:
    loopKeyStatemap = [StateMapItem("LoopOn".ct-8, colz["GREEN"], 50+ct, 1 ),
                     StateMapItem("LoopOff".ct-8, colz["RED"], 50+ct, 96 )]
    Controlz[ct]=LongStateBtn(50+ct, keys[keynum], midi1,loopKeyStatemap, None)
    ct=ct+1

#button to either navigate between boardStates or to save a current boardState

boardStatesBtnMap = [StateMapItem("Board1", colz["RED"], None, None ),
                     StateMapItem("Board2", colz["YELLOW"], None, None ),
                     StateMapItem("Board3", colz["GREEN"], None, None )
                     StateMapItem("Board4", colz["BLUE"], None, None )]


Controlz[ct] = LongStateBtn(exkeys[0], keys[exkeys[0]], None, boardStatesBtnMap, boardStatePressed)
ct+=1
songSelectionBtnMap =  [StateMapItem("Song".i, x, None, None) for i,x in enumerate(colz.values())] 

#song selection
Controlz[ct] = StateBtn(exkeys[1], keys[exkeys[1]], None,  songSelectionBtnMap, songChosenPressed)
ct+=1
#reset button (also does volume on/off)

resetBtnMap =       [StateMapItem("Off", colz["RED"], 60, 96 ),
                     StateMapItem("Playing", colz["GREEN"], 61, 96 ),
                     StateMapItem("Fadeout", colz["YELLOW"], 60, 1 )]



Controlz[ct] = StateBtn(exkeys[2], keys[exkeys[2]], midi1, resetPressed)
    
ct+=1
    
 #
# for footPedalPin in footPedalPins:
#     Controlz[ctrlCt] = FootSwitch(midi1, ctrlCt, footPedalPin, footPedalPressed)
#     ctrlCt+=1
# 
# for aPin in analoguePins:
#     Controlz[ctrlCt] = Pot(midi1, ctrlCt, aPin, potMoved)
#     ctrlCt+=1
    
drumPad = AnKeyPad(midi1, ct, board.A2, drumPadPressed)
Controlz[ct] = drumPad
ct+=1
#pagerPad = AnKeyPad(midi1, ctrlCt, board.A1, pagerPressed)

#pagerPad.set_notches([36,64,87,110,126],[0,1,2,4,3])

joyController = JoyStick(midi1,ct, board.A1, board.A0, board.GP22, joyStickAction)
Controlz[ct] = joyController



                  



# displayio.release_displays()
# tft_cs = board.GP13
# tft_dc = board.GP12
# spi_mosi = board.GP11
# spi_clk = board.GP10
# spi = busio.SPI(spi_clk, spi_mosi)
# display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
# display = ST7789(display_bus, width=240, height=240, rowstart=80, rotation=90)
#monitor = Monitor(display)
# funcs = Functions()
# 
# settings = Settings("settings.json",funcs,monitor)








def get_voltg(raw):
    return (raw * 3.3) / 65536

while True:
    
    if not midiReader.transmissionOn:
        keybow.update()        
        for i in range(0,len(Controlz)):
                Controlz[i].check()
        noteBasher.tidyUp()
        
    midiReader.displayMidiMessage(midi1.receive())
    

    

     
        
    




        






