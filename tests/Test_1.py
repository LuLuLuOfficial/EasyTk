import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Layout Example")
        self.root.geometry("600x200")
        
        # 创建主框架
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label1 - 固定宽度
        self.label1 = tk.Label(
            main_frame, 
            text="Label1", 
            bg="lightblue", 
            width=15,  # 固定字符宽度
            anchor="w"  # 左对齐
        )
        self.label1.pack(side=tk.LEFT, fill=tk.Y)
        
        # Label2 - 可变宽度，文本左对齐，可截断
        self.label2 = tk.Label(
            main_frame, 
            text="这是一个很长的文本内容，会根据窗口大小自动调整显示，超出部分会被截断显示...",
            bg="lightgreen",
            anchor="w",  # 文本左对齐
            justify="left"
        )
        self.label2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame包含三个按钮 - 固定宽度
        button_frame = tk.Frame(main_frame, bg="lightcoral")
        button_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # 三个按钮
        btn1 = tk.Button(button_frame, text="Btn1", width=8)
        btn1.pack(side=tk.LEFT, padx=(0, 5))
        
        btn2 = tk.Button(button_frame, text="Btn2", width=8)
        btn2.pack(side=tk.LEFT, padx=(0, 5))
        
        btn3 = tk.Button(button_frame, text="Btn3", width=8)
        btn3.pack(side=tk.LEFT)
        
        # 配置网格权重，确保Label2可以扩展
        # 由于使用pack布局，我们需要确保Label2的expand=True
        
        # 存储原始文本
        self.original_text = self.label2.cget("text")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()