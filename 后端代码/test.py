from flask import Flask, request, render_template, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from Functions import getUrl, getTime, getResourceUrl, getPicUrl, deleteResourceUrl
from ResourceOperation import addResource, deleteResource
from UserOperation import addUser, selectUser, selectUser_by_email, selectUser_by_phone, selectUser_by_name, deleteUser, updateUser
from ArticleOperation import *
from SocialOperation import *
from CommentOperation import *

app = Flask(__name__)
'''
app.config['MAIL_DEBUG'] = True  # 开启debug，便于调试看信息
app.config['MAIL_SUPPRESS_SEND'] = False  # 发送邮件，为True则不发送
app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 邮箱服务器
app.config['MAIL_PORT'] = 465  # 端口
app.config['MAIL_USE_SSL'] = True  # 重要，qq邮箱需要使用SSL
app.config['MAIL_USE_TLS'] = False  # 不需要使用TLS
app.config['MAIL_USERNAME'] = '2559440494@qq.com'  # 填邮箱
app.config['MAIL_PASSWORD'] = 'hrlstahnbkncdihd'  # 填授权码
app.config['MAIL_DEFAULT_SENDER'] = ('邓涵之', '2559440494@qq.com')  # 填邮箱，默认发送者
app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qaz123wsx@localhost:3306/blog_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.before_first_request
def config_server():
    pass

'''用户表(UID,name,密码,邮箱,电话,是否管理员,是否验证成功,md5)'''


# 数据库区
# 用户表
class User(db.Model):
    __tablename__ = "user"
    UID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(120), unique=True, nullable=True)

    def __init__(self, name, password, email, phone):
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone

    def __str__(self):
        return f"[{self.UID},{self.name},{self.password},{self.email},{self.phone}]"

    __repr__ = __str__


# 资源表
class Resource(db.Model):
    __tablename__ = "resource"
    RID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UID = db.Column(db.Integer, primary_key=False, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    location = db.Column(db.String(120), unique=False, nullable=False)
    time = db.Column(db.String(120), nullable=False)

    def __init__(self, UID, name, location):
        self.UID = UID
        self.name = name
        self.location = location
        self.time = getTime()

    def __str__(self):
        return f"{{OwnerID:{self.UID},RName:{self.name},RUrl:182.92.223.226{self.location}}}"

    __repr__ = __str__


# 文章内的图片直接放到/static/articlePics，删除文章的时候不用删
# 文章可以有多个分区，因此文章分区列表单独存放
class Article(db.Model):
    __tablename__ = "artcle"
    AID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)  # 表示这篇文章的ID
    Title = db.Column(db.String(120), unique=False, nullable=False)  # 这篇文章的标题
    Content = db.Column(db.Text, unique=False, nullable=False)  # 这篇文章的内容，是markdown格式的字符串
    UID = db.Column(db.Integer, nullable=False)  # 作者UID
    Time = db.Column(db.String(120), nullable=False)  # 文章发表时间
    NumRead = db.Column(db.Integer, nullable=False)

    def __init__(self, name, content, uid):
        self.Title = name
        self.Content = content
        self.UID = uid
        self.Time = getTime()
        self.NumRead = 0

    def __str__(self):
        return f"{{{self.AID},{self.name},{self.location},{self.likes},{self.UID},{self.PID},{self.time}}}"


# 点赞表
class Like(db.Model):
    __tablename__ = "likes"
    UID = db.Column(db.Integer, primary_key=True, nullable=False)
    AID = db.Column(db.Integer, primary_key=True, nullable=False)
    time = db.Column(db.String(120), nullable=False)

    def __init__(self, UID, AID):
        self.UID = UID
        self.AID = AID
        self.time = getTime()

    def __str__(self):  # 用来查看动态
        return f"{{doer:{self.UID},type:like,target:{self.AID},time:{self.time}}}"

    __repr__ = __str__


# 收藏表
class Collect(db.Model):
    __tablename__ = "collect"
    UID = db.Column(db.Integer, primary_key=True, nullable=False)
    AID = db.Column(db.Integer, primary_key=True, nullable=False)
    Time = db.Column(db.String(120), nullable=False)

    def __init__(self, UID, AID):
        self.UID = UID
        self.AID = AID
        self.Time = getTime()

    def __str__(self):
        return f"[{self.UID},{self.AID}]"

    __repr__ = __str__


# 分区表
class Partition(db.Model):
    __tablename__ = "partition"
    PID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    iconUrl = db.Column(db.String(120), nullable=False)

    def __init__(self, name, url):
        self.name = name
        self.iconUrl = url

    def __str__(self):
        return f"[{self.PID},{self.name},{self.iconUrl}]"

    __repr__ = __str__


# 文章分区表
class ArticlePartition(db.Model):
    __tablename__ = "article_partition"
    PID = db.Column(db.Integer, primary_key=True, nullable=False)
    AID = db.Column(db.String(120), nullable=False, primary_key=True)

    def __init__(self, pid, aid):
        self.PID = pid
        self.AID = aid

    def __str__(self):
        return f"{{{self.PID},{self.name}}}"

    __repr__ = __str__


# 文章标签表
class Label(db.Model):
    __tablename__ = "label"
    content = db.Column(db.String(120), primary_key=True, nullable=False)
    AID = db.Column(db.Integer, primary_key=True, nullable=False)

    def __init__(self, content, AID):
        self.content = content
        self.AID = AID

    def __str__(self):
        return f"[{self.content},{self.AID},{self.viewnum}]"

    __repr__ = __str__


# 评论表
class Comment(db.Model):
    __tablename__ = "comment"
    CID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    AID = db.Column(db.Integer, nullable=False)
    UID = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    IsReply = db.Column(db.Boolean, nullable=False)
    time = db.Column(db.String(120), nullable=False)

    def __init__(self, UID, AID, content, is_reply):
        self.AID = AID
        self.UID = UID
        self.content = content
        self.IsReply = is_reply
        self.time = getTime()

    def __str__(self):
        return f"[{self.CID},{self.AID},{self.UID},{self.content},{self.now_time}]"

    __repr__ = __str__


# 回复评论表，RPID是本体的CID，CID是被回复的
class ReplyComment(db.Model):
    __tablename__ = "reply_comment"
    RPID = db.Column(db.Integer, nullable=False, primary_key=True)
    CID = db.Column(db.Integer, nullable=False)

    def __init__(self, RPID, CID):
        self.RPID = RPID
        self.CID = CID

    def __str__(self):
        return f"[{self.RPID},{self.CID}]"

    __repr__ = __str__


# 博主关注表
class FollowBlogger(db.Model):
    __tablename__ = "follow_blogger"
    FanUID = db.Column(db.Integer, primary_key=True, nullable=False)
    BloggerUID = db.Column(db.Integer, primary_key=True, nullable=False)
    time = db.Column(db.String(120), nullable=False)

    def __init__(self, FanUID, BloggerUID):
        self.FanUID = FanUID
        self.BloggerUID = BloggerUID
        self.time = getTime()

    def __str__(self):
        return f"[{self.FanUID},{self.BloggerUID},{self.time}]"

    __repr__ = __str__


# 文章关键词表
class KeywordArticle(db.Model):
    __tablename__ = "keyword_artcle"
    word = db.Column(db.String(120), primary_key=True, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    AID = db.Column(db.Integer, primary_key=True, nullable=False)

    def __init__(self, word, weight, AID):
        self.word = word
        self.weight = weight
        self.AID = AID

    def __str__(self):
        return f"[{self.word},{self.weight},{self.AID}]"

    __repr__ = __str__


# 用户关键词表
class KeywordUser(db.Model):
    __tablename__ = "keyword_user"
    content = db.Column(db.String(120), primary_key=True, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    UID = db.Column(db.Integer, primary_key=True, nullable=False)

    def __init__(self, content, weight, UID):
        self.content = content
        self.weight = weight
        self.UID = UID

    def __str__(self):
        return f"[{self.content},{self.weight},{self.UID}]"

    __repr__ = __str__


# 文章相关，添加文章，以及相应的
# 各个域名的分工
# 首页
@app.route('/')
def home():
    return app.send_static_file('index.html')


# 提交注册表单的地方
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    mobile = request.form['mobile']
    password = request.form['password']
    if email is not None and email != "":
        name = email
    else:
        name = mobile
    u = addUser(db, User, name, password, email, mobile)
    registered = True
    result = {
        "uid": u.UID,
        "registered": registered,
        "username": u.name
    }
    return json.dumps(result)


# 检查手机号是否被占用
@app.route('/checkmobile', methods=['POST'])
def checkmobile():
    mobile = request.form['mobile']
    result = {
        'mobile': selectUser_by_phone(User, mobile) is not None and mobile != ""
    }
    return json.dumps(result)


# 检查邮箱是否被占用
@app.route('/checkemail', methods=['POST'])
def checkmail():
    email = request.form['email']
    result = {
        'email': selectUser_by_email(User, email) is not None and email != ""
    }
    return json.dumps(result)


# 检查用户名是否存在
@app.route('/checkname', methods=['POST'])
def checkname():
    name = request.form['name']
    result = {
        'name': selectUser_by_name(User, name) is not None
    }
    return json.dumps(result)


# 此处只能填手机或者邮箱
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    passwd = request.form['password']
    u = selectUser_by_phone(User, name)
    if u is None:  # 这个人不是通过手机登录
        u = selectUser_by_email(User, name)
    if u is None or u.password != passwd:  # 这个人输入的用户名有问题，或者密码错误
        result = {
            'validation': False
        }
        return json.dumps(result)
    else:  # 这次登陆没问题
        result = {
            'validation': True,
            'UID': u.UID,
            'name': u.name
        }
        return json.dumps(result)


# 用来给个人信息页面获取信息
@app.route('/profile', methods=['POST'])
def getProfile():
    uid = request.form['UID']
    u = selectUser(User, uid)
    result = {
        "username": u.name,
        "email": u.email,
        "mobile": u.phone
    }
    return json.dumps(result)


# 用来修改个人信息
@app.route('/changeinfo', methods=['POST'])
def changeProfile():
    uid = request.form['UID']
    u = selectUser(User, uid)
    username = u.name if request.form['username'] == "" else request.form['username']
    email = u.email if request.form['email'] == "" else request.form['email']
    mobile = u.phone if request.form['mobile'] == "" else request.form['mobile']
    password = request.form['password_old']
    password_new = u.password if request.form['password_new'] == "" else request.form['password_new']
    if u.password == password:  # 密码正确
        updateUser(db, User, uid, username, password_new, email, mobile)
        result = {
            "validation": True,
            "username_new": username,
            "email_new": email,
            "mobile_new": mobile
        }
        return json.dumps(result)
    else:  # 密码错误
        result = {
            "validation": False,
            "username_new": u.name,
            "email_new": u.email,
            "mobile_new": u.phone,
        }
        return json.dumps(result)


# 用来测试博文列表
@app.route('/ArticleTest', methods=['POST'])
def testArticle():
    writer_ids = [1, 2, 3, 4, 5]
    writer_names = ["郝晟", "邓涵之", "姜宝洋", "刘奕博", "张豪"]
    titles = ["为什么我叫郝晟", "为什么我叫邓涵之", "为什么我叫姜宝洋", "为什么我叫刘奕博", "为什么我叫张豪"]
    aids = [1, 2, 3, 4, 5]
    num_comments = [100, 100, 100, 100, 100]
    num_likes = [1000, 1000, 1000, 1000, 1000]
    num_collected = [500, 500, 500, 500, 500]
    times = ["2020-6-6 22:20:10", "2020-6-7 22:20:10", "2020-6-8 22:20:10", "2020-6-9 22:20:10", "2020-6-10 22:20:10"]
    result = {
        "WriterIDs": writer_ids,
        "WriterNames": writer_names,
        "Titles": titles,
        "AIDs": aids,
        "NumComments": num_comments,
        "Likes": num_likes,
        "Times": times,
        "Collects": num_collected  # 收藏数
    }
    return json.dumps(result)


# 用来获取博文列表
@app.route('/getArticle', methods=['POST'])
def getArticle():
    type = request.form['Type']
    if type == "Sector":  # 根据分区来获得博文
        pid = int(request.form['Value'])
        partitions = [pid]
        return json.dumps(getArticleByPartition(Article, Comment, User, Like, ArticlePartition, partitions))
    else:  # 根据用户ID来获取博文
        uid = request.form['Value']
        return json.dumps(getArticleByUID(Article, User, Like, Comment, uid))


# 用来接收文件上传的地方，返回调整过的文件名字，以及文件下载URL
@app.route('/resourceCenter', methods=['POST'])
def getResource():
    uid = request.form['uid']
    f = request.files['fileInput']
    new_file_url = getUrl(f.filename, uid)[0]
    new_file_name = getUrl(f.filename, uid)[1]
    rid = addResource(db, Resource, uid, new_file_name, new_file_url)
    f.save(new_file_url)
    result = {
        "fileName": new_file_name,
        "url": getResourceUrl(rid),
        "deleteUrl": deleteResourceUrl(rid),
        "RID": rid
    }
    return json.dumps(result)


# 用来展示文件列表
@app.route('/resourceList', methods=['POST'])
def getResourceList():
    uid = request.form['uid']
    resource_list = []
    resource_records = Resource.query.filter_by(UID=uid).order_by(Resource.time.desc()).all()
    for item in resource_records:
        resource = {
            "fileName": item.name,  # 这个文件的名字
            "url": getResourceUrl(item.RID),  # 获取这个文件的get请求
            "deleteUrl": deleteResourceUrl(item.RID),
            "RID": item.RID
        }
        resource_list.append(resource)
    res = {
        "list": resource_list
    }
    return json.dumps(res)


# 用来分发下载文件，请求的参数只有一个，就是RID
@app.route('/resourceDownloader', methods=['GET'])
def sendFile():
    file_record = Resource.query.get(request.args['RID'])
    if file_record is None:
        return app.send_static_file("ResourceNotFound.html")
    else:
        return send_file(file_record.location, as_attachment=True, attachment_filename=file_record.name)


# 用来给出全部的分区内容以及相应的图标url
@app.route('/getPartition', methods=['POST'])
def getAllPartition():
    p = Partition.query.filter_by().all()
    partitions = []
    for item in p:
        partitions.append({
            "partition_name": item.name,
            "partition_pid": item.PID,
            "partition_icon_url": item.iconUrl
        })
    result = {
        "partition_data": partitions
    }
    return result


# 用来删除已经发送上来的文件
@app.route('/deleteResource', methods=["POST"])
def deleteFile():
    rid = request.form['RID']
    deleteResource(db, Resource, rid)
    result = {
        "Status": True
    }
    return result


# 发往：182.92.223.226/picSave
# 返回：/picSave/filename.
# 用来接收前端文本编辑发送上来的文件
@app.route('/picSave', methods=['POST'])
def getPic():
    f = request.files['image']
    new_file_url = getPicUrl(f.filename)
    f.save("."+new_file_url)
    result = {
        "url": new_file_url
    }
    return json.dumps(result)


# 用来接收从前端发上来的文章
@app.route('/ArticleSubmit', methods=['POST'])
def receiveArticle():
    uid = request.form['UID']
    aid = request.form['AID']
    content = request.form['Content']
    partitions = request.form['Partitions']
    if partitions is not None and partitions != "":
        partitions = partitions.split(",")
    tags = request.form['Tags']
    if tags is not None and tags != "":
        tags = tags.split(",")
    title = request.form['Title']
    print(list(partitions))
    print(list(tags))
    addArticle(db, Article, Label, ArticlePartition, KeywordArticle, Partition, uid, aid, title, content, list(tags), list(partitions))
    result = {
        "Status": True,
    }
    return json.dumps(result)


# 用来向前端发送已经存在的文章
@app.route('/ArticleGet', methods=['POST'])
def sendArticle():
    aid = request.form['AID']
    uid = request.form['UID']
    if aid == -1:
        return json.dumps(getArticleByAID(db, Article, Partition, KeywordUser, ArticlePartition,  Label, User, aid, uid))
    else:
        return json.dumps(getArticleByAID(db, Article, Partition, KeywordUser, ArticlePartition,  Label, User, aid, uid))


# 用来删除文章
@app.route('/DeleteArticle', methods=["POST"])
def delArticle():
    aid = request.form['AID']
    deleteArticle(db, Article, Label, KeywordArticle, Comment, ReplyComment, Like, Collect, ArticlePartition, aid)
    result = {
        "Status": True
    }
    return result


# 用来向前端发送评论
@app.route('/CommentList', methods=['POST'])
def sendCommentList():
    aid = request.form['AID']
    return json.dumps(getCommentListByAID(Comment, ReplyComment, User, aid))


# 用来接收前端发上来的评论
@app.route('/NewComment', methods=['POST'])
def receiveComment():
    content = request.form['content']
    aid = request.form['AID']
    uid = request.form['UID']
    cid = addComment(db, Comment, ReplyComment, uid, aid, content)
    result = {
        "CID": cid
    }
    return json.dumps(result)


# 用来接收前端上传的回复评论
@app.route('/ReplyComment', methods=['POST'])
def replyComments():
    content = request.form['comment[content]']
    uid = request.form['comment[UID]']
    aid = request.form['comment[AID]']
    cid = request.form['RPID']
    new_cid = replyComment(db, Comment, ReplyComment, uid, aid, cid, content)
    result = {
        "CID": new_cid
    }
    return json.dumps(result)


# 删除评论的功能
@app.route('/DeleteComment', methods=['POST'])
def removeComment():
    cid = request.form['CID']
    deleteComment(db, Comment, ReplyComment, cid)
    result = {
        "Status": True
    }
    return result


# 用来获得文章与当前用户的关系
@app.route('/ArticleInfo', methods=["POST"])
def getArticleInfo():
    uid = request.form['UID']
    aid = request.form['AID']
    author_uid = getUIDByAID(Article, aid)
    result = {
        "NumLikes": getNumLike(Like, aid),
        "IsLiked": isLiked(Like, uid, aid),
        "IsCollected": isCollected(Collect, uid, aid),
        "IsSubscribed": isSubscribed(FollowBlogger, uid, author_uid)
    }
    return json.dumps(result)


# 用来修改文章点赞信息
@app.route('/ArticleLike', methods=['POST'])
def changeLikeState():
    uid = request.form['UID']
    aid = request.form['AID']
    changeLikeStatus(db, Like, uid, aid)
    result = {
        "Status": True
    }
    return json.dumps(result)


# 用来修改文章收藏信息
@app.route('/ArticleCollect', methods=['POST'])
def changeCollectState():
    uid = request.form['UID']
    aid = request.form['AID']
    changeCollectStatus(db, Collect, uid, aid)
    result = {
        "Status": True
    }
    return json.dumps(result)


# 用来修改关注信息
@app.route('/AuthorFollowed', methods=['POST'])
def changeSubscribeState():
    uid = request.form['UID']
    aid = request.form['AID']
    tar_uid = getUIDByAID(Article, aid)
    changeFollowStatus(db, FollowBlogger, uid, tar_uid)
    result = {
        "Status": True
    }
    return json.dumps(result)


# 搜索：全文检索
@app.route('/Search', methods=["POST"])
def search():
    Type = request.form['Type']
    input_value = request.form['Value']
    if Type == "All":
        return json.dumps(searchForAll(Article, KeywordArticle, Like, Comment, User, input_value))
    else:
        return json.dumps(searchByTag(Article, Label, Like, Comment, User, input_value))


'''
{
  "Username": "用户昵称",
  "NumSubscribed": "用户关注了几个人",
  "NumFans": "几个人关注此用户",
  "NumArticle": "此人有几篇文章"
}
'''


# 个人主页的信息获取
@app.route('/personInfo', methods=['POST'])
def getInfo():
    uid = request.form['UID']
    NumSubscribed = len(FollowBlogger.query.filter_by(FanUID=uid).all())
    NumFans = len(FollowBlogger.query.filter_by(BloggerUID=uid).all())
    NumArticle = len(Article.query.filter_by(UID=uid).all())
    Username = User.query.get(uid).name
    result = {
        "Username": Username,
        "NumSubscribed": NumSubscribed,
        "NumFans": NumFans,
        "NumArticle": NumArticle
    }
    return json.dumps(result)


# 获取动态列表
@app.route('/MovementList', methods=["POST"])
def getMovementList():
    uid = request.form['UID']
    return json.dumps(getMovement(Article, User, Comment, Like, Collect, FollowBlogger, uid))


if __name__ == '__main__':
    app.run(debug=True, port=8080)

