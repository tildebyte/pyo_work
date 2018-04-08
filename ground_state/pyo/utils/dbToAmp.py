# encoding: utf-8

# This is a utilty function for pyo <http://code.google.com/p/pyo> which
# calculates linear amplitiude from log10 dbFS. Latest version available from
# <http://gist.github.com/tildebyte>.
# Copyright (C) 2013  Ben Alkov <ground_state@quaestor.us>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version <http://www.gnu.org/licenses/>.

# dbToAmp 1.0
import math


def dbToAmp(db):
    return math.pow(10, 0.05*db)

# amps to dB: log(dB) / 0.05
