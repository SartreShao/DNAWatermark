"""Genbank 水印服务层，处理业务逻辑"""

from typing import Dict, Any, Optional
from dna_watermark import watermark, encoding

def insert_watermark_to_genbank(
    genbank_data: Dict[str, Any],
    watermark_text: str,
    algorithm: str = "plaintext",
    position: str = "before-cds",
    password: Optional[str] = None
) -> Dict[str, Any]:
    """在 Genbank 文件中插入水印
    
    Args:
        genbank_data: Genbank 数据字典
        watermark_text: 水印文本
        algorithm: 水印算法类型 ("plaintext" 或 "encrypted")
        position: 插入位置 ("before-cds" 或 "after-cds")
        password: 加密密码（仅在 algorithm 为 "encrypted" 时需要，如果不提供会自动生成）
        
    Returns:
        包含处理结果的字典
        
    Raises:
        ValueError: 当输入数据格式不正确时
        NotImplementedError: 当使用不支持的算法时
    """
    try:
        # 验证基本输入数据
        validate_genbank_data(genbank_data)
        validate_watermark_text(watermark_text)
        validate_position(position)
        validate_algorithm_type(algorithm)
        
        # 处理密码
        actual_password = None
        if algorithm == "encrypted":
            # 如果是加密模式，确保有密码
            if password is None:
                # 生成新密码
                actual_password = encoding.generate_secure_password()
                print(f"生成新密码: {actual_password}")  # 调试信息
            else:
                actual_password = password
                print(f"使用提供的密码: {actual_password}")  # 调试信息
        
        # 调用核心模块处理
        result = watermark.insert_watermark(
            genbank_data=genbank_data,
            watermark_text=watermark_text,
            algorithm=algorithm,
            position=position,
            password=actual_password
        )
        
        # 如果是加密模式，在返回结果中添加生成的密码
        if algorithm == "encrypted" and actual_password:
            if "data" not in result:
                result["data"] = {}
            if "watermarkInfo" not in result["data"]:
                result["data"]["watermarkInfo"] = {}
            result["data"]["watermarkInfo"]["password"] = actual_password
            print(f"返回结果中添加密码: {actual_password}")  # 调试信息
        
        return result
        
    except Exception as e:
        print(f"发生错误: {str(e)}")  # 调试信息
        raise

def validate_algorithm_type(algorithm: str) -> None:
    """验证算法类型
    
    Args:
        algorithm: 算法类型
        
    Raises:
        ValueError: 当算法类型不合法时
    """
    valid_algorithms = ["plaintext", "encrypted"]
    if algorithm not in valid_algorithms:
        raise ValueError(f"不支持的算法类型：{algorithm}。支持的算法：{', '.join(valid_algorithms)}")

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