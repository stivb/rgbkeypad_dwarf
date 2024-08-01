from dwarfmidiutils.longstatebtn import LongStateBtn
from dwarfmidiutils.drumbtn import DrumBtn
from dwarfmidiutils.notebasher import NoteBasher

from dwarfmidiutils.midireader import MidiReader
from dwarfmidiutils.song import Song

from dwarfmidiutils.statemap import *

import board

from adafruit_datetime import datetime

import time
from pmk import PMK

from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware  

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
# from adafruit_midi.control_change import ControlChange
# from adafruit_midi.program_change import ProgramChange

from collections import OrderedDict

keybow = PMK(Hardware())
keys = keybow.keys



drumMidiOffset = 0

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

midi1 = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    midi_out=usb_midi.ports[1],
    in_channel=0,
    out_channel=9,
)

song = Song(midi1, 100)

def fxBtnPressed(id, state, lp): 
    global fxkeys,ks

    for fxkey in fxkeys:
        if fxkey!=id and state==1:
            Controlz[fxkey].setState(0)

def resetCued(id, newState, lp):
    global song
    song.stop()

def resetPressed(id, newState, lp):
    global resetBtnMap
    global drumMidiOffset
    global song
    if newState==0:    
        for loopkey in loopkeys:
            Controlz[loopkey].setState(0)

        for fxkey in fxkeys:
            Controlz[fxkey].setState(0)

        midi1.send(ControlChange(61,96))
        Controlz[exkeys[0]].setState(0)
        drumMidiOffset=0
        song.stop()

def drumPadPressed(id, value):
    global noteBasher
    global drumMidiOffset
    noteBasher.noteOn(value + drumMidiOffset)

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
#ksInv = {v: k for k, v in ks.items()}

drumkeys = [ks["Drum1"],ks["Drum2"],ks["Drum3"],ks["Drum4"]]
loopkeys  = [ks["Loop1"],ks["Loop2"],ks["Loop3"],ks["Loop4"],ks["Loop5"],ks["Loop6"]]
fxkeys = [ks["Fx1"],ks["Fx2"],ks["Fx3"],ks["Fx4"]]
exkeys = [ks["Ex1"],ks["Ex2"]]

Controlz = {}
ct=0
gmDrums = [36,37,38,39]
for keynum in drumkeys:
    Controlz[keynum]=DrumBtn(keynum, keys[keynum], midi1, gmDrums[ct], .2, drumPadPressed)
    ct=ct+1

for keynum in fxkeys:
    fxKeyStateMap = StateMap([
                             StateMapItem("FxOff", colz["CYAN"], (ct+36), 1 ),
                             StateMapItem("FxOn", colz["BLUE"], (ct+36), 96 )
                             ]
                             )
    Controlz[keynum]=LongStateBtn(keynum, keys[keynum], midi1,fxKeyStateMap, None, fxBtnPressed)
    ct=ct+1

for keynum in loopkeys:
    loopKeyStateMap = StateMap([
                               StateMapItem("LoopOn", colz["PINK"], (ct+42), 1 ),
                               StateMapItem("LoopOff", colz["RED"], (ct+42), 96)
                               ])
    Controlz[keynum]=LongStateBtn(keynum, keys[keynum], midi1,loopKeyStateMap, None, None)
    ct=ct+1

songStateMap = StateMap(
                            [StateMapItem("Board1", colz["WHITE"], None, None),
                             StateMapItem("Board2", colz["RED"], None, None)
                             ]
                            )

def songPressed(id, state, longpress):
    # this short press should cause #127 noteOn
    # and a cc #127 high
    # the fadeout should do #127 noteOff
    # and a cc #127 low
    global resetBtnMap
    global drumMidiOffset
    print("_________________")
    print(resetBtnMap.currCol)
    
    if song.on:
        song.stop()
        drumMidiOffset=0
    else:
        song.start()
        drumMidiOffset=4
        


# nId, btn, adaMidi,stateMap, preCmdCallBack, postCmdCallBack):
Controlz[exkeys[0]] = LongStateBtn(exkeys[0], keys[exkeys[0]], None, songStateMap, None, songPressed)

resetBtnMap =        StateMap([StateMapItem("Off", colz["WHITE"], 60, 1 ),
                     StateMapItem("Playing", colz["GREEN"], 60, 96 ),
                     StateMapItem("Fadeout", colz["YELLOW"], 61, 1 )])

Controlz[exkeys[1]] = LongStateBtn(exkeys[1], keys[exkeys[1]], midi1, resetBtnMap, resetCued, resetPressed)

noteBasher = NoteBasher(midi1, 100, .1)

while True:

    keybow.update()        
    for ctrl in Controlz:
        Controlz[ctrl].check()
    noteBasher.tidyUp()



