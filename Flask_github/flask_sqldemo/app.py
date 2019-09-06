from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import randint

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

模型之间的关联
直接通过user查询出用户的

'''
db = SQLAlchemy(app)
class Role(db.Model):
    '''
    1. 定义表名__tablename__
    2. 定义字段名db.column
    '''
    # 在1的一方增加关联
    # db.relationship('User')在第一个表中增加User的关联
    # backref 给user表中增加一个反向引用

    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)
    users = db.relationship('User',backref="Role")
    # def __repr__(self):
    #     return "身份是{},id是".format(self.name,self.id)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(32),unique=True)
    password = db.Column(db.String(32))
    def __repr__(self):
        return "姓名: {}，邮箱: {}，密码: {}".format(self.name,self.email,self.password)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    #删除并创建数据表
    db.drop_all()
    db.create_all()
    role = Role(name='admin')
    role1 = Role(name='user')

    db.session.add_all([role,role1])
    db.session.commit()

    # # 数据库中表字段的增删改
    # user = User(name='chenqi',role_id=role.id)
    # db.session.add(user)
    # db.session.commit()
    #
    # user.name = '陈小春'
    # db.session.commit()
    #
    # db.session.delete(user)
    # db.session.commit()

    for i in range(10):
        user = User(name='张{}鸣'.format(i+1),role_id=role.id,email='{}@qq.com'.format(randint(10**9,10**10)),password=str(randint(10**5,10**6)))
        db.session.add(user)
        db.session.commit()
        # print(user.Role.name)  #可以获取到用户的身份信息

    for i in range(10):
        user = User(name='张{}丰'.format(i+1),role_id=role1.id,email='{}@qq.com'.format(randint(10**9,10**10)),password=str(randint(10**5,10**6)))
        db.session.add(user)
        db.session.commit()

    # 查询 所有用户
    print(User.query.all())
    # 查询用户个数
    print(User.query.count())
    # 查询 id 为1的信息
    print(User.query.get(1))
    # 查询id为4的信息
    print(User.query.filter_by(id=4).first())
    # 查询id为4的信息
    print(User.query.filter(User.id>=4).all())

    app.run()
