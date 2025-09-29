from ctypes import windll
from enum import IntFlag
from typing import Literal

class WinStyles(IntFlag):
    """Windows 窗口样式标志 (Window Styles) """
    
    WS_OVERLAPPED = 0x00000000
    """创建一个重叠窗口(默认顶层窗口).通常与 WS_CAPTION 一起使用."""

    WS_POPUP = 0x80000000
    """创建一个弹出窗口(无边框、无标题栏，通常用于对话框或自定义窗口)."""

    WS_CHILD = 0x40000000
    """创建一个子窗口(必须有父窗口).不能与 WS_POPUP 同时使用."""

    WS_MINIMIZE = 0x20000000
    """创建时窗口最小化."""

    WS_VISIBLE = 0x10000000
    """创建后窗口可见."""

    WS_DISABLED = 0x08000000
    """禁用窗口(不响应用户输入)."""

    WS_CLIPSIBLINGS = 0x04000000
    """剪裁子窗口区域，防止绘制到其他同级窗口上(常用于 MDI 或复杂 UI)."""

    WS_CLIPCHILDREN = 0x02000000
    """父窗口绘制时不绘制到子窗口区域(提高性能)."""

    WS_CAPTION = 0x00C00000
    """创建标题栏"""

    WS_BORDER = 0x00800000
    """创建细边框(单像素边框，无标题栏)."""

    WS_SYSMENU = 0x00080000
    """在标题栏左侧显示系统菜单(关闭按钮等).必须与 `WS_CAPTION` 一起使用才有效."""

    WS_DLGFRAME = 0x00400000
    """创建对话框风格边框(无标题栏，但有系统菜单区域)."""

    WS_VSCROLL = 0x00200000
    """包含垂直滚动条."""

    WS_HSCROLL = 0x00100000
    """包含水平滚动条."""

    WS_THICKFRAME = 0x00040000
    """可调整大小的边框(也称 WS_SIZEBOX).允许用户拖动边框改变窗口大小."""

    WS_MAXIMIZE = 0x01000000
    """创建时窗口最大化."""

    WS_MINIMIZEBOX = 0x00020000
    """显示最小化按钮(必须与 `WS_SYSMENU` 一起使用)."""

    WS_MAXIMIZEBOX = 0x00010000
    """显示最大化按钮(必须与 `WS_SYSMENU` 一起使用)."""

    # 扩展样式 (通常用于 CreateWindowEx 的 dwExStyle 参数) 
    WS_EX_DLGMODALFRAME = 0x00000001
    """为窗口添加双线边框(即使没有 WS_CAPTION)."""

    WS_EX_NOPARENTNOTIFY = 0x00000004
    """子窗口创建/销毁时不通知父窗口."""

    WS_EX_TOPMOST = 0x00000008
    """窗口置顶(总在最前)."""

    WS_EX_ACCEPTFILES = 0x00000010
    """允许窗口接收拖放文件(需处理 WM_DROPFILES)."""

    WS_EX_TRANSPARENT = 0x00000020
    """窗口透明(鼠标事件穿透到下层窗口，不是视觉透明)."""

    WS_EX_MDICHILD = 0x00000040
    """MDI 子窗口(必须有 MDI 客户区父窗口)."""

    WS_EX_TOOLWINDOW = 0x00000080
    """工具窗口：不在任务栏显示，标题栏较小."""

    WS_EX_WINDOWEDGE = 0x00000100
    """带凸起边缘的边框(3D 效果)."""

    WS_EX_CLIENTEDGE = 0x00000200
    """客户区带凹陷边框(如 Edit 控件)."""

    WS_EX_CONTEXTHELP = 0x00000400
    """标题栏右侧显示“?”帮助按钮(与 WS_MAXIMIZEBOX 互斥)."""

    WS_EX_RIGHT = 0x00001000
    """窗口文本从右到左(用于阿拉伯语等)."""

    WS_EX_LEFT = 0x00000000
    """默认：文本从左到右."""

    WS_EX_RTLREADING = 0x00002000
    """标题栏文本从右到左显示."""

    WS_EX_LEFTSCROLLBAR = 0x00004000
    """垂直滚动条在左侧(用于 RTL 语言)."""

    WS_EX_CONTROLPARENT = 0x00010000
    """父窗口可处理子控件的 Tab 键导航(用于对话框)."""

    WS_EX_STATICEDGE = 0x00020000
    """静态 3D 边框(无交互效果)."""

    WS_EX_APPWINDOW = 0x00040000
    """强制窗口在任务栏显示(即使没有父窗口或为工具窗口)."""

    WS_EX_LAYERED = 0x00080000
    """支持分层窗口(用于透明、异形窗口，需配合 SetLayeredWindowAttributes 或 UpdateLayeredWindow)."""

    WS_EX_NOINHERITLAYOUT = 0x00100000
    """不继承父窗口的布局(如 RTL 设置)."""

    WS_EX_LAYOUTRTL = 0x00400000
    """使用 RTL 布局(Mirrored window)."""

    WS_EX_COMPOSITED = 0x02000000
    """使用双缓冲绘制(减少闪烁，但可能影响性能)."""

    WS_EX_NOACTIVATE = 0x08000000
    """窗口显示时不激活(如通知气泡)."""

    @classmethod
    def ReturnAll(cls) -> dict[str, int]:
        return {member.name: member.value for member in cls}

class WinStates(IntFlag):
    """Windows 窗口显示状态 (ShowWindow 命令) """
    
    SW_HIDE = 0
    """隐藏窗口"""

    SW_SHOWNORMAL = 1
    """激活并显示窗口(如果是第一次显示, 窗口会按原始大小和位置显示)"""

    SW_NORMAL = 1
    """同 SW_SHOWNORMAL"""

    SW_SHOWMINIMIZED = 2
    """激活窗口并将其最小化"""

    SW_SHOWMAXIMIZED = 3
    """激活窗口并将其最大化"""

    SW_MAXIMIZE = 3
    """同 SW_SHOWMAXIMIZED"""

    SW_SHOWNOACTIVATE = 4
    """显示窗口但不激活(不获取焦点)"""

    SW_SHOW = 5
    """显示窗口(如果是隐藏的), 但不改变其激活状态"""

    SW_MINIMIZE = 6
    """最小化窗口, 激活Z序中的下一个顶层窗口"""

    SW_SHOWMINNOACTIVE = 7
    """显示窗口为最小化状态, 但不激活"""

    SW_SHOWNA = 8
    """显示窗口(如果是隐藏的), 但不改变其激活状态(同 SW_SHOW)"""

    SW_RESTORE = 9
    """激活并显示窗口(如果是最小化或最大化状态, 恢复到原始大小和位置)"""

    SW_SHOWDEFAULT = 10
    """根据启动应用程序时指定的 STARTUPINFO 结构中的值来显示窗口"""

    SW_FORCEMINIMIZE = 11
    """强制最小化窗口(即使用户正在使用其他窗口)"""

    @classmethod
    def ReturnAll(cls) -> dict[str, int]:
        return {member.name: member.value for member in cls}

def ResetWindowStyle(HWND: int, mode: Literal["Basic", "UnTtlBar"] | list | tuple = "Basic"):
    """Reset or customize the window style of a given HWND.

    Args:
        HWND (int): Handle to the target window.
        mode (optional): 
            - "Basic": Apply default window style.
            - "UnTtlBar": Remove title bar and border.
            - (Style_New, ExStyle_New): Custom style tuple, e.g., (0x12345678, 0x87654321).
              Both values should be integers representing new window style and extended style.
            Defaults to "Basic".

    Examples:
        >>> ResetWindowStyle(hwnd, "UnTtlBar")
        >>> ResetWindowStyle(hwnd, (0x12345678, 0x87654321))
    """
    WINDLLU32 = windll.user32

    GWL_STYLE = -16
    GWL_EXSTYLE = -20
    
    # 获取样式
    Style_Current = WINDLLU32.GetWindowLongPtrW(HWND, GWL_STYLE)
    ExStyle_Current = WINDLLU32.GetWindowLongPtrW(HWND, GWL_EXSTYLE)
    
    Style_New = None
    ExStyle_New = None

    match mode:
        case "Basic":
            Style_New = (
                WinStyles.WS_OVERLAPPED |
                WinStyles.WS_CAPTION |
                WinStyles.WS_SYSMENU |
                WinStyles.WS_THICKFRAME |
                WinStyles.WS_MINIMIZEBOX |
                WinStyles.WS_MAXIMIZEBOX |
                WinStyles.WS_VISIBLE
            )
            ExStyle_New = (
                WinStyles.WS_EX_WINDOWEDGE |
                WinStyles.WS_EX_APPWINDOW
            )
        case "UnTtlBar":
            Style_New = (
                WinStyles.WS_VISIBLE
            )
            ExStyle_New = (
                WinStyles.WS_EX_APPWINDOW
            )
        case _:
            Style_New = mode[0]
            ExStyle_New = mode[1]

    # 设置样式
    WINDLLU32.SetWindowLongPtrW(HWND, GWL_STYLE, Style_New)
    WINDLLU32.SetWindowLongPtrW(HWND, GWL_EXSTYLE, ExStyle_New)

    # 重新激活窗口以应用样式
    WINDLLU32.ShowWindow(HWND, WinStates.SW_MINIMIZE)
    WINDLLU32.ShowWindow(HWND, WinStates.SW_RESTORE)

    return Style_Current, ExStyle_Current

if __name__ == "__main__":
    from tkinter import Tk, Button, Label, Entry, Checkbutton, Radiobutton, Scale, Listbox, Text, Spinbox, OptionMenu, Frame
    import tkinter.font as tkFont

    root: Tk = Tk()

    root.configure(bg="#6CA9E7")
    root.wm_overrideredirect(True)
    root.geometry("600x500")

    # 获取窗口句柄并重置样式
    WINDLLU32 = windll.user32
    HWND = root.winfo_id()
    root.update_idletasks()
    ResetWindowStyle(HWND, "UnTtlBar")
    

    # 添加大量控件（10+）
    Label(root, text="Label 示例", bg="#6CA9E7", fg="white", font=("Arial", 12)).pack(pady=5)
    
    Entry(root, width=30).pack(pady=5)
    
    Button(root, text="按钮 Button", command=lambda: print("Clicked!")).pack(pady=5)
    
    Checkbutton(root, text="复选框 Checkbutton", bg="#6CA9E7").pack(pady=5)
    
    Radiobutton(root, text="单选按钮1", variable="radio", value=1, bg="#6CA9E7").pack()
    Radiobutton(root, text="单选按钮2", variable="radio", value=2, bg="#6CA9E7").pack(pady=5)
    
    Scale(root, from_=0, to=100, orient="horizontal", bg="#6CA9E7").pack(pady=5)
    
    listbox = Listbox(root, height=4)
    for i in range(1, 6):
        listbox.insert("end", f"列表项 {i}")
    listbox.pack(pady=5)
    
    Text(root, height=3, width=40).pack(pady=5)
    
    Spinbox(root, from_=0, to=100, width=10).pack(pady=5)
    
    options = ["选项1", "选项2", "选项3"]
    OptionMenu(root, "选择", *options).pack(pady=5)
    
    frame = Frame(root, bg="lightgray", width=200, height=50)
    frame.pack(pady=10)
    frame.pack_propagate(False)
    Label(frame, text="Frame 容器", bg="lightgray").pack()

    

    root.mainloop()