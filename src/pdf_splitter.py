import os
from PyPDF2 import PdfReader, PdfWriter
from typing import List, Optional
import logging

class PDFSplitter:
    """PDF分割工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def split_by_pages(self, input_file: str, output_dir: str, pages_per_file: int = 1) -> bool:
        """
        按页数分割PDF文件
        
        Args:
            input_file: 输入PDF文件路径
            output_dir: 输出目录
            pages_per_file: 每个文件的页数
            
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            
            os.makedirs(output_dir, exist_ok=True)
            
            with open(input_file, 'rb') as file:
                reader = PdfReader(file)
                total_pages = len(reader.pages)
                
                for i in range(0, total_pages, pages_per_file):
                    writer = PdfWriter()
                    end_page = min(i + pages_per_file, total_pages)
                    
                    for page_num in range(i, end_page):
                        writer.add_page(reader.pages[page_num])
                    
                    output_file = os.path.join(output_dir, f"split_{i+1}-{end_page}.pdf")
                    with open(output_file, 'wb') as output:
                        writer.write(output)
                    
                    self.logger.info(f"已生成: {output_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"PDF分割失败: {str(e)}")
            return False
    
    def split_by_page_ranges(self, input_file: str, output_dir: str, page_ranges: List[str]) -> bool:
        """
        按指定页码范围分割PDF文件
        
        Args:
            input_file: 输入PDF文件路径
            output_dir: 输出目录
            page_ranges: 页码范围列表，格式: ["1-3", "4-6", "7,9,11"]
            
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            
            os.makedirs(output_dir, exist_ok=True)
            
            with open(input_file, 'rb') as file:
                reader = PdfReader(file)
                
                for i, page_range in enumerate(page_ranges):
                    writer = PdfWriter()
                    pages = self._parse_page_range(page_range)
                    
                    for page_num in pages:
                        if 0 <= page_num < len(reader.pages):
                            writer.add_page(reader.pages[page_num])
                    
                    output_file = os.path.join(output_dir, f"range_{i+1}_{page_range}.pdf")
                    with open(output_file, 'wb') as output:
                        writer.write(output)
                    
                    self.logger.info(f"已生成: {output_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"PDF分割失败: {str(e)}")
            return False
    
    def extract_pages(self, input_file: str, output_file: str, page_numbers: List[int]) -> bool:
        """
        提取指定页面
        
        Args:
            input_file: 输入PDF文件路径
            output_file: 输出PDF文件路径
            page_numbers: 要提取的页码列表（从1开始）
            
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
                
                for page_num in page_numbers:
                    if 1 <= page_num <= len(reader.pages):
                        writer.add_page(reader.pages[page_num - 1])
                
                with open(output_file, 'wb') as output:
                    writer.write(output)
                
                self.logger.info(f"页面提取成功: {output_file}")
                return True
                
        except Exception as e:
            self.logger.error(f"页面提取失败: {str(e)}")
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
    
    def get_page_count(self, input_file: str) -> Optional[int]:
        """
        获取PDF文件页数
        
        Args:
            input_file: PDF文件路径
            
        Returns:
            int: 页数
        """
        try:
            with open(input_file, 'rb') as file:
                reader = PdfReader(file)
                return len(reader.pages)
        except Exception as e:
            self.logger.error(f"获取页数失败: {str(e)}")
            return None 