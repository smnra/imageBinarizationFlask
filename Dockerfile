# 使用官方Python运行时作为父镜像
FROM python:3.10.14-bookworm

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到容器的/app中
COPY ./app/requirements.txt /app/requirements.txt
COPY . /app


# 安装gcc编译器
apt update
apt install gcc -y

# 安装所需包
RUN pip install uwsgi
RUN pip install opencv-python-headless
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 5000

# 运行uWSGI，通过uwsgi.ini配置
CMD ["uwsgi", "--ini", "/app/config/uwsgi.ini"]
