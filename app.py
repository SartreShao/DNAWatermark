"""应用程序入口"""

from flask import Flask
from flask_cors import CORS

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
    app = Flask(__name__)
    
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

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) 