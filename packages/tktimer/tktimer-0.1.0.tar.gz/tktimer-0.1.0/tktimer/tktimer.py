import datetime
import tkinter as tk


SECONDS_IN = {
    "second": 1,
    "minute": 60,
    "hour": 3600,
    "day": 3600 * 24,
    "week": 3600 * 24 * 7,
    "year": 3600 * 24 * 365.2422,
}


class Stopwatch(tk.Frame):
    def __init__(
        self,
        parent,
        *args,
        prefix="",
        suffix="",
        unit="second",
        update_every=10,
        precision=2,
        offset=0,
        **kwargs,
    ):
        super().__init__(parent, *args, **kwargs)
        self.value = tk.DoubleVar()
        self.value.set(offset)
        self.label = _HybridLabel(
            self,
            text=prefix + "{{:.{}f}}".format(precision) + suffix,
            textvariable=self.value,
        )
        self.label.pack(fill="both", expand=True)
        self.unit = unit
        self.update_every = update_every
        self.precision = precision
        self.offset = offset
        self.starting_point = None
        self.paused_point = None
        self.continued_point = None
        self.paused = False
        self.been_paused = 0

    def start(self):
        if self.paused:
            self.paused = False
            self.continued_point = datetime.datetime.now()
            self.been_paused += (
                self.continued_point - self.paused_point
            ).total_seconds()
        else:
            self.starting_point = datetime.datetime.now()
        self._update()

    def pause(self):
        self.paused = True
        self.paused_point = datetime.datetime.now()

    def _update(self):
        if self.paused:
            return

        time_elapsed = (
            (datetime.datetime.now() - self.starting_point).total_seconds()
            + self.offset
            - self.been_paused
        )

        self.value.set(time_elapsed / SECONDS_IN[self.unit])
        self.after(self.update_every, self._update)


class Countdown(tk.Frame):
    def __init__(
        self,
        parent,
        *args,
        prefix="",
        suffix="",
        unit="second",
        beginning=10,
        update_every=10,
        precision=2,
        **kwargs
    ):
        super().__init__(parent, *args, **kwargs)
        self.value = tk.DoubleVar()
        self.value.set(beginning / SECONDS_IN[unit])
        self.label = _HybridLabel(
            self,
            text=prefix + "{{:.{}f}}".format(precision) + suffix,
            textvariable=self.value,
        )
        self.label.pack(fill="both", expand=True)
        self.unit = unit
        self.update_every = update_every
        self.beginning = beginning
        self.precision = precision
        self.paused = False

    def start(self):
        if self.paused:
            self.paused = False
        self._update()

    def pause(self):
        self.paused = True

    def _update(self):
        if self.paused or round(self.value.get(), self.precision) == 0:
            return

        self.beginning -= self.update_every / 1000

        self.value.set(self.beginning / SECONDS_IN[self.unit])
        self.after(self.update_every, self._update)


class _HybridLabel(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        self.text = kwargs.pop("text", "{}")
        self.textvariable = kwargs.pop("textvariable", tk.StringVar(parent))
        self.textvariable.trace_add("write", self._update_text)
        super().__init__(parent, *args, **kwargs)
        self._update_text()

    def _update_text(self, *args, **kwargs):
        self.config(text=self.text.format(self.textvariable.get()))
