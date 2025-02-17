"""健康检查相关的路由定义"""

from flask import Blueprint, jsonify

bp = Blueprint('health', __name__, url_prefix='/api')

def get_health_status():
    """获取系统健康状态
    
    Returns:
        dict: 包含以下字段的字典：
            - status (str): 系统状态，例如 "healthy"
            - version (str): 系统版本号
    """
    return {
        "status": "healthy",
        "version": "0.1.0"
    }

@bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口
    
    返回格式：
    {
        "status": str,   # 系统状态
        "version": str   # 系统版本号
    }
    """
    return jsonify(get_health_status()) 