"""水印服务层，处理业务逻辑"""

from dna_watermark.core import embed_watermark as core_embed
from dna_watermark.core import extract_watermark as core_extract

class WatermarkService:
    """水印服务"""
    
    @staticmethod
    def embed_watermark(sequence: str, message: str) -> str:
        """
        嵌入水印
        
        Args:
            sequence: DNA序列
            message: 水印信息
            
        Returns:
            str: 嵌入水印后的序列
        """
        # TODO: 添加业务逻辑，如验证、日志等
        return core_embed(sequence, message)
    
    @staticmethod
    def extract_watermark(sequence: str) -> str:
        """
        提取水印
        
        Args:
            sequence: 包含水印的DNA序列
            
        Returns:
            str: 提取的水印信息
        """
        # TODO: 添加业务逻辑，如验证、日志等
        return core_extract(sequence) 