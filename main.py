#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF工具箱 - 主程序
支持PDF合并、分割、转换、加密等功能
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gui.main_window import PDFToolboxGUI
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所有依赖包")
    sys.exit(1)

def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pdf_toolbox.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main():
    """主函数"""
    try:
        # 设置日志
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("启动PDF工具箱")
        
        # 创建主窗口
        root = tk.Tk()
        
        # 设置窗口图标（如果有的话）
        try:
            # 可以在这里设置窗口图标
            pass
        except:
            pass
        
        # 创建应用
        app = PDFToolboxGUI(root)
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        logger.error(f"程序启动失败: {e}")
        messagebox.showerror("错误", f"程序启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

