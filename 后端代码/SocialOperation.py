# 获取一篇文章的点赞数
from operator import and_


def getNumLike(Like, aid):
    return len(Like.query.filter_by(AID=aid).all())


# 获取一篇文章是否被用户点赞
def isLiked(Like, uid, aid):
    return len(Like.query.filter_by(AID=aid, UID=uid).all()) != 0


# 获取一篇文章是否被用户收藏
def isCollected(Collect, uid, aid):
    return len(Collect.query.filter_by(AID=aid, UID=uid).all()) != 0


# 获取一个作者是否被用户关注
def isSubscribed(FollowBlogger, cur_uid, tar_uid):
    return len(FollowBlogger.query.filter_by(FanUID=cur_uid, BloggerUID=tar_uid).all()) != 0


# 修改用户对文章的点赞状态
def changeLikeStatus(db, Like, uid, aid):
    if isLiked(Like, uid, aid):  # 如果点过赞了，就删除这个赞
        l = Like.query.filter_by(UID=uid, AID=aid).first()
        db.session.delete(l)
        db.session.commit()
    else:  # 如果没有点过赞，就加上
        l = Like(UID=uid, AID=aid)
        db.session.add(l)
        db.session.commit()


# 修改用户对于文章的收藏状态
def changeCollectStatus(db, Collect, uid, aid):
    if isCollected(Collect, uid, aid):  # 如果收藏过了，那就取消收藏
        c = Collect.query.filter_by(UID=uid, AID=aid).first()
        db.session.delete(c)
        db.session.commit()
    else:  # 如果没有点过赞，就加上
        c = Collect(UID=uid, AID=aid)
        db.session.add(c)
        db.session.commit()


# 修改用户对于作者的关注状态
def changeFollowStatus(db, FollowBlogger, cur_uid, tar_uid):
    if isSubscribed(FollowBlogger, cur_uid, tar_uid):  # 如果关注了，就取消关注
        s = FollowBlogger.query.filter_by(FanUID=cur_uid, BloggerUID=tar_uid).first()
        db.session.delete(s)
        db.session.commit()
    else:  # 如果没关注，就添加关注
        s = FollowBlogger(FanUID=cur_uid, BloggerUID=tar_uid)
        db.session.add(s)
        db.session.commit()
