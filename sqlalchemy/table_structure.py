"""创建表结构的方法"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sqlalchemy import Table, MetaData, ForeignKey
from sqlalchemy.orm import mapper


engine = create_engine('mysql+pymysql://root:11223@192.168.3.154/LearnWeb')

# 生成 ORM 基类
Base = declarative_base()


# 第一种创建表结构的方法
class User(Base):
    # 表名
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))


# 创建表结构
Base.metadata.create_all(engine)
# 当 create_engine() 第一次返回时，引擎实际上还没有尝试连接到数据库，
# 只有在第一次要求它对数据库执行任务时才会发生这种情况。


# 第二种创建表结构的方法
metadata = MetaData() # 生成metadata类
# 创建user类， 继承metadata类
# Engine使用Schama Type创建一个特定的结构对象

user = Table('new_user', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(50)),
             Column('fullname', String(50)),
             Column('password', String(12))
            )

class NewUser:
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

# 表元数据使用Table 构造单独创建的，然后通过mapper()函数与NewUser类关联
mapper(NewUser, user)

# 通过ConnectionPooling 连接数据库
engine = create_engine('mysql+pymysql://root:11223@192.168.3.154/LearnWeb')
metadata.create_all(engine)
# 事实上，第一种方式创建的表就是基于第二种方式的再封装。
