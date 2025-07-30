import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import logging

class PDFToolboxGUI:
    """PDF工具箱主窗口"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF工具箱 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
        
        # 初始化PDF处理模块
        self.init_pdf_modules()
        
        # 文件列表
        self.selected_files = []
        
        self.setup_ui()
        self.setup_logging()
    
    def init_pdf_modules(self):
        """初始化PDF处理模块"""
        try:
            # 直接导入PDF处理模块
            from pdf_merger import PDFMerger
            from pdf_splitter import PDFSplitter
            from pdf_converter import PDFConverter
            from pdf_security import PDFSecurity
            
            self.pdf_merger = PDFMerger()
            self.pdf_splitter = PDFSplitter()
            self.pdf_converter = PDFConverter()
            self.pdf_security = PDFSecurity()
            self.logger.info("PDF处理模块初始化成功")
        except ImportError as e:
            self.logger.error(f"导入PDF处理模块失败: {e}")
            messagebox.showerror("错误", f"导入PDF处理模块失败: {e}")
            self.pdf_merger = None
            self.pdf_splitter = None
            self.pdf_converter = None
            self.pdf_security = None
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="PDF工具箱", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文件选择区域
        self.setup_file_selection(main_frame)
        
        # 功能选项卡
        self.setup_notebook(main_frame)
        
        # 日志区域
        self.setup_log_area(main_frame)
    
    def setup_file_selection(self, parent):
        """设置文件选择区域"""
        file_frame = ttk.LabelFrame(parent, text="文件选择", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # 文件列表
        self.file_listbox = tk.Listbox(file_frame, height=6)
        self.file_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # 按钮框架
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="添加PDF文件", command=self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="添加图片文件", command=self.add_images).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="清空列表", command=self.clear_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="移除选中", command=self.remove_selected).pack(side=tk.LEFT)
    
    def setup_notebook(self, parent):
        """设置功能选项卡"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 合并功能
        self.merge_frame = self.create_merge_tab()
        self.notebook.add(self.merge_frame, text="PDF合并")
        
        # 分割功能
        self.split_frame = self.create_split_tab()
        self.notebook.add(self.split_frame, text="PDF分割")
        
        # 转换功能
        self.convert_frame = self.create_convert_tab()
        self.notebook.add(self.convert_frame, text="格式转换")
        
        # 安全功能
        self.security_frame = self.create_security_tab()
        self.notebook.add(self.security_frame, text="安全设置")
    
    def create_merge_tab(self):
        """创建合并功能选项卡"""
        frame = ttk.Frame(self.notebook, padding="10")

        # 合并文件选择区域
        file_frame = ttk.LabelFrame(frame, text="选择要合并的PDF文件", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.merge_file_list = []
        self.merge_file_listbox = tk.Listbox(file_frame, height=6)
        self.merge_file_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        merge_scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.merge_file_listbox.yview)
        merge_scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.merge_file_listbox.configure(yscrollcommand=merge_scrollbar.set)
        
        btn_frame = ttk.Frame(file_frame)
        btn_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        ttk.Button(btn_frame, text="选择PDF文件", command=self.add_merge_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="移除选中", command=self.remove_selected_merge_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="清空列表", command=self.clear_merge_files).pack(side=tk.LEFT, padx=(0, 5))

        # 合并选项
        options_frame = ttk.LabelFrame(frame, text="合并选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(options_frame, text="输出文件名:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.merge_output_var = tk.StringVar(value="merged.pdf")
        ttk.Entry(options_frame, textvariable=self.merge_output_var, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        ttk.Button(options_frame, text="选择位置", command=self.select_merge_output).grid(row=0, column=2, padx=(10, 0), pady=5)
        
        # 合并按钮
        ttk.Button(frame, text="开始合并", command=self.merge_pdfs).pack(pady=10)
        
        return frame
    
    def create_split_tab(self):
        """创建分割功能选项卡"""
        frame = ttk.Frame(self.notebook, padding="10")

        # 文件选择区域
        file_frame = ttk.LabelFrame(frame, text="选择要分割的PDF文件", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        self.split_file = None
        self.split_file_var = tk.StringVar(value="未选择文件")
        ttk.Label(file_frame, textvariable=self.split_file_var, width=50).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(file_frame, text="选择PDF文件", command=self.select_split_file).grid(row=0, column=1, padx=(10, 0))
        ttk.Button(file_frame, text="清空", command=self.clear_split_file).grid(row=0, column=2, padx=(10, 0))

        # 分割选项
        options_frame = ttk.LabelFrame(frame, text="分割选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))

        # 分割方式
        ttk.Label(options_frame, text="分割方式:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.split_method = tk.StringVar(value="pages")
        ttk.Radiobutton(options_frame, text="按页数分割", variable=self.split_method, value="pages", command=self.update_split_mode).grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(options_frame, text="按页码范围分割", variable=self.split_method, value="range", command=self.update_split_mode).grid(row=0, column=2, sticky=tk.W, pady=5)

        # 每文件页数
        self.pages_per_file = tk.StringVar(value="1")
        self.pages_per_file_label = ttk.Label(options_frame, text="每文件页数：")
        self.pages_per_file_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pages_per_file_entry = ttk.Entry(options_frame, textvariable=self.pages_per_file, width=10)
        self.pages_per_file_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        self.pages_per_file_hint = ttk.Label(options_frame, text="如：2，每2页一个文件", foreground="#888")
        self.pages_per_file_hint.grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=5)

        # 页码范围
        self.page_ranges = tk.StringVar(value="1-3,4-6,7-9")
        self.page_ranges_label = ttk.Label(options_frame, text="页码范围：")
        self.page_ranges_entry = ttk.Entry(options_frame, textvariable=self.page_ranges, width=30)
        self.page_ranges_hint = ttk.Label(options_frame, text="如：1-3,5,7-9", foreground="#888")

        # 说明Label
        self.split_mode_desc = ttk.Label(options_frame, text="将PDF每N页分割为一个新文件", foreground="#0078d4")
        self.split_mode_desc.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))

        # 输出目录
        ttk.Label(options_frame, text="输出目录:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.split_output_dir = tk.StringVar(value="./split_output")
        ttk.Entry(options_frame, textvariable=self.split_output_dir, width=30).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        ttk.Button(options_frame, text="浏览", command=self.select_split_output).grid(row=3, column=2, padx=(10, 0), pady=5)

        # 分割按钮
        ttk.Button(frame, text="开始分割", command=self.split_pdf).pack(pady=10)

        self.update_split_mode()
        return frame

    def update_split_mode(self):
        mode = self.split_method.get()
        if mode == "pages":
            # 显示每文件页数，隐藏页码范围
            self.pages_per_file_label.grid()
            self.pages_per_file_entry.grid()
            self.pages_per_file_hint.grid()
            self.page_ranges_label.grid_remove()
            self.page_ranges_entry.grid_remove()
            self.page_ranges_hint.grid_remove()
            self.split_mode_desc.config(text="将PDF每N页分割为一个新文件")
        else:
            # 显示页码范围，隐藏每文件页数
            self.pages_per_file_label.grid_remove()
            self.pages_per_file_entry.grid_remove()
            self.pages_per_file_hint.grid_remove()
            self.page_ranges_label.grid(row=1, column=0, sticky=tk.W, pady=5)
            self.page_ranges_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
            self.page_ranges_hint.grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=5)
            self.split_mode_desc.config(text="将PDF按指定页码范围分割为多个文件，如：1-3,5,7-9")
    
    def create_convert_tab(self):
        """创建转换功能选项卡"""
        frame = ttk.Frame(self.notebook, padding="10")
        # 文件选择区域
        file_frame = ttk.LabelFrame(frame, text="选择要转换的文件", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        self.convert_files_list = []
        self.convert_files_var = tk.StringVar(value="未选择文件")
        self.convert_files_listbox = tk.Listbox(file_frame, height=3, width=50)
        self.convert_files_listbox.grid(row=0, column=0, sticky=tk.W)
        ttk.Button(file_frame, text="选择文件", command=self.select_convert_files).grid(row=0, column=1, padx=(10, 0))
        ttk.Button(file_frame, text="清空", command=self.clear_convert_files).grid(row=0, column=2, padx=(10, 0))

        # 转换选项
        options_frame = ttk.LabelFrame(frame, text="转换选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))

        # 转换类型
        ttk.Label(options_frame, text="转换类型:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.convert_type = tk.StringVar(value="PDF转图片")
        convert_combo = ttk.Combobox(options_frame, textvariable=self.convert_type, state="readonly")
        convert_combo['values'] = ("PDF转图片", "图片转PDF", "PDF转文本", "PDF压缩")
        convert_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        convert_combo.bind('<<ComboboxSelected>>', self.on_convert_type_change)

        # 输出路径
        ttk.Label(options_frame, text="输出路径:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.convert_output = tk.StringVar(value="./convert_output")
        ttk.Entry(options_frame, textvariable=self.convert_output, width=30).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        ttk.Button(options_frame, text="浏览", command=self.select_convert_output).grid(row=1, column=2, padx=(10, 0), pady=5)

        # 转换按钮
        ttk.Button(frame, text="开始转换", command=self.convert_files).pack(pady=10)

        return frame

    def on_convert_type_change(self, event=None):
        # 可根据类型切换输出路径默认值
        t = self.convert_type.get()
        if t == "图片转PDF":
            self.convert_output.set("converted.pdf")
        elif t == "PDF转文本":
            self.convert_output.set("converted.txt")
        elif t == "PDF转图片":
            self.convert_output.set("./images_output")
        elif t == "PDF压缩":
            self.convert_output.set("compressed.pdf")

    def create_security_tab(self):
        """创建安全功能选项卡"""
        frame = ttk.Frame(self.notebook, padding="10")
        # 文件选择区域
        file_frame = ttk.LabelFrame(frame, text="选择要处理的PDF文件", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        self.security_file = None
        self.security_file_var = tk.StringVar(value="未选择文件")
        ttk.Label(file_frame, textvariable=self.security_file_var, width=50).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(file_frame, text="选择PDF文件", command=self.select_security_file).grid(row=0, column=1, padx=(10, 0))
        ttk.Button(file_frame, text="清空", command=self.clear_security_file).grid(row=0, column=2, padx=(10, 0))

        # 安全选项
        options_frame = ttk.LabelFrame(frame, text="安全选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 操作类型
        ttk.Label(options_frame, text="操作类型:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.security_operation = tk.StringVar(value="encrypt")
        security_combo = ttk.Combobox(options_frame, textvariable=self.security_operation, state="readonly")
        security_combo['values'] = ('encrypt', 'decrypt', 'remove_password')
        security_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 密码
        ttk.Label(options_frame, text="密码:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password = tk.StringVar()
        ttk.Entry(options_frame, textvariable=self.password, show="*", width=20).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 用户密码
        ttk.Label(options_frame, text="用户密码:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.user_password = tk.StringVar()
        ttk.Entry(options_frame, textvariable=self.user_password, show="*", width=20).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        ttk.Label(options_frame, text="(可选)").grid(row=2, column=2, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 输出文件
        ttk.Label(options_frame, text="输出文件:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.security_output = tk.StringVar()
        ttk.Entry(options_frame, textvariable=self.security_output, width=30).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        ttk.Button(options_frame, text="选择文件", command=self.select_security_output).grid(row=3, column=2, padx=(10, 0), pady=5)
        
        # 安全操作按钮
        ttk.Button(frame, text="执行操作", command=self.perform_security_operation).pack(pady=10)
        
        return frame
    
    def setup_log_area(self, parent):
        """设置日志区域"""
        log_frame = ttk.LabelFrame(parent, text="操作日志", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 日志文本框
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # 清空日志按钮
        ttk.Button(log_frame, text="清空日志", command=self.clear_log).grid(row=1, column=0, pady=(10, 0))
    
    # 文件操作方法
    def add_files(self):
        """添加PDF文件"""
        files = filedialog.askopenfilenames(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def add_images(self):
        """添加图片文件"""
        files = filedialog.askopenfilenames(
            title="选择图片文件",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("PNG文件", "*.png"),
                ("JPEG文件", "*.jpg *.jpeg"),
                ("所有文件", "*.*")
            ]
        )
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def clear_files(self):
        """清空文件列表"""
        self.selected_files.clear()
        self.file_listbox.delete(0, tk.END)
    
    def remove_selected(self):
        """移除选中的文件"""
        selection = self.file_listbox.curselection()
        for index in reversed(selection):
            self.file_listbox.delete(index)
            self.selected_files.pop(index)
    
    # 文件选择方法
    def select_merge_output(self):
        """选择合并输出文件"""
        filename = filedialog.asksaveasfilename(
            title="保存合并后的PDF",
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf")]
        )
        if filename:
            self.merge_output_var.set(filename)
    
    def select_split_output(self):
        """选择分割输出目录"""
        directory = filedialog.askdirectory(title="选择分割输出目录")
        if directory:
            self.split_output_dir.set(directory)
    
    def select_convert_output(self):
        """选择转换输出路径"""
        convert_type = self.convert_type.get()
        if convert_type == 'PDF转图片':
            # 这些功能输出到目录
            directory = filedialog.askdirectory(title="选择输出目录")
            if directory:
                self.convert_output.set(directory)
        elif convert_type in ['图片转PDF', 'PDF转文本', 'PDF压缩']:
            # 这些功能输出到文件
            filename = None
            if convert_type == '图片转PDF':
                filename = filedialog.asksaveasfilename(
                    title="保存转换后的PDF",
                    defaultextension=".pdf",
                    filetypes=[("PDF文件", "*.pdf")]
                )
            elif convert_type == 'PDF转文本':
                filename = filedialog.asksaveasfilename(
                    title="保存转换后的文本",
                    defaultextension=".txt",
                    filetypes=[("文本文件", "*.txt")]
                )
            elif convert_type == 'PDF压缩':
                filename = filedialog.asksaveasfilename(
                    title="保存压缩后的PDF",
                    defaultextension=".pdf",
                    filetypes=[("PDF文件", "*.pdf")]
                )
            if filename:
                self.convert_output.set(filename)
    
    def select_security_output(self):
        """选择安全操作输出文件"""
        filename = filedialog.asksaveasfilename(
            title="保存处理后的PDF",
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf")]
        )
        if filename:
            self.security_output.set(filename)
    
    # 操作执行方法
    def add_merge_files(self):
        files = filedialog.askopenfilenames(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        for file in files:
            if file not in self.merge_file_list:
                self.merge_file_list.append(file)
                self.merge_file_listbox.insert(tk.END, os.path.basename(file))

    def remove_selected_merge_file(self):
        selection = self.merge_file_listbox.curselection()
        for index in reversed(selection):
            self.merge_file_listbox.delete(index)
            self.merge_file_list.pop(index)

    def clear_merge_files(self):
        self.merge_file_list.clear()
        self.merge_file_listbox.delete(0, tk.END)

    def merge_pdfs(self):
        """执行PDF合并"""
        if not self.pdf_merger:
            messagebox.showerror("错误", "PDF合并模块未初始化")
            return
        if len(self.merge_file_list) < 2:
            messagebox.showwarning("警告", "请至少选择2个PDF文件进行合并")
            return
        output_file = self.merge_output_var.get()
        if not output_file:
            messagebox.showwarning("警告", "请选择输出文件")
            return
        def merge_thread():
            try:
                self.log_message("开始PDF合并...")
                success = self.pdf_merger.merge_pdfs(self.merge_file_list, output_file)
                if success:
                    self.log_message("PDF合并成功完成")
                    messagebox.showinfo("成功", "PDF合并完成")
                else:
                    self.log_message("PDF合并失败")
                    messagebox.showerror("错误", "PDF合并失败")
            except Exception as e:
                self.log_message(f"PDF合并出错: {str(e)}")
                messagebox.showerror("错误", f"PDF合并出错: {str(e)}")
        threading.Thread(target=merge_thread, daemon=True).start()
    
    def select_split_file(self):
        file = filedialog.askopenfilename(title="选择PDF文件", filetypes=[("PDF文件", "*.pdf")])
        if file:
            self.split_file = file
            self.split_file_var.set(file)
    def clear_split_file(self):
        self.split_file = None
        self.split_file_var.set("未选择文件")

    def split_pdf(self):
        if not self.pdf_splitter:
            messagebox.showerror("错误", "PDF分割模块未初始化")
            return
        if not self.split_file:
            messagebox.showwarning("警告", "请选择要分割的PDF文件")
            return
        input_file = self.split_file
        output_dir = self.split_output_dir.get()
        if not output_dir:
            messagebox.showwarning("警告", "请选择输出目录")
            return
        def split_thread():
            try:
                self.log_message("开始PDF分割...")
                success = False
                if self.split_method.get() == "pages":
                    try:
                        pages_per_file = int(self.pages_per_file.get())
                        success = self.pdf_splitter.split_by_pages(input_file, output_dir, pages_per_file)
                    except ValueError:
                        messagebox.showerror("错误", "页数必须是数字")
                        return
                else:
                    page_ranges = [r.strip() for r in self.page_ranges.get().split(',')]
                    success = self.pdf_splitter.split_by_page_ranges(input_file, output_dir, page_ranges)
                if success:
                    self.log_message("PDF分割成功完成")
                    messagebox.showinfo("成功", "PDF分割完成")
                else:
                    self.log_message("PDF分割失败")
                    messagebox.showerror("错误", "PDF分割失败")
            except Exception as e:
                self.log_message(f"PDF分割出错: {str(e)}")
                messagebox.showerror("错误", f"PDF分割出错: {str(e)}")
        threading.Thread(target=split_thread, daemon=True).start()

    def select_convert_files(self):
        t = self.convert_type.get()
        if t == "图片转PDF":
            files = filedialog.askopenfilenames(title="选择图片文件", filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        else:
            files = filedialog.askopenfilenames(title="选择PDF文件", filetypes=[("PDF文件", "*.pdf")])
        if files:
            self.convert_files_list = list(files)
            self.convert_files_listbox.delete(0, tk.END)
            for f in self.convert_files_list:
                self.convert_files_listbox.insert(tk.END, f)
    def clear_convert_files(self):
        self.convert_files_list = []
        self.convert_files_listbox.delete(0, tk.END)

    def convert_files(self):
        if not self.pdf_converter:
            messagebox.showerror("错误", "PDF转换模块未初始化")
            return
        if not self.convert_files_list:
            messagebox.showwarning("警告", "请选择要转换的文件")
            return
        convert_type = self.convert_type.get()
        output_path = self.convert_output.get()
        if not output_path:
            messagebox.showwarning("警告", "请选择输出路径")
            return
        def convert_thread():
            try:
                self.log_message("开始文件转换...")
                success = False
                final_output_path = output_path
                
                if convert_type == 'PDF转图片':
                    success = self.pdf_converter.pdf_to_images(
                        self.convert_files_list[0], final_output_path, 
                        format='PNG', dpi=300
                    )
                elif convert_type == '图片转PDF':
                    # 确保输出路径是文件而不是目录
                    if os.path.isdir(final_output_path):
                        final_output_path = os.path.join(final_output_path, "converted.pdf")
                    success = self.pdf_converter.images_to_pdf(self.convert_files_list, final_output_path)
                elif convert_type == 'PDF转文本':
                    # 确保输出路径是文件而不是目录
                    if os.path.isdir(final_output_path):
                        final_output_path = os.path.join(final_output_path, "converted.txt")
                    success = self.pdf_converter.pdf_to_text(self.convert_files_list[0], final_output_path)
                elif convert_type == 'PDF压缩':
                    # 确保输出路径是文件而不是目录
                    if os.path.isdir(final_output_path):
                        final_output_path = os.path.join(final_output_path, "compressed.pdf")
                    success = self.pdf_converter.compress_pdf(self.convert_files_list[0], final_output_path)
                
                if success:
                    self.log_message("文件转换成功完成")
                    messagebox.showinfo("成功", "文件转换完成")
                else:
                    self.log_message("文件转换失败")
                    messagebox.showerror("错误", "文件转换失败")
            except Exception as e:
                self.log_message(f"文件转换出错: {str(e)}")
                messagebox.showerror("错误", f"文件转换出错: {str(e)}")
        
        threading.Thread(target=convert_thread, daemon=True).start()

    def select_security_file(self):
        file = filedialog.askopenfilename(title="选择PDF文件", filetypes=[("PDF文件", "*.pdf")])
        if file:
            self.security_file = file
            self.security_file_var.set(file)
    def clear_security_file(self):
        self.security_file = None
        self.security_file_var.set("未选择文件")

    def perform_security_operation(self):
        if not self.pdf_security:
            messagebox.showerror("错误", "PDF安全模块未初始化")
            return
        if not self.security_file:
            messagebox.showwarning("警告", "请选择要处理的PDF文件")
            return
        input_file = self.security_file
        output_file = self.security_output.get()
        password = self.password.get()
        user_password = self.user_password.get() if self.user_password.get() else None
        if not output_file:
            messagebox.showwarning("警告", "请选择输出文件")
            return
        if not password:
            messagebox.showwarning("警告", "请输入密码")
            return
        operation = self.security_operation.get()
        def security_thread():
            try:
                self.log_message("开始安全操作...")
                success = False
                if operation == 'encrypt':
                    success = self.pdf_security.encrypt_pdf(input_file, output_file, password, user_password)
                elif operation == 'decrypt':
                    success = self.pdf_security.decrypt_pdf(input_file, output_file, password)
                elif operation == 'remove_password':
                    success = self.pdf_security.remove_password(input_file, output_file, password)
                if success:
                    self.log_message("安全操作成功完成")
                    messagebox.showinfo("成功", "安全操作完成")
                else:
                    self.log_message("安全操作失败")
                    messagebox.showerror("错误", "安全操作失败")
            except Exception as e:
                self.log_message(f"安全操作出错: {str(e)}")
                messagebox.showerror("错误", f"安全操作出错: {str(e)}")
        threading.Thread(target=security_thread, daemon=True).start()
    
    # 日志方法
    def log_message(self, message):
        """添加日志消息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.logger.info(message)
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END) 