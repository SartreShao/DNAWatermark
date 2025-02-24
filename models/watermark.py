"""数据库模型定义"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .database import Base

class WatermarkedSequence(Base):
    """带水印的基因序列记录"""
    
    __tablename__ = "watermarked_sequences"
    
    # 基本信息
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    object_id: Mapped[str] = mapped_column(
        String(36),
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # 水印信息
    algorithm: Mapped[str] = mapped_column(String(20))  # "plaintext" 或 "encrypted"
    original_text: Mapped[str] = mapped_column(String(100))
    password: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # 序列信息
    watermark_sequence: Mapped[str] = mapped_column(String(1000))  # DNA水印序列
    position: Mapped[str] = mapped_column(String(50))  # 格式：start..end
    original_sequence: Mapped[str] = mapped_column(Text)  # 原始DNA序列
    watermarked_sequence: Mapped[str] = mapped_column(Text)  # 插入水印后的DNA序列
    
    # GenBank信息（可选）
    genbank_accession: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    genbank_organism: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    genbank_definition: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # GenBank原始数据
    original_genbank: Mapped[str] = mapped_column(Text)  # 原始GenBank文件内容
    watermarked_genbank: Mapped[str] = mapped_column(Text)  # 插入水印后的GenBank文件内容
    
    def __repr__(self) -> str:
        return (
            f"<WatermarkedSequence(object_id={self.object_id}, "
            f"algorithm={self.algorithm}, "
            f"original_text={self.original_text}, "
            f"position={self.position})>"
        ) 