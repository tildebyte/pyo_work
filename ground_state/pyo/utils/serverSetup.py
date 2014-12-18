#!/usr/bin/env python
# encoding: utf-8
"""
pyo Server setup.
Call it thusly:
    's = serverSetup(10, dbToAmp(-8.79))'.
"""
from pyo import Server


# Server setup..
def serverSetup(device, bufsize, api='portaudio', amp=1.0):
    _s = Server(sr=48000, nchnls=2, buffersize=bufsize, duplex=0, audio=api)
    _s.setOutputDevice(device)
    _s.setAmp(amp)
    _s.boot()
    _s.start()
    return _s
