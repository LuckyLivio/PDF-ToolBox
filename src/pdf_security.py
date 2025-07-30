import os
from PyPDF2 import PdfReader, PdfWriter
from typing import Optional
import logging

class PDFSecurity:
    """PDF安全工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def encrypt_pdf(self, input_file: str, output_file: str, password: str, 
                   user_password: Optional[str] = None) -> bool:
        """
        加密PDF文件
        
        Args:
            input_file: 输入PDF文件路径
            output_file: 输出PDF文件路径
            password: 所有者密码
            user_password: 用户密码（可选）
            
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            
            with open(input_file, 'rb') as file:
                reader = PdfReader(file)
                writer = PdfWriter()
                
                # 添加所有页面
                for page in reader.pages:
                    writer.add_page(page)
                
                # 设置加密
                if user_password:
                    writer.encrypt(user_password, password)
                else:
                    writer.encrypt(password)
                
                with open(output_file, 'wb') as output:
                    writer.write(output)
                
                self.logger.info(f"PDF加密成功: {output_file}")
                return True
                
        except Exception as e:
            self.logger.error(f"PDF加密失败: {str(e)}")
            return False
    
    def decrypt_pdf(self, input_file: str, output_file: str, password: str) -> bool:
        """
        解密PDF文件
        
        Args:
            input_file: 输入PDF文件路径
            output_file: 输出PDF文件路径
            password: 密码
            
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            
            with open(input_file, 'rb') as file:
                reader = PdfReader(file)
                
                # 尝试解密
                if reader.is_encrypted:
                    try:
                        reader.decrypt(password)
                    except Exception as e:
                        self.logger.error(f"密码错误或解密失败: {str(e)}")
                        return False
                
                writer = PdfWriter()
                
                # 添加所有页面
                for page in reader.pages:
                    writer.add_page(page)
                
                with open(output_file, 'wb') as output:
                    writer.write(output)
                
                self.logger.info(f"PDF解密成功: {output_file}")
                return True
                
        except Exception as e:
            self.logger.error(f"PDF解密失败: {str(e)}")
            return False
    
    def is_encrypted(self, input_file: str) -> bool:
        """
        检查PDF是否已加密
        
        Args:
            input_file: PDF文件路径
            
        Returns:
            bool: 是否已加密
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            
            with open(input_file, 'rb') as file:
                reader = PdfReader(file)
                return reader.is_encrypted
                
        except Exception as e:
            self.logger.error(f"检查加密状态失败: {str(e)}")
            return False
    
    def get_encryption_info(self, input_file: str) -> Optional[dict]:
        """
        获取PDF加密信息
        
        Args:
            input_file: PDF文件路径
            
        Returns:
            dict: 加密信息字典
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return None
            
            with open(input_file, 'rb') as file:
                reader = PdfReader(file)
                
                if not reader.is_encrypted:
                    return {'encrypted': False}
                
                # 获取加密信息
                encryption_info = {
                    'encrypted': True,
                    'encryption_method': reader.encryption_method,
                    'file_id': reader.file_id,
                    'metadata': reader.metadata
                }
                
                return encryption_info
                
        except Exception as e:
            self.logger.error(f"获取加密信息失败: {str(e)}")
            return None
    
    def remove_password(self, input_file: str, output_file: str, password: str) -> bool:
        """
        移除PDF密码保护
        
        Args:
            input_file: 输入PDF文件路径
            output_file: 输出PDF文件路径
            password: 当前密码
            
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            
            with open(input_file, 'rb') as file:
                reader = PdfReader(file)
                
                if reader.is_encrypted:
                    try:
                        reader.decrypt(password)
                    except Exception as e:
                        self.logger.error(f"密码错误或解密失败: {str(e)}")
                        return False
                
                writer = PdfWriter()
                
                # 添加所有页面
                for page in reader.pages:
                    writer.add_page(page)
                
                # 复制元数据
                if reader.metadata:
                    writer.add_metadata(reader.metadata)
                
                with open(output_file, 'wb') as output:
                    writer.write(output)
                
                self.logger.info(f"密码移除成功: {output_file}")
                return True
                
        except Exception as e:
            self.logger.error(f"密码移除失败: {str(e)}")
            return False 