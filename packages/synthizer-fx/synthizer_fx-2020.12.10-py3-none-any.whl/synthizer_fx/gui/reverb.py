"""Provides a GUI for tuning reverbs."""

from typing import Dict, List, Optional, cast

import wx
from ..reverb import reverb_to_dict, ReverbDict, reverb_from_dict
from yaml import dump, load, FullLoader
from synthizer import (Buffer, BufferGenerator, Context, DirectSource,
                       GlobalFdnReverb, SynthizerError)

from ..reverb import ReverbValue
from .numeric_ctrl import NumericCtrl, FloatEvent, EVT_FLOAT
from .setting import Bounds, Setting

default_preset_name: str = 'Untitled Preset'

settings: List[Setting] = [
    Setting(
        'gain', 'The volume of the reverb', bounds=Bounds(0.0, 1.0)
    ),
    Setting(
        'input_filter_enabled', 'Whether or not the input filter is enabled'
    ),
    Setting(
        'input_filter_cutoff', 'The cutoff of the input filter',
        bounds=Bounds(0.0, 22050.0)
    ),
    Setting(
        'mean_free_path', 'The mean free path of the simulated environment',
        bounds=Bounds(0.0, 0.5)
    ),
    Setting(
        't60', 'The T60 of the reverb', bounds=Bounds(0.0, 100.0)
    ),
    Setting(
        'late_reflections_lf_rolloff', 'A multiplicative factor on T60 for '
        'the low frequency band', bounds=Bounds(0.0, 2.0)
    ),
    Setting(
        'late_reflections_lf_reference', 'Where the low band of the feedback '
        'equalizer ends', bounds=Bounds(0.0, 22050.0)
    ),
    Setting(
        'late_reflections_hf_rolloff', 'A multiplicative factor on T60 for '
        'the high frequency band', bounds=Bounds(0.0, 2.0)
    ),
    # Setting(
    #     'late_reflections_hf_reference', 'Where the high band of the '
    #     'equalizer starts', bounds=Bounds(0.0, 22050.0)
    # ),
    Setting(
        'late_reflections_diffusion', 'Controls the diffusion of the late '
        'reflections as a percent', bounds=Bounds(0.0, 1.0)
    ),
    Setting(
        'late_reflections_modulation_depth', 'The depth of the modulation of '
        'the delay lines on the feedback path in seconds',
        bounds=Bounds(0.0, 0.3)
    ),
    Setting(
        'late_reflections_modulation_frequency', 'The frequency of the '
        'modulation of the delay lines in the feedback paths',
        bounds=Bounds(0.01, 100.0)
    ),
    Setting(
        'late_reflections_delay', 'The delay of the late reflections relative '
        'to the input in seconds', bounds=Bounds(0.0, 0.5)
    ),
]


class ReverbFrame(wx.Frame):
    """A frame for configuring reverb."""

    context: Context
    generator: BufferGenerator
    source: DirectSource
    reverb: GlobalFdnReverb
    controls: Dict[str, wx.Control]
    modified: bool = False
    name_ctrl: wx.TextCtrl
    loop_ctrl: wx.CheckBox
    restart_ctrl: wx.Button
    filename: Optional[str] = None

    def __init__(self, context: Context) -> None:
        """Initialise the frame."""
        self.context = context
        self.generator = BufferGenerator(context)
        self.source = DirectSource(context)
        self.source.add_generator(self.generator)
        self.reverb = GlobalFdnReverb(context)
        context.config_route(self.source, self.reverb)
        super().__init__(None, title='Reverb')
        p: wx.Panel = wx.Panel(self)
        s: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        sizer: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(p, label='Preset &Name'), 0, wx.GROW)
        self.name_ctrl = wx.TextCtrl(p, value=default_preset_name)
        sizer.Add(self.name_ctrl, 1, wx.GROW)
        self.controls = {}
        setting: Setting
        for setting in settings:
            try:
                value: ReverbValue = getattr(self.reverb, setting.name)
            except SynthizerError:
                raise RuntimeError(setting.name)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            st: wx.StaticText = wx.StaticText(
                p, label=setting.description, name=''
            )
            sizer.Add(st, 0, wx.GROW)
            ctrl: wx.Control
            if isinstance(value, bool):
                ctrl = wx.CheckBox(
                    p, label=setting.description, name=setting.name,
                    id=wx.ID_ANY
                )
                ctrl.Bind(wx.EVT_CHECKBOX, self.on_checkbox)
                ctrl.SetValue(value)
            else:
                ctrl = NumericCtrl(
                    p, bounds=setting.bounds, value=str(value),
                    name=setting.name
                )
                ctrl.Bind(EVT_FLOAT, self.set_modified)
            self.controls[setting.name] = ctrl
            sizer.Add(ctrl, 1, wx.GROW)
            s.Add(sizer, 1, wx.GROW)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.loop_ctrl = wx.CheckBox(p, label='&Loop')
        self.loop_ctrl.SetValue(False)
        self.loop_ctrl.Bind(wx.EVT_CHECKBOX, self.set_looping)
        sizer.Add(self.loop_ctrl, 1, wx.GROW)
        self.restart_ctrl = wx.Button(p, label='&Restart Audio')
        self.restart_ctrl.Bind(wx.EVT_BUTTON, self.restart_audio)
        sizer.Add(self.restart_ctrl, 1, wx.GROW)
        s.Add(sizer, 1, wx.GROW)
        self.SetSizerAndFit(s)
        p.SetAutoLayout(True)
        self.CreateStatusBar()
        file_menu: wx.Menu = wx.Menu()
        self.Bind(
            wx.EVT_MENU, self.do_new, file_menu.Append(
                wx.ID_NEW, '&New Preset\tCTRL+N',
                'Reset the reverb and make a new preset'
            )
        )
        self.Bind(
            wx.EVT_MENU, self.do_open, file_menu.Append(
                wx.ID_OPEN, '&Open Preset...\tCTRL+O',
                'Open an existing preset for editing'
            )
        )
        self.Bind(
            wx.EVT_MENU, self.do_save, file_menu.Append(
                wx.ID_SAVE, '&Save\tCTRL+S', 'Save the current preset'
            )
        )
        self.Bind(
            wx.EVT_MENU, self.do_saveas, file_menu.Append(
                wx.ID_SAVEAS, 'Save &As...\tCTRL+SHIFT+S',
                'Save the preset under a new name'
            )
        )
        file_menu.AppendSeparator()
        self.Bind(
            wx.EVT_MENU, self.open_sound, file_menu.Append(
                wx.ID_ANY, 'O&pen Sound...\tCTRL+SHIFT+O',
                'Open a sound to preview reverb'
            )
        )
        file_menu.AppendSeparator()
        self.Bind(
            wx.EVT_MENU, lambda event: self.Close(force=True),
            file_menu.Append(wx.ID_EXIT, 'E&xit', 'Exit the program')
        )
        mb: wx.MenuBar = wx.MenuBar()
        mb.Append(file_menu, '&File')
        self.SetMenuBar(mb)

    def reset(self) -> None:
        """Reset the reverb, and start again."""
        self.modified = False
        self.reverb.reset()
        self.name_ctrl.SetValue(default_preset_name)
        self.load_values()

    def load_values(self) -> None:
        """Load values from the reverb."""
        name: str
        control: wx.Control
        value: ReverbValue
        for name, control in self.controls.items():
            value = getattr(self.reverb, name)
            if isinstance(control, wx.CheckBox):
                control.SetValue(value)
            elif isinstance(control, NumericCtrl):
                control.set_float(cast(float, value))

    def do_new(self, event: wx.MenuEvent) -> None:
        """Reset the reverb."""
        if not self.modified or wx.MessageBox(
            'Your changes will be lost.', caption='Are you sure?',
            style=wx.ICON_EXCLAMATION | wx.YES_NO
        ) == wx.YES:
            self.reset()

    def on_checkbox(self, event: wx.CommandEvent) -> None:
        """Respond to a checkbox being checked or unchecked."""
        value: bool = event.IsChecked()
        name: str = self.FindFocus().GetName()
        setattr(self.reverb, name, value)

    def set_modified(self, event: FloatEvent) -> None:
        """Set modified state and update reverb."""
        setattr(self.reverb, event.name, event.value)
        self.modified = True

    def set_looping(self, event: wx.CommandEvent) -> None:
        """Set looping state."""
        self.generator.looping = event.IsChecked()

    def restart_audio(self, event: wx.CommandEvent) -> None:
        """Restart audio."""
        self.generator.position = 0.0

    def open_sound(self, event: wx.MenuEvent) -> None:
        """Load a sound to test the reverb."""
        with wx.FileDialog(
            self, message='Open Sound', style=wx.FD_OPEN
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path: str = dlg.GetPath()
                try:
                    self.generator.buffer = Buffer.from_stream('file', path)
                except SynthizerError as e:
                    wx.MessageBox(
                        'Error opening file %s: %s.' % (path, e), 'Error',
                        style=wx.ICON_EXCLAMATION
                    )

    def do_save(self, event: wx.MenuEvent, overwrite: bool = False) -> None:
        """Save the preset."""
        data: ReverbDict = reverb_to_dict(
            self.reverb, name=self.name_ctrl.GetValue()
        )
        if self.filename is None or overwrite:
            with wx.FileDialog(
                self, 'Save As', defaultFile='reverb.yaml', wildcard='*.yaml',
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            ) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    self.filename = cast(str, dlg.GetPath())
                    with open(self.filename, 'w') as f:
                        dump(data, f)

    def do_open(self, event: wx.MenuEvent) -> None:
        """Open a preset file."""
        if not self.modified or wx.MessageBox(
            'Your modifications to the current preset will be lost.',
            caption='Are you sure?', style=wx.YES_NO | wx.ICON_EXCLAMATION
        ) == wx.YES:
            with wx.FileDialog(
                self, wildcard='*.yaml', style=wx.FD_OPEN
            ) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    self.filename = cast(str, dlg.GetPath())
                    with open(self.filename, 'r') as f:
                        data: ReverbDict = load(f, Loader=FullLoader)
                    self.reverb.destroy()
                    self.reverb = reverb_from_dict(self.context, data)
                    self.context.config_route(self.source, self.reverb)
                    self.load_values()

    def do_saveas(self, event: wx.MenuEvent) -> None:
        """Save the preset under a new name."""
        return self.do_save(event, overwrite=True)
