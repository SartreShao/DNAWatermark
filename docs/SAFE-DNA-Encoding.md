# SAFE-DNA 编码系统

## 简介

SAFE-DNA 编码系统是一个专门设计的 DNA 序列编码方案，用于在 DNA 序列中安全地嵌入水印信息。该系统采用三碱基编码方式，并遵循严格的生物安全原则，避免产生可能影响 DNA 功能的序列。

## 设计原则

系统设计遵循以下关键原则：

1. **避免起始密码子**
   - 不使用 ATG、GTG、TTG 作为编码
   - 防止意外启动翻译过程

2. **利用终止密码子**
   - TAA 用于编码字母 'V'
   - TAG 用于编码字母 'W'
   - TGA 用于编码句号 '.'
   - 在序列中自然分布终止信号

3. **防止 ORF 形成**
   - 编码设计避免形成连续有意义的密码子组合
   - 大量使用以 T 和 C 开头的密码子，降低形成起始位点的可能性

## 编码表

### 字母编码（A-Z）
```
A = ACC    B = AGT    C = CAT    D = CCA    E = CGT    F = CGA
G = CGC    H = CGG    I = CTA    J = CTC    K = CTG    L = GAC
M = GCA    N = GCC    O = GCG    P = GCT    Q = GGA    R = GGC
S = GGG    T = GTC    U = GTT    V = TAA    W = TAG    X = TCA
Y = TCC    Z = TCG
```

### 数字编码（0-9）
```
0 = ACA    1 = ACG    2 = ACT    3 = AGA    4 = AGC    5 = AGG
6 = CAA    7 = CAC    8 = CAG    9 = CCT
```

### 标点符号编码
```
. = TGA    , = TCT    ? = TGC    ! = TGG    - = AAC    _ = AAG
( = AAT    ) = ATA    [ = ATC    ] = ATT    @ = CCC    / = GAG
空格 = AAA
```

## 编码特点

1. **三碱基编码**
   - 每个字符使用固定长度的三个碱基编码
   - 便于解码和错误检测

2. **唯一映射**
   - 每个字符都有唯一的三碱基编码
   - 每个三碱基编码只对应一个字符
   - 确保编码和解码的一致性

3. **安全性考虑**
   - 避免生物学活性序列
   - 降低与自然 DNA 序列的相似性
   - 防止意外的基因表达

## 使用示例

### 编码示例
```python
# 编码单个字符
'H' -> 'CGG'
'E' -> 'CGT'
'L' -> 'GAC'
'O' -> 'GCG'

# 编码文本
"HELLO" -> "CGGCGTGACGACGCG"
"HELLO WORLD!" -> "CGGCGTGACGACGCGAAATAGGCGGACTGGTGG"
```

### 解码示例
```python
'CGG' -> 'H'
'CGT' -> 'E'
'GAC' -> 'L'
'GCG' -> 'O'

"CGGCGTGACGACGCG" -> "HELLO"
```

## 错误处理

系统会在以下情况下报错：

1. 编码时：
   - 输入包含不支持的字符
   - 输入为空

2. 解码时：
   - DNA 序列长度不是 3 的倍数
   - 序列包含非 ATCG 碱基
   - 序列包含未定义的三联体
   - 序列为空

## API 使用

### 编码 API
```bash
curl -X POST http://localhost:5000/api/encoding/encode \
     -H "Content-Type: application/json" \
     -d '{"text": "HELLO"}'
```

响应：
```json
{
    "dna_sequence": "CGGCGTGACGACGCG",
    "length": 15,
    "details": [
        {"char": "H", "triplet": "CGG"},
        {"char": "E", "triplet": "CGT"},
        {"char": "L", "triplet": "GAC"},
        {"char": "L", "triplet": "GAC"},
        {"char": "O", "triplet": "GCG"}
    ]
}
```

### 解码 API
```bash
curl -X POST http://localhost:5000/api/encoding/decode \
     -H "Content-Type: application/json" \
     -d '{"sequence": "CGGCGTGACGACGCG"}'
```

响应：
```json
{
    "text": "HELLO",
    "length": 5,
    "details": [
        {"triplet": "CGG", "char": "H"},
        {"triplet": "CGT", "char": "E"},
        {"triplet": "GAC", "char": "L"},
        {"triplet": "GAC", "char": "L"},
        {"triplet": "GCG", "char": "O"}
    ]
}
``` 