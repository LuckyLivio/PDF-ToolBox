# PDF工具箱

一个功能完整的PDF处理工具，支持PDF合并、分割、格式转换、加密等功能，提供友好的图形用户界面。

## 功能特性

### 🔗 PDF合并
- 合并多个PDF文件
- 支持按指定顺序合并
- 支持选择特定页面范围

### ✂️ PDF分割
- 按页数分割PDF文件
- 按指定页码范围分割
- 提取特定页面

### 🔄 格式转换
- PDF转图片（PNG、JPEG、TIFF）
- 图片转PDF
- PDF转文本
- PDF压缩

### 🔒 安全功能
- PDF加密
- PDF解密
- 移除密码保护

## 系统要求

- Windows 10/11
- Python 3.7+（开发环境）
- 无需额外安装Python环境（使用打包后的exe文件）

## 安装和使用

### 方法一：使用打包后的exe文件（推荐）

1. 下载 `PDF工具箱.exe` 文件
2. 双击运行，无需安装任何依赖

### 方法二：从源码运行

1. 克隆或下载项目源码
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行主程序：
   ```bash
   python main.py
   ```

## 打包成exe

如果你想自己打包exe文件：

```bash
python build_exe.py
```

打包完成后，exe文件将生成在 `dist` 目录中。

## 项目结构

```
PDFConverter/
├── main.py                 # 主程序入口
├── build_exe.py           # 打包脚本
├── requirements.txt       # 依赖包列表
├── README.md             # 项目说明
└── src/                  # 源代码目录
    ├── __init__.py
    ├── pdf_merger.py     # PDF合并模块
    ├── pdf_splitter.py   # PDF分割模块
    ├── pdf_converter.py  # PDF转换模块
    ├── pdf_security.py   # PDF安全模块
    └── gui/              # 图形界面模块
        ├── __init__.py
        └── main_window.py # 主窗口界面
```

## 使用说明

### PDF合并
1. 点击"添加PDF文件"选择要合并的PDF文件
2. 设置输出文件名
3. 点击"开始合并"

### PDF分割
1. 选择一个PDF文件
2. 选择分割方式（按页数或页码范围）
3. 设置输出目录
4. 点击"开始分割"

### 格式转换
1. 选择要转换的文件
2. 选择转换类型
3. 设置输出路径
4. 点击"开始转换"

### 安全操作
1. 选择一个PDF文件
2. 选择操作类型（加密/解密/移除密码）
3. 输入密码
4. 设置输出文件
5. 点击"执行操作"

## 技术栈

- **Python 3.7+**: 主要编程语言
- **tkinter**: 图形用户界面
- **PyPDF2**: PDF文件处理
- **PyMuPDF (fitz)**: PDF高级操作
- **Pillow**: 图像处理
- **img2pdf**: 图片转PDF
- **PyInstaller**: 打包工具

## 开发说明

### 模块化设计
项目采用模块化设计，每个功能都有独立的模块：
- `pdf_merger.py`: 处理PDF合并相关功能
- `pdf_splitter.py`: 处理PDF分割相关功能
- `pdf_converter.py`: 处理格式转换相关功能
- `pdf_security.py`: 处理安全相关功能
- `gui/main_window.py`: 图形界面实现

### 错误处理
所有模块都包含完善的错误处理和日志记录，确保程序稳定运行。

### 线程安全
耗时操作使用多线程处理，避免界面卡顿。

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持PDF合并、分割、转换、加密等基本功能
- 提供图形用户界面
- 支持打包成独立exe文件 