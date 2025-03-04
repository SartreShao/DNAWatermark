"""
DNA Watermark Insertion Module

这个模块负责将编码后的水印信息插入到 Genbank 格式的基因片段中。
采用纯函数式编程方式实现，确保函数的输入输出可预测性。
"""

from typing import Dict, Any, Tuple
from io import StringIO
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
from . import encoding

def get_insertion_position(position_strategy: str, cds_region: Dict[str, int]) -> int:
    """
    根据策略确定水印插入位置。

    Args:
        position_strategy: 插入位置策略 ("before-cds" 或 "after-cds")
        cds_region: CDS 区域信息，包含 start 和 end

    Returns:
        插入位置的索引

    Raises:
        ValueError: 当使用不支持的插入策略时
    """
    if position_strategy == "before-cds":
        return cds_region["start"]
    elif position_strategy == "after-cds":
        return cds_region["end"]
    else:
        raise ValueError(f"不支持的插入位置策略：{position_strategy}")

def insert_watermark(
    genbank_data: Dict[str, Any],
    watermark_text: str,
    algorithm: str = "plaintext",
    position: str = "before-cds",
    password: str | None = None
) -> Dict[str, Any]:
    """
    将水印信息插入到基因序列中。

    Args:
        genbank_data: 包含 Genbank 数据的字典
        watermark_text: 要插入的水印文本
        algorithm: 水印算法类型 ("plaintext" 或 "encrypted")
        position: 插入位置 ("before-cds" 或 "after-cds")
        password: 加密密码（仅在 algorithm 为 "encrypted" 时需要）

    Returns:
        包含处理结果的字典
    
    Raises:
        NotImplementedError: 当使用不支持的算法时
        ValueError: 当输入数据格式不正确或使用不支持的插入位置时
    """
    try:
        print(f"开始处理水印插入，算法：{algorithm}，位置：{position}")  # 调试信息
        
        if algorithm not in ["plaintext", "encrypted"]:
            raise ValueError(f"不支持的算法类型：{algorithm}")
        
        if position not in ["before-cds", "after-cds"]:
            raise ValueError(f"不支持的插入位置：{position}")

        # 提取必要的数据
        nucleotide_sequence = genbank_data["genbankInfo"]["nucleotideSequence"]
        cds_region = genbank_data["genbankInfo"]["cdsRegion"]
        
        print(f"提取的数据 - 序列长度：{len(nucleotide_sequence)}，CDS区域：{cds_region}")  # 调试信息
        
        # 生成水印序列
        if algorithm == "plaintext":
            print("使用明文算法生成水印")  # 调试信息
            watermark_dna = encoding.encode_text(watermark_text)
        else:  # encrypted
            print(f"使用加密算法生成水印，密码：{'已提供' if password else '未提供'}")  # 调试信息
            if not isinstance(password, str):
                raise ValueError("加密模式需要提供有效的密码字符串")
            watermark_dna = encoding.encode_encrypted_text(watermark_text, password)
        
        print(f"生成的水印序列长度：{len(watermark_dna)}")  # 调试信息
        
        insert_position = get_insertion_position(position, cds_region)
        print(f"插入位置：{insert_position}")  # 调试信息
        
        # 创建水印后的序列
        watermarked_sequence = create_watermarked_sequence(
            nucleotide_sequence,
            watermark_dna,
            insert_position
        )
        
        # 生成水印信息
        watermark_info = create_watermark_info(
            watermark_text,
            watermark_dna,
            insert_position,
            algorithm
        )
        
        # 使用 BioPython 更新 Genbank 文件
        updated_genbank = update_genbank_content(
            genbank_data["genbankData"],
            watermark_dna,
            insert_position,
            algorithm
        )
        
        print("水印插入处理完成")  # 调试信息
        
        return {
            "status": "success",
            "data": {
                "watermarkedSequence": watermarked_sequence,
                "watermarkInfo": watermark_info,
                "genbankFile": updated_genbank
            }
        }
        
    except Exception as e:
        print(f"水印插入过程中发生错误：{str(e)}")  # 调试信息
        raise

def create_watermarked_sequence(
    original_sequence: str,
    watermark_dna: str,
    insert_position: int
) -> str:
    """
    在原始序列中插入水印序列。

    Args:
        original_sequence: 原始 DNA 序列
        watermark_dna: 水印 DNA 序列
        insert_position: 插入位置

    Returns:
        插入水印后的新序列
    """
    return (
        original_sequence[:insert_position] +
        watermark_dna +
        original_sequence[insert_position:]
    )

def create_watermark_info(
    original_text: str,
    watermark_dna: str,
    insert_position: int,
    algorithm: str
) -> Dict[str, Any]:
    """
    创建水印信息字典。

    Args:
        original_text: 原始水印文本
        watermark_dna: 编码后的水印 DNA 序列
        insert_position: 插入位置
        algorithm: 水印算法类型

    Returns:
        包含水印信息的字典
    """
    info = {
        "position": {
            "start": insert_position,
            "end": insert_position + len(watermark_dna)
        },
        "sequence": watermark_dna,
        "originalText": original_text,
        "algorithm": algorithm
    }
    
    return info

def update_genbank_content(
    genbank_content: str,
    watermark_dna: str,
    insert_position: int,
    algorithm: str
) -> str:
    """
    使用 BioPython 更新 Genbank 文件内容。

    Args:
        genbank_content: 原始 Genbank 文件内容
        watermark_dna: 水印 DNA 序列
        insert_position: 插入位置
        algorithm: 水印算法类型

    Returns:
        更新后的 Genbank 文件内容
    """
    # 解析 Genbank 文件
    record = SeqIO.read(StringIO(genbank_content), "genbank")
    
    # 创建新的序列
    new_seq = (
        str(record.seq[:insert_position]) +
        watermark_dna.lower() +
        str(record.seq[insert_position:])
    )
    record.seq = Seq(new_seq)
    
    # 更新序列长度
    new_length = len(new_seq)
    record.annotations["sequence_length"] = new_length
    
    # 更新定义行
    if "definition" in record.annotations:
        definition = record.annotations["definition"]
        if "complete cds" in definition.lower():
            new_definition = definition.replace(
                "complete cds",
                "with watermark, complete cds"
            )
            # 创建新的 SeqRecord 对象来更新定义
            new_record = SeqRecord(
                record.seq,
                id=record.id,
                name=record.name,
                description=new_definition,
                annotations=record.annotations
            )
            record = new_record
    
    # 更新参考文献中的序列长度
    if "references" in record.annotations:
        references = record.annotations["references"]
        if isinstance(references, list):
            for ref in references:
                # 更新位置信息
                if hasattr(ref, "location"):
                    ref.location = (0, new_length)
                
                # 更新标题中的序列范围
                if hasattr(ref, "title"):
                    import re
                    # 使用正则表达式查找和替换序列范围
                    ref.title = re.sub(
                        r"bases \d+ to \d+",
                        f"bases 1 to {new_length}",
                        ref.title
                    )
    
    # 更新注释
    if "comment" in record.annotations:
        comment = str(record.annotations["comment"])
        watermark_comment = (
            f"\nDNA watermark information:"
            f"\n  Position: {insert_position + 1}..{insert_position + len(watermark_dna)}"
            f"\n  Length: {len(watermark_dna)} bp"
            f"\n  Sequence: {watermark_dna.lower()}"
        )
        record.annotations["comment"] = comment + watermark_comment
    
    # 更新所有特征的位置
    watermark_length = len(watermark_dna)
    new_features = []
    
    # 添加水印特征（放在最前面）
    watermark_feature = SeqFeature(
        FeatureLocation(insert_position, insert_position + watermark_length),
        type="watermark",
        qualifiers={
            "note": [
                "DNA watermark sequence",
                f"Position: {insert_position + 1}..{insert_position + watermark_length}",
                f"Length: {watermark_length} bp",
                f"Sequence: {watermark_dna.lower()}"
            ],
            "watermark_type": [algorithm]
        }
    )
    new_features.append(watermark_feature)
    
    # 更新其他特征
    from Bio.SeqFeature import ExactPosition, SimpleLocation
    for feature in record.features:
        if feature.location:
            # 获取位置信息
            try:
                # 使用字符串转换来获取位置值
                start_pos = int(str(feature.location.start))
                end_pos = int(str(feature.location.end))
            except (AttributeError, ValueError):
                # 如果转换失败，跳过这个特征
                continue
            
            # 特殊处理 CDS 特征
            if feature.type == "CDS" and end_pos == insert_position:
                # 如果是 CDS 特征且水印插入在其末尾，保持 CDS 长度不变
                new_location = SimpleLocation(
                    ExactPosition(start_pos),
                    ExactPosition(end_pos),
                    feature.location.strand
                )
            else:
                # 其他特征正常更新位置
                if start_pos >= insert_position:
                    start = start_pos + watermark_length
                    end = end_pos + watermark_length
                else:
                    start = start_pos
                    end = end_pos + watermark_length if end_pos >= insert_position else end_pos
                
                new_location = SimpleLocation(
                    ExactPosition(start),
                    ExactPosition(end),
                    feature.location.strand
                )
            
            feature.location = new_location
            
            # 确保蛋白质序列的格式正确
            if "translation" in feature.qualifiers:
                translation = feature.qualifiers["translation"][0]
                # 移除所有空白字符
                translation = "".join(translation.split())
                feature.qualifiers["translation"] = [translation]
                
            new_features.append(feature)
    
    # 更新特征列表
    record.features = new_features
    
    # 将记录转换回字符串，使用 BioPython 的格式化选项
    output = StringIO()
    SeqIO.write(record, output, "genbank")
    
    # 移除末尾多余的空白字符，确保文件以 // 结束
    result = output.getvalue().rstrip()
    
    return result

def extract_watermark(
    genbank_data: str,
    password: str | None = None,
    salt: bytes | None = None
) -> Dict[str, Any]:
    """
    从 GenBank 文件中提取水印。

    Args:
        genbank_data: GenBank 文件内容
        password: 解密密码（仅在加密模式下需要）
        salt: 盐值（仅在加密模式下需要）

    Returns:
        包含水印信息的字典

    Raises:
        ValueError: 当无法找到水印或解密失败时
    """
    try:
        print("开始提取水印...")  # 调试信息
        
        # 预处理 GenBank 文件内容
        print("正在预处理 GenBank 文件...")  # 调试信息
        # 修复缩进问题
        lines = genbank_data.split('\n')
        processed_lines = []
        for line in lines:
            # 修复特征限定符的缩进
            if line.strip().startswith('/'):
                line = ' ' * 21 + line.lstrip()
            processed_lines.append(line)
        processed_genbank = '\n'.join(processed_lines)
        
        # 解析 GenBank 文件
        print("正在解析 GenBank 文件...")  # 调试信息
        try:
            record = SeqIO.read(StringIO(processed_genbank), "genbank")
            print(f"成功解析 GenBank 文件，序列长度：{len(record.seq)}")  # 调试信息
        except Exception as e:
            print(f"GenBank 文件解析失败：{str(e)}")  # 调试信息
            raise ValueError(f"GenBank 文件解析失败：{str(e)}")
        
        # 查找水印特征
        print("正在查找水印特征...")  # 调试信息
        watermark_feature = None
        for feature in record.features:
            print(f"检查特征：{feature.type}")  # 调试信息
            if feature.type.lower().replace(' ', '') == "watermark":
                watermark_feature = feature
                break
        
        if not watermark_feature:
            # 尝试通过注释查找水印信息
            print("通过常规特征未找到水印，尝试从注释中查找...")  # 调试信息
            if "comment" in record.annotations:
                comment = record.annotations["comment"]
                if "DNA watermark information" in comment:
                    # 从注释中提取水印信息
                    import re
                    position_match = re.search(r"Position: (\d+)\.\.(\d+)", comment)
                    sequence_match = re.search(r"Sequence:\s*([actgACTG\s]+)", comment)
                    
                    if position_match and sequence_match:
                        start = int(position_match.group(1)) - 1  # 转换为0基索引
                        end = int(position_match.group(2))
                        sequence = sequence_match.group(1).replace(' ', '').lower()
                        
                        # 创建水印特征
                        watermark_feature = SeqFeature(
                            FeatureLocation(start, end),
                            type="watermark",
                            qualifiers={
                                "watermark_type": ["plaintext"]
                            }
                        )
                        print(f"从注释中找到水印信息：位置 {start+1}..{end}")  # 调试信息
        
        if not watermark_feature:
            print("未找到水印特征")  # 调试信息
            raise ValueError("未找到水印特征")
        
        print(f"找到水印特征，位置：{watermark_feature.location}")  # 调试信息
        
        # 获取水印信息
        algorithm = watermark_feature.qualifiers.get("watermark_type", ["plaintext"])[0]
        print(f"水印算法类型：{algorithm}")  # 调试信息
        
        # 获取序列
        if watermark_feature.location:
            # 使用 str() 转换位置对象，然后再转为整数
            start = int(str(watermark_feature.location.start))
            end = int(str(watermark_feature.location.end))
        else:
            # 如果位置信息不可用，尝试从注释中获取
            print("特征位置不可用，尝试从注释中获取...")  # 调试信息
            for note in watermark_feature.qualifiers.get("note", []):
                position_match = re.search(r"Position: (\d+)\.\.(\d+)", note)
                if position_match:
                    start = int(position_match.group(1)) - 1
                    end = int(position_match.group(2))
                    break
            else:
                raise ValueError("无法确定水印位置")
        
        sequence = str(record.seq[start:end])
        print(f"水印序列：{sequence}")  # 调试信息
        
        # 提取水印文本
        try:
            if algorithm == "plaintext":
                print("使用明文模式解码...")  # 调试信息
                watermark_text = encoding.decode_dna(sequence)
            else:  # encrypted
                print("使用加密模式解码...")  # 调试信息
                if not password:
                    raise ValueError("加密水印需要提供密码")
                watermark_text = encoding.decode_encrypted_dna(sequence, password)
            
            print(f"成功提取水印文本：{watermark_text}")  # 调试信息
        except Exception as e:
            print(f"水印解码失败：{str(e)}")  # 调试信息
            raise ValueError(f"水印解码失败：{str(e)}")

        return {
            "watermark_text": watermark_text,
            "position": {
                "start": start,
                "end": end
            },
            "sequence": sequence,
            "algorithm": algorithm
        }
        
    except Exception as e:
        print(f"提取水印过程中发生错误：{str(e)}")  # 调试信息
        raise ValueError(f"提取水印失败：{str(e)}") 