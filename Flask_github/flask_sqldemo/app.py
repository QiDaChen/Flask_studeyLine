from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 配置数据库的地址，
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/flask_sql_demo'
# 跟踪数据库的修改  不建议开启
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''
两张表
角色（管理员、普通用户）
用户（角色id 用户名  用户id）
数据库模型 
'''
db = SQLAlchemy(app)
class Role(db.Model):
    '''
    1. 定义表名__tablename__
    2. 定义字段名db.column
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    #删除并创建数据表
    db.drop_all()
    db.create_all()
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    # 数据库中表字段的增删改
    user = User(name='chenqi',role_id=role.id)
    db.session.add(user)
    db.session.commit()

    user.name = '陈小春'
    db.session.commit()

    db.session.delete(user)
    db.session.commit()

    for i in range(100):
        user = User(name='张{}鸣'.format(i+1),role_id=role.id)
        db.session.add(user)
        db.session.commit()


    app.run()
