# 使用官方Python运行时作为父镜像
FROM kubeovn/centos8-compile:v1.10.0-x86



# 将当前目录的内容复制到容器的/app中
COPY ./app  /app
COPY ./app/requirements.txt /app/requirements.txt

# 设置工作目录
WORKDIR /app

# 安装工具包
# RUN yum install -y epel-release
# RUN yum update

RUN yum install wget zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make zlib zlib-devel libffi-devel -y
RUN yum install vim net-tools sudo -y

RUN yum install mesa-libGL -y

RUN cd /app
RUN wget -P /app/ https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tgz
RUN tar -zxvf Python-3.10.5.tgz
RUN cd Python-3.10.5
RUN pwd && ls -lah
RUN bash /app/Python-3.10.5/configure --enable-optimizations --with-openssl=/usr/local/openssl-1.1.1 --with-openssl-rpath=auto
RUN make && sudo make install
RUN rm -rf /app/Python-3.10.5


RUN ln -s /usr/local/bin/python3.10 /usr/bin/python3.10
RUN ln -s /usr/local/bin/pip3.10 /usr/bin/pip3.10

RUN ls -l /usr/bin/python3.10
RUN ls -l /usr/bin/pip3.10

RUN export PATH=/usr/bin/python3.10:/usr/bin/pip3.10:$PATH

# 安装所需包
RUN python3.10 -m pip install --upgrade pip
RUN which python3.10
RUN pip3.10 install uwsgi -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN pip3.10 install opencv-python-headless  -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN pip3.10 install --no-cache-dir -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com




# 暴露端口
EXPOSE 5000



# ####运行uWSGI，通过uwsgi.ini配置
# CMD ["uwsgi", "--ini", "/app/config/uwsgi.ini"]


# 运行 python main.py
CMD ["python3.10","/app/main.py"]