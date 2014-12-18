from pyo import *

from ground_state.pyo.utils import Tempo
from ground_state.pyo.utils import dbToAmp
from ground_state.pyo.utils import serverSetup


# t = Tempo(63.5)  # q=944ms, w=3.776s

# Windows
s = serverSetup(10, 700)
s.boot()
s.start()
s.setAmp(dbToAmp(-40))

shruti = [261.6256,
          275.6220,
          279.0673,
          290.6951,
          294.3288,
          310.0747,
          313.9507,
          327.0319,
          331.1198,
          348.8341,
          353.1945,
          367.9109,
          372.5098,
          392.4383,
          413.4330,
          418.6009,
          436.0426,
          441.4931,
          465.1121,
          470.9260,
          490.5479,
          496.6798,
          523.251]


# met = Metro(.125).play()
# choice = TrigXnoise(met, dist='loopseg', x1=0.5, x2=0.135)  # Outputs (0,1)
# noteIndex = int(rescale(choice.get(), 0.0, 1.0, 0.0, 21.0))
# out = SineLoop([shruti[noteIndex], shruti[noteIndex]], feedback=0.07).out()
# out.setFeedback(.03)


met = Metro(.125).play()
out = SineLoop([shruti[note_index], shruti[note_index]], feedback=0.07).out()

note_index = 0
def chooseStep():
    global note_index
    try:
        step = int(random.normalvariate(1, 0.75))
        if note_index == 21 or random.uniform(0, 1) < 0.5:
            step = step * -1
        note_index += step
        out.freq = [shruti[note_index], shruti[note_index]]
    except:
        print('note_index is {0}, step is {1}'.format(note_index, step))
        raise

tf = TrigFunc(met, chooseStep)

s.start()
s.setAmp(dbToAmp(-40))

Clean_objects(1, met, out, note_index, tf).start()
Clean_objects(1, s)
s.stop()
s.shutdown()
s.reinit()
