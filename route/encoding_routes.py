"""
编码路由模块

提供将文本转换为 DNA 序列的 API 端点。
使用 SAFE-DNA 编码系统进行编码。
"""

from typing import Dict, List, Tuple
from flask import Blueprint, jsonify, request, Response

from dna_watermark.encoding import encode_text, encode_char, decode_dna, decode_triplet, is_valid_triplet

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

@bp.route('/decode', methods=['POST'])
def decode_sequence() -> Tuple[Response, int]:
    """
    将 DNA 序列解码为原始文本。
    
    请求体格式:
    {
        "sequence": "要解码的DNA序列"
    }
    
    返回:
        成功时返回:
        {
            "text": "解码后的文本",
            "length": 文本长度,
            "details": [
                {
                    "triplet": "碱基三联体",
                    "char": "对应的字符"
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
        if not data or 'sequence' not in data:
            return jsonify({
                'error': '请求体必须包含 sequence 字段'
            }), 400
            
        sequence = data['sequence'].upper().replace(' ', '')  # 移除可能的空格
        
        # 检查序列长度
        if len(sequence) % 3 != 0:
            return jsonify({
                'error': 'DNA序列长度必须是3的倍数'
            }), 400
            
        # 检查序列是否只包含 ATCG
        if not all(base in 'ATCG' for base in sequence):
            return jsonify({
                'error': 'DNA序列只能包含 A、T、C、G 碱基'
            }), 400
        
        # 解码序列
        text = decode_dna(sequence)
        
        # 生成详细的解码信息
        details = []
        triplets = [sequence[i:i+3] for i in range(0, len(sequence), 3)]
        
        # 先检查所有三联体是否有效
        for triplet in triplets:
            if not is_valid_triplet(triplet):
                return jsonify({
                    'error': f'不支持的三联体序列: {triplet}'
                }), 400
        
        # 生成解码详情
        for triplet in triplets:
            char = decode_triplet(triplet)
            details.append({
                'triplet': triplet,
                'char': char
            })
        
        return jsonify({
            'text': text,
            'length': len(text),
            'details': details
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
    except KeyError as e:
        return jsonify({
            'error': f'不支持的三联体序列: {str(e)}'
        }), 400 