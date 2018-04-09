from pyo import *  # Implicitly imports `random`?

from ground_state.pyo.utils import Tempo
from ground_state.pyo.utils import dbToAmp
from ground_state.pyo.utils import serverSetup


# t = Tempo(63.5)  # q=944ms, w=3.776s

# Windows
s = serverSetup(10, 700)
s.boot()
s.setAmp(dbToAmp(-34))

root = 261.6256
shruti_ratios = [1.0,
                 256.0 / 243.0,
                 16.0 / 15.0,
                 10.0 / 9.0,
                 9.0 / 8.0,
                 32.0 / 27.0,
                 6.0 / 5.0,
                 5.0 / 4.0,
                 81.0 / 64.0,
                 4.0 / 3.0,
                 27.0 / 20.0,
                 45.0 / 32.0,
                 729.0 / 512.0,
                 3.0 / 2.0,
                 128.0 / 81.0,
                 8.0 / 5.0,
                 5.0 / 3.0,
                 27.0 / 16.0,
                 16.0 / 9.0,
                 9.0 / 5.0,
                 15.0 / 8.0,
                 243.0 / 128.0,
                 2.0]

shruti_high = [root * x for x in shruti_ratios]
shruti_ratios_low = shruti_ratios[:]
shruti_ratios_low.reverse()
shruti_low = [root / x for x in shruti_ratios_low]
shruti = shruti_low[:-1] + shruti_high

lead_note_index = 22
accomp_note_index = 22
lead_met = Metro(0.125)
accomp_met = Metro(2)
drone = SineLoop([shruti[0], shruti[0]], feedback=0.07).out()
lead = SineLoop([shruti[lead_note_index], shruti[lead_note_index]], feedback=0.12, mul=dbToAmp(-4))
accomp = SineLoop([shruti[accomp_note_index], shruti[accomp_note_index]], feedback=0.08, mul=dbToAmp(-8))
mm = Mixer(outs=1, chnls=2, time=.025)
mm.addInput(0, lead)
mm.addInput(1, accomp)
mm.setAmp(0, 0, 0.5)
mm.setAmp(1, 0, 0.5)

def choose_lead_step():
    global lead_note_index
    step = int(random.normalvariate(1, 3))
    lead_note_index += step
    if lead_note_index < 0:
        lead_note_index *= -1
    if lead_note_index > len(shruti) - 1:
        lead_note_index = (len(shruti) - 1) - lead_note_index
    try:
        lead.freq = [shruti[lead_note_index], shruti[lead_note_index]]
    except:
        print('lead_note_index is {0}; step is {1}'.format(lead_note_index, step))
        raise

def choose_accomp_step():
    global accomp_note_index
    step = int(random.normalvariate(1, 3))
    accomp_note_index += step
    if accomp_note_index < 0:
        accomp_note_index *= -1
    if accomp_note_index > len(shruti) - 1:
        accomp_note_index = (len(shruti) - 1) - accomp_note_index
    try:
        accomp.freq = [shruti[accomp_note_index], shruti[accomp_note_index]]
    except:
        print('accomp_note_index is {0}; step is {1}'.format(accomp_note_index, step))
        raise


d = Delay(mm, delay=0.2, feedback=0.5, mul=0.4).out()

lead_trig = TrigFunc(lead_met, choose_lead_step)
accomp_trig = TrigFunc(accomp_met, choose_accomp_step)
lead_met.play()
accomp_met.play()


s.start()
s.setAmp(dbToAmp(-40))

s.stop()
s.shutdown()
s.reinit()
