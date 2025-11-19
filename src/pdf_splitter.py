import os
from PyPDF2 import PdfReader, PdfWriter
from typing import List, Optional
import logging
import fitz

class PDFSplitter:
    """PDF分割工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def split_by_pages(self, input_file: str, output_dir: str, pages_per_file: int = 1, cancel=None) -> bool:
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
                    if cancel and cancel():
                        self.logger.info("分割已取消")
                        return False
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
    
    def split_by_page_ranges(self, input_file: str, output_dir: str, page_ranges: List[str], cancel=None) -> bool:
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
                    if cancel and cancel():
                        self.logger.info("分割已取消")
                        return False
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

    def split_by_bookmarks(self, input_file: str, output_dir: str, level: int = 1, cancel=None) -> bool:
        """
        按书签分割PDF文件（基于PyMuPDF目录）
        Args:
            input_file: 输入PDF文件路径
            output_dir: 输出目录
            level: 分割的书签层级（1为顶层）
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            os.makedirs(output_dir, exist_ok=True)
            doc = fitz.open(input_file)
            toc = doc.get_toc(simple=True)
            # 过滤指定层级的书签
            anchors = [(t[2]-1, t[1]) for t in toc if t[0] == level]
            if not anchors:
                self.logger.info("未找到指定层级书签，无法按书签分割")
                return False
            # 计算每段的开始/结束页
            segments = []
            for i, (start_page, title) in enumerate(anchors):
                end_page = (anchors[i+1][0]-1) if i+1 < len(anchors) else doc.page_count-1
                segments.append((start_page, end_page, title))
            # 按段写出
            for i, (start, end, title) in enumerate(segments, start=1):
                if cancel and cancel():
                    self.logger.info("分割已取消")
                    return False
                writer = PdfWriter()
                with open(input_file, 'rb') as f:
                    reader = PdfReader(f)
                    for p in range(start, end+1):
                        writer.add_page(reader.pages[p])
                safe_title = ''.join(c for c in title if c not in '\\/:*?"<>|').strip() or f"segment_{i}"
                output_file = os.path.join(output_dir, f"bookmark_{i}_{safe_title}.pdf")
                with open(output_file, 'wb') as out:
                    writer.write(out)
                self.logger.info(f"已生成: {output_file}")
            return True
        except Exception as e:
            self.logger.error(f"按书签分割失败: {str(e)}")
            return False

    def split_by_size(self, input_file: str, output_dir: str, target_mb: float, cancel=None) -> bool:
        """
        按目标大小近似分割PDF（基于平均每页大小估算）
        Args:
            input_file: 输入PDF文件路径
            output_dir: 输出目录
            target_mb: 目标每文件大小（MB）
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            os.makedirs(output_dir, exist_ok=True)
            total_size = os.path.getsize(input_file)
            with open(input_file, 'rb') as file:
                reader = PdfReader(file)
                total_pages = len(reader.pages)
                if total_pages == 0:
                    return False
                avg_bytes = total_size / total_pages
                target_bytes = max(int(target_mb * 1024 * 1024), int(avg_bytes))
                pages_per_chunk = max(int(target_bytes / avg_bytes), 1)
                # 分块写出
                start = 0
                chunk_index = 1
                while start < total_pages:
                    if cancel and cancel():
                        self.logger.info("分割已取消")
                        return False
                    end = min(start + pages_per_chunk, total_pages)
                    writer = PdfWriter()
                    for p in range(start, end):
                        writer.add_page(reader.pages[p])
                    output_file = os.path.join(output_dir, f"size_{chunk_index}_{start+1}-{end}.pdf")
                    with open(output_file, 'wb') as out:
                        writer.write(out)
                    self.logger.info(f"已生成: {output_file}")
                    start = end
                    chunk_index += 1
            return True
        except Exception as e:
            self.logger.error(f"按大小分割失败: {str(e)}")
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