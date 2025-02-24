"""Genbank 水印服务层，处理业务逻辑"""

from typing import Dict, Any
from dna_watermark import watermark

def insert_watermark_to_genbank(
    genbank_data: Dict[str, Any],
    watermark_text: str,
    algorithm: str = "plaintext",
    position: str = "before-cds"
) -> Dict[str, Any]:
    """在 Genbank 文件中插入水印
    
    Args:
        genbank_data: Genbank 数据字典
        watermark_text: 水印文本
        algorithm: 水印算法类型 ("plaintext" 或 "encrypted")
        position: 插入位置 ("before-cds" 或 "after-cds")
        
    Returns:
        包含处理结果的字典
        
    Raises:
        ValueError: 当输入数据格式不正确时
        NotImplementedError: 当使用不支持的算法时
    """
    # 验证输入数据
    validate_genbank_data(genbank_data)
    validate_watermark_text(watermark_text)
    validate_position(position)
    
    # 调用核心模块处理
    return watermark.insert_watermark(
        genbank_data=genbank_data,
        watermark_text=watermark_text,
        algorithm=algorithm,
        position=position
    )

def validate_genbank_data(data: Dict[str, Any]) -> None:
    """验证 Genbank 数据格式
    
    Args:
        data: 要验证的数据
        
    Raises:
        ValueError: 当数据格式不正确时
    """
    required_fields = {
        "genbankData": str,
        "genbankInfo": dict
    }
    
    for field, field_type in required_fields.items():
        if field not in data:
            raise ValueError(f"缺少必要字段：{field}")
        if not isinstance(data[field], field_type):
            raise ValueError(f"字段 {field} 类型错误")
            
    if "nucleotideSequence" not in data["genbankInfo"]:
        raise ValueError("缺少核苷酸序列信息")
        
    if "cdsRegion" not in data["genbankInfo"]:
        raise ValueError("缺少 CDS 区域信息")

def validate_watermark_text(text: str) -> None:
    """验证水印文本
    
    Args:
        text: 要验证的文本
        
    Raises:
        ValueError: 当文本不合法时
    """
    if not text:
        raise ValueError("水印文本不能为空")
        
    if len(text) > 100:  # 设置最大长度限制
        raise ValueError("水印文本过长，最大支持 100 个字符")

def validate_position(position: str) -> None:
    """验证插入位置参数
    
    Args:
        position: 插入位置参数
        
    Raises:
        ValueError: 当位置参数不合法时
    """
    valid_positions = ["before-cds", "after-cds"]
    if position not in valid_positions:
        raise ValueError(f"不支持的插入位置：{position}。支持的位置：{', '.join(valid_positions)}") 