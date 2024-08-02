# 使用官方Python运行时作为父镜像
FROM python:3.8.3

# Set environment variables for proxy
# ENV http_proxy=http://10.210.180.148:7443
# ENV https_proxy=http://10.210.180.148:7443

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器中的/app
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8004

# 运行服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8004"]