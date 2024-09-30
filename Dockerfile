# 使用官方Python镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 将requirements.txt复制到容器中
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将项目文件复制到容器中
COPY . .

# 暴露应用的端口
EXPOSE 10001

# 启动Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "10001", "jyy_slide_web.asgi:application"]