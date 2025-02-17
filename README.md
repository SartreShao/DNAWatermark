# DNA Watermark

基因水印数字化工程 - 用于在合成生物学产品中嵌入可追溯的数字签名，实现知识产权保护。

## 功能特点

- 基因序列信息的标准化处理
- 支持 FASTA、GenBank 等标准基因数据格式
- 基于输入信息生成紧凑的数字签名
- 智能识别基因组合适的插入位点
- 提供水印序列的提取和验证方法
- 采用 AES-256 加密算法确保安全性

## 安装

```bash
# 使用 Poetry 安装依赖
poetry install
```

## 运行服务

1. 启动API服务：
```bash
# 在独立的终端窗口中运行
poetry run python run.py
```

2. 停止服务：
   - 如果在终端窗口运行：直接按 Ctrl+C
   - 如果在后台运行：使用 `taskkill /F /IM python.exe`

服务默认在以下地址运行：
- http://localhost:5000

## API使用说明

1. 健康检查
```bash
curl http://localhost:5000/api/health
```

2. 嵌入水印
```bash
curl -X POST http://localhost:5000/api/watermark/embed \
     -H "Content-Type: application/json" \
     -d '{
           "sequence": "ATCGATCGATCGATCG",
           "message": "test_user"
         }'
```

3. 提取水印
```bash
curl -X POST http://localhost:5000/api/watermark/extract \
     -H "Content-Type: application/json" \
     -d '{
           "sequence": "ATATCGGATCTGATCG"
         }'
```

## 开发

```bash
# 安装开发依赖
poetry install --with dev

# 运行测试
poetry run pytest

# 代码格式化
poetry run black .
poetry run isort .
```

## API响应格式

所有API响应都遵循以下格式：
```json
{
    "success": true,
    "data": "结果数据",
    "message": "操作说明"
}
```

## 注意事项

1. 开发环境运行
   - 服务默认以开发模式运行
   - 不要在生产环境使用开发服务器
   - 生产环境请使用 WSGI 服务器（如 Gunicorn）

2. 安全性
   - API服务默认允许所有来源的CORS请求
   - 生产环境部署时请配置适当的CORS策略

## 许可证

待补充...
