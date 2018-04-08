#!/usr/bin/env python3
# encoding: utf-8

# Test script for the Whale "instrument" for pyo
# <http://code.google.com/p/pyo>.
# Latest version always available at <http://gist.github.com/tildebyte>.
# Copyright (C) 2014  Ben Alkov <ground_state@quaestor.us>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version <http://www.gnu.org/licenses/>.
from pyo import Delay, Snap, Metro, TrigXnoiseMidi, WGVerb

from ground_state.pyo.instruments.whale import Whale
from ground_state.pyo.utils.tempo import Tempo
from ground_state.pyo.utils.dbToAmp import dbToAmp
from ground_state.pyo.utils.serverSetup import serverSetup


t = Tempo(63.5)
# OSX
s = serverSetup(2, 192, 'coreaudio')

metro = Metro(time=t.whole * 4).play()
note = TrigXnoiseMidi(metro, dist=0, mrange=(30, 41))
snap = Snap(note, choice=[0, 2, 4, 5, 7, 9, 11], scale=1)
w = Whale(snap, metro, dur=t.whole, mul=0.9)
delay = Delay(w, delay=t.whole, feedback=0.64,
              maxdelay=t.whole, mul=dbToAmp(-6))
wetdry = delay + w
d = WGVerb(wetdry, feedback=[0.73, 0.76], cutoff=5000,
           bal=dbToAmp(-12.04), mul=dbToAmp(-10.5)).out()
s.gui(locals())
