"""
编码路由模块

提供将文本转换为 DNA 序列的 API 端点。
使用 SAFE-DNA 编码系统进行编码。
"""

from typing import Dict, List, Tuple
from flask import Blueprint, jsonify, request, Response

from dna_watermark.encoding import encode_text, encode_char

bp = Blueprint('encoding', __name__, url_prefix='/api/encoding')

@bp.route('/encode', methods=['POST'])
def encode_string() -> Tuple[Response, int]:
    """
    将输入的文本字符串编码为 DNA 序列。
    
    请求体格式:
    {
        "text": "要编码的文本"
    }
    
    返回:
        成功时返回:
        {
            "dna_sequence": "编码后的DNA序列",
            "length": 序列长度,
            "details": [
                {
                    "char": "原字符",
                    "triplet": "对应的碱基三联体"
                },
                ...
            ]
        }
        
        失败时返回:
        {
            "error": "错误信息"
        }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'error': '请求体必须包含 text 字段'
            }), 400
            
        text = data['text']
        
        # 获取完整的 DNA 序列
        dna_sequence = encode_text(text)
        
        # 生成详细的编码信息
        details = []
        for char in text:
            triplet = encode_char(char)
            details.append({
                'char': char,
                'triplet': triplet
            })
        
        return jsonify({
            'dna_sequence': dna_sequence,
            'length': len(dna_sequence),
            'details': details
        }), 200
        
    except KeyError as e:
        return jsonify({
            'error': f'不支持的字符: {str(e)}'
        }), 400 