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

## 使用方法

待补充...

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

## 许可证

待补充...
