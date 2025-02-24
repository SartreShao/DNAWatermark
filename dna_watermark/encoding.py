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

def generate_encryption_key(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """
    使用密码生成加密密钥。
    
    Args:
        password: 用于生成密钥的密码
        salt: 可选的盐值，如果不提供则随机生成
        
    Returns:
        元组 (密钥, 盐值)
    """
    if salt is None:
        salt = random.randbytes(16)
        
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_text(text: str, password: str) -> tuple[str, bytes]:
    """
    加密文本。
    
    Args:
        text: 要加密的文本
        password: 加密密码
        
    Returns:
        元组 (加密后的文本, 盐值)
    """
    key, salt = generate_encryption_key(password)
    f = Fernet(key)
    encrypted_data = f.encrypt(text.encode())
    # 使用 urlsafe_b64encode 并移除填充字符 '='
    encoded = base64.urlsafe_b64encode(encrypted_data).decode().rstrip('=')
    # 将 '-' 和 '_' 替换为我们支持的字符
    encoded = encoded.replace('-', '.')
    encoded = encoded.replace('_', '/')
    return encoded, salt

def decrypt_text(encrypted_text: str, password: str, salt: bytes) -> str:
    """
    解密文本。
    
    Args:
        encrypted_text: 加密后的文本
        password: 解密密码
        salt: 加密时使用的盐值
        
    Returns:
        解密后的原始文本
    """
    # 还原 base64 字符
    padded_text = encrypted_text.replace('.', '-').replace('/', '_')
    # 添加回 base64 填充
    padding_length = (4 - len(padded_text) % 4) % 4
    padded_text += '=' * padding_length
    
    key, _ = generate_encryption_key(password, salt)
    f = Fernet(key)
    encrypted_data = base64.urlsafe_b64decode(padded_text.encode())
    return f.decrypt(encrypted_data).decode()

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

def encode_encrypted_text(text: str, password: str) -> tuple[str, bytes]:
    """
    将文本加密并编码为 DNA 序列。
    
    Args:
        text: 要编码的文本
        password: 加密密码
        
    Returns:
        元组 (编码后的 DNA 序列, 盐值)
    """
    # 加密文本
    encrypted_text, salt = encrypt_text(text, password)
    
    # 编码加密后的文本
    dna_sequence = encode_text(encrypted_text)
    
    # 添加随机噪音序列
    noise_length = random.randint(10, 30)
    prefix_noise = generate_noise_sequence(noise_length)
    suffix_noise = generate_noise_sequence(noise_length)
    
    return f"{prefix_noise}{dna_sequence}{suffix_noise}", salt

def decode_encrypted_dna(dna_sequence: str, password: str, salt: bytes) -> str:
    """
    解码并解密 DNA 序列。
    
    Args:
        dna_sequence: 编码后的 DNA 序列
        password: 解密密码
        salt: 加密时使用的盐值
        
    Returns:
        解密后的原始文本
    """
    # 移除噪音序列（假设真实序列长度是3的倍数）
    sequence_length = len(dna_sequence)
    for i in range(sequence_length):
        for j in range(i + 1, sequence_length + 1):
            sub_sequence = dna_sequence[i:j]
            if len(sub_sequence) % 3 == 0:
                try:
                    # 尝试解码
                    encrypted_text = decode_dna(sub_sequence)
                    # 尝试解密
                    return decrypt_text(encrypted_text, password, salt)
                except:
                    continue
    raise ValueError("无法解码序列")

def generate_secure_password(length: int = 16) -> str:
    """
    生成一个安全的随机密码。
    
    Args:
        length: 密码长度，默认16位
        
    Returns:
        生成的安全密码
    """
    # 定义可用的字符集（只使用编码表中支持的字符）
    available_chars = list(ENCODING_TABLE.keys())
    
    # 确保至少包含一个字母、一个数字和一个标点符号
    password = [
        random.choice(list(LETTERS.keys())),  # 一个字母
        random.choice(list(NUMBERS.keys())),  # 一个数字
        random.choice(list(PUNCTUATION.keys()))  # 一个标点符号
    ]
    
    # 填充剩余长度
    remaining_length = length - len(password)
    password.extend(random.choice(available_chars) for _ in range(remaining_length))
    
    # 打乱密码字符顺序
    random.shuffle(password)
    
    return ''.join(password) 