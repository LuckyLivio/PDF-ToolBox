#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制台版打包脚本 - 带控制台窗口，方便查看错误信息
"""

import os
import sys
import subprocess
import shutil

def build_console_exe():
    """构建带控制台窗口的exe文件"""
    print("开始构建控制台版exe...")
    
    # 带控制台窗口的PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个文件
        "--console",  # 有控制台窗口，方便查看错误
        "--name=PDF工具箱_控制台版",  # 可执行文件名称
        "--debug=all",  # 添加调试信息
        "run.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("控制台版exe文件构建成功！")
        
        # 检查输出文件
        exe_path = os.path.join("dist", "PDF工具箱_控制台版.exe")
        if os.path.exists(exe_path):
            print(f"控制台版exe文件位置: {os.path.abspath(exe_path)}")
            return True
        else:
            print("未找到生成的控制台版exe文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def clean_build():
    """清理构建文件"""
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["PDF工具箱_控制台版.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除目录: {dir_name}")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"已删除文件: {file_name}")

def main():
    """主函数"""
    print("PDF工具箱 - 控制台版打包脚本")
    print("=" * 50)
    
    # 清理之前的构建文件
    print("清理之前的构建文件...")
    clean_build()
    
    # 构建控制台版exe
    if build_console_exe():
        print("\n控制台版构建完成！")
        print("请尝试运行 dist/PDF工具箱_控制台版.exe")
        print("这个版本会显示控制台窗口，可以看到详细的错误信息")
    else:
        print("\n控制台版构建失败！")

if __name__ == "__main__":
    main() 