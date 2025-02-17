"""水印相关的路由定义"""

from flask import Blueprint, request, jsonify
from pydantic import BaseModel

from service.watermark_service import WatermarkService

bp = Blueprint('watermark', __name__, url_prefix='/api/watermark')

class WatermarkRequest(BaseModel):
    sequence: str
    message: str

class WatermarkResponse(BaseModel):
    success: bool
    data: str
    message: str = ""

@bp.route('/embed', methods=['POST'])
def embed():
    """嵌入水印API"""
    try:
        data = request.get_json()
        req = WatermarkRequest(**data)
        
        # 调用服务层处理
        result = WatermarkService.embed_watermark(req.sequence, req.message)
        
        return jsonify(WatermarkResponse(
            success=True,
            data=result,
            message="水印嵌入成功"
        ).dict())
    except Exception as e:
        return jsonify(WatermarkResponse(
            success=False,
            data="",
            message=f"错误：{str(e)}"
        ).dict())

@bp.route('/extract', methods=['POST'])
def extract():
    """提取水印API"""
    try:
        data = request.get_json()
        sequence = data.get('sequence', '')
        
        # 调用服务层处理
        result = WatermarkService.extract_watermark(sequence)
        
        return jsonify(WatermarkResponse(
            success=True,
            data=result,
            message="水印提取成功"
        ).dict())
    except Exception as e:
        return jsonify(WatermarkResponse(
            success=False,
            data="",
            message=f"错误：{str(e)}"
        ).dict()) 