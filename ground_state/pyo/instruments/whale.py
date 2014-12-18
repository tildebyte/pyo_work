#!/usr/bin/env python
# encoding: utf-8

# This is an "instrument" for pyo <http://code.google.com/p/pyo>.
# Latest version always available at <http://gist.github.com/tildebyte>.
# Copyright (C) 2013  Ben Alkov <ground_state@quaestor.us>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version <http://www.gnu.org/licenses/>.

from pyo import PyoObject, CosTable, EQ, Osc
from pyo import Sine, TrigEnv, convertArgsToLists
# For test
# from pyo import Delay, Metro, Pan, Reverb, Server, Snap, TrigXnoiseMidi
from ground_state.pyo.generators import TriTable


class Whale(PyoObject):
    """
    Whale 1.0

    Signal chain:
    lfo -> lfoEnv -> triOsc -> triEnv -> out

    The concept is that of a low-frequency instrument which has a
    delayed-onset vibrato. It is meant to be used at low tempos, to allow
    the vibrato to fade in slowly.

    :Parent: :py:class:`PyoObject`

    :Args:

        freq : PyoObject
            Frequency to generate.
        trig : PyoObject
            A trigger to drive note-ons.
        dur : float
            Time in seconds for the instrument to play once triggered.

    """
    def __init__(self, freq=1000, trig=PyoObject, dur=3.78, mul=1):
        PyoObject.__init__(self, mul)
        self._freq = freq
        self._trig = trig
        self._dur = dur
        self._mul = mul

        freq, trig, dur, mul, lmax = convertArgsToLists(freq, trig, dur, mul)

        # LFO signal chain.
        # This envelope drives the LFO which creates the vibrato effect. Its
        # volume stays very low until just before it ends.
        lfoEnvTable = CosTable([(0, 0.0), (2457, 0.0), (6481, 0.3),
                                (7350, 0.0), (8191, 0.0)])
        # lfoEnvTable.graph()
        self._lfoEnv = TrigEnv(self._trig, lfoEnvTable, dur=self._dur)
        self._lfo = Sine(4.27, mul=self._lfoEnv)

        # Triangle oscillator signal chain.
        triEnvTable = CosTable([(0, 0.0), (1535, 1.0), (2046, 0.95),
                                (6143, 0.95), (8191, 0.0)])
        # triEnvTable.graph()
        self._triEnv = TrigEnv(self._trig, triEnvTable, dur=self._dur)
        # TriTable Table oscillator from the pyo docs.
        triTable = TriTable(order=50, size=24000).normalize()
        self._osc = Osc(triTable, self._freq, interp=4,
                        mul=((self._triEnv + self._lfo) * self._mul))

        self._whale = EQ(self._osc, freq=self._freq * 16, q=1, type=1)

        self._base_objs = self._whale.getBaseObjects()

    def setFreq(self, x):
        """
        Replace the `freq` attribute.

        :Args:

            x : float or PyoObject
                New `freq` attribute.

        """
        self._freq = x

    def setTrig(self, x):
        """
        Replace the `trig` attribute.

        :Args:

            x : PyoObject
                New `trig` attribute.

        """
        self._trig = x
        self._lfoEnv.trig = x
        self._triEnv.trig = x

    def setDur(self, x):
        """
        Replace the `dur` attribute.

        :Args:

            x : PyoObject
                New `dur` attribute.

        """
        self._dur = x
        self._lfoEnv.dur = x
        self._triEnv.dur = x

    @property
    def freq(self):
        """float or PyoObject. Frequency."""
        return self._freq

    @freq.setter
    def freq(self, x):
        self.setFreq(x)

    @property
    def trig(self):
        """PyoObject. Trigger the instrument."""
        return self._trig

    @trig.setter
    def trig(self, x):
        self.setTrig(x)

    @property
    def dur(self):
        """float. Duration in seconds."""
        return self._dur

    @dur.setter
    def dur(self, x):
        self.setDur(x)

    # This doesn't work (causes the LFO to stop working, reason unknown).
    # Hmm...
    # def ctrl(self, map_list=None, title=None, wxnoserver=False):
    #     self._map_list = [SLMapMul(self._mul)]
    #     PyoObject.ctrl(self, map_list, title, wxnoserver)

    def play(self, dur=0, delay=0):
        self._lfoEnv.play(dur, delay)
        self._lfo.play(dur, delay)
        self._triEnv.play(dur, delay)
        self._osc.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self):
        self._lfoEnv.stop()
        self._lfo.stop()
        self._triEnv.stop()
        self._osc.stop()
        return PyoObject.stop(self)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self._lfoEnv.out(dur, delay)
        self._lfo.out(dur, delay)
        self._triEnv.out(dur, delay)
        self._osc.out(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)

# Run this script to test the Whale object.
# Broken. We don't have access to the TriTable object from here
# if __name__ == "__main__":
#     s = Server(duplex=0).boot()
#     t = 3.78
#     metro = Metro(time=t).play()
#     note = TrigXnoiseMidi(metro, dist=0, mrange=(16, 40))
#     snap = Snap(note, choice=[0, 2, 4, 5, 7, 9, 11], scale=1)
#     w = Whale(snap, metro, t)
#     delay = Delay(a, delay=t, feedback=0.6, maxdelay=t, mul=0.5957)
#     rev = Freeverb(delay + w, size=0.83, damp=0.5, bal=0.5708, mul=0.5821)
#     pan = Pan(rev).out()
#     s.gui(locals())
