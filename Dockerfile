# 使用官方Python运行时作为父镜像
FROM python:3.10.14-slim-bullseye



# 将当前目录的内容复制到容器的/app中
COPY ./app  /app
COPY ./app/requirements.txt /app/requirements.txt

# 设置工作目录
WORKDIR /app

# 安装工具包
RUN apt update


RUN apt install vim net-tools sudo -y

#安装 opencv 依赖包
# RUN yum install mesa-libGL -y
RUN apt install libgl1-mesa-glx -y



RUN cd /app

# 安装所需包
RUN python3.10 -m pip install --upgrade pip

# RUN pip3.10 install opencv-python-headless  -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN pip3.10 install --no-cache-dir -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com




# 暴露端口
EXPOSE 5000



# 运行uWSGI，通过uwsgi.ini配置
# CMD ["uwsgi", "--ini", "/app/config/uwsgi.ini"]


# 运行 python main.py
CMD ["python3.10","/app/main.py"]
