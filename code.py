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
from dwarfmidiutils.drumbtn import DrumBtn
from dwarfmidiutils.notebasher import NoteBasher
from dwarfmidiutils.pot import Pot
from dwarfmidiutils.footswitch import FootSwitch
from dwarfmidiutils.ankeypad import AnKeyPad
from dwarfmidiutils.joystick import JoyStick
from dwarfmidiutils.midireader import MidiReader
from dwarfmidiutils.monitor import Monitor
from dwarfmidiutils.settings import Settings

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
            
 
def stateBtnPressed(id, state): #turning off all the other fx but not the one just turned on
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
    
def midiModePressed(id, state):
    global gCurrMidiMode
    print("Midi Mode Pressed")
    gCurrMidiMode=state
    print(id,state)
    
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

def soundFadePressed(id, state):
    global debugging
    if debugging: print("Sound Fade Pressed")
    
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
        
    
#EAST NORTH FOR ACOUSTIC GUITAR
currUsbRelToHand = SOUTH
#EDIT THESE DEPENDING ON ORIENTATION   
    


if currUsbRelToHand==SOUTH:
    drumkeys = [3,2,1,0]
    loopkeys  = [15,7,6,5,4]
    fxkeys = [11,10,9,8]
    exkeys = [14,13,12] 
    loopFxTethers = {7:11,6:10,5:9,4:8}
    
if currUsbRelToHand==WEST:
    drumkeys = [0,4,8,12]
    loopkeys  = [3,1,5,9,13]
    fxkeys = [2,6,10,14]
    exkeys = [7,11,15] 
    loopFxTethers = {1:2,5:6,9:10,13:14}
    
if currUsbRelToHand==NORTH:
    drumkeys = [12,13,14,15]
    loopkeys  = [0,8,9,10,11]
    fxkeys = [4,5,6,7]
    exkeys = [1,2,3] 
    loopFxTethers = {8:4,9:5,10:6,11:7}
    
if currUsbRelToHand==EAST:
    drumkeys = [15,11,7,3]
    loopkeys  = [12,13,9,5,1]
    fxkeys = [14,10,6,2]
    exkeys = [8,4,0] 
    loopFxTethers = {13:14,9:10,5:6,1:2}

    

print(drumkeys)
print(currUsbRelToHand)

#footPedalPins = [board.GP20,board.GP21]
#analoguePins = [board.A0,board.A1]

gmDrums = [36,37,38,39]

#utility singleton classes
noteBasher = NoteBasher(midi1, 100, .1)
midiReader = MidiReader(midi1)


Controlz = {}
ct=0
for keynum in drumkeys:
    Controlz[keynum]=DrumBtn(keynum, keys[keynum], midi1, gmDrums[ct], .2, drumPadPressed)
    ct=ct+1
    
for keynum in fxkeys:
    Controlz[keynum]=StateBtn(keynum, keys[keynum], midi1,stateBtnPressed,[0,0],[(128,128,128),(255,0,0)])
    ct=ct+1
    
for keynum in loopkeys:
    Controlz[keynum]=StateBtn(keynum, keys[keynum], midi1, stateBtnPressed,[0,0],[(0,0,255),(255,0,0)])
    ct=ct+1
    

    
ctrlCt=16  #
# for footPedalPin in footPedalPins:
#     Controlz[ctrlCt] = FootSwitch(midi1, ctrlCt, footPedalPin, footPedalPressed)
#     ctrlCt+=1
# 
# for aPin in analoguePins:
#     Controlz[ctrlCt] = Pot(midi1, ctrlCt, aPin, potMoved)
#     ctrlCt+=1
    
drumPad = AnKeyPad(midi1, ctrlCt, board.A2, drumPadPressed)
#pagerPad = AnKeyPad(midi1, ctrlCt, board.A1, pagerPressed)

#pagerPad.set_notches([36,64,87,110,126],[0,1,2,4,3])

joyController = JoyStick(midi1,ctrlCt+1, board.A1, board.A0, board.GP22, joyStickAction)

Controlz[ctrlCt] = drumPad
Controlz[ctrlCt+1] = joyController
#Controlz[ctrlCt+1] = pagerPad


                  



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


# bars button
rgbs = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(255,255,255)]
cmdVals = [4,12,28,60,96,127]
states=[0,1,2,3,4,5]
currKey=exkeys[0]
#Controlz[currKey] = StateBtn(currKey, keys[currKey], midi1, barsPressed, states, rgbs, cmdVals)

#midi mode button
#def __init__(self, nId, btn, midi, callback=None, states=None, colors=None, cmdVals=None, ctrlChangeChn=None):
#currKey=exkeys[1]

#three midi modes - exclusive (only one fx at a time), yoked (as before, but turning on loop turns on corresponding fx)
# and learn - when just getting the pedalboard to follow the commands
MidiModeColors = [(255,255,0),(255,0,0),(0,0,255)]
Controlz[exkeys[0]] = StateBtn(currKey, keys[exkeys[0]], None, midiModePressed, [0,1,2], MidiModeColors)

#volume off button
currKey=exkeys[1]
Controlz[exkeys[1]] = StateBtn(currKey, keys[exkeys[1]], midi1, soundFadePressed)

#reset button (also does volume on/off)
currKey=exkeys[2]
Controlz[exkeys[2]] = StateBtn(currKey, keys[exkeys[2]], midi1, resetPressed)



def get_voltg(raw):
    return (raw * 3.3) / 65536

while True:
    
    if not midiReader.transmissionOn:
        keybow.update()        
        for i in range(0,len(Controlz)):
                Controlz[i].check()
        noteBasher.tidyUp()
        
    midiReader.displayMidiMessage(midi1.receive())
    

    

     
        
    




        






