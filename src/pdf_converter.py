import os
import fitz  # PyMuPDF
from PIL import Image
import img2pdf
from typing import List, Optional
import logging

class PDFConverter:
    """PDF格式转换工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def pdf_to_images(self, input_file: str, output_dir: str, format: str = 'PNG', 
                     dpi: int = 300, page_range: Optional[List[int]] = None) -> bool:
        """
        将PDF转换为图片
        
        Args:
            input_file: 输入PDF文件路径
            output_dir: 输出目录
            format: 图片格式 (PNG, JPEG, TIFF)
            dpi: 分辨率
            page_range: 页码范围，None表示所有页面
            
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            
            os.makedirs(output_dir, exist_ok=True)
            
            # 打开PDF文件
            pdf_document = fitz.open(input_file)
            
            # 确定要处理的页面
            if page_range is None:
                pages_to_process = range(len(pdf_document))
            else:
                pages_to_process = [p - 1 for p in page_range if 1 <= p <= len(pdf_document)]
            
            # 设置缩放矩阵
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            
            for page_num in pages_to_process:
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap(matrix=mat)
                
                # 保存图片
                output_file = os.path.join(output_dir, f"page_{page_num + 1:03d}.{format.lower()}")
                pix.save(output_file)
                
                self.logger.info(f"已生成: {output_file}")
            
            pdf_document.close()
            return True
            
        except Exception as e:
            self.logger.error(f"PDF转图片失败: {str(e)}")
            return False
    
    def images_to_pdf(self, image_files: List[str], output_file: str, 
                     page_size: str = 'A4', orientation: str = 'portrait') -> bool:
        """
        将图片转换为PDF
        
        Args:
            image_files: 图片文件路径列表
            output_file: 输出PDF文件路径
            page_size: 页面大小 (A4, A3, Letter等)
            orientation: 方向 (portrait, landscape)
            
        Returns:
            bool: 是否成功
        """
        try:
            if not image_files:
                self.logger.error("没有提供图片文件")
                return False
            
            # 检查所有图片文件是否存在
            for img_file in image_files:
                if not os.path.exists(img_file):
                    self.logger.error(f"图片文件不存在: {img_file}")
                    return False
            
            # 使用img2pdf转换
            with open(output_file, "wb") as f:
                f.write(img2pdf.convert(image_files))
            
            self.logger.info(f"图片转PDF成功: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"图片转PDF失败: {str(e)}")
            return False
    
    def pdf_to_text(self, input_file: str, output_file: str, 
                   page_range: Optional[List[int]] = None) -> bool:
        """
        将PDF转换为文本
        
        Args:
            input_file: 输入PDF文件路径
            output_file: 输出文本文件路径
            page_range: 页码范围，None表示所有页面
            
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            
            pdf_document = fitz.open(input_file)
            
            # 确定要处理的页面
            if page_range is None:
                pages_to_process = range(len(pdf_document))
            else:
                pages_to_process = [p - 1 for p in page_range if 1 <= p <= len(pdf_document)]
            
            with open(output_file, 'w', encoding='utf-8') as text_file:
                for page_num in pages_to_process:
                    page = pdf_document.load_page(page_num)
                    text = page.get_text()
                    text_file.write(f"=== 第 {page_num + 1} 页 ===\n")
                    text_file.write(text)
                    text_file.write("\n\n")
            
            pdf_document.close()
            self.logger.info(f"PDF转文本成功: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"PDF转文本失败: {str(e)}")
            return False
    
    def compress_pdf(self, input_file: str, output_file: str, 
                    quality: int = 85, image_quality: int = 70) -> bool:
        """
        压缩PDF文件
        
        Args:
            input_file: 输入PDF文件路径
            output_file: 输出PDF文件路径
            quality: 压缩质量 (0-100)
            image_quality: 图片压缩质量 (0-100)
            
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return False
            
            pdf_document = fitz.open(input_file)
            
            # 创建新的PDF文档
            new_doc = fitz.open()
            
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
                
                # 复制页面内容
                new_page.show_pdf_page(page.rect, pdf_document, page_num)
            
            # 保存压缩后的PDF
            new_doc.save(output_file, garbage=4, deflate=True, clean=True)
            new_doc.close()
            pdf_document.close()
            
            self.logger.info(f"PDF压缩成功: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"PDF压缩失败: {str(e)}")
            return False
    
    def get_pdf_info(self, input_file: str) -> Optional[dict]:
        """
        获取PDF文件详细信息
        
        Args:
            input_file: PDF文件路径
            
        Returns:
            dict: PDF信息字典
        """
        try:
            if not os.path.exists(input_file):
                self.logger.error(f"文件不存在: {input_file}")
                return None
            
            pdf_document = fitz.open(input_file)
            
            info = {
                'pages': len(pdf_document),
                'file_size': os.path.getsize(input_file),
                'metadata': pdf_document.metadata,
                'page_info': []
            }
            
            # 获取每页信息
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                page_info = {
                    'page_number': page_num + 1,
                    'width': page.rect.width,
                    'height': page.rect.height,
                    'rotation': page.rotation
                }
                info['page_info'].append(page_info)
            
            pdf_document.close()
            return info
            
        except Exception as e:
            self.logger.error(f"获取PDF信息失败: {str(e)}")
            return None 