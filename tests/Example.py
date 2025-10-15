# from EasyTk.__Discard__ import EasyTk

# if __name__ == "__main__":
#     root = EasyTk(True)
#     root.geometry("1000x600+970+550")
#     root.Run()

# ----------------------------------------------------------------------------------------------------

from EasyTk import ezTk, ezFrame, ezFrameManager

from tkinter import Tk, Frame, Label, Entry, Text, Scrollbar, Listbox, Checkbutton, Radiobutton, StringVar, BooleanVar
from tkinter.ttk import Style, Button
# from typing import Literal, Callable

class UIInit:
    def __init__(self, root: Tk):
        self.root = root
        self.setup_styles()
        self.create_frame_manager()
        self.create_frames()
        
    def setup_styles(self):
        """设置现代化样式"""
        style = Style()
        
        # 配置现代化主题
        style.theme_use('clam')  # 使用clam主题，更现代化
        
        # 配置按钮样式
        style.configure('Modern.TButton',
                       padding=(20, 10),
                       font=('Segoe UI', 10),
                       background='#0078D4',
                       foreground='white')
        
        style.configure('Accent.TButton',
                       padding=(20, 10),
                       font=('Segoe UI', 10, 'bold'),
                       background='#005A9E',
                       foreground='white')
        
        # 配置标签样式
        style.configure('Title.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground='#323130')
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       foreground='#605E5C')
        
        # 配置框架样式
        style.configure('Card.TFrame',
                       background='#FFFFFF',
                       relief='raised',
                       borderwidth=1)
    
    def create_frame_manager(self):
        """创建帧管理器"""
        self.frame_manager = ezFrameManager(self.root)
        self.frame_manager.SwitchMode("tkraise")
    
    def create_frames(self):
        """创建两个页签帧"""
        # 主页帧
        self.home_frame = HomeFrame(self.frame_manager, "home")
        self.frame_manager.AddFrame(self.home_frame)
        
        # 详情页帧
        self.detail_frame = DetailFrame(self.frame_manager, "detail")
        self.frame_manager.AddFrame(self.detail_frame)
        
        # 默认显示主页
        self.frame_manager.Switch("home")

class HomeFrame(ezFrame):
    def UIInit(self):
        """主页UI初始化"""
        # 创建主框架
        self.Frame = Frame(self.master, name=self.name, 
                          bg='#F3F2F1', padx=40, pady=40)
        self.Frame.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        
        self.create_header()
        self.create_content()
        self.create_navigation()
    
    def create_header(self):
        """创建页眉"""
        header_frame = Frame(self.Frame, bg='#F3F2F1')
        header_frame.pack(fill='x', pady=(0, 30))
        
        # 标题
        title_label = Label(header_frame, 
                          text="现代化应用界面",
                          font=('Segoe UI', 24, 'bold'),
                          bg='#F3F2F1',
                          fg='#323130')
        title_label.pack(anchor='w')
        
        # 副标题
        subtitle_label = Label(header_frame,
                             text="欢迎使用现代化UI框架",
                             font=('Segoe UI', 12),
                             bg='#F3F2F1',
                             fg='#605E5C')
        subtitle_label.pack(anchor='w', pady=(5, 0))
    
    def create_content(self):
        """创建内容区域"""
        content_frame = Frame(self.Frame, bg='#F3F2F1')
        content_frame.pack(fill='both', expand=True)
        
        # 左侧卡片
        left_card = self.create_card(content_frame, "功能特性")
        left_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 右侧卡片
        right_card = self.create_card(content_frame, "快速操作")
        right_card.pack(side='right', fill='both', expand=True, padx=(10, 0))
    
    def create_card(self, parent, title):
        """创建卡片组件"""
        card = Frame(parent, bg='#FFFFFF', relief='raised', 
                    borderwidth=1, padx=20, pady=20)
        
        # 卡片标题
        card_title = Label(card, text=title,
                         font=('Segoe UI', 14, 'bold'),
                         bg='#FFFFFF',
                         fg='#323130')
        card_title.pack(anchor='w', pady=(0, 15))
        
        # 卡片内容
        if title == "功能特性":
            self.create_features_content(card)
        else:
            self.create_quick_actions(card)
            
        return card
    
    def create_features_content(self, parent):
        """创建功能特性内容"""
        features = [
            "• 现代化UI设计",
            "• 响应式布局",
            "• 多页签支持", 
            "• 丰富的控件",
            "• 自定义样式"
        ]
        
        for feature in features:
            feature_label = Label(parent, text=feature,
                                font=('Segoe UI', 10),
                                bg='#FFFFFF',
                                fg='#323130',
                                justify='left')
            feature_label.pack(anchor='w', pady=2)
    
    def create_quick_actions(self, parent):
        """创建快速操作"""
        actions = [
            ("查看详情", lambda: self.master.Switch("detail")),
            ("刷新数据", self.refresh_data),
            ("设置", self.open_settings)
        ]
        
        for text, command in actions:
            btn = Button(parent, text=text, command=command,
                           style='Modern.TButton')
            btn.pack(fill='x', pady=5)

    def create_navigation(self):
        """创建导航区域"""
        nav_frame = Frame(self.Frame, bg='#F3F2F1')
        nav_frame.pack(fill='x', pady=(20, 0))
        
        # 主要导航按钮
        next_btn = Button(nav_frame, 
                            text="前往详情页 →",
                            command=lambda: (self.master.Switch("detail"), self.master.master.Geometry.Size(1000, 1050)),
                            style='Accent.TButton')
        next_btn.pack(side='right', padx=(10, 0))
        
        home_btn = Button(nav_frame,
                            text="🏠 回到主页",
                            command=lambda: (self.master.Switch("home"), self.master.master.Geometry.Size(1000, 700)),
                            style='Modern.TButton')
        home_btn.pack(side='right')
    
    def refresh_data(self):
        """刷新数据"""
        print("数据已刷新")
    
    def open_settings(self):
        """打开设置"""
        print("打开设置")

class DetailFrame(ezFrame):
    def __init__(self, master: ezFrameManager, name: str, **kwargs: dict):
        super().__init__(master, name, **kwargs)
        self.selected_option = StringVar(value="option1")
        self.check_var = BooleanVar(value=True)
    
    def UIInit(self):
        """详情页UI初始化"""
        self.Frame = Frame(self.master, name=self.name, 
                          bg='#F3F2F1', padx=40, pady=40)
        self.Frame.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        self.create_header()
        self.create_form_section()
        self.create_text_section()
        self.create_interactive_section()
        self.create_navigation()
    
    def create_header(self):
        """创建页眉"""
        header_frame = Frame(self.Frame, bg='#F3F2F1')
        header_frame.pack(fill='x', pady=(0, 30))
        
        title_label = Label(header_frame, 
                          text="详情页面",
                          font=('Segoe UI', 20, 'bold'),
                          bg='#F3F2F1',
                          fg='#323130')
        title_label.pack(anchor='w')
        
        subtitle_label = Label(header_frame,
                             text="包含多种现代化控件的演示",
                             font=('Segoe UI', 11),
                             bg='#F3F2F1',
                             fg='#605E5C')
        subtitle_label.pack(anchor='w', pady=(5, 0))
    
    def create_form_section(self):
        """创建表单区域"""
        form_frame = Frame(self.Frame, bg='#FFFFFF', 
                          relief='raised', borderwidth=1,
                          padx=20, pady=20)
        form_frame.pack(fill='x', pady=(0, 20))
        
        # 表单标题
        form_title = Label(form_frame, text="表单输入",
                         font=('Segoe UI', 14, 'bold'),
                         bg='#FFFFFF',
                         fg='#323130')
        form_title.pack(anchor='w', pady=(0, 15))
        
        # 输入字段
        self.create_form_fields(form_frame)
    
    def create_form_fields(self, parent):
        """创建表单字段"""
        fields = [
            ("用户名:", "输入您的用户名"),
            ("邮箱:", "example@email.com"),
            ("密码:", "输入密码")
        ]
        
        for i, (label_text, placeholder) in enumerate(fields):
            field_frame = Frame(parent, bg='#FFFFFF')
            field_frame.pack(fill='x', pady=8)
            
            # 标签
            label = Label(field_frame, text=label_text,
                        font=('Segoe UI', 10),
                        bg='#FFFFFF',
                        fg='#323130',
                        width=10,
                        anchor='w')
            label.pack(side='left')
            
            # 输入框
            entry = Entry(field_frame, 
                         font=('Segoe UI', 10),
                         relief='solid',
                         borderwidth=1,
                         width=30)
            entry.insert(0, placeholder)
            entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
    
    def create_text_section(self):
        """创建文本区域"""
        text_frame = Frame(self.Frame, bg='#FFFFFF',
                          relief='raised', borderwidth=1,
                          padx=20, pady=20)
        text_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # 标题
        text_title = Label(text_frame, text="文本编辑器",
                         font=('Segoe UI', 14, 'bold'),
                         bg='#FFFFFF',
                         fg='#323130')
        text_title.pack(anchor='w', pady=(0, 15))
        
        # 文本框和滚动条
        text_widget = Text(text_frame,
                          height=8,
                          font=('Segoe UI', 10),
                          wrap='word',
                          relief='solid',
                          borderwidth=1)
        
        scrollbar = Scrollbar(text_frame, orient='vertical', 
                            command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 添加示例文本
        sample_text = """这是一个多行文本框的示例。
您可以在这里输入和编辑多行文本。

支持的功能：
• 文本编辑
• 滚动查看
• 自动换行"""
        text_widget.insert('1.0', sample_text)
    
    def create_interactive_section(self):
        """创建交互控件区域"""
        interactive_frame = Frame(self.Frame, bg='#F3F2F1')
        interactive_frame.pack(fill='x', pady=(0, 20))
        
        # 左侧：选择控件
        left_frame = Frame(interactive_frame, bg='#FFFFFF',
                          relief='raised', borderwidth=1,
                          padx=20, pady=20)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_selection_controls(left_frame)
        
        # 右侧：列表控件
        right_frame = Frame(interactive_frame, bg='#FFFFFF',
                           relief='raised', borderwidth=1,
                           padx=20, pady=20)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.create_list_controls(right_frame)
    
    def create_selection_controls(self, parent):
        """创建选择控件"""
        # 标题
        title = Label(parent, text="选择控件",
                    font=('Segoe UI', 12, 'bold'),
                    bg='#FFFFFF',
                    fg='#323130')
        title.pack(anchor='w', pady=(0, 15))
        
        # 单选按钮
        radio_frame = Frame(parent, bg='#FFFFFF')
        radio_frame.pack(fill='x', pady=(0, 15))
        
        radio_label = Label(radio_frame, text="选项:",
                          font=('Segoe UI', 10),
                          bg='#FFFFFF',
                          fg='#323130')
        radio_label.pack(anchor='w')
        
        options = [("选项一", "option1"), ("选项二", "option2"), ("选项三", "option3")]
        for text, value in options:
            radio = Radiobutton(radio_frame, text=text,
                              variable=self.selected_option,
                              value=value,
                              font=('Segoe UI', 9),
                              bg='#FFFFFF',
                              fg='#323130',
                              selectcolor='#E1E1E1')
            radio.pack(anchor='w', pady=2)
        
        # 复选框
        check = Checkbutton(parent, text="启用高级功能",
                          variable=self.check_var,
                          font=('Segoe UI', 10),
                          bg='#FFFFFF',
                          fg='#323130',
                          selectcolor='#E1E1E1')
        check.pack(anchor='w', pady=(10, 0))
        
        # 操作按钮
        action_btn = Button(parent, text="应用选择",
                              command=self.apply_selection,
                              style='Modern.TButton')
        action_btn.pack(anchor='w', pady=(15, 0))
    
    def create_list_controls(self, parent):
        """创建列表控件"""
        # 标题
        title = Label(parent, text="列表控件",
                    font=('Segoe UI', 12, 'bold'),
                    bg='#FFFFFF',
                    fg='#323130')
        title.pack(anchor='w', pady=(0, 15))
        
        # 列表框
        listbox = Listbox(parent,
                         height=6,
                         font=('Segoe UI', 10),
                         relief='solid',
                         borderwidth=1)
        
        # 添加示例项目
        items = ["项目 1", "项目 2", "项目 3", "项目 4", "项目 5", "项目 6"]
        for item in items:
            listbox.insert('end', item)
        
        listbox.pack(fill='both', expand=True)
        
        # 列表操作按钮
        btn_frame = Frame(parent, bg='#FFFFFF')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        add_btn = Button(btn_frame, text="添加",
                           command=self.add_list_item,
                           style='Modern.TButton')
        add_btn.pack(side='left', padx=(0, 5))
        
        remove_btn = Button(btn_frame, text="删除",
                              command=self.remove_list_item,
                              style='Modern.TButton')
        remove_btn.pack(side='left')
    
    def create_navigation(self):
        """创建导航区域"""
        nav_frame = Frame(self.Frame, bg='#F3F2F1')
        nav_frame.pack(fill='x')
        
        # 返回按钮
        back_btn = Button(nav_frame,
                            text="← 返回主页",
                            command=lambda: (self.master.Switch("home"), self.master.master.Geometry.Size(1000, 700)),
                            style='Modern.TButton')
        back_btn.pack(side='left')
        
        # 提交按钮
        submit_btn = Button(nav_frame,
                              text="提交表单",
                              command=self.submit_form,
                              style='Accent.TButton')
        submit_btn.pack(side='right')
    
    def apply_selection(self):
        """应用选择"""
        print(f"选中的选项: {self.selected_option.get()}")
        print(f"高级功能启用: {self.check_var.get()}")
    
    def add_list_item(self):
        """添加列表项"""
        print("添加列表项")
    
    def remove_list_item(self):
        """删除列表项"""
        print("删除列表项")
    
    def submit_form(self):
        """提交表单"""
        print("表单已提交")


# 主程序入口
if __name__ == "__main__":
    # 创建主窗口
    root = ezTk("现代化UI界面演示")
    
    # 设置窗口大小和位置
    root.Geometry.Size(1000, 700)
    root.Geometry.Pos(100, 100)
    
    # 创建现代化UI
    root.UIInit = UIInit
    
    # 运行应用
    root.Run()