#!/usr/bin/env python3
# encoding: utf-8
# This generator is taken verbatim from the Pyo documentation.
from pyo import PyoTableObject, Server, Osc, HarmTable


class TriTable(PyoTableObject):
    """
    Triangle waveform generator.

    Generates triangle waveforms made up of fixed number of harmonics.

    :Parent: :py:class:`PyoTableObject`

    :Args:

        order : int, optional
            Number of harmonics triangle waveform is made of. The waveform
            will contain `order` odd harmonics. Defaults to 10.
        size : int, optional
            Table size in samples. Defaults to 8192.

    >>> s = Server().boot()
    >>> s.start()
    >>> t = TriTable(order=15).normalize()
    >>> a = Osc(table=t, freq=[199,200], mul=.2).out()

    """
    def __init__(self, order=10, size=8192):
        PyoTableObject.__init__(self, size)
        self._order = order
        self._tri_table = HarmTable(self._create_list(order), size)
        self._base_objs = self._tri_table.getBaseObjects()
        self.normalize()

    @staticmethod
    def _create_list(order):
        # internal method used to compute the harmonics's weight
        l = []
        ph = 1.0
        for i in range(1, order*2):
            if i % 2 == 0:
                l.append(0)
            else:
                l.append(ph / (i*i))
                ph *= -1
        return l

    def setOrder(self, x):
        """
        Change the `order` attribute and redraw the waveform.

        :Args:

            x : int
                New number of harmonics

        """
        self._order = x
        self._tri_table.replace(self._create_list(x))
        self.normalize()
        self.refreshView()

    @property
    def order(self):
        """int. Number of harmonics triangular waveform is made of."""
        return self._order

    @order.setter
    def order(self, x):
        self.setOrder(x)

# Run the script to test the TriTable object.
if __name__ == "__main__":
    s = Server(duplex=0).boot()
    s.setAmp(0.05)
    s.start()
    t = TriTable(10, 8192)
    t.view()
    a = Osc(t, 500, mul=.3).out()
    s.gui(locals())
