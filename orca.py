#!/usr/bin/env python3
# encoding: utf-8

# <http://code.google.com/p/pyo>.
# Latest version always available at <http://gist.github.com/tildebyte>.
# Copyright (C) 2014  Ben Alkov <ground_state@quaestor.us>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version <http://www.gnu.org/licenses/>.
from pyo import Delay, Metro, Pattern, Snap, STRev, TrigXnoiseMidi

# iPython: %cd \path\to\pyo\files
from ground_state.pyo.instruments.aqueous import Aqueous
from ground_state.pyo.instruments.whale import Whale
from ground_state.pyo.utils.tempo import Tempo
from ground_state.pyo.utils.dbToAmp import dbToAmp
from ground_state.pyo.utils.serverSetup import serverSetup


t = Tempo(63.5)  # q=944ms, w=3.776s
# Windows
# server = serverSetup(10, 700)
# OSX
server = serverSetup(2, 192, 'coreaudio')
metroWhale = Metro(time=t.whole * 4).play()
metroAqueous = Metro(time=t.whole).play()
noteWhale = TrigXnoiseMidi(metroWhale, dist=0, mrange=(30, 41))
noteAqeous = TrigXnoiseMidi(metroAqueous, dist=0, mrange=(42, 83))
snapWhale = Snap(noteWhale, choice=[0, 2, 4, 5, 7, 9, 11], scale=1)
snapAqueous = Snap(noteAqeous, choice=[0, 2, 4, 5, 7, 9, 11], scale=1)
whale = Whale(snapWhale, metroWhale, dur=t.whole, mul=dbToAmp(-9.0))
aqueous = Aqueous(snapAqueous, dur=t.whole * 2, mul=dbToAmp(-12.0))


def noteOn():
    aqueous.play()

playAqueous = Pattern(function=noteOn, time=t.whole * 2).play()
delayWhale = Delay(whale, delay=t.whole, feedback=0.64,
               maxdelay=t.whole, mul=dbToAmp(-6.0))
wetdry = delayWhale + whale + aqueous
volume = wetdry * 1.0
volume.setMul(dbToAmp(-3.0))
reverb = STRev(wetdry, revtime=2, bal=dbToAmp(-7.95), roomSize=1.4).out()
server.gui(locals())
