# encoding: utf-8

# This is a utilty class for pyo <http://code.google.com/p/pyo>, representing
# musical tempo and derived note values. Latest version available from
# <http://gist.github.com/tildebyte>.
# Copyright (C) 2013  Ben Alkov <ground_state@quaestor.us>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version <http://www.gnu.org/licenses/>.


class Tempo(object):
    """
    Tempo 1.0
    A simple container for note duration values.
    """

    def __init__(self, bpm):
        self.spb = 60.0 / bpm
        self.quarter = self.spb
        self.eighth = self.quarter / 2.0
        self.six10th = self.eighth / 2.0
        self.thirty2nd = self.six10th / 2.0
        self.sixty4th = self.thirty2nd / 2.0
        self.one28th = self.sixty4th / 2.0
        self.whole = self.quarter * 4.0
        self.minim = self.quarter * 2.0
        self.__float__ = 0.0

    def setTempo(self, bpm):
        # bpm is BPM, example 120 beats per minute.
        self.spb = 60.0 / bpm  # seconds per beat.
