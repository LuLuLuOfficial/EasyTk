from EasyTk import ezTk
from tkinter import Tk, Frame
from abc import ABC, abstractmethod
from typing import Literal

class ezFrameManager(Frame): pass

class ezFrame(ABC):
    def __init__(self, master: ezFrameManager, name: str, **kwargs: dict):
        self.master: ezFrameManager = master
        self.name: str = name
        self.kwargs: dict = kwargs

        self.Frame: Frame = None

    @abstractmethod
    def UIInit(self): # Frame need be pack or place or guid... in here
        self.Frame: Frame = Frame(master=self.master, name=self.name, **self.kwargs)
        pass # hook

    def draw(self):
        self.UIInit()

    def destroy(self):
        if self.Frame is None: return
        self.Frame.destroy()
        self.Frame = None
    
    def tkraise(self, aboveThis=None):
        self.Frame.tkraise(aboveThis)

class ezFrameManager(Frame):
    SwitchModeList: list = ["tkraise", "redraw"]
    def __init__(self, master: Tk | ezTk, **kwargs: dict):
        super().__init__(master=master, **kwargs)

        self.master: Tk | ezTk = master

        self._SwitchMode_: Literal["tkraise", "redraw"] = "tkraise"

        self.Frames_NextIndex: int = 0
        self.Frames_IndexName: dict[int, str] = {}
        self.Frames_NameFrame: dict[str, ezFrame] = {}
        self.Frame_Now: str = None

        self.place(x=0, y=0, relwidth=1.0, relheight=1.0)

    def AddFrame(self, frame: ezFrame):
        name = frame.name
        self.Frames_IndexName[self.Frames_NextIndex] = name
        self.Frames_NameFrame[name] = frame
        self.Frames_NextIndex += 1
        if self._SwitchMode_ == "tkraise": frame.draw()

    def __getitem__(self, key: int | str):
        if isinstance(key, int):
            return self.Frames_NameFrame[self.Frames_IndexName[key]]
        else:
            return self.Frames_NameFrame[key]

    def remove(self, key: int | str):
        index: int
        name: str
        if isinstance(key, int):
            index = key
            name = self.Frames_IndexName[key]
        else:
            for _index, _name in self.Frames_IndexName.items():
                if _name == name:
                    index = _index; break
            name = key

        self.Frames_NameFrame[key].destroy()

        self.Frames_IndexName.pop(index)
        self.Frames_NameFrame.pop(key)

    def Switch(self, key: str | int):
        key = self.Frames_IndexName[key] if isinstance(key, int) else key
        NewFrame = self.Frames_NameFrame[key]

        if self._SwitchMode_ == "redraw":
            if not self.Frame_Now is None: self.Frames_NameFrame[self.Frame_Now].destroy()
            NewFrame.draw()
        else:
            NewFrame.tkraise()

        self.Frame_Now = key

    def SwitchMode(self, mode: Literal["tkraise", "redraw"]):
        if not mode in self.SwitchModeList: return
        self._SwitchMode_ = mode

        match self._SwitchMode_:
            case "tkraise":
                for name, frame in self.Frames_NameFrame.items():
                    if frame.Frame is None: frame.draw()
                if self.Frame_Now: self.Frames_NameFrame[self.Frame_Now].tkraise()
            case "redraw":
                for name, frame in self.Frames_NameFrame.items():
                    if frame.Frame is None or frame.name == self.Frame_Now: continue
                    frame.destroy()
                if self.Frame_Now: self.Frames_NameFrame[self.Frame_Now].draw()