"""基因侵权检测相关的路由"""

from flask import Blueprint, jsonify, request
from service.infringement_service import detect_sequence_infringement

bp = Blueprint('infringement', __name__, url_prefix='/api/infringement')

def create_response(success: bool, data=None, message: str = "") -> dict:
    """创建统一的响应格式"""
    return {
        "success": success,
        "data": data,
        "message": message
    }

@bp.route('/detect', methods=['POST'])
def detect_infringement():
    """检测序列是否存在侵权
    
    请求体格式：
    {
        "sequence": str,  # 待检测的核苷酸序列
    }
    
    返回格式：
    {
        "success": bool,
        "data": {
            "matches": [  # 匹配到的记录列表
                {
                    "record_id": int,        # 记录ID
                    "object_id": str,        # UUID
                    "created_at": str,       # 创建时间
                    "algorithm": str,        # 水印算法类型
                    "position": str,         # 匹配位置（格式：start..end）
                    "matched_sequence": str,  # 匹配到的序列
                    "original_text": str,    # 原始水印文本
                    "genbank_accession": str,  # GenBank登录号
                    "genbank_organism": str    # 生物体名称
                },
                ...
            ],
            "total_matches": int  # 匹配到的记录总数
        },
        "message": str
    }
    """
    try:
        data = request.get_json()
        
        # 验证输入
        if not data or "sequence" not in data:
            return jsonify(create_response(
                success=False,
                message="缺少必要参数：sequence"
            )), 400
            
        # 调用服务层处理
        result = detect_sequence_infringement(data["sequence"])
        
        return jsonify(create_response(
            success=True,
            data=result,
            message="检测完成"
        ))
        
    except ValueError as e:
        return jsonify(create_response(
            success=False,
            message=str(e)
        )), 400
        
    except Exception as e:
        return jsonify(create_response(
            success=False,
            message=f"检测失败：{str(e)}"
        )), 500 