import os as os


# 资源相关，添加资源记录，返回RID
def addResource(db, Resource, uid, name, location):
    r = Resource(uid, name, location)
    db.session.add(r)
    db.session.commit()
    return r.RID


# 如何删除一个资源
def deleteResource(db, Resource, rid):
    r = Resource.query.get(rid)
    os.remove(r.location)
    db.session.delete(r)
    db.session.commit()
