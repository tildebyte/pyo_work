#!/usr/bin/env python
# encoding: utf-8

# Test script for the Aqueous "instrument" for pyo
# <http://code.google.com/p/pyo>.
# Latest version always available at <http://gist.github.com/tildebyte>.
# Copyright (C) 2014  Ben Alkov <ground_state@quaestor.us>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version <http://www.gnu.org/licenses/>.
from pyo import Delay, Snap, Metro, TrigXnoiseMidi, WGVerb

from ground_state.pyo.instruments.Aqueous import Aqueous
from ground_state.pyo.utils.Tempo import Tempo
from ground_state.pyo.utils.dbToAmp import dbToAmp
from ground_state.pyo.utils.serverSetup import serverSetup


t = Tempo(63.5)

# Windows
s = serverSetup(6, dbToAmp(-12))

# OSX
# s = serverSetup(2, dbToAmp(0))


metro = Metro(time=t.whole * 2).play()
note = TrigXnoiseMidi(metro, dist=0, mrange=(30, 77))
snap = Snap(note, choice=[0, 2, 4, 5, 7, 9, 11], scale=1)

a = Aqueous(snap, metro, t.quarter * 3)

delay = Delay(a, delay=t.quarter * 3, feedback=0.6,
              maxdelay=t.quarter * 3, mul=dbToAmp(-7))

wetdry = delay + a

d = WGVerb(wetdry, feedback=[0.73, 0.76], cutoff=5000,
           bal=dbToAmp(-12.04), mul=dbToAmp(-10.5)).out()

s.gui(locals())
