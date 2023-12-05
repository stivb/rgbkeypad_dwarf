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
from dwarfmidiutils.boardstates import BoardStates
from dwarfmidiutils.statemap import *
from dwarfmidiutils.pinswitch import PinSwitch

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

from collections import OrderedDict



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

colz = OrderedDict()
colz["BLACK"] = (0,0,0)
colz["RED"] = (255,0,0)
colz["GREEN"]=(0,255,0)
colz["BLUE"]=(0,0,255)
colz["CYAN"]=(0,255,255)
colz["VIOLET"]=(255,0,255)
colz["YELLOW"]=(255,255,0)
colz["ORANGE"]=(255,70,0)
colz["GRAY"]=(30,30,30)
colz["PINK"]=(255,128,128)
colz["WHITE"]=(255,255,255)


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
            
 
def fxBtnPressed(id, state, lp): #turning off all the other fx but not the one just turned on
    global fxkeys,ks
    print(id, "is id of button just pressed in state ", state," with long press? ", lp, "with the other keys being ", fxkeys)
    for fxkey in fxkeys:
        print("currently the fxkey ", fxkey," has the state ",Controlz[fxkey].getState())
        if fxkey!=id and state==1:
            Controlz[fxkey].setState(0)

def pinPressed(id):
    global boardStates
    pinValDict = {19:1,18:2,17:3,16:0}
    goto = pinValDict[id]
    boardStates.gotoState(goto)
    
    
def footPedalPressed(id, state):
    global debugging
    if debugging: print(id,state)
    
def potMoved(id,state):
    global debugging
    if debugging: print(id,state)
    
def barsPressed(id, state):
    global debugging
    if debugging: print(id,state)
    

def notificationMade(numbers):
    print("THERE ARE ", len(numbers), "STATES IN THIS SONG ")
    for x in numbers:
        boardStates.setStates(num2binIndexes(x))

    
def num2binIndexes(num):
    #converting to binary and removing the first two "0b" characters
    global loopkeys
    q= list(bin(num)[2:])
    #if not six characters long, adding in zeros
    while (len(q)<6): q.insert(0, '0')
    #converting to array of numbers from string
    onoffs = [eval(i) for i in q]
    #just getting the ones which are on
    onsIndexes =  [i for i in range(len(onoffs)) if onoffs[i] > 0]
    #mapping them to the actual keys
    return [loopkeys[i] for i in onsIndexes]
    
    
#reset - the toggling of volume and loop handled by midilearn
#when in non-midilearn state, just switches off all loopsand fx
#sets midi back to exclusive mode
def resetCued(id, newState, lp):
    if newState==0:
        midiReader.reset()

def resetPressed(id, newState, lp):
    global resetBtnMap
    if newState==0:    
        for loopkey in loopkeys:
            Controlz[loopkey].setState(0)
        #turning all fx off (regardless of ending or starting song)
        for fxkey in fxkeys:
            Controlz[fxkey].setState(0)
    #hack here, just turning the fader off
        midi1.send(ControlChange(61,96))

        


    
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
    currBoardLoops = set(currBoardState)
    nextBoardLoops = set(nextBoardState)
    turnOffs = currBoardLoops-nextBoardLoops
    turnOns = nextBoardLoops-currBoardLoops
    
    print ("currBoardState ", currBoardState)
    print ("nextBoardState ", nextBoardState)
    
    for turnOff in turnOffs:
        Controlz[turnOff].press(False)
    for turnOn in turnOns:
        Controlz[turnOn].press(False)
    
    

def boardStateUpdated(aBoardState,enact=True):
    print("Navigation", justNav)
    print(aBoardState)
    if enact:
        setAndEnactBoardState()
        
def songSelectionPressed(id, state, longpress):
    print("Song chosen")
    
def boardCapture():
    global loopKeys
    activeLoops = list(filter((lambda keyNum: Controlz[keyNum].getState()!=0), loopkeys))
    return activeLoops

boardStates = BoardStates(boardStateUpdated)

#really need some documentation about why these numbers correspond to the buttons  

keysSouth = {"Drum1":3,"Drum2":2,"Drum3":1,"Drum4":0,
             "Loop1":15,"Loop2":14,"Loop3":7,"Loop4":6,"Loop5":5,"Loop6":4,
             "Fx1":11,"Fx2":10,"Fx3":9,"Fx4":8,
             "Ex1":13,"Ex2":12}
keysWest = {"Drum1":0,"Drum2":4,"Drum3":8,"Drum4":12,
             "Loop1":3,"Loop2":7,"Loop3":1,"Loop4":5,"Loop5":9,"Loop6":13,
             "Fx1":2,"Fx2":6,"Fx3":10,"Fx4":14,
             "Ex1":11,"Ex2":15}
keysNorth = {"Drum1":12,"Drum2":13,"Drum3":14,"Drum4":15,
             "Loop1":0,"Loop2":1,"Loop3":8,"Loop4":9,"Loop5":10,"Loop6":11,
             "Fx1":4,"Fx2":5,"Fx3":6,"Fx4":7,
             "Ex1":2,"Ex2":3}
keysEast =  {"Drum1":15,"Drum2":11,"Drum3":7,"Drum4":3,
             "Loop1":12,"Loop2":8,"Loop3":13,"Loop4":9,"Loop5":5,"Loop6":1,
             "Fx1":14,"Fx2":10,"Fx3":6,"Fx4":2,
             "Ex1":4,"Ex2":0}
    
ks = keysSouth
ksInv = {v: k for k, v in ks.items()}

drumkeys = [ks["Drum1"],ks["Drum2"],ks["Drum3"],ks["Drum4"]]
loopkeys  = [ks["Loop1"],ks["Loop2"],ks["Loop3"],ks["Loop4"],ks["Loop5"],ks["Loop6"]]
fxkeys = [ks["Fx1"],ks["Fx2"],ks["Fx3"],ks["Fx4"]]
exkeys = [ks["Ex1"],ks["Ex2"]]
loopFxTethers = {ks["Loop2"]:ks["Fx1"],ks["Loop3"]:ks["Fx2"],ks["Loop4"]:ks["Fx3"],ks["Loop5"]:ks["Fx4"]}


print ("loop keys ", loopkeys, " fx keys:", fxkeys)

#footPedalPins = [board.GP20,board.GP21]
#analoguePins = [board.A0,board.A1]

#utility singleton classes
noteBasher = NoteBasher(midi1, 100, .1)
midiReader = MidiReader(midi1, notificationMade)


Controlz = {}
ct=0
gmDrums = [36,37,38,39]
for keynum in drumkeys:
    Controlz[keynum]=DrumBtn(keynum, keys[keynum], midi1, gmDrums[ct], .2, drumPadPressed)
    ct=ct+1
    
for keynum in fxkeys:
    fxKeyStateMap = StateMap([
                             StateMapItem("FxOff", colz["CYAN"], (ct+40-4), 1 ),
                             StateMapItem("FxOn", colz["BLUE"], (ct+40-4), 96 )
                             ]
                             )
    Controlz[keynum]=LongStateBtn(keynum, keys[keynum], midi1,fxKeyStateMap, None, fxBtnPressed)
    ct=ct+1
    print(keynum)
    
for keynum in loopkeys:
    loopKeyStateMap = StateMap([
                               StateMapItem("LoopOn", colz["PINK"], (ct+50-8), 1 ),
                               StateMapItem("LoopOff", colz["RED"], (ct+50-8), 96)
                               ])
    Controlz[keynum]=LongStateBtn(keynum, keys[keynum], midi1,loopKeyStateMap, None, None)
    ct=ct+1
    print(keynum)

#button to either navigate between boardStates or to save a current boardState

boardStatesBtnMap = StateMap(
                            [StateMapItem("Board1", colz["BLACK"], None, None),
                             StateMapItem("Board2", colz["RED"], None, None),
                             StateMapItem("Board3", colz["YELLOW"], None, None),
                             StateMapItem("Board4", colz["GREEN"], None, None)
                             ]
                            )

# boardStates.setState(BoardState(ks["Fx4"],[ks["Loop1"],ks["Loop2"],ks["Loop3"],ks["Loop4"],ks["Loop5"]]));
# boardStates.setState(BoardState(ks["Fx4"],[ks["Loop1"],ks["Loop2"]]));
# boardStates.setState(BoardState(ks["Fx4"],[ks["Loop1"],ks["Loop2"],ks["Loop3"]]));
# boardStates.setState(BoardState(ks["Fx4"],[ks["Loop1"],ks["Loop2"],ks["Loop3"],ks["Loop4"]]));

notificationMade([47,40,44,46])
boardStates.status()




Controlz[exkeys[0]] = LongStateBtn(exkeys[0], keys[exkeys[0]], None, boardStatesBtnMap, None, boardStatePressed)

songSelectionBtnMap =  StateMap([StateMapItem("Song", x, None, None) for i,x in enumerate(list(colz.values()))])


resetBtnMap =        StateMap([StateMapItem("Off", colz["WHITE"], 60, 1 ),
                     StateMapItem("Playing", colz["GREEN"], 60, 96 ),
                     StateMapItem("Fadeout", colz["YELLOW"], 61, 1 )])


#reset cued created in order to turn on the midi listener just before the trigger command send to pedal board
Controlz[exkeys[1]] = LongStateBtn(exkeys[1], keys[exkeys[1]], midi1, resetBtnMap, resetCued, resetPressed)
    
    
 #
# for footPedalPin in footPedalPins:
#     Controlz[ctrlCt] = FootSwitch(midi1, ctrlCt, footPedalPin, footPedalPressed)
#     ctrlCt+=1
# 
# for aPin in analoguePins:
#     Controlz[ctrlCt] = Pot(midi1, ctrlCt, aPin, potMoved)
#     ctrlCt+=1

ct=16
pinz = [board.GP2, board.GP3, board.GP6, board.GP7]
for pin in pinz:
    Controlz[ct] = PinSwitch(ct,pin,pinPressed)
    ct=ct+1



    
drumPad = AnKeyPad(midi1, ct, board.A2, drumPadPressed)
Controlz[ct] = drumPad
ct+=1
#pagerPad = AnKeyPad(midi1, ctrlCt, board.A1, pagerPressed)

#pagerPad.set_notches([36,64,87,110,126],[0,1,2,4,3])

joyController = JoyStick(midi1,ct, board.A1, board.A0, board.GP22, joyStickAction)
Controlz[ct] = joyController

displayio.release_displays()
tft_cs = board.GP13
tft_dc = board.GP12
spi_mosi = board.GP11
spi_clk = board.GP10
spi = busio.SPI(spi_clk, spi_mosi)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(display_bus, width=240, height=240, rowstart=80, rotation=90)
monitor = Monitor(display)
funcs = Functions()

settings = Settings("keypadsettings.json",funcs,monitor)


def get_voltg(raw):
    return (raw * 3.3) / 65536

while True:
    

    keybow.update()        
    for i in range(0,len(Controlz)):
            Controlz[i].check()
    noteBasher.tidyUp()
        
    if midiReader.on:
        midiReader.read(midi1.receive())
    

    

     
        
    




        