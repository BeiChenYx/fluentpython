import table_structure
from sqlalchemy.orm import sessionmaker


# 创建与数据库的会话 session class, 这里返回的session是个class，不是实例
Session_class = sessionmaker(bind=table_structure.engine)

session = Session_class() # 生成session实例

user_obj = table_structure.User(name='王昭君', password='111')
user_obj2 = table_structure.User(name='韩信', password='12324')

# 把要创建的数据对象添加到session
session.add(user_obj)
session.add(user_obj2)
# 提交
session.commit()
