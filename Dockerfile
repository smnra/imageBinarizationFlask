# 使用官方Python运行时作为父镜像
FROM kubeovn/centos8-compile:v1.10.0-x86



# 将当前目录的内容复制到容器的/app中
COPY ./app  /app
COPY ./app/requirements.txt /app/requirements.txt

# 设置工作目录
WORKDIR /app

# 安装工具包
RUN yum install -y epel-release
RUN yum update
RUN yum install wget zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make zlib zlib-devel libffi-devel -y

RUN wget https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tgz
RUN tar zxf Python-3.10.5.tgz
RUN cd Python-3.10.5
RUN ./configure --enable-optimizations --with-openssl=/usr/local/openssl-1.1.1 --with-openssl-rpath=auto
RUN  make && sudo make install




# 安装所需包
RUN pip install --upgrade pip
RUN pip install uwsgi
RUN pip install opencv-python-headless
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 5000

# 运行uWSGI，通过uwsgi.ini配置
CMD ["uwsgi", "--ini", "/app/config/uwsgi.ini"]
