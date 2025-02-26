"""应用程序入口"""

from flask import Flask, send_from_directory, Response, render_template_string
from flask_cors import CORS
import os

from models.database import Base, engine
from route import (
    database_routes,
    watermark_routes,
    encoding_routes,
    genbank_routes,
    health_routes,
    infringement_routes
)

def create_app():
    """创建Flask应用实例"""
    
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    # 创建应用实例
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    
    # 配置CORS
    CORS(app)
    
    # 注册路由
    app.register_blueprint(watermark_routes.bp)
    app.register_blueprint(database_routes.bp)
    app.register_blueprint(encoding_routes.bp)
    app.register_blueprint(genbank_routes.bp)
    app.register_blueprint(health_routes.bp)
    app.register_blueprint(infringement_routes.bp)
    
    return app

# 创建应用实例
app = create_app()

# 处理根路径请求
@app.route('/')
def index():
    # 返回静态文件夹中的index.html
    static_folder = app.static_folder or 'static'
    try:
        with open(os.path.join(static_folder, 'index.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        return render_template_string(content)
    except Exception as e:
        return f"Error serving index.html: {str(e)}", 500

# 处理其他静态文件
@app.route('/<path:path>')
def serve_static(path: str) -> Response:
    # 检查请求路径是否是API路由
    if path.startswith('api/'):
        # 让Flask继续处理API请求
        return app.response_class(status=404)
    
    static_folder = app.static_folder
    if static_folder is None:
        static_folder = 'static'
        
    if os.path.exists(os.path.join(static_folder, path)):
        # 提供静态文件
        return send_from_directory(static_folder, path)
    else:
        # 返回index.html以支持前端路由
        return send_from_directory(static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) 