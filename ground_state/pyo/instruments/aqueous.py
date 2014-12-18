#!/usr/bin/env python
# encoding: utf-8

# This is an "instrument" for pyo <http://code.google.com/p/pyo>.
# Latest version always available at <http://gist.github.com/tildebyte>.
# Copyright (C) 2014  Ben Alkov <ground_state@quaestor.us>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version <http://www.gnu.org/licenses/>.

from pyo import PyoObject, Adsr, ButBP, EQ, Mix, Osc, SawTable
# For test
# from pyo import Delay, Metro, Server, Snap, TrigXnoiseMidi, WGVerb


class Aqueous(PyoObject):
    """
    Aqueous 1.0

    This instrument is (loosely) based on a favorite patch from the Analog
    synthesizer device in Ableton Live. Doesn't really sound like the
    original at all, but I like it... Meant for a MIDI range of 30-77.

    Signal chain:
    saw1 -> reson1 -> resonEnv -> ampEnv -> filter -> out
    |________                      ^
            |                      |
    saw2 -> reson2 -> resonEnv --->|

    We have four independent envelopes (reson1Env, reson2Env, amp1Env,
    amp2Env) with slightly different sustain levels/timing. The envelopes are
    the most complex aspect of this instrument. I don't entirely understand
    what goes on here (design by tweak).

    :Parent: :py:class:`PyoObject`

    :Args:

        freq : PyoObject
            Frequency to generate.
        dur : float
            Time in seconds for the instrument to play once triggered.

    """
    def __init__(self, freq=1000, dur=1, mul=1, add=0):
        self._freq = freq
        self._dur = dur
        self._mul = mul
        self._add = add

        # Begin processing.

        # 1st Saw oscillator.
        saw1Table = SawTable(order=50, size=24000).normalize()
        self._saw1 = Osc(saw1Table, self._freq, interp=4, mul=0.6839)
        # Dummy amplitude knobs to split Saw 1 into two paths with independent
        # amplitudes.
        # Out to Reson1.
        saw1Dummy1 = self._saw1 * 1.0
        saw1Dummy1.setMul(0.63)
        # Out to Reson2.
        saw1Dummy2 = self._saw1 * 1.0
        saw1Dummy2.setMul(0.38)

        # 1st Resonant filter.
        # total duration =  note value + 1954ms
        # sustain at 95%
        self._reson1Env = Adsr(1.280, 0.097, 0.95, 0.577, dur=self._dur)
        reson1 = EQ(saw1Dummy1, freq=self._freq, q=100, boost=3.0, type=1,
                    mul=self._reson1Env * 0.7079)
        # Dummy amplitude knob; lets us more easily balance the filter levels.
        reson1Dummy = reson1 * 1.0

        # 2nd Saw oscillator.
        saw2Table = SawTable(order=50, size=24000).normalize()
        self._saw2 = Osc(saw2Table, self._freq / 2, interp=4, mul=0.5433)
        # Dummy amplitude knob to allow mixing with Saw1, going into Reson2.
        saw2Dummy = self._saw2 * 1.0
        saw2Dummy.setMul(0.38)

        # 2nd Resonant filter.
        # total duration =  note value + 1954ms
        # sustain at 53%
        self._reson2Env = Adsr(1.280, 0.097, 0.53, 0.577, dur=self._dur)
        reson2 = EQ(saw1Dummy2 + saw2Dummy, freq=self._freq + 1300, q=100,
                    boost=3.0, type=1, mul=self._reson2Env * 0.7079)
        # Dummy amplitude knob; lets us more easily balance the filter levels.
        reson2Dummy = reson2 * 1.0

        # Amplitude envelopes for the filters.
        # total duration =  note value + 1954ms
        # sustain at %100
        self._amp1Env = Adsr(0.577, 0.097, 1.0, 1.280, dur=self._dur)
        # total duration =  note value + 1862ms
        # sustain at %100
        self._amp2Env = Adsr(0.577, 0.005, 1.0, 1.280, dur=self._dur)

        # Tweak filter levels
        reson1Dummy.setMul(self._amp1Env * 0.3)
        reson2Dummy.setMul(self._amp2Env * 0.4842)

        filtersDummy = reson1Dummy + reson2Dummy

        bpf = ButBP(filtersDummy, freq=325, q=1)

        # Volume knob
        aqueous = Mix(bpf, mul=self._mul)

        self._base_objs = aqueous.getBaseObjects()

    def setFreq(self, x):
        """
        Replace the `freq` attribute.

        :Args:

            x : float or PyoObject
                New `freq` attribute.

        """
        self._freq = x
        self._saw1.freq = x
        self._saw2.freq = x

    @property
    def freq(self):
        """float or PyoObject. Frequency."""
        return self._freq

    @freq.setter
    def freq(self, x):
        self.setFreq(x)

    def __dir__(self):
        return ["freq", "mul", "add"]

    # Works, but not particularly useful. It would be nice to show sliders
    # for some of the muls e.g. the two oscillators...
    # def ctrl(self, map_list=None, title=None, wxnoserver=False):
    #     self._map_list = [SLMap(18.0, 400.0, "log", "reson1 freq",
    #                             self._reson1.freq),
    #                       SLMap(0.00001, 500.0, "log", "reson1 q",
    #                             self._reson1.q),
    #                       SLMapMul(self._reson1.mul),
    #                       SLMap(18.0, 1700.0, "log", "reson2 freq",
    #                             self._reson2.freq),
    #                       SLMap(0.00001, 500.0, "log", "reson2 q",
    #                             self._reson2.q),
    #                       SLMap(18.0, 5000.0, "log", "filter freq",
    #                             self._aqueous.freq),
    #                       SLMapMul(self._mul)]
    #     PyoObject.ctrl(self, map_list, title, wxnoserver)

    def play(self, dur=0, delay=0):
        self._reson1Env.play(dur, delay)
        self._reson2Env.play(dur, delay)
        self._amp1Env.play(dur, delay)
        self._amp2Env.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self):
        self._reson1Env.stop()
        self._reson2Env.stop()
        self._amp1Env.stop()
        self._amp2Env.stop()
        return PyoObject.stop(self)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self._reson1Env.play(dur, delay)
        self._reson2Env.play(dur, delay)
        self._amp1Env.play(dur, delay)
        self._amp2Env.play(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)

# Run this script to test the Aqueous object.
if __name__ == "__main__":
    s = Server(duplex=0).boot()
    s.setAmp(0.1023)
    s.start()

    t = 3.776
    metro = Metro(time=t * 2).play()
    note = TrigXnoiseMidi(metro, dist=0, mrange=(30, 77))
    snap = Snap(note, choice=[0, 2, 4, 5, 7, 9, 11], scale=1)

    a = Aqueous(snap, metro, t * 0.75, mul=0.9)

    delay = Delay(a, delay=t * 0.75, feedback=0.6, maxdelay=t * 0.75,
                  mul=0.445)

    wetdry = delay + a

    d = WGVerb(wetdry, feedback=[0.73, 0.76], cutoff=5000,
               bal=0.25, mul=0.2985).out()

    s.gui(locals())
