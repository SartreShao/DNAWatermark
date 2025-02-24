"""
SAFE-DNA Encoding System

这个模块实现了一个安全的 DNA 编码系统，用于在 DNA 序列中嵌入水印信息。
编码系统的设计遵循以下原则：
1. 避免起始密码子（ATG、GTG、TTG）以防止意外启动翻译
2. 利用终止密码子（TAA、TAG、TGA）作为特定字符的编码
3. 防止 ORF 形成，避免可能形成连续有意义密码子的组合
"""

import random
import string
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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

def encrypt_text(text: str, password: str) -> str:
    """
    使用简单的替换加密文本。
    
    Args:
        text: 要加密的文本
        password: 加密密码
        
    Returns:
        加密后的文本
    """
    # 获取所有可用字符
    available_chars = list(ENCODING_TABLE.keys())
    char_count = len(available_chars)
    
    # 使用密码生成偏移量
    password_len = len(password)
    
    # 加密过程：对每个字符在可用字符集中进行偏移
    encrypted_chars = []
    for i, c in enumerate(text):
        if c.upper() not in available_chars:
            raise ValueError(f"不支持的字符：{c}")
        
        # 在可用字符集中找到当前字符的位置
        current_index = available_chars.index(c.upper())
        
        # 使用密码中对应位置的字符的ASCII值作为偏移量
        password_char = password[i % password_len]
        offset = sum(ord(c) for c in password[:i % password_len + 1]) % char_count
        
        # 计算偏移后的位置
        new_index = (current_index + offset) % char_count
        
        # 获取加密后的字符
        encrypted_char = available_chars[new_index]
        encrypted_chars.append(encrypted_char)
    
    return ''.join(encrypted_chars)

def decrypt_text(encrypted_text: str, password: str) -> str:
    """
    解密文本。
    
    Args:
        encrypted_text: 加密后的文本
        password: 解密密码
        
    Returns:
        解密后的原始文本
    """
    # 获取所有可用字符
    available_chars = list(ENCODING_TABLE.keys())
    char_count = len(available_chars)
    
    # 使用密码生成偏移量
    password_len = len(password)
    
    # 解密过程：对每个字符在可用字符集中进行反向偏移
    decrypted_chars = []
    for i, c in enumerate(encrypted_text):
        if c not in available_chars:
            raise ValueError(f"不支持的字符：{c}")
            
        # 在可用字符集中找到当前字符的位置
        current_index = available_chars.index(c)
        
        # 使用密码中对应位置的字符的ASCII值作为偏移量
        password_char = password[i % password_len]
        offset = sum(ord(c) for c in password[:i % password_len + 1]) % char_count
        
        # 计算反向偏移后的位置
        new_index = (current_index - offset) % char_count
        
        # 获取解密后的字符
        decrypted_char = available_chars[new_index]
        decrypted_chars.append(decrypted_char)
    
    return ''.join(decrypted_chars)

def generate_noise_sequence(length: int) -> str:
    """
    生成指定长度的随机 DNA 序列。
    
    Args:
        length: 序列长度
        
    Returns:
        随机 DNA 序列
    """
    bases = ['A', 'T', 'C', 'G']
    return ''.join(random.choice(bases) for _ in range(length))

def encode_encrypted_text(text: str, password: str) -> str:
    """
    将文本加密并编码为 DNA 序列。
    
    Args:
        text: 要编码的文本
        password: 加密密码
        
    Returns:
        编码后的 DNA 序列
    """
    # 加密文本
    encrypted_text = encrypt_text(text, password)
    
    # 编码加密后的文本
    dna_sequence = encode_text(encrypted_text)
    
    # 不再添加随机噪声序列，直接返回编码后的序列
    return dna_sequence

def decode_encrypted_dna(dna_sequence: str, password: str) -> str:
    """
    解码并解密 DNA 序列。
    
    Args:
        dna_sequence: 编码后的 DNA 序列
        password: 解密密码
        
    Returns:
        解密后的原始文本
        
    Raises:
        ValueError: 如果解码或解密失败
    """
    try:
        # 去除空白并转换为大写
        sequence = dna_sequence.strip().upper()
        
        print(f"解码序列：{sequence}，长度：{len(sequence)}")  # 调试信息
        
        # 确保序列长度是3的倍数
        if len(sequence) % 3 != 0:
            raise ValueError(f"DNA序列长度必须是3的倍数，当前长度：{len(sequence)}")
            
        # 直接尝试解码整个序列
        encrypted_text = decode_dna(sequence)
        print(f"解码后的加密文本：{encrypted_text}")  # 调试信息
        
        # 解密文本
        decrypted_text = decrypt_text(encrypted_text, password)
        print(f"解密后的文本：{decrypted_text}")  # 调试信息
        
        return decrypted_text
        
    except Exception as e:
        raise ValueError(f"解密失败：{str(e)}")

def generate_secure_password(length: int = 8) -> str:
    """
    生成一个安全的随机密码。
    
    Args:
        length: 密码长度，默认8位
        
    Returns:
        生成的安全密码
    """
    # 只使用字母和数字，避免特殊字符
    password_chars = list(LETTERS.keys()) + list(NUMBERS.keys())
    
    # 确保至少包含一个字母和一个数字
    password = [
        random.choice(list(LETTERS.keys())),   # 一个字母
        random.choice(list(NUMBERS.keys()))    # 一个数字
    ]
    
    # 填充剩余长度
    remaining_length = length - len(password)
    password.extend(random.choice(password_chars) for _ in range(remaining_length))
    
    # 打乱密码字符顺序
    random.shuffle(password)
    
    return ''.join(password) 