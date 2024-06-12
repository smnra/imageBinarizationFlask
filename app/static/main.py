from flask import Flask
import os


app = Flask(__name__)

#methods参数用于指定允许的请求格式

#常规输入url的访问就是get方法
@app.route("/hello",methods=['GET','POST'])
def hello():
    return "Hello World!"


# 可以在路径内以/<参数名>的形式指定参数，默认接收到的参数类型是string

'''#######################
以下为框架自带的转换器，可以置于参数前将接收的参数转化为对应类型
string 接受任何不包含斜杠的文本
int 接受正整数
float 接受正浮点数
path 接受包含斜杠的文本
########################'''


@app.route("/index/<int:id>", )
def index(id):
    if id == 1:
        return 'first'
    elif id == 2:
        return 'second'
    elif id == 3:
        return 'thrid'
    else:
        return 'hello world!'


@app.route("/st/<string:id>", )
def st(id):
    if id == 'aaa':
        print(os.getcwd())
        return 'firstaaa'
    elif id == 'bbb':
        return 'secondbbb'
    elif id == 'ccc':
        return 'thridccc'
    else:
        return 'hello world! ' + id



if __name__ == '__main__':
    print(app.view_functions)
    print(app.url_map)
    app.run()

