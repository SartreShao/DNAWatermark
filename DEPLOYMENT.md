# DNA水印系统部署文档

本文档详细说明了如何在服务器上部署DNA水印系统。

## 目录

- [系统要求](#系统要求)
- [环境准备](#环境准备)
- [项目部署](#项目部署)
- [使用Nginx作为反向代理（可选）](#使用nginx作为反向代理可选)
- [前端配置](#前端配置)
- [系统启动与停止](#系统启动与停止)
- [故障排除](#故障排除)
- [安全注意事项](#安全注意事项)

## 系统要求

- Python 3.11或更高版本
- 足够的存储空间用于数据库和日志
- 建议至少2GB RAM
- Linux操作系统（本文档基于OpenCloudOS 9，但其他Linux发行版也适用）

## 环境准备

1. 更新系统并安装必要的软件包：

```bash
# 更新系统
sudo dnf update -y  # CentOS/RHEL/OpenCloudOS
# 或
sudo apt update && sudo apt upgrade -y  # Debian/Ubuntu

# 安装Python和相关工具
sudo dnf install -y python3 python3-pip python3-devel gcc  # CentOS/RHEL/OpenCloudOS
# 或
sudo apt install -y python3 python3-pip python3-dev gcc  # Debian/Ubuntu

# 安装Nginx（如果需要反向代理）
sudo dnf install -y nginx  # CentOS/RHEL/OpenCloudOS
# 或
sudo apt install -y nginx  # Debian/Ubuntu

# 启动Nginx并设置开机自启
sudo systemctl start nginx
sudo systemctl enable nginx
```

2. 创建项目目录：

```bash
# 创建项目目录
sudo mkdir -p /var/www/flask_app
sudo chmod 755 /var/www/flask_app
```

## 项目部署

1. 将项目文件上传到服务器的`/var/www/flask_app`目录。可以使用scp、rsync或SFTP客户端（如FileZilla、XFTP等）。

2. 创建和配置Python虚拟环境：

```bash
# 进入项目目录
cd /var/www/flask_app

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装项目依赖
pip install poetry
pip install gunicorn

# 使用Poetry安装依赖
poetry install --without dev
# 如果遇到问题，可能需要先运行
# poetry lock
```

3. 测试应用是否能正常运行：

```bash
# 确保您在虚拟环境中且位于项目目录
gunicorn --bind 127.0.0.1:5000 "run:app"
```

如果一切正常，按Ctrl+C停止测试服务器。

4. 创建Systemd服务文件：

```bash
# 退出虚拟环境
deactivate

# 创建服务文件
sudo nano /etc/systemd/system/dna-watermark.service
# 或使用vim
sudo vim /etc/systemd/system/dna-watermark.service
```

将以下内容添加到服务文件中（请确保路径与您的实际部署一致）：

```
[Unit]
Description=DNAWatermark Flask Application
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/flask_app
Environment="PATH=/var/www/flask_app/venv/bin"
ExecStart=/var/www/flask_app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 "run:app"
Restart=always

[Install]
WantedBy=multi-user.target
```

5. 启动并设置服务自启动：

```bash
sudo systemctl daemon-reload
sudo systemctl start dna-watermark
sudo systemctl enable dna-watermark
sudo systemctl status dna-watermark  # 检查状态
```

6. 配置防火墙（如果需要）：

对于使用firewalld的系统：
```bash
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

对于使用iptables的系统：
```bash
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
sudo netfilter-persistent save
```

对于云服务器，您可能需要在云服务商的控制面板中添加安全组规则，允许TCP 5000端口的入站流量。

## 使用Nginx作为反向代理（可选）

虽然可以直接暴露Gunicorn（5000端口），但在生产环境中，建议使用Nginx作为反向代理，以获得更好的性能和安全性。

1. 创建Nginx配置文件：

```bash
sudo nano /etc/nginx/conf.d/dna-watermark.conf
# 或使用vim
sudo vim /etc/nginx/conf.d/dna-watermark.conf
```

添加以下配置：

```
server {
    listen 80;
    server_name _;  # 使用服务器IP地址或域名

    # 静态文件处理
    location /assets {
        alias /var/www/flask_app/static/assets;
        expires 30d;
    }
    
    location /static {
        alias /var/www/flask_app/static;
        expires 30d;
    }

    # 所有请求转发到Flask应用
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

2. 测试并重启Nginx：

```bash
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

3. 修改systemd服务文件，使Gunicorn只监听本地连接（安全性考虑）：

```bash
sudo nano /etc/systemd/system/dna-watermark.service
# 或使用vim
sudo vim /etc/systemd/system/dna-watermark.service
```

将`ExecStart`行修改为：

```
ExecStart=/var/www/flask_app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 "run:app"
```

4. 重新加载并重启服务：

```bash
sudo systemctl daemon-reload
sudo systemctl restart dna-watermark
```

5. 配置防火墙（如果需要）：

```bash
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --reload
```

## 前端配置

Vue3前端应用需要配置正确的API基础URL，以便连接到后端服务。

### 方式一：本地修改并重新构建（推荐）

1. 在本地Vue项目中，找到定义API基础URL的文件
2. 将`localhost:5000`修改为服务器IP或域名，或使用相对路径
3. 重新构建Vue项目：`npm run build`
4. 使用SFTP/XFTP将整个`dist`目录上传到服务器的`/var/www/flask_app/static`目录

### 方式二：直接修改已构建的JS文件

如果不方便重新构建，可以直接修改已构建的JS文件：

```bash
cd /var/www/flask_app/static/assets
sudo nano index-*.js
# 或使用vim
sudo vim index-*.js

# 搜索并替换所有的localhost:5000为服务器IP或域名
```

### 推荐：使用相对路径

为了避免在不同环境中修改API地址，建议在前端代码中使用相对路径：

```javascript
// 将绝对URL改为相对路径
const API_BASE_URL = '/api'
```

这样，无论应用部署在哪里，它都会自动向当前域名发送API请求。

## 系统启动与停止

```bash
# 启动服务
sudo systemctl start dna-watermark

# 停止服务
sudo systemctl stop dna-watermark

# 重启服务
sudo systemctl restart dna-watermark

# 查看服务状态
sudo systemctl status dna-watermark

# 查看日志
sudo journalctl -u dna-watermark -f
```

## 故障排除

### 1. 服务无法启动

检查服务日志：
```bash
sudo journalctl -u dna-watermark -f
```

常见问题：
- 路径错误：确保服务文件中的路径正确
- 权限问题：确保目录和文件有正确的权限
- 依赖缺失：确保所有必要的依赖都已安装

### 2. 网站可以访问但API调用失败

- 检查前端API地址配置是否正确
- 检查CORS设置是否正确
- 查看Flask应用日志以获取更多信息

### 3. Nginx配置问题

```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

## 安全注意事项

1. 定期更新系统和依赖包
2. 考虑使用HTTPS（通过Let's Encrypt免费获取SSL证书）
3. 限制对服务器的SSH访问
4. 使用更严格的防火墙规则
5. 定期备份数据库

## 附录：systemd服务配置选项

Systemd服务文件可以包含更多高级选项，例如：

```
[Unit]
Description=DNAWatermark Flask Application
After=network.target
Wants=network-online.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/flask_app
Environment="PATH=/var/www/flask_app/venv/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/var/www/flask_app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 --timeout 60 --access-logfile /var/log/dna-watermark/access.log --error-logfile /var/log/dna-watermark/error.log "run:app"
Restart=always
RestartSec=5
StartLimitIntervalSec=0

[Install]
WantedBy=multi-user.target
```

根据您的需求进行调整。 