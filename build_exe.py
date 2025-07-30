#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF工具箱 - 打包脚本
使用PyInstaller将应用打包成独立的exe文件
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller安装成功")
    except subprocess.CalledProcessError:
        print("PyInstaller安装失败")
        return False
    return True

def build_exe():
    """构建exe文件"""
    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个文件
        "--windowed",  # 无控制台窗口
        "--name=PDF工具箱",  # 可执行文件名称
        # "--icon=icon.ico",  # 图标文件（如果有的话）
        "--add-data=src;src",  # 包含src目录
        "--paths=src",  # 添加src到Python路径
        "--hidden-import=PyPDF2",
        "--hidden-import=PIL",
        "--hidden-import=img2pdf",
        "--hidden-import=fitz",
        "--hidden-import=reportlab",
        "main.py"
    ]
    
    try:
        print("开始构建exe文件...")
        subprocess.check_call(cmd)
        print("exe文件构建成功！")
        
        # 检查输出文件
        exe_path = os.path.join("dist", "PDF工具箱.exe")
        if os.path.exists(exe_path):
            print(f"可执行文件位置: {os.path.abspath(exe_path)}")
            return True
        else:
            print("未找到生成的exe文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def clean_build():
    """清理构建文件"""
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["PDF工具箱.spec"]
    
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
    print("PDF工具箱 - 打包脚本")
    print("=" * 50)
    
    # 检查是否安装了PyInstaller
    try:
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        if not install_pyinstaller():
            return
    
    # 清理之前的构建文件
    print("清理之前的构建文件...")
    clean_build()
    
    # 构建exe
    if build_exe():
        print("\n构建完成！")
        print("你可以在dist目录中找到PDF工具箱.exe文件")
        print("这个exe文件可以在任何Windows系统上运行，无需安装Python环境")
    else:
        print("\n构建失败！")
        print("请检查错误信息并重试")

if __name__ == "__main__":
    main() 