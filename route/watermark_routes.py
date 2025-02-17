"""水印相关的路由定义"""

from flask import Blueprint, request, jsonify
from service.watermark_service import embed_watermark_with_service, extract_watermark_with_service

bp = Blueprint('watermark', __name__, url_prefix='/api/watermark')

def create_response(success, data="", message=""):
    """创建统一的响应格式
    
    Args:
        success: 操作是否成功
        data: 返回的数据
        message: 提示信息
        
    Returns:
        dict: 包含以下字段的字典：
            - success (bool): 操作是否成功
            - data (str): 返回的数据
            - message (str): 提示信息
    """
    return {
        "success": success,
        "data": data,
        "message": message
    }

@bp.route('/embed', methods=['POST'])
def embed():
    """嵌入水印API
    
    期望的请求体格式：
    {
        "sequence": str,  # DNA序列，只包含ATCG
        "message": str    # 要嵌入的水印信息
    }
    
    返回格式：
    {
        "success": bool,  # 操作是否成功
        "data": str,      # 嵌入水印后的序列
        "message": str    # 提示信息
    }
    """
    try:
        data = request.get_json()
        
        # 调用服务层处理
        result = embed_watermark_with_service(data['sequence'], data['message'])
        
        return jsonify(create_response(
            success=True,
            data=result,
            message="水印嵌入成功"
        ))
    except Exception as e:
        return jsonify(create_response(
            success=False,
            message=f"错误：{str(e)}"
        ))

@bp.route('/extract', methods=['POST'])
def extract():
    """提取水印API
    
    期望的请求体格式：
    {
        "sequence": str  # 包含水印的DNA序列
    }
    
    返回格式：
    {
        "success": bool,  # 操作是否成功
        "data": str,      # 提取出的水印信息
        "message": str    # 提示信息
    }
    """
    try:
        data = request.get_json()
        sequence = data.get('sequence', '')
        
        # 调用服务层处理
        result = extract_watermark_with_service(sequence)
        
        return jsonify(create_response(
            success=True,
            data=result,
            message="水印提取成功"
        ))
    except Exception as e:
        return jsonify(create_response(
            success=False,
            message=f"错误：{str(e)}"
        )) 