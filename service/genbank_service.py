"""GenBank 数据解析服务"""

from io import StringIO
from typing import Any, Dict, List, Union
from Bio import SeqIO
from Bio.SeqFeature import SimpleLocation

def convert_to_serializable(obj: Any) -> Union[Dict[str, Any], List[Any], str, None]:
    """将对象转换为可序列化的格式
    
    Args:
        obj: 需要转换的对象
    
    Returns:
        转换后的可序列化对象
    """
    if hasattr(obj, '__dict__'):
        return {key: convert_to_serializable(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (SimpleLocation, type(None), str, int, float, bool)):
        return str(obj) if obj is not None else None
    else:
        return str(obj)

def parse_genbank_data(data: str) -> Dict[str, Any]:
    """使用 BioPython 解析 GenBank 格式数据
    
    Args:
        data: GenBank 格式的字符串数据
    
    Returns:
        解析后的数据字典，包含完整的 GenBank 记录
    """
    handle = StringIO(data)
    
    try:
        # 解析 GenBank 记录
        record = SeqIO.read(handle, "genbank")
        
        # 创建基本结果字典
        result: Dict[str, Any] = {
            'id': record.id,
            'name': record.name,
            'description': record.description,
            'seq': str(record.seq),
            'features': [
                {
                    'type': feature.type,
                    'location': str(feature.location),
                    'qualifiers': feature.qualifiers,
                    'id': feature.id,
                    'ref': feature.ref,
                    'ref_db': feature.ref_db
                }
                for feature in record.features
            ],
            'annotations': convert_to_serializable(record.annotations),
            'dbxrefs': record.dbxrefs,
            'letter_annotations': convert_to_serializable(record.letter_annotations)
        }
        
        # 添加其他字段
        record_dict = convert_to_serializable(record.__dict__)
        if isinstance(record_dict, dict):
            for key, value in record_dict.items():
                if key not in result:
                    result[key] = value
        
        return result
    
    except Exception as e:
        raise ValueError(f"无法解析 GenBank 数据: {str(e)}")
    
    finally:
        handle.close()

def format_sequence(sequence: str, line_length: int = 60, positions_per_line: int = 10) -> list:
    """格式化 DNA 序列
    
    Args:
        sequence: 原始序列
        line_length: 每行的碱基数
        positions_per_line: 每行显示的位置数
    
    Returns:
        格式化后的序列列表
    """
    formatted = []
    for i in range(0, len(sequence), line_length):
        # 获取当前行的序列
        line_seq = sequence[i:i + line_length]
        # 计算位置
        position = i + 1
        # 将序列分成固定长度的片段
        chunks = [line_seq[j:j + 10] for j in range(0, len(line_seq), 10)]
        formatted.append({
            "position": position,
            "sequence": " ".join(chunks)
        })
    return formatted 