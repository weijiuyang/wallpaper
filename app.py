import click
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import sys 
import click
from wallpaperextend import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, flash,request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy



    
app = Flask(__name__)
CORS().init_app(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = '123456'   # 替换为您自己的密钥
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     username = db.Column(db.String(20))  # 用户名
#     password_hash = db.Column(db.String(128))  # 密码散列值

#     def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
#         self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

#     def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
#         return check_password_hash(self.password_hash, password)  # 返回布尔值

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Login')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


class WallPaper(db.Model):  # 表名将会是 wallpaper
    id = db.Column(db.Integer, primary_key=True)  # 主键
    uploader = db.Column(db.String(20))  # 上传者
    location = db.Column(db.String(20),default='快乐星球')  # 地点
    theme = db.Column(db.String(10)) #主题
    name = db.Column(db.String(20)) #名字

@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()
    # 全局的两个变量移动到这个函数内
    password = '123456'
    wallpapers = [
        {'name': 'zr1', 'uploader': 'Chen Cat','location':'Shanghai','theme':'zr'},
        {'name': 'zr2', 'uploader': 'Chen Cat','location':'Beijing','theme':'zr'},
        {'name': 'zr3', 'uploader': 'Chen Cat','location':'Shenzhen','theme':'zr'},
        {'name': 'rw1', 'uploader': 'Chen Cat','location':'Xiamen','theme':'rw'},
        {'name': 'rw2', 'uploader': 'Chen Cat','location':'India','theme':'rw'},
        {'name': 'jw1', 'uploader': 'Chen Cat','location':'Singapore','theme':'jw'},
        {'name': 'jw2', 'uploader': 'Chen Cat','location':'California','theme':'jw'},
        {'name': 'jw3', 'uploader': 'Chen Cat','location':'Japan','theme':'jw'},
        {'name': 'dm1', 'uploader': 'Chen Cat','location':'fantasyworld','theme':'dm'},
        {'name': 'dm2', 'uploader': 'Chen Cat','location':'fantasyworld','theme':'dm'},
        {'name': 'dm3', 'uploader': 'Chen Cat','location':'fantasyworld','theme':'dm'},
        {'name': 'dm4', 'uploader': 'Chen Cat','location':'fantasyworld','theme':'dm'},
        {'name': 'dm5', 'uploader': 'Chen Cat','location':'fantasyworld','theme':'dm'},
        {'name': 'art1', 'uploader': 'Chen Cat','location':'otherworld','theme':'art'},
        {'name': 'art2', 'uploader': 'Chen Cat','location':'otherworld','theme':'art'},
    ]

    user = User(username = 'Chen Cat',password =password )
    db.session.add(user)
    for paper in wallpapers:
        wallpaper = WallPaper(name=paper['name'], uploader=paper['uploader'],location=paper['location'],theme = paper['theme'])
        db.session.add(wallpaper)

    db.session.commit()
    click.echo('Done.')


@app.route('/mypaper',methods=['GET', 'POST'])
def mypaper():
    username = request.args.get('username')  # 传入表单对应输入字段的 name 值

    user = User.query.filter(User.username == username)  # 读取用户记录
    papers = WallPaper.query.filter(WallPaper.uploader == username)   # 读取所有电影记录
    papers = safework(papers)
    print(papers)
    return render_template('mypaper.html', user=user, papers=papers,username=username)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        username = request.form['username']  # 传入表单对应输入字段的 name 值
        location = request.form['location']
        theme = request.form['theme']
        # print(savepath)
        filepath = os.path.join('./static/images', f.filename)
        f.save(filepath)
        print(username)
        wallpaper = WallPaper(name=f.filename.split('.')[0], uploader = username,location = location , theme = theme)
        db.session.add(wallpaper)
        db.session.commit()

        return redirect(request.referrer) 
    else:
        return render_template('upload.html')


@app.route('/modify', methods=['GET', 'POST'])
def modify_file():
    username = request.form['username']  # 传入表单对应输入字段的 name 值
    location = request.form['location']
    theme = request.form['theme']
    paper = WallPaper.query.filter(WallPaper.uploader == username).first()
    paper.location = location
    paper.theme = theme
    db.session.commit()
    return redirect(request.referrer) 

    
@app.route('/delete-image', methods=['POST'])
def delete_image():
    data = request.json
    src = data['src']
    print('qqqqq')
    print(src)
    name = src.split('/images/')[-1].split('.')[0]
    print(name)
    paper = WallPaper.query.filter(WallPaper.name == name).first()
    db.session.delete(paper)
    db.session.commit()
    return 'success'


@app.route('/')
def index():
    user = User.query.first()  # 读取用户记录
    papers = WallPaper.query.all()  # 读取所有电影记录
    papers = safework(papers)
    print(papers)
    recent_papers = WallPaper.query.order_by(WallPaper.id).limit(4).all()
    return render_template('index.html', user=user, papers=papers ,recent_papers = recent_papers)

    return render_template('index.html')
    return jsonify({'code':1000})

@app.route('/search', methods = ['POST','GET'])
def search():
    theme = request.args.get('theme')
    papers = WallPaper.query.filter(WallPaper.theme == theme).all()  # 读取所有电影记录
    papers = safework(papers)
    print(papers)
    # latestpapers = WallPaper.query.filter(WallPaper.theme == theme).all()  # 读取所有电影记录
    return render_template('search.html',  papers=papers)


if __name__ == '__main__':
    # app.run(debug=True)
    # app.run()

    app.run(host='0.0.0.0', port='6677', debug=True)
