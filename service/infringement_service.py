"""基因侵权检测服务"""

from typing import Dict, List, Any
from models.database import get_db
from models.watermark import WatermarkedSequence

def find_sequence_match(target_sequence: str, watermark_sequence: str) -> Dict[str, Any]:
    """查找目标序列中是否包含水印序列
    
    Args:
        target_sequence: 待检测的目标序列
        watermark_sequence: 水印序列
        
    Returns:
        包含匹配信息的字典：
        {
            "matched": bool,          # 是否匹配
            "position": str | None,   # 匹配位置（格式：start..end）
            "matched_sequence": str | None  # 匹配到的序列
        }
    """
    # 转换为小写进行比较
    target_sequence = target_sequence.lower()
    watermark_sequence = watermark_sequence.lower()
    
    # 查找水印序列在目标序列中的位置
    start_pos = target_sequence.find(watermark_sequence)
    
    if start_pos != -1:
        end_pos = start_pos + len(watermark_sequence)
        return {
            "matched": True,
            "position": f"{start_pos + 1}..{end_pos}",  # 转换为1-based位置
            "matched_sequence": watermark_sequence
        }
    
    return {
        "matched": False,
        "position": None,
        "matched_sequence": None
    }

def detect_sequence_infringement(sequence: str) -> Dict[str, Any]:
    """检测序列是否存在侵权
    
    Args:
        sequence: 待检测的核苷酸序列
        
    Returns:
        包含检测结果的字典：
        {
            "matches": [  # 匹配到的记录列表
                {
                    "record_id": int,        # 记录ID
                    "object_id": str,        # UUID
                    "created_at": str,       # 创建时间
                    "updated_at": str,       # 更新时间
                    "algorithm": str,        # 水印算法类型
                    "original_text": str,    # 原始水印文本
                    "password": str,         # 密码（仅加密模式）
                    "watermark_sequence": str,  # 水印DNA序列
                    "position": str,         # 匹配位置（格式：start..end）
                    "original_sequence": str,  # 原始DNA序列
                    "watermarked_sequence": str,  # 插入水印后的DNA序列
                    "original_genbank": str,  # 原始GenBank文件内容
                    "watermarked_genbank": str,  # 插入水印后的GenBank文件内容
                    "genbank_accession": str,  # GenBank登录号
                    "genbank_organism": str,   # 生物体名称
                    "genbank_definition": str,  # 序列定义
                    "matched_sequence": str,    # 匹配到的序列
                    "matched_position": str     # 在目标序列中的匹配位置
                },
                ...
            ],
            "total_matches": int  # 匹配到的记录总数
        }
        
    Raises:
        ValueError: 当输入序列为空时
    """
    if not sequence:
        raise ValueError("输入序列不能为空")
        
    # 获取数据库会话
    db = next(get_db())
    
    # 查询所有水印记录
    records = db.query(WatermarkedSequence).all()
    
    # 进行序列匹配
    matches = []
    for record in records:
        match_result = find_sequence_match(sequence, record.watermark_sequence)
        
        if match_result["matched"]:
            # 处理换行符
            original_genbank = record.original_genbank.replace('\\n', '\n').replace('\n', '\\n') if record.original_genbank else None
            watermarked_genbank = record.watermarked_genbank.replace('\\n', '\n').replace('\n', '\\n') if record.watermarked_genbank else None
            original_sequence = record.original_sequence.replace('\\n', '\n').replace('\n', '\\n') if record.original_sequence else None
            watermarked_sequence = record.watermarked_sequence.replace('\\n', '\n').replace('\n', '\\n') if record.watermarked_sequence else None
            
            matches.append({
                "record_id": record.id,
                "object_id": record.object_id,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat(),
                "algorithm": record.algorithm,
                "original_text": record.original_text,
                "password": record.password,
                "watermark_sequence": record.watermark_sequence,
                "position": record.position,
                "original_sequence": original_sequence,
                "watermarked_sequence": watermarked_sequence,
                "original_genbank": original_genbank,
                "watermarked_genbank": watermarked_genbank,
                "genbank_accession": record.genbank_accession,
                "genbank_organism": record.genbank_organism,
                "genbank_definition": record.genbank_definition,
                "matched_sequence": match_result["matched_sequence"],
                "matched_position": match_result["position"]
            })
    
    return {
        "matches": matches,
        "total_matches": len(matches)
    } 