# 导入tkinter库，这是Python的标准GUI工具包，用于创建图形用户界面
import tkinter as tk
# 导入ttk模块，提供了themed Tk widgets，是tkinter的扩展，提供更现代的界面组件，导入messagebox用于显示消息对话框，simpledialog用于创建简单的输入对话框
from tkinter import ttk, messagebox, simpledialog
# 导入json模块，用于处理JSON格式数据，在与Ollama API通信时解析和生成JSON数据
import json
# 导入requests库，用于发送HTTP请求，与Ollama服务器进行API通信
import requests
# 导入time库，用于显示时间
import time
# 导入webbrowser模块，用于打开系统默认浏览器
import webbrowser
# 导入re模块，用于正则表达式处理
import re

class OllamaGUI:
    def __init__(self, root):
        # 初始化方法，接收主窗口对象作为参数
        self.root = root
        # 设置应用程序窗口标题
        self.root.title("Ollama GUI操作界面")
        # 设置窗口初始大小为1200x800像素
        self.root.geometry("1200x800")
        # 禁止用户调整窗口大小，确保界面布局稳定
        self.root.resizable(False, False)
        
        # 计算屏幕尺寸，用于将窗口居中显示
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # 计算窗口左上角坐标，使窗口在屏幕中央显示
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        # 应用计算出的位置
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # 创建StringVar变量用于存储当前选择的模型名称
        self.selected_model = tk.StringVar()
        
        # 定义应用程序默认字体，使用微软雅黑16号字体
        self.default_font = ('Microsoft YaHei', 16)
        # 检查default_font是否已存在，如不存在则使用备用字体
        if not hasattr(self, 'default_font'):
            self.default_font = ('TkDefaultFont', 16)
        
        # 调用方法设置消息框样式，确保对话框文字显示正常
        self.setup_messagebox_style()
        
        # 设置Ollama服务器默认连接参数
        self.ip_address = "127.0.0.1"  # 默认本地IP地址
        self.port = "11434"  # Ollama服务的默认端口
        # 初始化对话历史记录列表，用于存储聊天内容
        self.conversation_history = []
        
        # 调用方法设置全局UI样式，统一界面风格
        self.setup_styles()
        
        # 调用方法构建完整GUI界面
        self.setup_gui()
# 这段代码是OllamaGUI类的初始化方法，负责设置应用程序的基本参数、窗口属性、默认值和界面样式。它为整个应用程序奠定了基础，包括窗口大小、位置、字体设置、服务器连接参数等，并调用其他方法来完成界面的构建。
    
    def setup_styles(self):
        # 创建ttk样式对象，用于统一配置应用程序中所有ttk组件的外观
        style = ttk.Style()
        
        # 设置全局默认字体为微软雅黑16号，应用于所有ttk组件
        # '.'表示应用于所有ttk组件的基础样式
        style.configure('.', font=('Microsoft YaHei', 16))
        
        # 配置选项卡(Notebook)的标签样式
        # 设置内边距为左右20像素、上下5像素，前景色为黑色，背景色为白色
        style.configure('TNotebook.Tab', 
                       padding=[20, 5],
                       foreground='black',
                       background='white')
        
        # 为选项卡设置不同状态下的样式映射
        # 选中状态前景色为黑色，未选中状态为灰色
        # 选中状态字体为微软雅黑16号加粗，未选中状态为普通微软雅黑16号
        style.map('TNotebook.Tab',
                 foreground=[('selected', 'black'), ('!selected', 'gray')],
                 font=[('selected', ('Microsoft YaHei', 16, 'bold')), 
                       ('!selected', ('Microsoft YaHei', 16))])
        
        # 配置标签框架样式，设置内边距为10像素
        style.configure('TLabelframe', padding=10)
        
        # 配置标准按钮样式，设置内边距为5像素
        style.configure('TButton', padding=5)
        
        # 配置发送按钮特殊样式，水平内边距为1像素，垂直内边距为3像素
        style.configure('SendButton.TButton', padding=(1, 3))
        
        # 配置输入框样式（无特殊设置，使用默认配置）
        style.configure('TEntry')
        
        # 配置下拉框样式（无特殊设置，使用默认配置）
        style.configure('TCombobox')
        
        # 配置树状视图样式，设置行高为35像素，使内容更易读
        style.configure('Treeview', rowheight=35)
        
        # 配置树状视图表头样式，设置字体为微软雅黑16号
        style.configure('Treeview.Heading', font=('Microsoft YaHei', 16))
        
        # 再次配置按钮样式，确保使用默认字体和5像素内边距
        # 这是为了覆盖可能的样式冲突
        style.configure('TButton', font=self.default_font, padding=5)
        
        # 再次配置发送按钮样式，确保使用默认字体和特定内边距
        style.configure('SendButton.TButton', font=self.default_font, padding=(1, 3))
        
        # 配置标签样式，设置字体为默认字体
        style.configure('TLabel', font=self.default_font)
        
        # 配置输入框样式，设置字体为TkDefaultFont 16号
        style.configure('TEntry', font=("TkDefaultFont", 16))
        
        # 配置下拉框样式，设置字体为TkDefaultFont 16号
        style.configure('TCombobox', font=("TkDefaultFont", 16))
# 这个方法负责设置应用程序的整体视觉风格，确保所有界面元素具有一致的外观。它通过ttk.Style对象配置各种组件的样式属性。

    def setup_messagebox_style(self):
        # 配置应用程序中所有消息对话框的显示样式和行为
        # 设置对话框文本使用默认字体，确保消息文本清晰易读
        self.root.option_add('*Dialog.msg.font', self.default_font)
        # 设置消息文本在300像素宽度处自动换行，防止对话框过宽影响用户体验
        self.root.option_add('*Dialog.msg.wrapLength', '300')
# 这个方法负责统一设置应用程序中所有消息对话框（如错误提示、警告框、确认框等）的显示样式。通过tkinter的option_add机制，它为所有对话框设置了统一的字体和文本换行规则，确保无论在应用程序的哪个部分弹出对话框，都能保持一致的视觉效果和良好的可读性。统一的样式设置有助于提升整体用户体验和界面美观度。

    def setup_gui(self):
        # 初始化主界面布局，创建选项卡控件作为主要容器
        # ttk.Notebook提供多页面切换功能，fill='both'和expand=True使其填充整个窗口
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 初始化第一个选项卡：模型对话页面
        # 创建专用的Frame容器用于存放对话界面的组件
        self.chat_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.chat_frame, text='模型对话')
        self.setup_chat_page()  # 调用专门的方法设置对话页面的详细内容
        
        # 初始化第二个选项卡：模型操作页面
        # 创建专用的Frame容器用于存放模型管理界面的组件
        self.operation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.operation_frame, text='模型操作')
        self.setup_operation_page()  # 调用专门的方法设置操作页面的详细内容
        
        # 为选项卡切换事件绑定回调函数
        # 当用户切换标签页时，触发on_tab_changed方法执行相应的操作
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
#  这个方法是GUI界面的核心构建方法，负责创建应用程序的主要布局结构。它使用ttk.Notebook组件实现了一个双页面的标签页界面，分别用于模型对话和模型操作两个主要功能。通过事件绑定机制，它还能够在用户切换页面时自动更新相关内容。

    def on_tab_changed(self, event):
        # 标签页切换事件处理方法，当用户在界面上切换标签页时自动触发
        # 参数event包含了标签页切换的相关信息
        current_tab = self.notebook.index("current")
        
        # 判断用户是否切换到了模型操作页面
        # notebook.index("current")返回当前选中标签页的索引值
        # 索引值1对应模型操作页面，0对应模型对话页面
        if current_tab == 1:
            # 自动刷新并显示当前系统中已安装的模型列表
            self.list_models()
# 这个方法是一个事件处理器，负责处理标签页（Tab）切换时的逻辑。它通过监听ttk.Notebook的标签页切换事件，在用户切换到模型操作页面时自动刷新模型列表，确保用户始终能看到最新的模型信息。这种自动刷新机制提高了用户体验，避免了用户需要手动刷新模型列表的麻烦。
    
    def setup_chat_page(self):
        # 构建聊天页面的服务器配置区域
        # 创建带标题的LabelFrame作为服务器配置的容器
        config_frame = ttk.LabelFrame(self.chat_frame, text='服务器配置')
        config_frame.pack(fill='x', padx=10, pady=(5, 10))  # 水平填充并设置边距
        
        # 使用网格布局管理服务器配置的具体内容
        grid_frame = ttk.Frame(config_frame)
        grid_frame.pack(fill='x', padx=5, pady=5)
        
        # 第一行：配置IP地址和端口输入区域
        # IP地址输入框及其标签
        ttk.Label(grid_frame, text='IP地址:').grid(row=0, column=0, padx=(0,5), pady=5, sticky='e')
        self.ip_entry = ttk.Entry(grid_frame, width=30, font=("TkDefaultFont", 16))
        self.ip_entry.insert(0, self.ip_address)  # 设置默认IP地址
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # 端口输入框及其标签
        ttk.Label(grid_frame, text='端口:').grid(row=0, column=2, padx=(20,5), pady=5, sticky='e')
        self.port_entry = ttk.Entry(grid_frame, width=8, font=("TkDefaultFont", 16))
        self.port_entry.insert(0, self.port)  # 设置默认端口号
        self.port_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        # 版本查询按钮
        version_button = ttk.Button(grid_frame, text='Ollama版本号', command=self.show_version_in_chat)
        version_button.grid(row=0, column=4, padx=(20,0), pady=5, sticky='e')
        
        # 第二行：模型选择区域
        # 模型选择下拉框及其标签
        ttk.Label(grid_frame, text='模型:').grid(row=1, column=0, padx=(0,5), pady=5, sticky='e')
        self.model_combobox = ttk.Combobox(grid_frame, textvariable=self.selected_model, 
                                          width=30, state='readonly', font=("TkDefaultFont", 16))
        self.model_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # 刷新模型列表按钮
        refresh_button = ttk.Button(grid_frame, text='刷新模型列表', command=self.refresh_models)
        refresh_button.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
        # 设置网格布局最后一列的权重，使其自动扩展
        grid_frame.grid_columnconfigure(4, weight=1)
        
        # 初始化模型列表
        self.refresh_models()
        
        # 构建聊天消息显示区域
        chat_area = ttk.Frame(self.chat_frame)
        chat_area.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 创建聊天消息显示文本框，配备垂直滚动条
        chat_scroll = ttk.Scrollbar(chat_area)
        chat_scroll.pack(side='right', fill='y')
        
        # 聊天文本框初始化为禁用状态，防止用户直接编辑
        self.chat_text = tk.Text(chat_area, height=15, font=self.default_font, 
                                state='disabled', yscrollcommand=chat_scroll.set)
        self.chat_text.pack(fill='both', expand=True)
        chat_scroll.config(command=self.chat_text.yview)
        
        # 构建用户输入区域
        input_frame = ttk.Frame(self.chat_frame)
        input_frame.pack(fill='x', padx=10, pady=(5, 10))
        
        # 创建左侧输入框容器
        input_left_frame = ttk.Frame(input_frame)
        input_left_frame.pack(side='left', fill='both', expand=True)
        
        # 创建用户输入文本框的滚动条
        input_scroll = ttk.Scrollbar(input_left_frame)
        input_scroll.pack(side='right', fill='y')
        
        # 创建输入文本框并正确关联滚动条
        self.input_text = tk.Text(input_left_frame, height=4, font=self.default_font,
                                 yscrollcommand=input_scroll.set, wrap='word')
        self.input_text.pack(side='left', fill='both', expand=True)
        input_scroll.config(command=self.input_text.yview)
        

        # 创建发送按钮并应用蓝色样式
        send_button = tk.Button(input_frame, text="发送", command=self.send_message,
                              width=8, bg='#B0E2FF', fg='white', relief='raised',
                              font=self.default_font)
        send_button.pack(side='right', padx=5, pady=(0, 5), ipady=2)
        
        # 创建自定义按钮样式
        style = ttk.Style()
        style.configure('Custom.TButton', 
                       padding=(5, 2),  # 内边距调整
                       relief='raised',  # 凸起效果
                       borderwidth=2)    # 边框宽度

        # 修改回车键事件绑定
        self.input_text.bind('<Return>', lambda event: self.handle_enter(event))
# 这个方法负责构建聊天界面的整体布局，包括三个主要部分：
# 1. 服务器配置区域：用于设置Ollama服务器的连接参数和模型选择
# 2. 聊天消息显示区域：展示用户与AI模型的对话内容
# 3. 用户输入区域：供用户输入消息的文本框
# 通过设计的网格布局和合理的组件配置，确保了界面的美观性和易用性。每个组件都配备了适当的字体大小和间距，并且通过滚动条支持长文本的显示和输入。

    def setup_operation_page(self):
        # 创建模型操作页面的主要布局框架
        # 左侧框架用于显示模型列表，只在垂直方向填充
        left_frame = ttk.Frame(self.operation_frame)
        left_frame.pack(side='left', fill='y', padx=5, pady=5)

        # 右侧框架用于显示操作结果，需要在两个方向都填充并自动扩展
        right_frame = ttk.Frame(self.operation_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        # === 构建左侧区域组件 ===
        # 创建刷新按钮的容器框架
        list_button_frame = ttk.Frame(left_frame)
        list_button_frame.pack(pady=5)
        
        # 添加刷新按钮，点击时触发list_models方法更新模型列表
        ttk.Button(list_button_frame, text='列出模型', command=self.list_models).pack(fill='x')
        
        # 创建模型列表显示区域的容器，包含表格和滚动条
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 创建垂直滚动条，用于长列表的滚动显示
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_y.pack(side='right', fill='y')
        
        # 创建Treeview表格组件，用于展示模型的详细信息
        # show='headings'用于隐藏默认的树形图标列
        self.model_tree = ttk.Treeview(tree_frame, columns=('名称', '大小', '修改时间'), 
                                      show='headings', yscrollcommand=tree_scroll_y.set)
        
        # 配置表格的三个列标题
        self.model_tree.heading('名称', text='名称')
        self.model_tree.heading('大小', text='大小')
        self.model_tree.heading('修改时间', text='修改时间')
        
        # 设置各列的宽度和对齐方式
        self.model_tree.column('名称', width=400)  # 名称列宽度较大
        self.model_tree.column('大小', width=180, anchor='e')  # 大小列右对齐
        self.model_tree.column('修改时间', width=200, anchor='e')  # 时间列右对齐
        self.model_tree.pack(fill='both', expand=True)
        
        # 将滚动条与Treeview的垂直滚动关联
        tree_scroll_y.config(command=self.model_tree.yview)

        # === 构建右侧区域组件 ===
        # 创建操作按钮区域的容器框架
        right_buttons_frame = ttk.Frame(right_frame)
        right_buttons_frame.pack(fill='x', pady=5)

        # 定义模型管理的操作按钮配置
        # 每个元组包含按钮显示文本和对应的处理方法
        operations = [
            ('拉取模型', self.pull_model),    # 用于下载新的AI模型
            ('删除模型', self.delete_model)    # 用于移除已安装的模型
        ]
        
        # 动态创建操作按钮并设置布局
        for text, command in operations:
            ttk.Button(right_buttons_frame, text=text, command=command).pack(
                side='left',     # 按钮左对齐排列
                fill='x',        # 水平方向填充
                padx=5,          # 水平间距5像素
                expand=True      # 允许按钮扩展占用可用空间
            )
        
        # 创建操作结果显示区域的容器框架
        result_frame = ttk.Frame(right_frame)
        result_frame.pack(fill='both', expand=True, padx=5, pady=5)  # 双向填充并扩展
        
        # 创建垂直滚动条组件
        result_scroll_y = ttk.Scrollbar(result_frame)
        result_scroll_y.pack(side='right', fill='y')  # 右侧垂直填充
                
        # 创建文本显示区域
        # height=20：显示20行文本
        # wrap='none'：禁用自动换行
        # yscrollcommand和xscrollcommand：关联滚动条
        self.result_text = tk.Text(result_frame, height=20, font=self.default_font,
                                  yscrollcommand=result_scroll_y.set,
                                  wrap='word')
        self.result_text.pack(fill='both', expand=True)
        
        # 配置垂直滚动条
        result_scroll_y.config(command=self.result_text.yview)
# 这段代码是模型操作页面布局的核心部分，主要实现了以下功能：
# 1. 创建左右分栏布局，提供清晰的视觉分区
# 2. 左侧区域包含：
#    - 刷新按钮：用于更新模型列表
#    - 模型列表表格：使用Treeview组件展示模型信息，包含名称、大小和修改时间三列
#    - 垂直滚动条：支持长列表的浏览
# 3. 右侧区域为操作区，初始化顶部按钮容器框架
# 4. 操作按钮区：提供模型管理的核心功能按钮（拉取和删除模型）
# 5. 结果显示区：使用可滚动的文本框展示操作结果和进度信息
#    - 支持垂直和水平滚动，适合显示长文本和宽文本
#    - 使用统一的字体样式，确保显示效果的一致性
#    - 文本框禁用自动换行，保证长文本的完整显示
# 通过这种设计，用户可以方便地执行模型管理操作，并实时查看操作的执行状态和结果。

    def custom_message_box(self, message):
        # 创建一个自定义的模态对话框，用于显示提示信息
        # 参数message: 需要显示的提示文本内容
        dialog = tk.Toplevel(self.root)  # 创建顶层窗口作为对话框
        dialog.title("提示")  # 设置对话框标题
        
        # 获取主窗口在屏幕上的位置和尺寸信息
        window_x = self.root.winfo_x()      # 主窗口左上角的X坐标
        window_y = self.root.winfo_y()      # 主窗口左上角的Y坐标
        window_width = self.root.winfo_width()   # 主窗口的宽度
        window_height = self.root.winfo_height() # 主窗口的高度
        
        # 定义对话框的固定尺寸
        dialog_width = 300    # 对话框宽度
        dialog_height = 150   # 对话框高度
        
        # 计算对话框在主窗口中居中显示的坐标
        dialog_x = window_x + (window_width - dialog_width) // 2   # 对话框左上角X坐标
        dialog_y = window_y + (window_height - dialog_height) // 2 # 对话框左上角Y坐标
        
        # 设置对话框的大小和位置
        dialog.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")
        
        # 设置对话框的模态属性
        dialog.transient(self.root)  # 将对话框设置为主窗口的临时窗口
        dialog.grab_set()  # 将输入焦点锁定在对话框上，使其他窗口无法操作
        
        # 创建显示消息的标签控件
        label = tk.Label(dialog, text=message, 
                        font=self.default_font,  # 使用默认字体
                        wraplength=250)  # 设置文本自动换行宽度
        label.pack(expand=True, pady=20)  # 居中显示并设置垂直间距
        
        # 创建确定按钮
        button = ttk.Button(dialog, text="确定", 
                           command=dialog.destroy)  # 点击时关闭对话框
        button.pack(pady=10)  # 设置按钮的垂直间距
        
        # 等待对话框被关闭后再继续执行
        self.root.wait_window(dialog)
# 这个方法实现了一个自定义的消息对话框，主要功能和特点：
# 1. 创建一个模态对话框，显示提示信息
# 2. 对话框总是相对于主窗口居中显示
# 3. 具有模态特性，显示时会阻止用户与主窗口交互
# 4. 提供了统一的视觉风格，包括字体、大小和布局
# 5. 支持消息文本自动换行，适应不同长度的提示内容
# 6. 包含一个确定按钮，点击后关闭对话框
# 自定义对话框的设计比系统默认的消息框更灵活，可以更好地控制显示效果和用户交互体验。

    def refresh_models(self):
        # 从界面输入框获取Ollama服务器的连接信息
        ip = self.ip_entry.get().strip()    # 获取并清理IP地址的空白字符
        port = self.port_entry.get().strip() # 获取并清理端口号的空白字符
        
        try:
            # 根据不同的IP地址格式智能构建API基础URL
            # 处理本地服务器地址的多种形式
            if ip.lower() == 'localhost' or ip.lower() == 'http://localhost' or ip.lower() == 'https://localhost':
                base_url = f"http://localhost:{port}"
            # 处理已包含HTTP协议头的地址
            elif ip.startswith('http://') or ip.startswith('https://'):
                base_url = ip
                # 如果URL中没有指定端口且不是默认80端口，则添加端口号
                if ':' not in ip.split('//')[1] and port != '80':
                    base_url = f"{ip}:{port}"
            # 处理标准IPv4地址格式（如192.168.1.1）
            elif ip.replace(".", "").isdigit() and len(ip.split(".")) == 4:
                base_url = f"http://{ip}:{port}"
            # 处理其他格式的地址
            else:
                base_url = f"http://{ip}:{port}" if ":" in ip else f"http://{ip}"
            
            # 调用Ollama API获取已安装的模型列表
            url = f"{base_url}/api/tags"
            response = requests.get(url)      # 发送GET请求
            response.raise_for_status()       # 检查请求是否成功
            models = response.json().get('models', [])  # 解析JSON响应获取模型列表
            
            # 处理获取到的模型列表数据
            model_names = [model['name'] for model in models]  # 提取所有模型的名称
            model_names.sort()  # 按字母顺序对模型名称进行排序
            self.model_combobox['values'] = model_names  # 更新下拉列表的选项
            
            # 自动选择第一个可用的模型
            if model_names:
                self.model_combobox.set(model_names[0])
            
        except Exception as e:
            # 发生错误时的异常处理
            messagebox.showerror("错误", f"获取模型列表失败: {str(e)}")  # 显示错误对话框
            # 设置默认值，确保界面可用性
            self.model_combobox['values'] = ["llama2"]  # 设置默认模型选项
            self.model_combobox.set("llama2")          # 选择默认模型
# 这个方法的主要功能是刷新和更新可用的AI模型列表，具体实现了以下功能：
# 1. 智能处理多种服务器地址格式，支持本地服务器、HTTP/HTTPS地址、IPv4地址等
# 2. 通过API获取Ollama服务器上已安装的模型列表
# 3. 对获取到的模型列表进行处理和排序
# 4. 更新界面上的模型选择下拉框
# 5. 包含完善的错误处理机制，确保即使在出错情况下界面也能正常工作
# 6. 自动选择默认模型，提供良好的用户体验
# 这个方法在以下情况下会被调用：
# - 程序启动时初始化模型列表
# - 用户手动点击刷新按钮时
# - 完成模型安装或删除操作后需要更新列表时

    def get_selected_model(self):
        # 从下拉列表框(Combobox)获取用户当前选择的AI模型名称
        # self.model_combobox是在界面初始化时创建的ttk.Combobox组件
        selected = self.model_combobox.get()
        # 如果没有选择任何模型（返回空字符串），则返回默认值"qwq"
        # 使用三元运算符简化if-else逻辑
        return selected if selected else "qwq"
# 这个方法的主要功能是：
# 1. 提供一个简单的接口来获取用户在界面上当前选择的AI模型名称
# 2. 通过访问Combobox组件的值来获取选择的模型名称
# 3. 包含默认值处理机制，确保即使用户没有选择模型也能返回一个有效值
# 4. 主要被其他需要获取当前选择模型的功能模块调用，如聊天功能或模型操作功能
# 该方法设计简单但很实用，确保了程序在任何情况下都能获取到有效的模型名称，提高了程序的健壮性
    
    def list_models(self):
        # 从界面输入框获取Ollama服务器的连接参数
        ip = self.ip_entry.get().strip()    # 获取并清理IP地址的空白字符
        port = self.port_entry.get().strip() # 获取并清理端口号的空白字符
        
        try:
            # 构建并发送HTTP GET请求获取模型列表
            url = f"http://{ip}:{port}/api/tags"  # 构建Ollama API的URL端点
            response = requests.get(url)          # 发送GET请求获取模型列表
            response.raise_for_status()           # 检查HTTP响应状态，如果不是200则抛出异常
            
            # 解析服务器返回的JSON数据
            data = response.json()               # 将响应内容解析为Python字典
            models = data.get('models', [])      # 提取模型列表，如果不存在则返回空列表
            
            # 处理没有找到模型的情况
            if not models:
                # 在结果文本框中显示提示信息
                self.result_text.insert(tk.END, "没有找到可用的模型\n")
                return
            
            # 导入datetime模块用于处理时间戳
            from datetime import datetime
            
            # 定义内部函数用于解析ISO格式的时间字符串
            def parse_time(time_str):
                try:
                    # 将ISO格式时间字符串转换为datetime对象
                    # 处理UTC时区标识'Z'，将其替换为Python支持的'+00:00'格式
                    return datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    # 时间解析失败时返回Unix纪元时间作为默认值
                    return datetime(1970, 1, 1)
            
            # 对模型列表按照模型名称进行升序排序
            # 使用lambda函数获取每个模型的name属性并进行字符串比较
            models.sort(key=lambda model: model.get('name', '').lower())

            # 清理界面上的模型列表显示
            # 遍历并删除Treeview组件中的所有现有项目
            for item in self.model_tree.get_children():
                self.model_tree.delete(item)

            # 遍历处理每个模型的信息并添加到界面显示
            for model in models:
                # 获取模型名称，如果不存在则返回None
                name = model.get('name')
                
                # 处理模型大小信息
                size = model.get('size', 0)  # 获取模型大小，默认为0
                # 将字节大小转换为KB单位，如果size不是数字类型则显示'N/A'
                size_kb = size / 1024 if isinstance(size, (int, float)) else 'N/A'
                # 格式化大小显示，添加千位分隔符
                if isinstance(size_kb, (int, float)):
                    size_str = "{:,}kB".format(int(size_kb))  # 格式化为带千位分隔符的KB值
                else:
                    size_str = size_kb  # 保持'N/A'的显示
                
                # 处理模型修改时间信息
                modified_at = model.get('modified_at', 'N/A')  # 获取修改时间，默认为'N/A'
                try:
                    # 导入datetime用于时间处理
                    from datetime import datetime
                    # 将ISO格式时间字符串转换为datetime对象
                    # 处理UTC时区标识'Z'，转换为Python支持的格式
                    dt = datetime.fromisoformat(modified_at.replace('Z', '+00:00'))
                    # 将时间格式化为年/月/日 时:分格式
                    modified_at_str = dt.strftime('%Y/%m/%d %H:%M')
                except (ValueError, AttributeError):
                    # 时间格式转换失败时保持原始值
                    modified_at_str = modified_at

                # 将处理后的模型信息添加到Treeview控件中显示
                # 参数说明：
                # ''：父节点为根节点
                # 'end'：插入到末尾
                # values：包含要显示的所有列的值元组
                self.model_tree.insert('', 'end', values=(name, size_str, modified_at_str))
                
        # 异常处理：捕获并显示在获取模型列表过程中可能出现的错误
        except Exception as e:
            # 在结果文本框中显示错误信息
            self.result_text.insert(tk.END, f"错误: {str(e)}\n")
            # 弹出错误对话框显示详细错误信息
            messagebox.showerror("错误", f"获取模型列表失败: {str(e)}")
#  list_models 方法主要实现以下功能：
# 1. 获取服务器连接信息并发送API请求
# 2. 解析服务器返回的模型数据
# 3. 实现模型列表的时间排序功能
# 4. 准备更新GUI界面显示
# 5. 格式化和显示模型信息
# 6. 处理模型大小的单位转换和格式化
# 7. 处理时间戳的格式转换
# 8. 将处理后的信息添加到界面的树形视图中
# 9. 提供完善的错误处理机制
# 该方法的设计特点：
# 1. 使用异常处理确保程序稳定性
# 2. 实现了自定义的时间解析逻辑
# 3. 支持按时间排序的模型列表管理
# 4. 数据处理健壮性高，能处理各种异常情况
# 5. 时间和大小的显示格式统一规范
# 6. 使用try-except确保程序稳定运行
# 7. 提供友好的错误提示机制
# 这部分代码为后续的模型信息显示做好数据准备工作。
    
    def pull_model(self):
        # pull_model方法：负责处理模型下载功能的核心方法
        # 从输入框获取Ollama服务器连接信息
        ip = self.ip_entry.get().strip()    # 获取并清理IP地址字符串
        port = self.port_entry.get().strip() # 获取并清理端口号字符串
        
        while True:
            # 创建模型下载的输入界面
            # 使用Toplevel创建模态对话框，确保用户完成输入前不能操作主窗口
            dialog = tk.Toplevel(self.root)
            dialog.title("拉取模型")         # 设置对话框标题
            dialog.geometry("500x350")       # 增加对话框高度，从300改为350
            
            # 计算对话框在主窗口中的居中位置
            window_x = self.root.winfo_x()        # 主窗口X坐标
            window_y = self.root.winfo_y()        # 主窗口Y坐标
            window_width = self.root.winfo_width()    # 主窗口宽度
            window_height = self.root.winfo_height()  # 主窗口高度
            # 计算对话框左上角坐标，使其在主窗口中居中显示
            dialog_x = window_x + (window_width - 500) // 2
            dialog_y = window_y + (window_height - 350) // 2  # 调整Y坐标计算
            dialog.geometry(f"+{dialog_x}+{dialog_y}")  # 应用计算出的位置

            # 创建对话框的内容区域
            content_frame = ttk.Frame(dialog)  # 使用Frame组织对话框内容

            # 设置内容区域的填充和扩展属性
            content_frame.pack(padx=20, pady=20, fill='both', expand=True)
            
            # 创建提示标签
            label = ttk.Label(content_frame, text="请输入要拉取的模型名称：", font=self.default_font)
            label.pack(pady=(10, 5))  # 设置标签上下间距

            # 创建模型名称输入框
            entry = ttk.Entry(content_frame, font=self.default_font, width=40)
            entry.pack(pady=5, ipady=5)
            
            # 创建按钮容器
            button_frame = ttk.Frame(content_frame)
            button_frame.pack(pady=15)
            
            # 定义模型名称变量和确认回调函数
            model_name = None  # 存储用户输入的模型名称
            def on_confirm():
                # 确认按钮的回调函数
                nonlocal model_name  # 使用nonlocal访问外层作用域的变量
                model_name = entry.get().strip()  # 获取并清理输入的模型名称
                if model_name:  # 只有当输入不为空时才关闭对话框
                    dialog.destroy()  # 关闭对话框
                else:
                    messagebox.showwarning("警告", "请输入模型名称！")

            # 创建确认和取消按钮
            confirm_button = ttk.Button(button_frame, text="确认拉取", command=on_confirm)
            confirm_button.pack(side='left', padx=(0, 10))
            
            cancel_button = ttk.Button(button_frame, text="取消", command=dialog.destroy)
            cancel_button.pack(side='left')
            
            # 添加模型名称示例标签
            example_label = ttk.Label(content_frame, 
                                    text="模型名称示例：gemma3:27b", 
                                    font=(self.default_font[0], self.default_font[1]-2),
                                    foreground='#555555')
            example_label.pack(pady=(5, 10))

            # 添加分隔线
            separator = ttk.Separator(content_frame, orient='horizontal')
            separator.pack(fill='x', pady=10)
            
            # 添加Ollama官网链接（放在底部）
            link_label = ttk.Label(content_frame, 
                                text="访问 Ollama 官网查看可用模型",
                                font=(self.default_font[0], self.default_font[1], 'underline'),
                                foreground='blue',
                                cursor='hand2')
            link_label.pack(pady=(5, 10))
            
            # 绑定点击事件
            # 定义点击链接时的回调函数
            # 参数event：鼠标点击事件对象，包含点击的详细信息
            def open_ollama_website(event):
                # 使用系统默认浏览器打开Ollama官方网站
                webbrowser.open('https://ollama.ai')
            
            # 将鼠标左键点击事件（<Button-1>）绑定到链接标签上
            # 当用户点击链接时，会调用open_ollama_website函数
            link_label.bind('<Button-1>', open_ollama_website)
            
            # 配置模型名称输入对话框的模态特性
            dialog.transient(self.root)      # 将对话框设置为主窗口的从属窗口，确保对话框始终显示在主窗口之上
            dialog.grab_set()                # 设置输入焦点锁定，阻止用户与其他窗口交互
            dialog.wait_window()             # 暂停程序执行，等待对话框关闭
            
            # 检查用户输入，如果用户未输入模型名称或点击取消，则终止操作
            if not model_name:
                return

            # 验证模型是否已存在的处理流程
            try:
                # 构建API请求URL，用于获取已安装模型列表
                check_url = f"http://{ip}:{port}/api/tags"
                # 发送HTTP GET请求获取模型列表
                response = requests.get(check_url)
                # 从响应JSON中提取模型名称列表，如果'models'键不存在则返回空列表
                existing_models = [m['name'] for m in response.json().get('models', [])]
                
                # 检查用户要下载的模型是否已在系统中
                if model_name in existing_models:
                    # 如果模型已存在，显示警告对话框并继续循环让用户重新输入
                    messagebox.showwarning("警告", f"模型 {model_name} 已存在！")
                    continue
                # 模型不存在，跳出循环继续执行下载流程

                # 创建下载进度显示窗口
                progress_dialog = tk.Toplevel(self.root)
                progress_dialog.title("拉取进度")  # 设置进度窗口标题
                break
            except Exception as e:
                # 捕获并处理验证过程中的所有异常
                messagebox.showerror("错误", f"验证模型失败: {str(e)}")
                return
        
        # 获取主窗口的位置信息，用于计算进度窗口的位置
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # 定义进度窗口的固定尺寸
        dialog_width = 750
        dialog_height = 150
        
        # 计算进度窗口在主窗口中的居中显示位置
        dialog_x = window_x + (window_width - dialog_width) // 2
        dialog_y = window_y + (window_height - dialog_height) // 2
        
        # 设置进度对话框的位置和大小
        progress_dialog.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")        
        # 配置进度对话框的窗口属性
        progress_dialog.transient(self.root)  # 将进度对话框设置为主窗口的子窗口，跟随主窗口最小化和移动
        progress_dialog.grab_set()  # 锁定用户输入焦点在进度对话框上，阻止与其他窗口的交互

        # 创建并配置进度显示标签组件
        progress_label = ttk.Label(progress_dialog, text="正在连接服务器...")  # 创建初始状态提示标签
        progress_label.pack(pady=5)  # 设置标签的垂直间距
        
        # 创建并配置进度条组件
        progress = ttk.Progressbar(progress_dialog, mode='determinate', length=730)  # 创建确定模式的进度条
        progress.pack(pady=15)  # 设置进度条的垂直间距

        # 开始模型下载流程的异常处理块
        try:
            # 在主界面的结果文本区域添加下载开始提示
            # 获取当前时间
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 在结果文本区域添加下载开始提示（带时间）
            self.result_text.insert(tk.END, f"\n[{current_time}] 正在拉取模型 {model_name}...\n")
            self.root.update()  # 强制更新界面显示

            # 构建模型下载请求
            url = f"http://{ip}:{port}/api/pull"  # 构建Ollama API的下载端点URL
            data = {
                "name": model_name,  # 设置要下载的模型名称
                "insecure": True     # 允许非安全连接，用于处理自签名证书的情况
            }
            
            # 发送HTTP POST请求并获取流式响应
            response = requests.post(url, json=data, stream=True)  # 使用流式传输处理大型下载
            response.raise_for_status()  # 检查响应状态，如果不是200则抛出异常
            
            # 更新进度对话框显示下载开始状态
            progress_label.config(text="连接成功，开始下载模型...")  # 更新状态文本
            progress['value'] = 0  # 设置进度条初始值
            progress_dialog.update()  # 刷新对话框显示

            # 初始化下载进度追踪变量
            total_bytes = 0          # 记录总下载字节数
            downloaded_bytes = 0      # 记录已下载字节数
            layer_info = {}          # 用字典存储每个层的下载信息，键为层的digest，值为该层的下载状态
            
            # 使用迭代器处理服务器返回的流式响应数据
            for line in response.iter_lines():
                # 跳过空行，确保数据有效性
                if not line:
                    continue
                
                try:
                    # 解析每行JSON格式的响应数据，转换为Python字典
                    progress_data = json.loads(line.decode('utf-8'))
                    # 获取当前下载状态信息，如果不存在则返回空字符串
                    status = progress_data.get('status', '')
                    
                    # 根据不同的下载状态更新进度界面显示
                    if 'pulling manifest' in status:
                        # 当正在获取模型清单时，更新状态标签和进度条
                        progress_label.config(text="正在获取模型信息...")
                        progress['value'] = 0  # 设置进度条为初始状态
                        progress_dialog.update()  # 刷新进度对话框显示
                    elif 'pulling' in status:
                        # 当正在下载模型文件时，处理具体的下载进度
                        # 获取当前下载层的唯一标识符
                        digest = progress_data.get('digest', '')
                        # 获取当前已完成的字节数
                        completed = int(progress_data.get('completed', 0))
                        # 获取当前层的总字节数
                        total = int(progress_data.get('total', 0))
                        
                        # 处理每个下载层的信息
                        if digest:
                            # 如果是新的下载层，初始化其信息并更新总字节数
                            if digest not in layer_info:
                                layer_info[digest] = {'total': total, 'completed': 0}
                                total_bytes += total  # 累加总下载大小
                            # 更新当前层的已下载字节数
                            layer_info[digest]['completed'] = completed
                            
                            # 计算总体下载进度
                            # 累加所有层的已下载字节数
                            downloaded_bytes = sum(layer['completed'] for layer in layer_info.values())
                            if total_bytes > 0:
                                # 计算下载百分比，最大显示95%，预留验证阶段的进度空间
                                progress_percent = min(95, (downloaded_bytes / total_bytes) * 100)
                                # 将字节数转换为MB单位，便于显示
                                downloaded_mb = downloaded_bytes / (1024 * 1024)
                                total_mb = total_bytes / (1024 * 1024)
                                # 格式化进度显示文本
                                status_text = f"正在下载模型: {downloaded_mb:.1f}MB/{total_mb:.1f}MB ({progress_percent:.1f}%)"
                                # 更新进度显示界面
                                progress_label.config(text=status_text)
                                progress['value'] = progress_percent
                                progress_dialog.update()
                    # 处理模型文件的SHA256校验阶段
                    elif 'verifying sha256 digest' in status:
                        # 更新进度标签显示校验状态
                        progress_label.config(text="正在验证模型完整性...")
                        # 设置进度条为96%，表示进入校验阶段
                        progress['value'] = 96
                        # 刷新进度对话框显示
                        progress_dialog.update()
                    # 处理模型清单文件写入阶段
                    elif 'writing manifest' in status:
                        # 更新进度标签显示写入状态
                        progress_label.config(text="正在写入模型文件...")
                        # 设置进度条为97%，表示进入文件写入阶段
                        progress['value'] = 97
                        progress_dialog.update()
                    # 处理清理临时文件阶段
                    elif 'removing unused layers' in status:
                        # 更新进度标签显示清理状态
                        progress_label.config(text="正在清理未使用的文件...")
                        # 设置进度条为98%，表示进入清理阶段
                        progress['value'] = 98
                        progress_dialog.update()
                    # 处理下载成功完成状态
                    elif status == 'success':
                        # 更新进度标签显示完成状态
                        progress_label.config(text="下载完成！")
                        # 设置进度条为100%，表示下载全部完成
                        progress['value'] = 100
                        progress_dialog.update()
                    
                # 捕获JSON解析异常，跳过无效的数据行
                except json.JSONDecodeError:
                    continue
           
            # 通过API验证下载的模型是否可用
            verify_url = f"http://{ip}:{port}/api/show"
            # 发送POST请求验证模型状态
            verify_response = requests.post(verify_url, json={"name": model_name})
            # 如果验证失败，抛出异常并包含错误信息
            if not verify_response.ok:
                raise Exception(f"模型验证失败: {verify_response.text}")

            # 验证下载是否完整，比较总字节数和已下载字节数
            if total_bytes > 0 and downloaded_bytes < total_bytes:
                # 如果下载不完整，抛出异常并显示下载进度
                raise Exception(f"下载未完成 ({downloaded_bytes//1024}kB/{total_bytes//1024}kB)")

            # 更新进度条显示为完成状态
            progress['value'] = 100
            # 更新状态标签显示初始化提示
            progress_label.config(text="下载完成，正在初始化模型...")
            # 强制刷新界面显示
            self.root.update()
            
            # 添加2秒延迟，等待模型完全加载
            # 使用after方法实现非阻塞延迟
            self.root.after(2000, lambda: None)
            
            # 清理资源，关闭进度对话框
            progress_dialog.destroy()
            
            # 刷新模型列表显示
            # list_models更新树形视图中的模型列表
            self.list_models()
            # refresh_models更新对话界面的模型下拉列表
            self.refresh_models()
            
            # 获取当前时间（用于完成提示）
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 在结果文本区域添加成功提示（带时间）
            self.result_text.insert(tk.END, f"\n[{current_time}] 模型 {model_name} 拉取完成!\n")
            # 显示成功提示对话框
            messagebox.showinfo("完成", "模型拉取成功！")
            
        # 异常处理块，捕获下载过程中的所有异常
        except Exception as e:
            # 清理资源，关闭进度对话框
            progress_dialog.destroy()
            # 在结果文本区域显示错误信息
            self.result_text.insert(tk.END, f"错误: {str(e)}\n")
            # 显示错误提示对话框
            messagebox.showerror("错误", f"拉取模型失败: {str(e)}")
# 主要实现：
# 1. 创建模型下载的用户输入界面
# 2. 处理对话框的位置计算和居中显示
# 3. 组织输入控件的布局和样式
# 4. 实现用户输入的获取和确认机制
# 5. 模型名称输入对话框的模态控制
# 6. 用户输入的有效性验证
# 7. 模型重复性检查
# 8. 下载进度窗口的创建和位置计算
# 9. 进度对话框的位置设置和模态控制
# 10. 创建进度显示组件（标签和进度条）
# 11. 初始化下载请求和流式响应处理
# 12. 设置下载进度追踪机制
# 13. 流式处理服务器响应数据，实时获取下载进度
# 14. 多层模型文件的下载进度追踪和管理
# 15. 精确的下载进度计算和显示
# 16. 友好的用户界面反馈机制
# 17- 模型完整性校验阶段（96%）
# 18- 模型清单写入阶段（97%）
# 19- 临时文件清理阶段（98%）
# 20- 下载完成确认阶段（100%）
# 21. 模型验证：确保下载的模型可以正常使用
# 22. 完整性检查：验证所有数据是否完整下载
# 23. 界面更新：更新进度显示和状态提示
# 24. 延迟处理：等待模型初始化完成
# 25. 列表刷新：更新界面上的模型列表
# 26. 异常处理：统一处理下载过程中的错误
# 代码设计特点：
# 1. 使用模态对话框确保操作的完整性
# 2. 精确的位置计算确保界面美观
# 3. 统一字体和样式设置
# 4. 良好的空间布局和间距控制
# 代码采用分层设计模式，通过字典结构（layer_info）管理多层下载进度，并使用流式处理确保与大模型对话的实时反馈，提供良好的用户体验。
# 每个阶段都通过进度条和文本标签向用户提供清晰的反馈。代码使用了异常处理机制确保即使遇到无效数据也能继续运行，提高程序的稳定性。
# 代码采用完整的错误处理机制，确保即使在出错情况下也能正确清理资源并给出用户友好的提示。通过多层验证确保模型下载的完整性和可用性。
            
    # delete_model方法：用于删除已安装的Ollama模型
    # 该方法创建一个交互式对话框，让用户选择并删除模型
    def delete_model(self):
        # 从界面输入框获取Ollama服务器连接参数
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        
        # 使用try-except结构处理网络请求可能出现的异常
        try:
            # 构建API请求URL，获取已安装的模型列表
            url = f"http://{ip}:{port}/api/tags"
            # 发送GET请求获取模型列表
            response = requests.get(url)
            # 检查响应状态码，如果不是2xx则抛出异常
            response.raise_for_status()
            
            # 解析服务器返回的JSON数据
            data = response.json()
            # 获取模型列表，如果'models'键不存在则返回空列表
            models = data.get('models', [])
            
            # 检查是否存在可用模型
            if not models:
                messagebox.showinfo("提示", "没有找到可用的模型")
                return
            
            # 从模型数据中提取模型名称列表
            model_names = [model.get('name') for model in models]
            
            # 对模型名称列表进行升序排序
            # 简单的字符串升序排序，适用于各种模型名称格式
            model_names.sort()
            
            # 创建模型删除对话框
            dialog = tk.Toplevel(self.root)
            dialog.title("删除模型")
            dialog.geometry("500x250")
            
            # 计算对话框在主窗口中的居中位置
            # 获取主窗口的位置和尺寸信息
            window_x = self.root.winfo_x()
            window_y = self.root.winfo_y()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            # 计算对话框的居中坐标
            dialog_x = window_x + (window_width - 500) // 2
            dialog_y = window_y + (window_height - 250) // 2
            # 设置对话框位置
            dialog.geometry(f"+{dialog_x}+{dialog_y}")
            
            # 设置对话框的模态属性
            # transient设置对话框为主窗口的临时子窗口
            dialog.transient(self.root)
            # grab_set使对话框成为模态窗口，阻止用户与其他窗口交互
            dialog.grab_set()
            
            # 创建对话框的内容区域
            # 使用ttk.Frame创建一个带内边距的框架容器
            content_frame = ttk.Frame(dialog, padding=20)
            # 设置框架填充和扩展属性
            content_frame.pack(fill='both', expand=True)
            
            # 在内容框架中创建标签组件，显示"已有模型列表"文本
            # 使用ttk.Label确保与系统主题一致的外观
            label = ttk.Label(content_frame, text="已有模型列表:", font=self.default_font)
            # 将标签靠左对齐放置，并设置上下边距
            label.pack(anchor='w', pady=(0, 10))
            
            # 创建StringVar变量用于存储下拉列表框的当前选择值
            model_var = tk.StringVar()
            # 创建下拉列表框组件，用于显示可选的模型列表
            # values参数设置可选项列表
            # state='readonly'防止用户手动输入
            # width=30设置显示宽度
            model_combobox = ttk.Combobox(content_frame, textvariable=model_var, 
                                          values=model_names, state='readonly', 
                                          font=self.default_font, width=30)
            # 设置下拉列表框的布局，使其填充整个水平空间
            model_combobox.pack(anchor='w', pady=(0, 20), fill='x')
            
            # 如果模型列表不为空，默认选择第一个模型（降序排序后的第一个）
            if model_names:
                model_combobox.current(0)

            # 创建按钮容器框架，用于组织确认和取消按钮
            button_frame = ttk.Frame(content_frame)
            # 设置按钮框架水平居中
            button_frame.pack(anchor='center', pady=10)
            
            # 定义确认按钮的回调函数（保持原有逻辑不变）
            def on_confirm():
                selected_model = model_var.get()
                if selected_model:
                    dialog.destroy()
                    confirm = messagebox.askyesno("确认删除", f"确定要删除模型 {selected_model} 吗?")
                    if confirm:
                        self.perform_delete_model(selected_model)
            
            # 创建确认删除按钮，并绑定回调函数
            confirm_button = ttk.Button(button_frame, text="确认删除", command=on_confirm)
            confirm_button.pack(side='left', padx=20)
            
            # 创建取消按钮，点击时直接关闭对话框
            cancel_button = ttk.Button(button_frame, text="取消", command=dialog.destroy)
            cancel_button.pack(side='left', padx=20)
            
            # 等待对话框关闭后继续执行
            # wait_window会阻塞程序执行直到对话框被关闭
            self.root.wait_window(dialog)
            
        # 异常处理：捕获在获取模型列表过程中可能出现的所有异常
        except Exception as e:
            # 在结果文本区域显示错误信息
            self.result_text.insert(tk.END, f"错误: {str(e)}\n")
            # 弹出错误消息框显示详细错误信息
            messagebox.showerror("错误", f"获取模型列表失败: {str(e)}")
# 主要功能包括：
# 1. 获取服务器连接信息
# 2. 请求并获取已安装的模型列表
# 3. 创建可视化的删除模型对话框
# 4. 实现对话框的居中显示
# 5. 设置模态窗口属性，确保用户完成当前操作
# 6. 使用ttk主题化组件，提供现代的视觉效果
# 7. 创建可视化的模型选择界面
# 8. 提供下拉列表方式选择要删除的模型
# 9. 实现删除确认的双重验证机制
# 10. 提供清晰的用户操作反馈
# 11. 完善的异常处理机制
# 整体设计采用模态对话框的方式，确保用户完成当前操作后才能进行其他操作，提高操作的安全性和可靠性。

    # perform_delete_model方法：执行模型删除操作
    # 参数：model_name - 要删除的模型名称
    # 功能：通过Ollama API删除指定的AI模型
    def perform_delete_model(self, model_name):
        # 从界面输入框获取Ollama服务器的连接参数
        # strip()方法去除字符串两端的空白字符
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        
        # 使用try-except结构处理删除过程中可能出现的异常
        try:
            # 获取当前时间
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 在结果文本区域追加删除操作的开始提示（带时间）
            self.result_text.insert(tk.END, f"\n[{current_time}] 正在删除模型 {model_name}...\n")
            
            # 构建Ollama API的删除请求
            # 使用f-string构建完整的API URL
            delete_url = f"http://{ip}:{port}/api/delete"
            # 准备请求数据，包含要删除的模型名称
            delete_data = {"name": model_name}
            # 发送DELETE请求到Ollama服务器
            # json参数将Python字典转换为JSON格式发送
            delete_response = requests.delete(delete_url, json=delete_data)
            # 检查响应状态码，如果不是2xx则抛出异常
            delete_response.raise_for_status()
            
            # 获取当前时间（用于完成提示）
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 删除成功后在结果文本区域显示成功消息（带时间）
            self.result_text.insert(tk.END, f"[{current_time}] 模型 {model_name} 已成功删除!\n")
            
            # 更新界面显示
            # 刷新模型列表树形视图
            self.list_models()
            # 更新对话界面的模型选择下拉列表
            self.refresh_models()
            
            # 使用消息框显示删除成功的提示
            # showinfo创建一个信息类型的消息框
            messagebox.showinfo("成功", f"模型 {model_name} 已成功删除!")
            
        # 异常处理：捕获删除过程中可能出现的所有异常
        except Exception as e:
            # 在结果文本区域显示错误信息
            self.result_text.insert(tk.END, f"错误: {str(e)}\n")
            # 使用错误消息框显示详细的错误信息
            messagebox.showerror("错误", f"删除模型失败: {str(e)}")
# 主要功能包括：
# 1. 执行实际的模型删除操作
# 2. 通过HTTP请求与Ollama服务器通信
# 3. 提供实时的操作反馈
# 4. 自动更新界面显示
# 5. 完善的错误处理机制
# 设计特点：
# 1. 使用异步更新确保界面响应性
# 2. 多重反馈机制（文本区域和消息框）
# 3. 完整的错误处理和提示
# 4. 自动刷新相关界面元素
# 5. 统一的错误提示格式

    
    # show_version_in_chat方法：显示Ollama服务器版本信息的对话框界面
    # 功能：获取并展示Ollama服务器的版本信息和配置详情
    def show_version_in_chat(self):
        # 从界面输入框获取Ollama服务器的连接信息
        # 使用strip()方法移除可能的首尾空格
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        
        # 使用try-except结构处理网络请求和界面操作可能的异常
        try:
            # 构建Ollama版本查询API的完整URL
            # 使用f-string动态生成API地址
            url = f"http://{ip}:{port}/api/version"
            # 发送HTTP GET请求获取版本信息
            response = requests.get(url)
            # 检查响应状态码，非2xx状态会抛出异常
            response.raise_for_status()
            
            # 将服务器返回的JSON响应解析为Python字典
            data = response.json()
            # 从响应数据中提取版本号，如果不存在则返回'Unknown'
            version = data.get('version', 'Unknown')
            
            # 创建新的顶层窗口作为版本信息显示对话框
            dialog = tk.Toplevel(self.root)
            # 设置对话框窗口标题
            dialog.title("版本信息")
            
            # 获取主窗口的位置和尺寸信息
            # 用于计算对话框的居中显示位置
            window_x = self.root.winfo_x()
            window_y = self.root.winfo_y()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            # 定义版本信息对话框的固定尺寸
            # 设置适合显示版本信息的窗口大小
            dialog_width = 400
            dialog_height = 300
            
            # 计算对话框的居中显示坐标
            # 基于主窗口的位置和尺寸计算对话框的显示位置
            dialog_x = window_x + (window_width - dialog_width) // 2
            dialog_y = window_y + (window_height - dialog_height) // 2
            
            # 使用geometry方法设置对话框的尺寸和位置
            # 格式为"宽度x高度+X坐标+Y坐标"
            dialog.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")
            
            # 设置对话框的模态属性
            # transient使对话框依附于主窗口
            dialog.transient(self.root)
            # grab_set使对话框成为模态窗口，阻止用户与其他窗口交互
            dialog.grab_set()
            
            # 创建文本显示区域用于展示版本信息
            # wrap=tk.WORD设置自动换行
            # height=10设置文本区域的初始高度
            text_widget = tk.Text(dialog, wrap=tk.WORD, font=self.default_font, height=10)
            # 设置文本区域的填充和扩展属性
            text_widget.pack(expand=True, fill='both', padx=10, pady=10)
            
            # 配置文本显示的样式和内容
            # 创建名为"purple"的文本标签，设置其前景色为紫色
            text_widget.tag_configure("purple", foreground="purple")
            # 使用紫色样式插入Ollama版本号信息到文本区域末尾
            text_widget.insert(tk.END, f"Ollama 版本: {version}\n", "purple")
            # 使用紫色样式插入分隔行
            text_widget.insert(tk.END, "\n完整信息:\n", "purple")
            # 将完整的配置信息转换为格式化的JSON字符串并插入
            # indent=2设置JSON缩进格式，ensure_ascii=False支持中文显示
            text_widget.insert(tk.END, json.dumps(data, indent=2, ensure_ascii=False))
            
            # 将文本区域设置为只读状态，防止用户修改显示内容
            text_widget.config(state='disabled')
            
            # 在对话框底部创建一个确定按钮
            # command参数绑定dialog.destroy方法，点击时关闭对话框
            button = ttk.Button(dialog, text="确定", command=dialog.destroy)
            # 设置按钮在垂直方向上的内边距为10像素
            button.pack(pady=10)
            
            # 阻塞程序执行，等待对话框被关闭
            # wait_window方法会暂停当前线程，直到指定窗口被销毁
            self.root.wait_window(dialog)
            
        # 异常处理块：捕获在获取和显示版本信息过程中可能出现的所有异常
        except Exception as e:
            # 使用错误消息框显示异常信息
            # showerror创建一个错误类型的消息框，显示具体的错误原因
            messagebox.showerror("错误", f"获取版本信息失败: {str(e)}")
# 主要功能和主要特点包括：
# 1. 使用模态对话框展示信息
# 2. 实现界面居中显示
# 3. 支持版本信息的格式化展示
# 4. 采用异常处理机制确保程序稳定性
# 5. 提供清晰的用户界面反馈
# 6. 文本内容的格式化显示
# 7. 版本信息的突出展示
# 8. JSON数据的美化输出
# 9. 用户界面的交互控制
# 10. 异常情况的友好提示
# 设计特点：
# 1. 界面布局合理，视觉效果优雅
# 2. 使用ttk主题化组件保持系统风格一致性
# 3. 文本区域支持自动换行
# 4. 对话框模态设计确保操作专注性
# 5. 完善的错误处理机制
# 6. 使用紫色突出显示重要信息
# 7. 采用JSON格式化提高可读性
# 8. 实现只读保护机制
# 9. 提供简单的用户确认机制
# 10. 完善的错误处理流程
    
    # exit_program方法：处理程序退出功能
    # 功能：
    # 1. 通过调用Tkinter的quit方法安全地终止程序运行
    # 2. 结束主事件循环，关闭所有窗口
    # 3. 释放程序占用的系统资源
    # 4. 确保程序能够正常退出而不会造成资源泄露
    def exit_program(self):
        self.root.quit()
# 主要特点：
# 1. 提供一个干净的程序退出机制
# 2. 使用Tkinter内置的quit方法确保安全退出
# 3. 可以通过菜单项或按钮调用实现程序退出
# 4. 不会强制终止程序，而是通过事件循环正常结束
# 5. 适合作为GUI程序的标准退出方式


    def handle_enter(self, event):
        """
        处理用户在输入框中按下回车键的事件
        
        功能：
        - 拦截回车键事件，用于快速发送消息
        - 区分普通回车和Shift+回车组合键
        - 实现类似聊天软件的消息发送机制
        
        参数：
        - event: Tkinter事件对象，包含按键事件的详细信息
        
        返回值：
        - "break"字符串，用于阻止事件继续传播
        """
        # 检测是否按下了Shift+Enter组合键
        # event.state是一个位掩码，0x1表示Shift键
        # 如果按下了Shift+Enter，则不拦截事件，允许在文本框中换行
        if event.state & 0x1:  # 检查Shift键是否按下
            return
            
        # 将输入焦点转移到下一个可获得焦点的控件
        # tk_focusNext()是Tkinter的内置方法，用于获取下一个焦点控件
        # focus()方法将焦点设置到该控件
        event.widget.tk_focusNext().focus()
        
        # 调用消息发送方法处理用户输入的内容
        # send_message()方法会获取输入框内容并发送到Ollama模型
        self.send_message()
        
        # 返回"break"字符串阻止事件继续传播
        # 这样可以防止Tkinter执行文本框的默认回车行为(换行)
        return "break"
# 实现聊天界面中回车键快捷发送消息功能的关键部分，它通过拦截回车键事件并调用消息发送方法，同时保留了使用Shift+Enter进行换行的能力，提高用户体验。

    def get_selected_model(self):
        """
        获取用户当前在界面上选择的AI模型名称
        功能：
        - 从下拉选择框中获取用户选择的模型名称
        - 提供默认模型回退机制，确保始终返回有效的模型名称
        - 作为模型选择与API请求之间的桥梁
        实现细节：
        - 通过Combobox控件的get()方法获取当前选中值
        - 进行空值检查，防止在未选择模型时出现错误
        - 当未选择模型时返回默认模型"llama2"
        返回值：
        - 字符串类型，表示当前选择的模型名称或默认模型名称
        """
        # 从界面的下拉选择框(Combobox)获取当前选中的模型名称
        model = self.model_combobox.get()
        # 进行空值检查，如果用户未选择任何模型或清空了选择
        if not model:
            return "gemma3:27b"  # 返回默认模型名称作为回退选项
        return model  # 返回用户选择的模型名称
# 是模型选择功能的核心部分，它确保在与Ollama API通信时始终使用有效的模型名称，即使用户未明确选择模型也能提供默认值“gemma3:27b”模型，增强程序的健壮性。
    
    def send_message(self):
        """
        发送用户消息到Ollama模型并处理AI回复的核心方法
        功能概述：
        - 获取用户输入的消息并发送到Ollama API
        - 在聊天界面实时显示用户消息和AI回复
        - 使用流式响应技术实现AI回复的实时显示
        - 处理网络请求过程中可能出现的各种异常
        - 维护对话历史记录
        工作流程：
        1. 获取用户输入和服务器配置
        2. 在界面显示用户消息
        3. 发送API请求并获取流式响应
        4. 实时更新界面显示AI回复
        5. 保存对话历史
        6. 处理可能的异常情况
        """
        # 获取输入框内容并去除首尾空白
        message = self.input_text.get("1.0", tk.END).strip()
        
        # 检查消息是否为空
        if not message:
            messagebox.showinfo("提示", "您想聊啥？")
            return

        # 获取当前系统时间，用于在聊天记录中显示消息发送时间
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 从输入文本框获取用户输入的消息内容并去除首尾空白字符
        user_message = self.input_text.get("1.0", tk.END).strip()
        
        # 消息为空时直接返回，不执行后续操作
        if not user_message:
            return
        
        # 从界面输入框获取Ollama服务器的IP地址和端口号
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        # 获取当前选择的AI模型名称
        model = self.get_selected_model()
        
        # 临时解除聊天文本区域的只读状态，以便添加新内容
        self.chat_text.config(state='normal')
        # 在聊天区域添加用户消息，包含时间戳和消息内容
        self.chat_text.insert(tk.END, f"\n[{current_time}]\n你: {user_message}\n\n")
        # 添加AI回复的前缀标识，不包含时间戳
        self.chat_text.insert(tk.END, "AI: ")
        # 自动滚动聊天区域到最新内容
        self.chat_text.see(tk.END)
        # 恢复聊天文本区域的只读状态，防止用户修改历史消息
        self.chat_text.config(state='disabled')
        
        # 清空用户输入框，为下一次输入做准备
        self.input_text.delete("1.0", tk.END)
        
        # 强制更新界面显示，确保用户消息立即可见
        self.root.update()
        
        try:            
            # 构建完整的Ollama API请求URL
            url = f"http://{ip}:{port}/api/generate"
            
            # 准备API请求的JSON数据
            data = {
                "model": model,      # 指定使用的AI模型
                "prompt": user_message,  # 用户输入的提示文本
                "stream": True       # 启用流式响应模式，实现实时显示
            }            
            # 向Ollama API发送POST请求，启用流式响应模式
            # stream=True参数使请求保持连接，逐步接收响应内容
            response = requests.post(url, json=data, stream=True)
            # 检查HTTP响应状态码，非2xx状态会抛出异常
            response.raise_for_status()
            
            # 初始化空字符串，用于累积存储完整的AI回复内容
            full_response = ""
            
            """
            流式响应处理循环：
            1. 使用iter_lines()方法逐行获取响应数据
            2. 每行数据代表AI回复的一个片段
            3. 解析每个片段并实时更新到界面
            4. 同时累积构建完整回复文本
            """
            for line in response.iter_lines():
                if line:  # 确保行内容非空
                    # 将字节流解码为UTF-8字符串并解析JSON数据
                    result = json.loads(line.decode('utf-8'))
                    # 从JSON响应中提取当前文本片段
                    response_part = result.get('response', '')
                    
                    if response_part:  # 确保响应片段非空
                        # 将当前片段追加到完整回复字符串中
                        full_response += response_part
                        
                        """
                        实时更新聊天界面：
                        1. 临时解除文本区域的只读状态
                        2. 追加当前响应片段到文本末尾
                        3. 自动滚动确保最新内容可见
                        4. 恢复文本区域的只读状态
                        5. 强制刷新UI确保实时显示
                        """
                        self.chat_text.config(state='normal')  # 临时启用编辑状态
                        self.chat_text.insert(tk.END, response_part)  # 插入当前片段
                        self.chat_text.see(tk.END)  # 自动滚动到最新内容
                        self.chat_text.config(state='disabled')  # 恢复只读状态
                        # 强制更新GUI界面，确保用户能实时看到AI回复
                        self.root.update()
            
            # AI回复完成后的界面处理
            # 添加额外换行，提高可读性并为下一次对话做准备
            self.chat_text.config(state='normal')  # 临时启用编辑状态
            self.chat_text.insert(tk.END, "\n\n")  # 插入两个换行符
            self.chat_text.see(tk.END)  # 确保滚动到最新位置
            self.chat_text.config(state='disabled')  # 恢复只读状态
            
            """
            对话历史管理：
            1. 检查conversation_history属性是否存在
            2. 不存在则初始化为空列表
            3. 将当前对话(用户问题和AI完整回复)添加到历史记录
            4. 采用字典结构存储，便于后续处理和显示
            """
            if not hasattr(self, 'conversation_history'):
                self.conversation_history = []  # 首次使用时初始化历史记录列表
            # 将当前对话添加到历史记录中，包含用户问题和AI完整回复
            self.conversation_history.append({"user": user_message, "ai": full_response})
            
        except Exception as e:
            """
            异常处理机制：
            1. 捕获请求过程中可能出现的所有异常
            2. 包括网络错误、服务器错误、JSON解析错误等
            3. 提供多层次的错误反馈（控制台、聊天窗口、对话框）
            4. 确保即使出错也不会导致程序崩溃
            """
            # 构建详细的错误信息字符串
            error_message = f"发送消息时出错: {str(e)}"
            # 在控制台输出错误信息，便于调试
            print(f"错误: {error_message}")
            
            # 在聊天窗口中显示错误信息，让用户直接看到错误
            self.chat_text.config(state='normal')  # 临时启用编辑状态
            self.chat_text.insert(tk.END, f"错误: {error_message}\n\n")  # 插入错误信息
            self.chat_text.see(tk.END)  # 滚动到错误信息位置
            self.chat_text.config(state='disabled')  # 恢复只读状态
            
            # 弹出错误对话框，确保用户注意到错误情况
            messagebox.showerror("错误", error_message)
        
        finally:
            """
            消息发送完成后的清理和重置操作：
            1. 无论消息发送成功还是失败，都会执行此代码块
            2. 确保输入区域恢复到可用状态
            3. 重新聚焦到输入框，方便用户继续输入
            
            执行顺序：
            - 首先清空输入框内容
            - 然后确保输入框处于可编辑状态
            - 最后将输入焦点重新设置到输入框
            
            设计目的：
            - 提供一致的用户体验
            - 确保即使在错误情况下界面也能正常使用
            - 遵循资源管理的最佳实践
            """
            # 清空输入文本框中的所有内容，为下一次输入做准备
            self.input_text.delete("1.0", tk.END)
            # 确保输入框处于可编辑状态，防止因异常导致输入框被锁定
            self.input_text.config(state='normal')
            # 将键盘焦点重新设置到输入框，用户可以直接开始输入下一条消息
            self.input_text.focus()
# 该方法是 OllamaGUI 类中的核心功能方法，负责处理用户消息发送和 AI 回复的整个流程。下面是该方法的详细功能和技术特点分析：
# 主要功能
# 1. 用户消息处理 ：获取用户在输入框中输入的消息，并在聊天界面中显示
# 2. 服务器通信 ：与 Ollama API 服务器建立连接并发送用户消息
# 3. 流式响应处理 ：实时接收和显示 AI 模型的回复内容
# 4. 对话历史管理 ：维护用户与 AI 之间的对话历史记录
# 5. 异常处理 ：处理网络请求、数据解析等过程中可能出现的各种异常情况
# ## 技术特点
# ### 1. 流式响应技术
# 该方法采用了流式响应（Streaming Response）技术，这是其最核心的技术特点：
# - 使用 requests.post(..., stream=True) 建立持久连接
# - 通过 response.iter_lines() 逐行获取服务器返回的数据
# - 实时解析 JSON 数据并更新界面显示
# - 提供即时的用户反馈，无需等待完整响应
# 这种技术特别适合大语言模型的应用场景，因为模型生成回复可能需要较长时间，流式处理可以让用户立即看到部分回复，提升用户体验。
# ### 2. 实时界面更新机制
# - 使用 self.chat_text.config(state='normal'/'disabled') 动态控制文本区域的编辑状态
# - 通过 self.root.update() 强制刷新界面，确保实时显示
# - 使用 self.chat_text.see(tk.END) 自动滚动到最新内容
# ### 3. 健壮的异常处理机制
# - 采用完整的 try-except-finally 结构
# - 提供多层次的错误反馈（控制台日志、聊天窗口提示、弹窗警告）
# - 即使在出错情况下也能保持程序稳定运行
# - 在 finally 块中确保界面状态一致性
# ### 4. 对话历史管理
# - 动态创建对话历史存储结构
# - 使用字典格式保存用户问题和 AI 回复
# - 支持后续功能扩展（如对话导出、上下文管理等）
# ### 5. 用户体验优化
# - 在发送请求前立即清空输入框，提供更好的交互体验
# - 显示时间戳，便于用户追踪对话时间
# - 区分用户消息和 AI 回复的显示格式
# - 在等待 AI 回复时保持界面响应性
# ## 实现流程
# 1. 获取用户输入和服务器配置信息
# 2. 在聊天界面显示用户消息
# 3. 构建并发送 API 请求
# 4. 流式处理响应数据并实时更新界面
# 5. 保存对话历史
# 6. 处理可能的异常情况
# 7. 重置输入区域状态
# ## 总结
# send_message 方法通过流式处理技术实现与大语言模型的实时交互，提供良好的用户体验。其健壮的异常处理机制和界面状态管理确保程序在各种情况下的稳定运行。该方法是整个聊天应用的核心组件，以尽力体现现代 GUI 应用与 AI 服务交互的最佳实践。


"""
程序入口点模块：
这是整个GUI应用程序的启动入口，主要负责：
1. 环境初始化和配置
2. 异常输出控制
3. GUI程序的启动和生命周期管理
4. 全局异常处理机制
5. 资源清理和程序退出管理
"""
if __name__ == '__main__':
    # 导入基础系统操作模块
    import os
    import sys
    import io
    
    """
    环境变量配置块：
    设置Python解释器的基本运行环境，主要用于处理字符编码和输出控制
    - PYTHONIOENCODING：确保所有IO操作使用UTF-8编码
    - PYTHONLEGACYWINDOWSSTDIO：处理Windows平台的特殊编码需求
    """
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
    
    """
    警告控制机制：
    通过warnings模块配置全局警告过滤器，抑制不必要的警告信息
    特别用于处理PIL库等第三方模块的警告
    """
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    
    """
    标准错误输出重定向块：
    创建内存中的文本缓冲区，用于捕获所有标准错误输出
    避免警告和错误信息直接显示在终端中
    保存原始stderr以便后续恢复
    """
    stderr_capture = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = stderr_capture
    
# ... existing code ...

"""
程序入口点模块：
这是整个GUI应用程序的启动入口，主要负责：
1. 环境初始化和配置
2. 异常输出控制
3. GUI程序的启动和生命周期管理
4. 全局异常处理机制
5. 资源清理和程序退出管理
"""
if __name__ == '__main__':
    # 导入基础系统操作模块
    import os
    import sys
    import io
    
    # 设置环境变量来抑制libpng警告
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
    
    # 更彻底的警告抑制方法
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    
    # 创建内存文本流来捕获stderr输出
    stderr_capture = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = stderr_capture
    
    # 尝试使用PIL的日志设置来抑制警告
    try:
        import logging
        logging.getLogger('PIL').setLevel(logging.ERROR)
        logging.getLogger().setLevel(logging.ERROR)
    except:
        pass
    
    try:
        # 创建Tkinter主窗口对象
        root = tk.Tk()
        
        # 实例化应用程序主类
        app = OllamaGUI(root)
        
        # 启动Tkinter的事件循环，开始处理用户交互
        root.mainloop()
    
        # 处理用户通过Ctrl+C等方式的主动中断
        sys.stderr = original_stderr  # 恢复原始的stderr
        print("程序已退出。")
        
    except KeyboardInterrupt:
        sys.stderr = original_stderr  # 恢复原始的stderr
        print("\n程序正在优雅地退出...")
    
    except Exception as e:
        sys.stderr = original_stderr  # 恢复原始的stderr
        print(f"\n发生错误: {str(e)}")