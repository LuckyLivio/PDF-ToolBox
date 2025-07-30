#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试版打包脚本 - 简化版本用于诊断问题
"""

import os
import sys
import subprocess
import shutil

def build_test_exe():
    """构建测试版exe文件"""
    print("开始构建测试版exe...")
    
    # 简化的PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个文件
        "--windowed",  # 无控制台窗口
        "--name=PDF工具箱_测试版",  # 可执行文件名称
        "--debug=all",  # 添加调试信息
        "test_simple.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("测试版exe文件构建成功！")
        
        # 检查输出文件
        exe_path = os.path.join("dist", "PDF工具箱_测试版.exe")
        if os.path.exists(exe_path):
            print(f"测试版exe文件位置: {os.path.abspath(exe_path)}")
            return True
        else:
            print("未找到生成的测试版exe文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def clean_build():
    """清理构建文件"""
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["PDF工具箱_测试版.spec"]
    
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
    print("PDF工具箱 - 测试版打包脚本")
    print("=" * 50)
    
    # 清理之前的构建文件
    print("清理之前的构建文件...")
    clean_build()
    
    # 构建测试版exe
    if build_test_exe():
        print("\n测试版构建完成！")
        print("请尝试运行 dist/PDF工具箱_测试版.exe")
        print("如果测试版能正常运行，说明打包环境没问题")
        print("如果测试版也无法运行，可能是系统环境问题")
    else:
        print("\n测试版构建失败！")

if __name__ == "__main__":
    main() 