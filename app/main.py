
from flask import Flask, render_template, request, url_for, redirect,send_from_directory
import os
from werkzeug.utils import secure_filename
from imageBinarization import imageBinarizationAdaptive


app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = 'outputs'  # 新增输出目录配置
app.config['UPLOAD_FOLDER'] = 'uploads'  # 新增上传目录配置


#methods参数用于指定允许的请求格式

#常规输入url的访问就是get方法
@app.route("/test",methods=['GET','POST'])
def test():
    return "Hello Test!"

# 可以在路径内以/<参数名>的形式指定参数，默认接收到的参数类型是string

'''#######################
以下为框架自带的转换器，可以置于参数前将接收的参数转化为对应类型
string 接受任何不包含斜杠的文本
int 接受正整数
float 接受正浮点数
path 接受包含斜杠的文本
########################'''




@app.route("/test_1/<int:id>", )
def test_1(id):
    if id == 1:
        return 'first'
    elif id == 2:
        return 'second'
    elif id == 3:
        return 'thrid'
    else:
        return 'hello world!'


@app.route("/test_2/<string:id>", )
def test_2(id):
    if id == 'aaa':
        print(os.getcwd())
        return 'firstaaa'
    elif id == 'bbb':
        return 'secondbbb'
    elif id == 'ccc':
        return 'thridccc'
    else:
        return 'hello world! ' + id


@app.route('/index')
def index():
    # redirect重定位（服务器向外部发起一个请求跳转）到一个url界面；
    # url_for给指定的函数构造 URL；
    # return redirect('/hello') 不建议这样做,将界面限死了
    return redirect(url_for('hello'))



# 欲实现url与视图函数的绑定，除了使用路由装饰器@app.route，我们还可以通过add_url_rule(rule,endpoint=None,view_func=None)方法，其中：
def test_url_rule():
    return '这是 test_url_rule 测试页面'
app.add_url_rule(rule='/test_url_rule',endpoint='test_url_rule',view_func=test_url_rule)






# 请求钩子before/after_request
# 想要在正常执行的代码的前、中、后时期，强行执行一段我们想要执行的功能代码，便要用到钩子函数——用特定装饰器装饰的函数。
@app.before_request
def before_request_a():
    print('I am in before_request_a')


@app.before_request
def before_request_b():
    print('I am in before_request_b')


# after_request：每一次请求之后都会调用；
# 该钩子函数表示每一次请求之后，可以执行某个特定功能的函数，这个函数接收response对象，所以执行完后必须归还response对象
# 执行的顺序是先绑定的后执行；
# 一般可以用于产生csrf_token验证码等场景；
@app.after_request
def after_request_a(response):
    print('I am in after_request_a')
    # 该装饰器接收response参数，运行完必须归还response，不然程序报错
    return response


@app.after_request
def after_request_b(response):
    print('I am in after_request_b')
    return response





@app.route("/test_index", methods=['GET', 'POST'])
# url映射的函数，要传参则在上述route（路由）中添加参数申明
def test_index():
    if request.method == 'GET':
        # 想要html文件被该函数访问到，首先要创建一个templates文件，将html文件放入其中
        # 该文件夹需要被标记为模板文件夹，且模板语言设置为jinja2
        return render_template('index.html')
    # 此处欲发送post请求，需要在对应html文件的form表单中设置method为post
    elif request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        return name + " " + password



def allowed_file(filename):
    ext = filename.split('.')[-1]
    return ext in ['jpg', 'png', 'jpeg']




@app.route('/upload', methods=['GET', 'POST'])
def upload_and_process():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):  # 添加允许的文件类型检查
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 处理图片
            output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            imageBinarizationAdaptive(filepath, output_filepath)

            return render_template('result.html', original_img=url_for('uploaded_file', filename=filename),
                                   processed_img=url_for('uploaded_processed_file', filename=filename))
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/outputs/<filename>')
def uploaded_processed_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)  # 确保输出目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # 确保上传目录存在
    app.run(host='0.0.0.0', port=5000)
