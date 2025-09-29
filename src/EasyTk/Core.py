
from tkinter import Widget as tk_Widget, Frame as tk_Frame, Label as tk_Label, Entry as tk_Entry, Button as tk_Button, Canvas as tk_Canvas
from tkinter import Tk, PhotoImage, Event
from tkinter.font import Font

from PIL import Image as PILImage, ImageTk as PILImageTk
from typing import Literal, Callable

from sys import exit as SysExit
from os.path import exists as FileExists

from ctypes import windll

from EasyTk.WindowStyles import WinStyles, WinStates, ResetWindowStyle

WINDLLU32 = windll.user32

import logging

LogPrint = print

# --------------------------------------------------

class EasyTk(Tk):
    def __init__(self): self.RootType: str; self.Type: str
class Widget():
    def __init__(self): self.RootType: str; self.Type: str
class Label(Widget, tk_Label): pass
class Button(Widget, tk_Button): pass

# --------------------------------------------------

class Content():
    def __init__(self, master: EasyTk | Widget | Button = None):
        self.Master = master

    def Text(self, text: str):
        match self.Master.Type:
            case "EasyTk":
                self.Master.wm_title(text)
            case "Label":
                self.Master.configure(text=text)
            case "Button":
                self.Master.configure(text=text)
    
    def Image(
            self,
            path: str,
            scale: Literal["Cut", "Fill", "Ratio", "Stretch"] | None = None,

            ratio: float = 1.00,
            width: int = None,
            height: int = None
    ):
        if not FileExists(path): return

        Img = PILImage.open(path)
        if any((scale == None, width==None, height==None)) != True or scale == "Ratio":
            SizeW, SizeH = Img.width, Img.height
            match scale:
                case "Cut":
                    Img.resize((width, height))
                case "Fill":
                    WHRatio_Target: float = width / height
                    WHRatio_Image: float = SizeW / SizeH
                    if WHRatio_Target > WHRatio_Image:
                        if WHRatio_Image > 1:
                            ratio = width / SizeW
                        else:
                            ratio = height / SizeH
                    else:
                        if WHRatio_Image > 1:
                            ratio = height / SizeH
                        else:
                            ratio = width / SizeW
                    Img = Img.resize((int(SizeW * ratio), int(SizeH * ratio)), PILImage.LANCZOS)
                    # Img = Img.resize((10, 10), PILImage.LANCZOS)
                case "Ratio":
                    Img = Img.resize((int(SizeW * ratio), int(SizeH * ratio)), PILImage.LANCZOS)
                case "Stretch":
                    pass
                case _: return

        Img = PILImageTk.PhotoImage(Img)

        match self.Master.Type:
            case "EasyTk":
                pass
            case "Label":
                self.Master.configure(image=Img)

class Style():
    def __init__(self, master: EasyTk | Widget | Button = None):
        self.Master = master

    def Geometry(self, width: int = None, height: int = None) -> tuple:
        match self.Master.Type:
            case "EasyTk":
                width = self.Master.winfo_width() if width == None else width
                height = self.Master.winfo_height() if height == None else height
                self.Master.wm_geometry(f"{width}x{height}")
                return (width, height)
            case "Frame":
                geometry = {}
                if width  != None: geometry['width']  = width
                if height != None: geometry['height'] = height
                self.Master.configure(**geometry)
    
    def SizeLimit(self, mode: Literal["MAX", "MIN", "ALL"] = None, size: tuple | None = None) -> tuple:
        match self.Master.Type:
            case "EasyTk":
                if mode == "MAX":
                    return self.Master.wm_maxsize(*size) if size != None else self.Master.wm_maxsize()
                if mode == "MIN":
                    return self.Master.wm_minsize(*size) if size != None else self.Master.wm_minsize()

    def SizeFix(self, mode: Literal["Execute", "Cancel"] = "Execute") -> None:
        match self.Master.Type:
            case "EasyTk":
                def __SizeFix():
                    if self.Master.winfo_viewable() == 0: self.Master.after(50, __SizeFix); return
                    Size: tuple = (self.Master.winfo_width(), self.Master.winfo_height())
                    if mode == "Execute": self.Master.wm_maxsize(*Size); self.Master.wm_minsize(*Size)
                    elif mode == "Cancel": self.Master.wm_maxsize(self.Master.winfo_screenwidth(), self.Master.winfo_screenheight()); self.Master.wm_minsize(0, 0)
                __SizeFix()

    def Font(
            self,
            font: str | Font,
            size: int = ...,
            style: tuple | Literal["bold", "italic", "underline", "overstrike"] = ()
    ):
        if isinstance(font, str) and size: font = (font, size, *style) if isinstance(style, tuple) else (font, size, style)
        match self.Master.Type:
            case "EasyTk":
                pass
            case "Label":
                self.Master.configure(font=font)
            case "Button":
                self.Master.configure(font=font)

    def Foreground(self, color: str):
        match self.Master.RootType:
            case "EasyTk":
                self.Master.configure(foreground=color)
            case "Widget":
                self.Master.configure(foreground=color)

    def Background(self, color: str):
        match self.Master.RootType:
            case "EasyTk":
                self.Master.configure(bg=color)
            case "Widget":
                self.Master.configure(bg=color)

    def Alignment(self, anchor: Literal["center", "n", "s", "w", "e", "nw", "ne", "sw", "se"]):
        match self.Master.Type:
            case "Label":
                self.Master.configure(anchor=anchor)

class Behavior():
    def __init__(self, master: EasyTk | Widget | Button = None):
        self.Master = master

    def Bind(self):
        match self.Master.Type:
            case "Button":
                return self.Master.bind

    def After(self, ms: int | None = None, func: Callable = None, *args) -> int | None:
        if (ms, func) == (None, None): return 
        match self.Master.Type:
            case 'EasyTk':
                return self.Master.after_idle(func, *args) if ms in (None, 0) else self.Master.after(ms, func, *args)

    def AfterCancel(self, id: int) -> None:
        match self.Master.Type:
            case 'EasyTk':
                return self.Master.after_cancel(id)

    def MaxedSize(self):
        match self.Master.Type:
            case 'EasyTk':
                WINDLLU32.ShowWindow(self.Master.HWND, WinStates.SW_MAXIMIZE)

    def MinedSize(self):
        match self.Master.Type:
            case 'EasyTk':
                WINDLLU32.ShowWindow(self.Master.HWND, WinStates.SW_MINIMIZE)
    
    def RestoredSize(self):
        match self.Master.Type:
            case 'EasyTk':
                WINDLLU32.ShowWindow(self.Master.HWND, WinStates.SW_RESTORE)

class Layout():
    def __init__(self, master: EasyTk | Widget = None):
        self.Master = master
    
    def Pack(
            self,
            anchor: Literal["center", "n", "s", "w", "e", "nw", "ne", "sw", "se"] = ...,
            expand: bool = ...,
            fill: Literal['none', 'x', 'y', 'both'] = ...,
            side: Literal['left', 'right', 'top', 'bottom'] = ...,
            ipadx: int = ...,
            ipady: int = ...,
            padx: int = ...,
            pady: int = ...,
            **kwargs
    ):
        _kwargs: dict = {Key: Value for Key, Value in locals().items() if Key not in ("self", "args", "kwargs") and Value is not ...}; _kwargs.update(kwargs)
        self.Master.pack_configure(**_kwargs)

    def Place(
            self,
            bordermode: Literal['inside', 'outside', 'ignore'] = ...,
            width: int = ...,
            height: int = ...,
            x: int = ...,
            y: int = ...,
            relheight: str | float = ...,
            relwidth: str | float = ...,
            relx: str | float = ...,
            rely: str | float = ...,
            **kwargs
    ):
        _kwargs: dict = {Key: Value for Key, Value in locals().items() if Key not in ("self", "args", "kwargs") and Value is not ...}; _kwargs.update(kwargs)
        self.Master.place_configure(**_kwargs)

class Configure():
    def __init__(self, master: EasyTk | Widget = None):
        self.Master = master
    
    def Configure(self, cnf=None, **kw):
        return self.Master.configure(cnf, **kw)

# --------------------------------------------------

class Widget():
    def __init__(self, master = None, *args, **kwargs):
        self.Master: EasyTk | Widget = master
        self.RootType: str = "Widget"
        self.Type: str = "Widget"

    def _Configure(self, cnf=None, **kw):
        return self.Master.configure(cnf, kw)

    Configure = _Configure

class Frame(Widget, tk_Frame):
    def __init__(self, master = None, *args, **kwargs):
        Widget.__init__(self, master=master)
        tk_Frame.__init__(self, master=master, *args, **kwargs)

        self.Type: str = "Frame"

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)

    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Layout(self) -> Layout:
        return Layout(self)

class Label(Widget, tk_Label):
    def __init__(self, master = None, *args, **kwargs):
        Widget.__init__(self, master=master)
        tk_Label.__init__(self, master=master, *args, **kwargs)

        self.Type: str = "Label"

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)

    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Layout(self) -> Layout:
        return Layout(self)

class Button(Widget, tk_Button):
    def __init__(self, master = None, *args, **kwargs):
        Widget.__init__(self, master=master)
        tk_Button.__init__(self, master=master, *args, **kwargs)

        self.Type: str = "Button"

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)

    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Layout(self) -> Layout:
        return Layout(self)

class Canvas(Widget, tk_Canvas):
    def __init__(self, master = None, *args, **kwargs):
        Widget.__init__(self, master=master)
        tk_Canvas.__init__(self, master=master, *args, **kwargs)

        self.Type: str = "Canvas"

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)

    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Layout(self) -> Layout:
        return Layout(self)

# --------------------------------------------------

class TitleBar(Widget):
    def __init__(self, master: EasyTk, DPIScale: float = 1.00, ResizeEdgePx: int = 5, bg:str = "#2c3e50", height: int = 45, *args, **kwargs):
        Widget.__init__(self, master=master)

        self.Master: EasyTk = master
        for zWidget in self.Master.winfo_children(): zWidget.destroy()

        self.DPIScale: float = DPIScale

        self.Resources: dict[str] = {
            "TitleIcon": r"C:\Users\Lucas\Desktop\星星.png"
        }

        self.ResizeArgs: dict = {
            "InResizeZone": False,
            "EdgePx": ResizeEdgePx,
            "Type": None,
            "WinSizeW": None,
            "WinSizeH": None,
            "CursorX": None,
            "CursorY": None,
        }

        self.DragArgs: dict = {
            "DragStarted": False,
            "WinPosX": None,
            "WinPosY": None,
            "CursorX": None,
            "CursorY": None,
            "RelativeX": None,
            "RelativeY": None,
        }

        self.SetStyle(bg, height)
        self.InitUI()
        self.InitWidgetInfo()
        self.UIConfig()
        self.UILayout()
        self.BindEvents()
        self.BindResizeZones()

    def SetStyle(self, bg: str, height: int):
        self.SIZE_Mainheight: int = int(height * self.DPIScale)
        self.SIZE_Btnheight: int = int(2 * self.DPIScale)

        self.COLOR_MainBackground: str = bg
        self.COLOR_BtnBackground: str = "#4F4F4F"

    def InitUI(self):
        self.TitleBar: Frame = Frame(self.Master)
        self.TitleIcon: Label = Label(self.TitleBar)
        self.TitleText: Label = Label(self.TitleBar)
        self.TitleBtns: Frame = Frame(self.TitleBar)

        self.TitleBtn_Min: Button = Button(self.TitleBtns)
        self.TitleBtn_Max: Button = Button(self.TitleBtns)
        self.TitleBtn_Ext: Button = Button(self.TitleBtns)

        self.LayoutedMark: Frame = Frame(self.TitleBar)

    def InitWidgetInfo(self):
        self.TitleWidgets: dict[int, dict[str, Button | Frame | Label, str]] = {
            1: {
                "Name": "TitleBar",
                "Widget": self.TitleBar,
                "Bind": [("<Button-1>", self.Drag_Press), ("<B1-Motion>", self.Drag_Move), ("<ButtonRelease-1>", self.Drag_Release), ("<Double-Button-1>", self.DBClick_Maximize)]
            },
            2: {
                "Name": "TitleIcon",
                "Widget": self.TitleIcon,
                "Bind": [("<Button-1>", self.Drag_Press), ("<B1-Motion>", self.Drag_Move), ("<ButtonRelease-1>", self.Drag_Release), ("<Double-Button-1>", self.DBClick_Maximize)]
            },
            3: {
                "Name": "TitleText",
                "Widget": self.TitleText,
                "Bind": [("<Button-1>", self.Drag_Press), ("<B1-Motion>", self.Drag_Move), ("<ButtonRelease-1>", self.Drag_Release), ("<Double-Button-1>", self.DBClick_Maximize)]
            },
            4: {
                "Name": "TitleBtns",
                "Widget": self.TitleBtns,
                "Bind": [("<Button-1>", self.Drag_Press), ("<B1-Motion>", self.Drag_Move), ("<ButtonRelease-1>", self.Drag_Release), ("<Double-Button-1>", self.DBClick_Maximize)]
            },
            5: {
                "Name": "TitleBtn_Min",
                "Widget": self.TitleBtn_Min,
                "Icon_Default": "━",
                "Bind": [("<ButtonRelease-1>", self.Btn_Minimize)]
            },
            6: {
                "Name": "TitleBtn_Max",
                "Widget": self.TitleBtn_Max,
                "Icon_Default": "❐",
                "Bind": [("<ButtonRelease-1>", self.Btn_Maximize)]
            },
            7: {
                "Name": 'TitleBtn_Ext',
                "Widget": self.TitleBtn_Ext,
                "Icon_Default": "✖",
                "Bind": [("<ButtonRelease-1>", self.Btn_Exit)]
            }
        }

    def UIConfig(self): 
        self.TitleBar.Style.Background(self.COLOR_MainBackground)
        self.TitleBar.Style.Geometry(height=self.SIZE_Mainheight)

        self.TitleIcon.Style.Background(self.TitleBar["bg"])
        self.TitleIcon.Content.Image(self.Resources["TitleIcon"], scale="Fill", width=30, height=30)

        self.TitleText.Style.Foreground("#FFFFFF")
        self.TitleText.Style.Background(self.TitleBar["bg"])
        self.TitleText.Style.Font("Arial", 13)
        self.TitleText.Style.Alignment("w")
        self.TitleText.Content.Text("TitleBar测试")

        self.TitleBtns.Style.Background(self.TitleBar["bg"])

        for TitleBtnIndex in self.TitleWidgets:
            if self.TitleWidgets[TitleBtnIndex]["Widget"].Type != "Button": continue
            TitleBtn: Button = self.TitleWidgets[TitleBtnIndex]["Widget"]
            Icon: str = self.TitleWidgets[TitleBtnIndex]["Icon_Default"]

            TitleBtn.Style.Font("Arial", 13)
            TitleBtn.Content.Text(Icon)

        self.LayoutedMark.Style.Geometry(0, 0)

    def UILayout(self):
        self.TitleBar.Layout.Place(x=0, y=0, relwidth=1.0, height=self.SIZE_Mainheight, bordermode="inside")

        self.TitleIcon.Layout.Pack(anchor="center", side="left")
        self.TitleText.Layout.Pack(anchor="center", side="left")

        self.TitleBtns.Layout.Pack(anchor="center", side="right")

        for TitleBtnIndex in self.TitleWidgets:
            if self.TitleWidgets[TitleBtnIndex]["Widget"].Type != "Button": continue
            self.TitleWidgets[TitleBtnIndex]["Widget"].Layout.Pack(anchor="center", side="left", padx=(0, 5))

        self.LayoutedMark.Layout.Place(x=0, y=0)

    # ----------
    def BindEvents(self):
        for TitleBtnIndex in self.TitleWidgets:
            zWidget = self.TitleWidgets[TitleBtnIndex]["Widget"]
            zBindConfigs: list[str] = self.TitleWidgets[TitleBtnIndex]["Bind"]
            for zEvent, zFunc in zBindConfigs: zWidget.bind(zEvent, zFunc)

        def LayoutedMarkFunc(event: Event):
            self.Master.Style.SizeLimit(
                "MIN",
                size=(self.TitleIcon.winfo_width() + self.TitleText.winfo_width() + self.TitleBtns.winfo_width() + 5, 0)
            )
            self.LayoutedMark.unbind("<Map>")
            self.LayoutedMark.destroy()
        self.LayoutedMark.bind( "<Map>", LayoutedMarkFunc)
    # ----------
    def Drag_Press(self, event: Event):
        # 校验
        if self.Master.Maximized["Cooldown"]: return # 确保不处于最大化冷却期

        self.DragArgs["WinPosX"], self.DragArgs["WinPosY"] = self.Master.winfo_x(), self.Master.winfo_y()
        self.DragArgs["CursorX"], self.DragArgs["CursorY"] = event.x_root, event.y_root
        self.DragArgs["RelativeX"], self.DragArgs["RelativeY"] = self.DragArgs["CursorX"] - self.DragArgs["WinPosX"], self.DragArgs["CursorY"] - self.DragArgs["WinPosY"]
        
        self.DragArgs["DragStarted"] = True

    def Drag_Move(self, event: Event):
        # 校验
        if self.Master.Maximized["Cooldown"]: return # 确保不处于最大化冷却期
        if not self.DragArgs["DragStarted"]: return # 确保处于拖拽开始状态

        if self.Master.Maximized["State"]:
            WinPosSize: list[str] = self.Master.Maximized["Pos"].split('+')
            SizeW = int(WinPosSize[0].split("x")[0])
            PosX, PosY = (int(Pos) for Pos in WinPosSize[1:])
            
            if SizeW + PosX <= self.DragArgs["CursorX"]:
                PosX = event.x_root - SizeW*event.x//self.Master.winfo_width()
            else:
                PosX = event.x_root - SizeW//2
            PosY = event.y_root-self.SIZE_Mainheight//2
            PosY = PosY if PosY > 0 else 0
            self.DragArgs["RelativeX"] = event.x_root - PosX
            self.DragArgs["RelativeY"] = event.y_root - PosY

            self.Btn_Maximize()

            self.Master.Maximized["State"] = False
        else:
            PosX, PosY = (int(Pos) for Pos in self.Master.geometry().split("+")[1:])
            NewX = event.x_root - self.DragArgs["RelativeX"]
            NewY = event.y_root - self.DragArgs["RelativeY"]
            self.Master.geometry(f"+{NewX}+{NewY}")

    def Drag_Release(self, event: Event):
        self.DragArgs["DragStarted"] = False
    # ----------
    def DBClick_Maximize(self, event: Event):
        # 校验
        if self.ResizeArgs["Type"]: return # 确保不处于 ReSize 判定区
        if self.Master.Maximized["Cooldown"]: return # 确保不处于双击最大化冷却期

        self.Master.Maximized["Cooldown"] = True

        if self.Master.Maximized["State"]:
            self.Master.Maximized["State"] = False
            self.Master.Behavior.RestoredSize()
        else:
            self.Master.Maximized["State"] = True
            self.Master.Maximized["Pos"] = self.Master.geometry()
            self.Master.Behavior.MaxedSize()

        self.Master.Behavior.After(self.Master.Maximized["CooldownTime"], lambda: self.Master.Maximized.__setitem__("Cooldown", False))
    # ----------
    def Btn_Minimize(self, event: Event = None):
        self.Master.Behavior.MinedSize()

    def Btn_Maximize(self, event: Event = None):
        if self.Master.Maximized["State"]:
            self.Master.Maximized["State"] = False
            self.Master.Behavior.RestoredSize()
        else:
            self.Master.Maximized["State"] = True
            self.Master.Maximized["Pos"] = self.Master.geometry()
            self.Master.Behavior.MaxedSize()

    def Btn_Exit(self, event: Event):
        self.Master.Exit()
    # ----------
    def BindResizeZones(self):
        self.Master.bind("<Motion>", self.Resize_ZoneHitCheck)
        self.Master.bind("<Button-1>", self.Resize_Press)
        self.Master.bind("<B1-Motion>", self.Resize_Move)

    def Resize_ZoneHitCheck(self, event: Event):
        # 校验
        if self.Master.Maximized["State"]: return # 确保不处于最大化状态

        WinPos_X = event.x_root - self.Master.winfo_x()
        WinPos_Y = event.y_root - self.Master.winfo_y()
        WinSize_W = self.Master.winfo_width()
        WinSize_H = self.Master.winfo_height()

        HitState: tuple = (
            WinPos_X < self.ResizeArgs["EdgePx"],              # Hit_Left
            WinPos_X > WinSize_W - self.ResizeArgs["EdgePx"],  # Hit_Right
            WinPos_Y < self.ResizeArgs["EdgePx"],              # Hit_Top
            WinPos_Y > WinSize_H - self.ResizeArgs["EdgePx"]   # Hit_Bottom
        )

        match HitState:
            case (True, False, True, False): # Hit_Left & Hit_Top
                self.ResizeArgs["Type"] = 'nw'
                self.Master.configure(cursor='top_left_corner')
            case (True, False, False, True): # Hit_Left & Hit_Bottom
                self.ResizeArgs["Type"] = 'sw'
                self.Master.configure(cursor='bottom_left_corner')
            case (False, True, True, False): # Hit_Right & Hit_Top
                self.ResizeArgs["Type"] = 'ne'
                self.Master.configure(cursor='top_right_corner')
            case (False, True, False, True): # Hit_Right & Hit_Bottom
                self.ResizeArgs["Type"] = 'se'
                self.Master.configure(cursor='bottom_right_corner')
            case (True, False, False, False): # Hit_Left
                self.ResizeArgs["Type"] = 'w'
                self.Master.configure(cursor='sb_h_double_arrow')
            case (False, True, False, False): # Hit_Right
                self.ResizeArgs["Type"] = 'e'
                self.Master.configure(cursor='sb_h_double_arrow')
            case (False, False, True, False): # Hit_Top
                self.ResizeArgs["Type"] = 'n'
                self.Master.configure(cursor='sb_v_double_arrow')
            case (False, False, False, True): # Hit_Bottom
                self.ResizeArgs["Type"] = 's'
                self.Master.configure(cursor='sb_v_double_arrow')
            case _:
                self.ResizeArgs["Type"] = None
                self.Master.configure(cursor='')

    def Resize_Press(self, event: Event):
        self.Resize_ZoneHitCheck(event)  # 确保按下时仍处于热区
        if self.ResizeArgs["Type"]:
            self.ResizeArgs["CursorX"] = event.x_root
            self.ResizeArgs["CursorY"] = event.y_root
            self.ResizeArgs["WinSizeW"] = self.Master.winfo_width()
            self.ResizeArgs["WinSizeH"] = self.Master.winfo_height()
        else:
            self.ResizeArgs["Type"] = None

    def Resize_Move(self, event: Event):
        # 校验
        if not self.ResizeArgs["Type"]: return # 确保光标处于 ReSize 判定区域

        DeltaX = event.x_root - self.ResizeArgs["CursorX"]
        DeltaY = event.y_root - self.ResizeArgs["CursorY"]

        Width_New = self.ResizeArgs["WinSizeW"]
        Height_New = self.ResizeArgs["WinSizeH"]
        X_New = self.Master.winfo_x()
        Y_New = self.Master.winfo_y()

        Min_Height = self.SIZE_Mainheight
        Min_Width = self.Master.minsize()[0]

        if 'e' in self.ResizeArgs["Type"]:
            Width_New = max(Min_Width, self.ResizeArgs["WinSizeW"] + DeltaX)
        if 's' in self.ResizeArgs["Type"]:
            Height_New = max(Min_Height, self.ResizeArgs["WinSizeH"] + DeltaY)
        if 'w' in self.ResizeArgs["Type"]:
            # 新宽度 = 原宽度 - 鼠标横向移动量(向左拖 DeltaX<0, 宽度应增加)
            Width_New = max(Min_Width, self.ResizeArgs["WinSizeW"] - DeltaX)
            # 窗口左上角 x 应移动 DeltaX, 以保持鼠标“吸附”在左边缘
            X_New = self.ResizeArgs["CursorX"] - (Width_New - self.ResizeArgs["WinSizeW"])
        if 'n' in self.ResizeArgs["Type"]:
            # 新高度 = 原高度 - 鼠标纵向移动量(向上拖 DeltaY<0, 高度应增加)
            Height_New = max(Min_Height, self.ResizeArgs["WinSizeH"] - DeltaY)
            # 窗口左上角 y 应移动 DeltaY, 以保持鼠标“吸附”在上边缘
            Y_New = self.ResizeArgs["CursorY"] - (Height_New - self.ResizeArgs["WinSizeH"])

        self.Master.geometry(f"{int(Width_New)}x{int(Height_New)}+{int(X_New)}+{int(Y_New)}")

# --------------------------------------------------

class EasyTk(Tk):
    def __init__(
            self,
            IndepTitleBar: bool = False,
            WinTransparent: tuple[bool, str] = (False, "gray15")
    ):
        super().__init__(className = 'EasyTk')

        self.RootType: str = 'EasyTk'
        self.Type: str = 'EasyTk'

        self.HWND: int = 0

        self.DPIScale: float = self.GetSysDPI()

        # 重写
        self.RewriteEvent()

        # self.Configure: Configure = Configure(self)

        # 窗口状态
        self.Destroyed: bool = False
        self.Maximized: dict[str | bool | str] = {
            "State": False,
            "Cooldown": False,
            "CooldownTime": 200,
            "Pos": ""
        }
        self.Minimized: dict[str | bool | str] = {
            "State": False,
            "Cooldown": False,
            "CooldownTime": 200,
            "Pos": ""
        }

        # 启用独立标题栏
        self.TitleBar = self.IndepTitleBar() if IndepTitleBar else None

        # 启用透明窗口支持
        self.TRANSPARENT_COLOR: str = WinTransparent[1]
        if WinTransparent[0]: self.wm_attributes("-transparentcolor", self.TRANSPARENT_COLOR)

        self.bind("<F3>", self.Debug_ShowZones)

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)
    
    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Configure(self) -> Configure:
        return Configure(self)

    @property
    def WinState(self) -> Literal["Waiting", "Displaying", "Destroyed", "Minimized"]:
        if self.Destroyed: return "Destroyed"
        if self.Minimized["State"]: return "Minimized"
        State: int | str = self.winfo_viewable()
        return "Waiting" if State == 0 else "Displaying" if State else State

    def GetSysDPI(self) -> float:
        windll.shcore.SetProcessDpiAwareness(1)
        user32 = WINDLLU32
        user32.SetProcessDPIAware()
        dpi = user32.GetDpiForSystem()
        return dpi / 96.0

    def RewriteEvent(self):
        self.protocol("WM_DELETE_WINDOW", self.Exit)

    def IndepTitleBar(self):
        self.wm_overrideredirect(True)
        zTitleBar = TitleBar(self)
        return zTitleBar

    def Run(self):
        self.update_idletasks()
        self.HWND = WINDLLU32.GetParent(self.winfo_id())
        if self.TitleBar != None: ResetWindowStyle(self.HWND, "UnTtlBar")

        self.mainloop()

    def Exit(self, Level: Literal["Window", "Program"] = "Window", ExitCode: int | tuple[int, str] = 0):
        if isinstance(ExitCode, int): ExitCode = (ExitCode, "")
        elif isinstance(ExitCode, tuple):
            if len(ExitCode) == 1 and isinstance(ExitCode[0], int): ExitCode = (ExitCode[0], "")
            elif all([len(ExitCode) == 2, isinstance(ExitCode[0], int), isinstance(ExitCode[1], str)]): pass
            else: raise ValueError(f"Expect <tuple[int, str]>, got <tuple{[type(Value).__name__ for Value in ExitCode]}>.")
        else: raise ValueError(f"Expect <int | tuple>, got <{type(ExitCode).__name__}>.")

        self.quit()
        self.destroy()

        self.Destroyed = True

        if Level == "Program":
            if isinstance(ExitCode, int):
                ExitMessage: str = "" ; ExitCode: int = ExitCode
            else:
                ExitMessage: str = ExitCode[1]; ExitCode: int = ExitCode[0]
            LogPrint(ExitMessage) if ExitMessage else None
            SysExit(ExitCode if isinstance(ExitCode, int) else ExitCode[0])

    """ --- 调试显示器 --- """
    def Debug_ShowZones(self, event: Event = None):
        pass

if __name__ == "__main__":
    root = EasyTk(True)
    root.geometry("1000x600+970+550")
    root.Run()

    