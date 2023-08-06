"""Provides the NumericCtrl class."""

from typing import List, Optional

import wx
from wx.lib.newevent import NewEvent

from .setting import Bounds

FloatEvent, EVT_FLOAT = NewEvent()


class NumericCtrl(wx.TextCtrl):
    """A text control which only allows numbers."""

    bounds: Optional[Bounds]
    increment: float

    def __init__(
        self, *args, bounds: Optional[Bounds] = None, increment: float = 0.1,
        **kwargs
    ) -> None:
        """Initialise this object."""
        super().__init__(*args, **kwargs)
        self.bounds = bounds
        self.increment = increment
        self.Bind(wx.EVT_KEY_UP, self.on_text)

    def on_text(self, event: wx.KeyEvent) -> None:
        """Handle characters being typed."""
        f: float
        value: str = self.GetValue()
        allowed_keys: List[int] = [wx.WXK_DELETE, wx.WXK_BACK]
        keycode: int = event.GetKeyCode()
        if keycode < 255:
            # Valid ascii.
            char: str = chr(keycode)
            if char.isdigit() or (
                value and char == '.' and '.' not in value
            ) or keycode in allowed_keys:
                event.Skip()
                if value.endswith('.'):
                    self.AppendText('0')
                    self.SetSelection(len(value), len(value) + 1)
                if value.startswith('.'):
                    self.SetValue('0' + value)
                    self.SetSelection(0, 1)
            else:
                return None
            if self.bounds is not None:
                f = self.get_float()
                if f < self.bounds.min:
                    self.SetValue(str(self.bounds.min))
                    self.SelectAll()
                if f > self.bounds.max:
                    self.SetValue(str(self.bounds.max))
                    self.SelectAll()
        elif keycode == wx.WXK_UP:
            self.set_float(self.get_float() + self.increment)
        elif keycode == wx.WXK_DOWN:
            self.set_float(self.get_float() - self.increment)
        elif keycode == wx.WXK_HOME and self.bounds is not None:
            self.set_float(self.bounds.min)
        elif keycode == wx.WXK_END and self.bounds is not None:
            self.set_float(self.bounds.max)
        elif keycode == wx.WXK_PAGEUP:
            self.set_float(self.get_float() + (self.increment * 10))
        elif keycode == wx.WXK_PAGEDOWN:
            self.set_float(self.get_float() - (self.increment * 10))
        else:
            return None  # Don't skip.
        print(keycode)
        event.Skip()
        f = self.get_float()
        e = FloatEvent(name=self.GetName(), value=f)
        wx.PostEvent(self, e)

    def get_float(self) -> float:
        """Return the value as a float."""
        return float(self.GetValue() or '0')

    def set_float(self, value: float) -> None:
        """Set the value as a float."""
        if self.bounds is not None:
            if value > self.bounds.max:
                value = self.bounds.max
            if value < self.bounds.min:
                value = self.bounds.min
        self.SetValue(str(value))
