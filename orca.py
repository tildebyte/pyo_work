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
s = serverSetup(10, 700)
# s.shutdown()
# s.reinit()
# s.boot()
# s.start()
# OSX
# s = serverSetup(2, 'coreaudio')
metroW = Metro(time=t.whole * 4).play()
metroA = Metro(time=t.whole).play()
noteW = TrigXnoiseMidi(metroW, dist=0, mrange=(30, 41))
noteA = TrigXnoiseMidi(metroA, dist=0, mrange=(42, 83))
snapW = Snap(noteW, choice=[0, 2, 4, 5, 7, 9, 11], scale=1)
snapA = Snap(noteA, choice=[0, 2, 4, 5, 7, 9, 11], scale=1)
w = Whale(snapW, metroW, dur=t.whole, mul=dbToAmp(-9.0))
a = Aqueous(snapA, dur=t.whole * 2, mul=dbToAmp(-12.0))


def noteOn():
    a.play()

playAqueous = Pattern(function=noteOn, time=t.whole * 2).play()
delayW = Delay(w, delay=t.whole, feedback=0.64,
               maxdelay=t.whole, mul=dbToAmp(-6.0))
wetdry = delayW + w + a
volume = wetdry * 1.0
volume.setMul(dbToAmp(-3.0))
rev = STRev(wetdry, revtime=2, bal=dbToAmp(-7.95), roomSize=1.4).out()
s.gui(locals())
