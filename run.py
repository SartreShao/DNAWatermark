"""DNA水印系统启动脚本"""

from app import app

if __name__ == '__main__':
    # 直接运行app.py中的应用实例
    app.run(debug=True, host='0.0.0.0', port=5000) 