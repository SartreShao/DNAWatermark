"""DNA水印系统的API入口"""

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 导入路由
from route import health_routes, genbank_routes, encoding_routes, watermark_routes

# 注册路由
app.register_blueprint(health_routes.bp)
app.register_blueprint(genbank_routes.bp)
app.register_blueprint(encoding_routes.bp)
app.register_blueprint(watermark_routes.bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 