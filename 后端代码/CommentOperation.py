# 添加评论
def addComment(db, Comment, ReplyComment, uid, aid, content):
    c = Comment(uid, aid, content, False)
    db.session.add(c)
    db.session.commit()
    return c.CID


# 回复评论
def replyComment(db, Comment, ReplyComment, uid, aid, cid, content):
    c = Comment(uid, aid, content, True)  # 创建新的评论
    db.session.add(c)
    db.session.commit()
    r = ReplyComment(CID=cid, RPID=c.CID)
    db.session.add(r)
    db.session.commit()
    return r.RPID


# 获取文章的评论列表
def getCommentListByAID(Comment, ReplyComment, User, aid):
    comments = list(Comment.query.filter_by(AID=aid,IsReply=False).all())
    comments.sort(key=lambda c: c.time, reverse=True)
    comment_list = []
    for comment in comments:
        comment_list.append(getCommentItem(Comment, ReplyComment, User, comment.CID))
    result = {
        "comments": comment_list
    }
    return result


# 删除评论
def deleteComment(db, Comment, ReplyComment, cid):
    deleted = []
    deleted.append(cid)
    comments = ReplyComment.query.filter_by(CID=cid).all()  # 找到与它相关的评论
    for c in comments:
        deleted.append(c.CID)
    for cids in deleted:
        c = Comment.query.get(cids)
        db.session.delete(c)
    for c in comments:
        db.session.delete(c)
    db.session.commit()


# 根据CID获取完整的回复评论信息
def getCommentReplyItem(Comment, ReplyComment, User, rpid):
    reply_record = ReplyComment.query.get(rpid)
    source_comment = Comment.query.filter_by(CID=reply_record.CID).first()  # 获取被回复评论
    reply_comment = Comment.query.get(reply_record.RPID)  # 获取回复评论本身
    uid = source_comment.UID  # 获取被回复评论
    user_replied = User.query.get(uid)  # 被回复人
    user_reply = User.query.get(reply_comment.UID)
    result = {
        "cid": reply_comment.CID,
        "to": user_replied.name,
        "uid": reply_comment.UID,
        "name": user_reply.name,
        "email": user_reply.email,
        "mobile": user_reply.phone,
        "comment": reply_comment.content,
        "time": reply_comment.time,
        "inputShow": False
    }
    return result


# 根据CID获取评论的完整信息
def getCommentItem(Comment, ReplyComment, User, cid):
    c = Comment.query.get(cid)
    user = User.query.get(c.UID)
    reps = list(ReplyComment.query.filter_by(CID=cid).all())  # 回复本评论的全部评论
    rpids= []  # 回复本评论的全部评论的RPID
    for rep in reps:
        rpids.append(rep.RPID)
    replies = []
    for rpid in rpids:
        reply = getCommentReplyItem(Comment, ReplyComment, User, rpid)
        replies.append(reply)
    replies.sort(key=lambda r: r['time'], reverse=True)
    result = {
        "cid": cid,
        "content": c.content,
        "uid": user.UID,
        "name": user.name,
        "email": user.email,
        "mobile": user.phone,
        "time": c.time,
        "inputShow": False,
        "reply": replies
    }
    return result