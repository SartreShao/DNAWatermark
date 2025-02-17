"""GenBank 数据处理相关的路由定义"""

from flask import Blueprint, request, jsonify
from service.genbank_service import parse_genbank_data

bp = Blueprint('genbank', __name__, url_prefix='/api/genbank')

@bp.route('/parse', methods=['POST'])
def parse_genbank():
    """解析 GenBank 格式数据
    
    请求体：
    {
        "data": str  # GenBank 格式的数据
    }
    
    返回格式：
    {
        "id": str,                # 序列标识符（如 "L29345.1"）
        "name": str,              # 序列名称（如 "AEVGFP"）
        "description": str,       # 序列描述
        "seq": str,              # 完整的核苷酸序列
        "annotations": {          # 注释信息
            "accessions": [str],  # 登录号列表
            "comment": str,       # 注释说明
            "data_file_division": str,  # 数据文件分区（如 "INV"）
            "date": str,          # 日期
            "keywords": [str],    # 关键词列表
            "molecule_type": str, # 分子类型（如 "mRNA"）
            "organism": str,      # 生物体名称
            "references": [       # 参考文献列表
                {
                    "authors": str,    # 作者
                    "title": str,      # 标题
                    "journal": str,    # 期刊信息
                    "pubmed_id": str,  # PubMed ID
                    "location": list   # 位置信息
                }
            ],
            "sequence_version": str,  # 序列版本
            "source": str,           # 来源
            "taxonomy": [str],       # 分类学信息
            "topology": str          # 拓扑结构（如 "linear"）
        },
        "features": [             # 特征列表
            {
                "type": str,         # 特征类型（如 "source", "gene", "CDS"）
                "location": str,     # 位置信息
                "qualifiers": {      # 限定符
                    "key": [str]     # 各种限定符信息
                },
                "id": str,           # 特征ID
                "ref": str,          # 参考信息
                "ref_db": str        # 参考数据库
            }
        ],
        "dbxrefs": [str],        # 数据库交叉引用
        "letter_annotations": {   # 字母注释
            "_length": str        # 序列长度
        }
    }
    """
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
        
    request_data = request.json
    if not request_data:
        return jsonify({"error": "Request body is empty"}), 400
        
    data = request_data.get('data')
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        parsed_data = parse_genbank_data(data)
        return jsonify(parsed_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400 