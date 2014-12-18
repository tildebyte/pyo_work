    def setFoo(self, x):
        """
        Replace the `foo` attribute.

        :Args:

            x : PyoObject
                New `foo` attribute.

        """
        self._foo = x
        self._bar.foo = x

    @property
    def foo(self):
        """float or PyoObject. foo."""
        return self._foo

    @bar.setter
    def foo(self, x):
        self.setFoo(x)
