"""Genbank 水印相关的路由定义"""

from flask import Blueprint, request, jsonify
from service.watermark_service import insert_watermark_to_genbank, extract_watermark_from_genbank

bp = Blueprint('watermark', __name__, url_prefix='/api/watermark')

def create_response(success: bool, data=None, message: str = "") -> dict:
    """创建统一的响应格式"""
    return {
        "success": success,
        "data": data,
        "message": message
    }

@bp.route('/genbank/insert', methods=['POST'])
def insert_watermark():
    """在 Genbank 文件中插入水印
    
    请求体格式：
    {
        "genbankData": str,          # Genbank 文件内容
        "watermarkMetadata": str,    # 水印文本
        "algorithm": str,            # 水印算法 ("plaintext" 或 "encrypted")
        "insertionPosition": str,    # 插入位置 ("before-cds" 或 "after-cds")
        "genbankInfo": {            # Genbank 信息
            "nucleotideSequence": str,  # 核苷酸序列
            "cdsRegion": {
                "start": int,
                "end": int
            },
            "metadata": {
                "locus": str,
                "version": str,
                "length": int,
                "organism": str
            }
        }
    }
    
    返回格式：
    {
        "success": bool,
        "data": {
            "watermarkedSequence": str,    # 插入水印后的序列
            "watermarkInfo": {             # 水印信息
                "position": {
                    "start": int,
                    "end": int
                },
                "sequence": str,           # 水印 DNA 序列
                "originalText": str,       # 原始水印文本
                "algorithm": str,          # 使用的算法
                "salt": str,              # 加密盐值（仅在加密模式下返回）
                "password": str           # 生成的密码（仅在加密模式下返回）
            },
            "genbankFile": str            # 更新后的 Genbank 文件内容
        },
        "message": str
    }
    """
    try:
        data = request.get_json()
        
        # 验证必要字段
        required_fields = ["genbankData", "watermarkMetadata", "algorithm", 
                         "insertionPosition", "genbankInfo"]
        for field in required_fields:
            if field not in data:
                return jsonify(create_response(
                    success=False,
                    message=f"缺少必要字段：{field}"
                )), 400
        
        # 调用服务层处理
        result = insert_watermark_to_genbank(
            genbank_data=data,
            watermark_text=data["watermarkMetadata"],
            algorithm=data["algorithm"],
            position=data["insertionPosition"]
        )
        
        return jsonify(create_response(
            success=True,
            data=result,
            message="水印插入成功"
        ))
        
    except NotImplementedError as e:
        return jsonify(create_response(
            success=False,
            message=str(e)
        )), 400
        
    except ValueError as e:
        return jsonify(create_response(
            success=False,
            message=f"输入数据错误：{str(e)}"
        )), 400
        
    except Exception as e:
        return jsonify(create_response(
            success=False,
            message=f"服务器错误：{str(e)}"
        )), 500

@bp.route('/genbank/extract', methods=['POST'])
def extract_watermark():
    """从 Genbank 文件中提取水印
    
    请求体格式：
    {
        "watermarkSequence": str,     # 水印 DNA 序列
        "algorithm": str,             # 水印算法类型 ("plaintext" 或 "encrypted")
        "password": str               # 可选，加密模式下的密码
    }
    
    返回格式：
    {
        "success": bool,
        "data": {
            "watermarkText": str,     # 提取的水印文本
            "algorithm": str          # 使用的算法
        },
        "message": str
    }
    """
    try:
        data = request.get_json()
        
        # 验证必要字段
        if "watermarkSequence" not in data:
            return jsonify(create_response(
                success=False,
                message="缺少必要字段：watermarkSequence"
            )), 400
            
        if "algorithm" not in data:
            return jsonify(create_response(
                success=False,
                message="缺少必要字段：algorithm"
            )), 400
        
        # 调用服务层处理
        result = extract_watermark_from_genbank(
            watermark_sequence=data["watermarkSequence"],
            algorithm=data["algorithm"],
            password=data.get("password")  # 可选
        )
        
        return jsonify(create_response(
            success=True,
            data=result,
            message="水印提取成功"
        ))
        
    except ValueError as e:
        return jsonify(create_response(
            success=False,
            message=f"输入数据错误：{str(e)}"
        )), 400
        
    except Exception as e:
        return jsonify(create_response(
            success=False,
            message=f"服务器错误：{str(e)}"
        )), 500 