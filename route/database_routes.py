"""数据库操作相关的路由"""

from datetime import datetime
from typing import Optional

from flask import Blueprint, jsonify, request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models.database import get_db
from models.watermark import WatermarkedSequence

bp = Blueprint('database', __name__, url_prefix='/api/database')

class WatermarkRecord(BaseModel):
    """水印记录数据模型"""
    algorithm: str = Field(..., description="水印算法类型（plaintext 或 encrypted）")
    original_text: str = Field(..., description="水印原文")
    password: Optional[str] = Field(None, description="密码（仅加密模式需要）")
    watermark_sequence: str = Field(..., description="水印DNA序列")
    position: str = Field(..., description="插入位置（格式：start..end）")
    original_sequence: str = Field(..., description="原始DNA序列")
    watermarked_sequence: str = Field(..., description="插入水印后的DNA序列")
    original_genbank: str = Field(..., description="原始GenBank文件内容")
    watermarked_genbank: str = Field(..., description="插入水印后的GenBank文件内容")
    genbank_accession: Optional[str] = Field(None, description="GenBank登录号")
    genbank_organism: Optional[str] = Field(None, description="生物体名称")
    genbank_definition: Optional[str] = Field(None, description="序列定义")

def create_response(success: bool, data=None, message: str = "") -> dict:
    """创建统一的响应格式"""
    return {
        "success": success,
        "data": data,
        "message": message
    }

@bp.route('/watermark', methods=['POST'])
def insert_watermark():
    """插入水印记录
    
    请求体格式：
    {
        "algorithm": str,          # "plaintext" 或 "encrypted"
        "original_text": str,      # 水印原文
        "password": str,           # 密码（可选，仅加密模式需要）
        "watermark_sequence": str, # 水印DNA序列
        "position": str,           # 插入位置（格式：start..end）
        "original_sequence": str,  # 原始DNA序列
        "watermarked_sequence": str,  # 插入水印后的DNA序列
        "original_genbank": str,   # 原始GenBank文件内容
        "watermarked_genbank": str,  # 插入水印后的GenBank文件内容
        "genbank_accession": str,  # GenBank登录号（可选）
        "genbank_organism": str,   # 生物体名称（可选）
        "genbank_definition": str  # 序列定义（可选）
    }
    
    返回格式：
    {
        "success": bool,
        "data": {
            "id": int,            # 记录ID
            "object_id": str,     # UUID
            "created_at": str     # 创建时间
        },
        "message": str
    }
    """
    try:
        data = request.get_json()
        
        # 处理 Genbank 数据中的换行符
        if "original_genbank" in data:
            data["original_genbank"] = data["original_genbank"].replace("\r\n", "\n").replace("\r", "\n")
        if "watermarked_genbank" in data:
            data["watermarked_genbank"] = data["watermarked_genbank"].replace("\r\n", "\n").replace("\r", "\n")
            
        record = WatermarkRecord(**data)
        
        # 创建数据库记录
        db_record = WatermarkedSequence(
            algorithm=record.algorithm,
            original_text=record.original_text,
            password=record.password,
            watermark_sequence=record.watermark_sequence,
            position=record.position,
            original_sequence=record.original_sequence,
            watermarked_sequence=record.watermarked_sequence,
            original_genbank=record.original_genbank,
            watermarked_genbank=record.watermarked_genbank,
            genbank_accession=record.genbank_accession,
            genbank_organism=record.genbank_organism,
            genbank_definition=record.genbank_definition
        )
        
        # 获取数据库会话
        db = next(get_db())
        
        # 保存记录
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return jsonify(create_response(
            success=True,
            data={
                "id": db_record.id,
                "object_id": db_record.object_id,
                "created_at": db_record.created_at.isoformat()
            },
            message="水印记录保存成功"
        ))
        
    except Exception as e:
        return jsonify(create_response(
            success=False,
            message=f"保存失败：{str(e)}"
        )), 400 

@bp.route('/watermark', methods=['GET'])
def get_all_watermarks():
    """获取所有水印记录
    
    返回格式：
    {
        "success": bool,
        "data": [
            {
                "id": int,                    # 记录ID
                "object_id": str,             # UUID
                "created_at": str,            # 创建时间
                "updated_at": str,            # 更新时间
                "algorithm": str,             # 水印算法类型
                "original_text": str,         # 原始水印文本
                "password": str,              # 密码（仅加密模式）
                "watermark_sequence": str,    # 水印DNA序列
                "position": str,              # 插入位置
                "original_sequence": str,     # 原始DNA序列
                "watermarked_sequence": str,  # 插入水印后的DNA序列
                "original_genbank": str,      # 原始GenBank文件内容
                "watermarked_genbank": str,   # 插入水印后的GenBank文件内容
                "genbank_accession": str,     # GenBank登录号
                "genbank_organism": str,      # 生物体名称
                "genbank_definition": str     # 序列定义
            },
            ...
        ],
        "message": str
    }
    """
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 查询所有记录并按创建时间倒序排序
        records = db.query(WatermarkedSequence).order_by(WatermarkedSequence.created_at.desc()).all()
        
        # 转换为JSON格式
        result = []
        for record in records:
            # 处理换行符，确保统一格式
            def normalize_newlines(text):
                if text:
                    # 将所有换行符统一为 \n
                    return text.replace('\\n', '\n').replace('\r\n', '\n').replace('\r', '\n')
                return text
            
            result.append({
                "id": record.id,
                "object_id": record.object_id,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat(),
                "algorithm": record.algorithm,
                "original_text": record.original_text,
                "password": record.password,
                "watermark_sequence": record.watermark_sequence,
                "position": record.position,
                "original_sequence": normalize_newlines(record.original_sequence),
                "watermarked_sequence": normalize_newlines(record.watermarked_sequence),
                "original_genbank": normalize_newlines(record.original_genbank),
                "watermarked_genbank": normalize_newlines(record.watermarked_genbank),
                "genbank_accession": record.genbank_accession,
                "genbank_organism": record.genbank_organism,
                "genbank_definition": record.genbank_definition
            })
        
        return jsonify(create_response(
            success=True,
            data=result,
            message="查询成功"
        ))
        
    except Exception as e:
        return jsonify(create_response(
            success=False,
            message=f"查询失败：{str(e)}"
        )), 500 