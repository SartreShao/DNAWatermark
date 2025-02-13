"""测试DNA水印的核心功能"""

from dna_watermark.core import embed_watermark, extract_watermark, text_to_binary


def test_embed_and_extract_watermark():
    """测试水印的嵌入和提取"""
    # 测试数据
    sequence = "ATCGATCGATCGATCG"  # 原始DNA序列
    message = "test_user"          # 水印信息
    
    # 调试信息：查看二进制转换
    binary = text_to_binary(message)
    print(f"原始DNA序列: {sequence}")
    print(f"\n原始消息: {message}")
    print(f"二进制形式: {binary}")
    
    # 嵌入水印
    embedded = embed_watermark(sequence, message)
    print(f"嵌入水印后的序列: {embedded}")
    assert isinstance(embedded, str)
    assert all(base in 'ATCG' for base in embedded)  # 确保结果是有效的DNA序列
    
    # 提取水印
    extracted = extract_watermark(embedded)
    print(f"提取的水印: {extracted}")
    assert extracted == message  # 确保能够正确提取水印信息 