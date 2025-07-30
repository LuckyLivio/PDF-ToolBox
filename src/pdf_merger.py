import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from typing import List, Optional
import logging

class PDFMerger:
    """PDF合并工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def merge_pdfs(self, input_files: List[str], output_file: str) -> bool:
        """
        合并多个PDF文件
        
        Args:
            input_files: 输入PDF文件路径列表
            output_file: 输出PDF文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            merger = PdfMerger()
            
            for file_path in input_files:
                if not os.path.exists(file_path):
                    self.logger.error(f"文件不存在: {file_path}")
                    return False
                
                with open(file_path, 'rb') as file:
                    merger.append(file)
            
            with open(output_file, 'wb') as output:
                merger.write(output)
            
            merger.close()
            self.logger.info(f"PDF合并成功: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"PDF合并失败: {str(e)}")
            return False
    
    def merge_pdfs_with_order(self, file_order: List[tuple], output_file: str) -> bool:
        """
        按指定顺序合并PDF文件
        
        Args:
            file_order: [(文件路径, 页码范围), ...] 页码范围格式: "1-3" 或 "1,3,5"
            output_file: 输出PDF文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            merger = PdfMerger()
            
            for file_path, page_range in file_order:
                if not os.path.exists(file_path):
                    self.logger.error(f"文件不存在: {file_path}")
                    return False
                
                with open(file_path, 'rb') as file:
                    if page_range:
                        # 解析页码范围
                        pages = self._parse_page_range(page_range)
                        merger.append(file, pages=pages)
                    else:
                        merger.append(file)
            
            with open(output_file, 'wb') as output:
                merger.write(output)
            
            merger.close()
            self.logger.info(f"PDF合并成功: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"PDF合并失败: {str(e)}")
            return False
    
    def _parse_page_range(self, page_range: str) -> List[int]:
        """解析页码范围字符串"""
        pages = []
        parts = page_range.split(',')
        
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start - 1, end))  # PDF页码从0开始
            else:
                pages.append(int(part) - 1)
        
        return pages
    
    def get_pdf_info(self, file_path: str) -> Optional[dict]:
        """
        获取PDF文件信息
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            dict: PDF信息字典
        """
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                info = {
                    'pages': len(reader.pages),
                    'title': reader.metadata.get('/Title', ''),
                    'author': reader.metadata.get('/Author', ''),
                    'subject': reader.metadata.get('/Subject', ''),
                    'creator': reader.metadata.get('/Creator', ''),
                    'producer': reader.metadata.get('/Producer', ''),
                    'file_size': os.path.getsize(file_path)
                }
                return info
        except Exception as e:
            self.logger.error(f"获取PDF信息失败: {str(e)}")
            return None 