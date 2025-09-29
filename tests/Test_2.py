import tkinter as tk

root = tk.Tk()

# 配置网格，确保有足够的垂直空间
root.grid_rowconfigure(0, weight=1, minsize=100)
root.grid_columnconfigure(0, weight=1)

# 关键：只设置 sticky="e"，不要设置 "n" 或 "s"
label = tk.Label(root, text="垂直居中且靠右", bg="lightyellow")
label.grid(row=0, column=0, sticky="e")  # 仅 east

root.mainloop()