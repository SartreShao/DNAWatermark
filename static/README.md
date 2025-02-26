# Vue3 静态文件目录

此目录用于存放Vue3打包后的静态网站文件。

## 使用说明

1. 在Vue3项目中运行构建命令（例如：`npm run build`）
2. 将构建生成的静态文件（通常在Vue项目的`dist`目录中）复制到此目录
3. Flask应用会自动提供这些静态文件

## 目录结构示例

```
static/
  ├── index.html
  ├── favicon.ico
  ├── js/
  │   └── (JavaScript文件)
  ├── css/
  │   └── (CSS文件)
  └── img/
      └── (图片文件)
``` 