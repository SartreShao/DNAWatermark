"""DNA水印系统启动脚本"""

from dna_watermark.api import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 