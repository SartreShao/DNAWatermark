"""水印服务层，处理业务逻辑"""

from dna_watermark.core import embed_watermark as core_embed
from dna_watermark.core import extract_watermark as core_extract

def validate_dna_sequence(sequence):
    """验证DNA序列是否合法
    
    Args:
        sequence (str): 要验证的DNA序列
        
    Returns:
        bool: 序列是否合法（只包含ATCG）
    """
    return all(base in 'ATCG' for base in sequence)

def validate_watermark_message(message):
    """验证水印信息是否合法
    
    Args:
        message (str): 要验证的水印信息
        
    Returns:
        bool: 水印信息是否合法（长度在1-100之间）
    """
    return len(message) > 0 and len(message) <= 100  # 示例验证规则

def embed_watermark_with_service(sequence, message):
    """嵌入水印（服务层）
    
    Args:
        sequence (str): DNA序列，只能包含ATCG
        message (str): 水印信息，长度需在1-100之间
        
    Returns:
        str: 嵌入水印后的序列
        
    Raises:
        ValueError: 当输入参数不合法时抛出，可能的错误信息：
            - "无效的DNA序列，只能包含ATCG"
            - "无效的水印信息"
    """
    # 输入验证
    if not validate_dna_sequence(sequence):
        raise ValueError("无效的DNA序列，只能包含ATCG")
    
    if not validate_watermark_message(message):
        raise ValueError("无效的水印信息")
    
    # TODO: 添加日志记录
    # TODO: 添加审计跟踪
    
    return core_embed(sequence, message)

def extract_watermark_with_service(sequence):
    """提取水印（服务层）
    
    Args:
        sequence (str): 包含水印的DNA序列，只能包含ATCG
        
    Returns:
        str: 提取的水印信息
        
    Raises:
        ValueError: 当输入序列不合法时抛出，错误信息：
            - "无效的DNA序列，只能包含ATCG"
    """
    # 输入验证
    if not validate_dna_sequence(sequence):
        raise ValueError("无效的DNA序列，只能包含ATCG")
    
    # TODO: 添加日志记录
    # TODO: 添加审计跟踪
    
    return core_extract(sequence) 