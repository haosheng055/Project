# 数据库相关函数
# 用户相关
# 增加记录函数
def addUser(db, User, name, password, email, phone):
    u = User(name, password, email, phone)
    db.session.add(u)
    db.session.commit()
    return u


# 删除记录函数(只允许按照用户UID删除)
def deleteUser(db, User, UID):
    u = User.query.filter_by(UID=UID).all()
    for row in u:
        db.session.delete(row)
    db.session.commit()


# 修改记录函数
def updateUser(db, User, UID, name=None, password=None, email=None, phone=None):
    u = User.query.filter_by(UID=UID).first()
    if name is not None:
        u.name = name
    if password is not None:
        u.password = password
    if email is not None:
        u.email = email
    if phone is not None:
        u.phone = phone
    db.session.commit()


# 查询数据函数
# 通过email查
def selectUser_by_email(User, email):
    return User.query.filter_by(email=email).first()


# 通过电话查
def selectUser_by_phone(User, phone):
    return User.query.filter_by(phone=phone).first()


# 通过用户名查
def selectUser_by_name(User, name):
    return User.query.filter_by(name=name).first()


# 查询User
def selectUser(User, UID):
    return User.query.get(UID)
