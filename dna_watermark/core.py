"""DNA水印的核心功能模块"""

def text_to_binary(text: str) -> str:
    """将文本转换为二进制字符串"""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary: str) -> str:
    """将二进制字符串转换为文本"""
    # 确保二进制字符串长度是8的倍数
    if not binary:
        return ""
    padding = (8 - len(binary) % 8) % 8
    binary = binary + '0' * padding
    try:
        return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    except ValueError:
        return ""

def embed_watermark(sequence: str, watermark: str) -> str:
    """将水印信息嵌入到DNA序列中
    
    Args:
        sequence: 原始DNA序列，只包含 ATCG
        watermark: 水印信息（如用户名）
        
    Returns:
        str: 嵌入水印后的DNA序列
    """
    # 将水印文本转换为二进制
    binary = text_to_binary(watermark)
    print(f"Debug - 二进制长度: {len(binary)}")  # 调试信息
    
    # 在序列中每个碱基后插入一个标记碱基（A表示0，T表示1）
    result = []
    binary_index = 0
    
    for base in sequence:
        result.append(base)
        if binary_index < len(binary):
            mark = 'A' if binary[binary_index] == '0' else 'T'
            result.append(mark)
            binary_index += 1
    
    # 如果还有剩余的二进制位，继续添加
    while binary_index < len(binary):
        result.append('G')  # 使用G作为填充碱基
        mark = 'A' if binary[binary_index] == '0' else 'T'
        result.append(mark)
        binary_index += 1
    
    return ''.join(result)

def extract_watermark(sequence: str) -> str:
    """从DNA序列中提取水印信息
    
    Args:
        sequence: 包含水印的DNA序列
        
    Returns:
        str: 提取出的水印信息
    """
    # 提取标记碱基（每个原始碱基后的一个碱基）
    binary = ''
    for i in range(1, len(sequence), 2):
        if i >= len(sequence):
            break
        mark = sequence[i]
        if mark not in 'AT':  # 如果不是标记碱基，说明这部分不包含水印信息
            continue
        binary += '0' if mark == 'A' else '1'
    
    print(f"Debug - 提取的二进制: {binary}")  # 调试信息
    return binary_to_text(binary) 