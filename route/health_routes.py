"""健康检查相关的路由定义"""

from flask import Blueprint, jsonify

bp = Blueprint('health', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "version": "0.1.0"
    }) 