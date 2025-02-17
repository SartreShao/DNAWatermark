"""
SAFE-DNA Encoding System

这个模块实现了一个安全的 DNA 编码系统，用于在 DNA 序列中嵌入水印信息。
编码系统的设计遵循以下原则：
1. 避免起始密码子（ATG、GTG、TTG）以防止意外启动翻译
2. 利用终止密码子（TAA、TAG、TGA）作为特定字符的编码
3. 防止 ORF 形成，避免可能形成连续有意义密码子的组合
"""

# 字母编码表（A-Z）
LETTERS = {
    'A': 'ACC', 'B': 'AGT', 'C': 'CAT', 'D': 'CCA', 'E': 'CGT', 'F': 'CGA',
    'G': 'CGC', 'H': 'CGG', 'I': 'CTA', 'J': 'CTC', 'K': 'CTG', 'L': 'GAC',
    'M': 'GCA', 'N': 'GCC', 'O': 'GCG', 'P': 'GCT', 'Q': 'GGA', 'R': 'GGC',
    'S': 'GGG', 'T': 'GTC', 'U': 'GTT', 'V': 'TAA', 'W': 'TAG', 'X': 'TCA',
    'Y': 'TCC', 'Z': 'TCG'
}

# 数字编码表（0-9）
NUMBERS = {
    '0': 'ACA', '1': 'ACG', '2': 'ACT', '3': 'AGA', '4': 'AGC', '5': 'AGG',
    '6': 'CAA', '7': 'CAC', '8': 'CAG', '9': 'CCT'
}

# 标点符号编码表
PUNCTUATION = {
    '.': 'TGA', ',': 'TCT', '?': 'TGC', '!': 'TGG', '-': 'AAC', '_': 'AAG',
    '(': 'AAT', ')': 'ATA', '[': 'ATC', ']': 'ATT', '@': 'CCC', '/': 'GAG',
    ' ': 'AAA'  # 空格字符使用 AAA 编码
}

# 合并所有编码表
ENCODING_TABLE = {**LETTERS, **NUMBERS, **PUNCTUATION}

# 创建解码表（反向映射）
DECODING_TABLE = {dna: char for char, dna in ENCODING_TABLE.items()}

def encode_char(char: str) -> str:
    """
    将单个字符编码为对应的 DNA 序列。
    
    Args:
        char: 要编码的字符
        
    Returns:
        对应的 DNA 三联体序列
        
    Raises:
        KeyError: 如果字符不在编码表中
    """
    return ENCODING_TABLE[char.upper()]

def decode_triplet(triplet: str) -> str:
    """
    将 DNA 三联体解码为对应的字符。
    
    Args:
        triplet: 要解码的 DNA 三联体序列
        
    Returns:
        对应的字符
        
    Raises:
        KeyError: 如果三联体不在解码表中
    """
    return DECODING_TABLE[triplet.upper()]

def encode_text(text: str) -> str:
    """
    将文本字符串编码为 DNA 序列。
    
    Args:
        text: 要编码的文本
        
    Returns:
        编码后的 DNA 序列
        
    Raises:
        KeyError: 如果文本包含不支持的字符
    """
    return ''.join(encode_char(c) for c in text)

def decode_dna(dna: str) -> str:
    """
    将 DNA 序列解码为文本字符串。
    
    Args:
        dna: 要解码的 DNA 序列
        
    Returns:
        解码后的文本
        
    Raises:
        ValueError: 如果 DNA 序列长度不是 3 的倍数
        KeyError: 如果 DNA 序列包含无效的三联体
    """
    if len(dna) % 3 != 0:
        raise ValueError("DNA sequence length must be a multiple of 3")
    return ''.join(decode_triplet(dna[i:i+3]) for i in range(0, len(dna), 3))

def is_valid_triplet(triplet: str) -> bool:
    """
    检查给定的三联体是否是有效的编码。
    
    Args:
        triplet: 要检查的 DNA 三联体序列
        
    Returns:
        如果三联体在编码表中则返回 True，否则返回 False
    """
    return triplet.upper() in DECODING_TABLE

def get_all_valid_triplets() -> set:
    """
    获取所有有效的三联体编码。
    
    Returns:
        包含所有有效三联体的集合
    """
    return set(DECODING_TABLE.keys()) 