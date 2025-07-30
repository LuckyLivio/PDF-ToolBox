#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF工具箱 - 启动脚本
避免相对导入问题
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

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
        
        # 导入GUI模块
        from gui.main_window import PDFToolboxGUI
        
        # 创建主窗口
        root = tk.Tk()
        
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