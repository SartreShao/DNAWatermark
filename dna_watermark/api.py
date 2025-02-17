"""DNA水印系统的API接口"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel

from .core import embed_watermark, extract_watermark

app = Flask(__name__)
CORS(app)

class WatermarkRequest(BaseModel):
    sequence: str
    message: str

class WatermarkResponse(BaseModel):
    success: bool
    data: str
    message: str = ""

@app.route('/api/watermark/embed', methods=['POST'])
def embed():
    """嵌入水印API"""
    try:
        data = request.get_json()
        req = WatermarkRequest(**data)
        
        # 嵌入水印
        result = embed_watermark(req.sequence, req.message)
        
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

@app.route('/api/watermark/extract', methods=['POST'])
def extract():
    """提取水印API"""
    try:
        data = request.get_json()
        sequence = data.get('sequence', '')
        
        # 提取水印
        result = extract_watermark(sequence)
        
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "version": "0.1.0"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 