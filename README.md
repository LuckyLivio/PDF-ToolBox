# PDF-ToolBox｜PDF 工具箱

一个本地运行的 Python 桌面工具，把常见 PDF 处理步骤集中到一个 Tkinter 窗口，适合不想上传文件到在线服务的场景。仓库含源码和打包脚本，**未提交可直接下载的 exe**。

## 已实现

| 模块 | 代码中可核对的功能 |
| --- | --- |
| 合并 | 添加和排序多个 PDF，按文件或选定页范围合并 |
| 拆分 | 按页数、页码范围、书签或近似文件大小拆分；提取指定页 |
| 转换 | PDF 转 PNG/JPEG/TIFF 或文本，图片转 PDF，PDF 压缩 |
| 安全 | 加密、用已知密码解密、移除密码保护 |

入口在 [`main.py`](main.py)，界面事件在 [`src/gui/main_window.py`](src/gui/main_window.py)，文件处理分为 [`src/pdf_merger.py`](src/pdf_merger.py)、[`src/pdf_splitter.py`](src/pdf_splitter.py)、[`src/pdf_converter.py`](src/pdf_converter.py) 和 [`src/pdf_security.py`](src/pdf_security.py)。仓库没有记录多人分工；以下是实现层面的面试讲解点，个人负责范围待作者确认。

## 面试可讲的技术点

1. 将 GUI 的文件选择、参数校验和日志反馈与 PDF 处理模块分开；耗时操作由界面线程外执行，避免窗口卡死。
2. 统一处理用户可理解的 1 起始页码与库内部页码，并明确按“目标大小”拆分只是估算，压缩效果取决于源文件。

## 从源码运行

建议 Windows 10/11、Python 3.10+。在仓库根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

界面有合并、拆分、转换、安全四个页签。先选择输入文件与输出位置，再执行操作。处理自己的私有文件时，建议先用副本试运行。仓库暂无经核实可公开的截图或在线演示。

如需自己打包，可在安装依赖后运行 `python build_exe.py`；脚本会尝试安装 PyInstaller。仓库当前没有预构建二进制，也没有验证所有 Windows 环境的兼容性。

## 已知边界

- 加解密需要已知密码；这不是密码破解工具。
- 图像转 PDF、PDF 压缩可能改变图像质量；按大小拆分使用平均每页大小估算，结果不保证严格落在目标大小以内。
- 未提供自动化 GUI 回归测试；具体文件格式和复杂 PDF 的兼容性需要按样本验证。
