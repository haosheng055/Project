import os as os
import datetime


# 常用函数
def getTime():
    dt = datetime.datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# 与存取资源相关的
# 应该返回一个本地存储地址，和文件名
def getUrl(filename, uid):
    try:  # 先构建相应的目录
        os.mkdir("./static/"+"userFile"+"/"+str(uid))
    except FileExistsError:
        pass
    # print(os.listdir(os.curdir+"/"+str(uid)))
    num = 0
    for item in os.listdir(os.curdir+"/static/userFile/"+str(uid)):  # 找出有多少重名的
        if item.find(filename) == 0:
            num = num + 1
    if num != 0:
        if filename.find(".") != -1:  # 文件有扩展名
            suffix = filename.split(".")[-1]
            pos = filename.rindex("."+suffix)
            name = filename[0:pos]
            name = name + f"({num})"
            filename = name + "." + suffix
        else:  # 文件没有扩展名
            filename = filename + f"({num})"
    return "./static/userFile"+f"/{uid}"+"/"+filename, filename


# 根据RID返回一个get的连接
def getResourceUrl(rid):
    return "/resourceDownloader?RID="+str(rid)


# 上传一张照片，返回一张组装好的get请求
def getPicUrl(filename):
    num = 0
    for item in os.listdir(os.curdir+"/static/articlePics"):
        if item.find(filename) == 0:
            num = num + 1
    if num != 0:
        if filename.find(".") != -1:  # 文件有扩展名
            suffix = filename.split(".")[-1]
            pos = filename.rindex("."+suffix)
            name = filename[0:pos]
            name = name + f"({num})"
            filename = name + "." + suffix
        else:
            filename = filename + f"({num})"
    return "/static/articlePics/" + filename


# 根据RID返回一个GET连接，用来删除文件
def deleteResourceUrl(rid):
    return "/deleteResource?RID="+str(rid)
