#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的测试程序 - 用于诊断exe打包问题
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def main():
    try:
        # 创建主窗口
        root = tk.Tk()
        root.title("PDF工具箱 - 测试版")
        root.geometry("400x300")
        
        # 添加测试信息
        info_text = f"""
系统信息:
- Python版本: {sys.version}
- 操作系统: {os.name}
- 当前目录: {os.getcwd()}

如果能看到这个窗口，说明基本环境正常。
        """
        
        label = tk.Label(root, text=info_text, justify=tk.LEFT, font=("Arial", 10))
        label.pack(pady=20, padx=20)
        
        # 测试按钮
        def test_click():
            messagebox.showinfo("测试", "按钮点击正常！")
        
        test_btn = tk.Button(root, text="点击测试", command=test_click)
        test_btn.pack(pady=10)
        
        # 退出按钮
        exit_btn = tk.Button(root, text="退出", command=root.quit)
        exit_btn.pack(pady=10)
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        # 如果GUI失败，尝试显示错误信息
        try:
            messagebox.showerror("错误", f"程序启动失败: {str(e)}")
        except:
            print(f"程序启动失败: {str(e)}")
            input("按回车键退出...")

if __name__ == "__main__":
    main() 