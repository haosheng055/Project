from jieba import *


# 添加/修改一篇文章
def addArticle(db, Article, Label, ArticlePartition, KeywordArticle, Partition, uid, aid, title, content, tags=None, partitions=None):
    print(type(aid))
    print(aid)
    if aid is None or aid == -1 or aid == "-1":  # 新文章，创建新记录
        a = Article(title, content, uid)
        db.session.add(a)
        db.session.commit()
        aid = a.AID
    else:  # 旧文章
        a = Article.query.get(aid)  # 获得这篇文章
        # 更改这篇文章的题目
        a.Title = title
        # 更改这篇文章的内容
        a.Content = content
        article_tags = Label.query.filter_by(AID=a.AID).all()
        article_partitions = ArticlePartition.query.filter_by(AID=a.AID).all()
        db.session.commit()
        for tag in article_tags:  # 删掉相关的tags
            db.session.delete(tag)
            db.session.commit()
        for part in article_partitions:  # 删掉相关的partition
            db.session.delete(part)
            db.session.commit()
    if tags is not None and len(tags) != 0:  # 如果有标签
        for tag in tags:
            t = Label(tag, a.AID)
            db.session.add(t)
            db.session.commit()
    if partitions is not None and len(partitions) != 0:  # 如果有分区信息
        for part in partitions:
            p = ArticlePartition(part, a.AID)
            db.session.add(p)
            db.session.commit()
    keywordManage(db, Article, KeywordArticle, Label, ArticlePartition, Partition, aid)


# 删除一篇文章
def deleteArticle(db, Article, Label, KeywordArticle, Comment, ReplyComment, Like, Collect, ArticlePartition, aid):
    a = Article.query.filter_by(AID=aid)
    article_tags = Label.query.filter_by(AID=a.AID).all()
    article_partitions = ArticlePartition.query.filter_by(AID=a.AID).all()
    article_keyword = KeywordArticle.query.filter_by(AID=aid).all()
    article_comment = Comment.query.filter_by(AID=aid).all()
    article_like = Like.query.filter_by(AID=aid).all()
    article_collect = Collect.query.filter_by(AID=aid).all()
    for tag in article_tags:
        db.session.delete(tag)
        db.session.commit()
    for part in article_partitions:
        db.session.delete(part)
        db.session.commit()
    for keyword in article_keyword:
        db.session.delete(keyword)
        db.session.commit()
    for like in article_like:
        db.session.delete(like)
        db.session.commit()
    for collect in article_collect:
        db.session.delete(collect)
        db.session.commit()
    for comment in article_comment:
        if comment.IsReply:
            reply = ReplyComment.query.get(comment.CID)
            db.session.delete(reply)
            db.session.delete(comment)
            db.session.commit()
        else:
            db.session.delete(comment)
            db.session.commit()


# 根据分区获得文章列表，按照阅读量排序
def getArticleByPartition(Article, Comment, User, Like, ArticlePartition, partitions):
    aids = []  # 此分区全部的aid
    if -1 in partitions or "-1" in partitions:
        aid_part = Article.query.filter_by().all()
        for aid in aid_part:
            aids.append(aid.AID)
    else:
        for part in partitions:  # 找出每一个分区的全部文章
            aid_part = ArticlePartition.query.filter_by(PID=part).all()
            for article in aid_part:  # 把每一篇文章的AID放在一起
                aids.append(article.AID)
    AidReadDict = {}
    for aid in aids:
        AidReadDict[aid] = Article.query.get(aid).NumRead
    AidReadList = list(AidReadDict.items())
    AidReadList.sort(key=lambda a: a[1], reverse=False)
    WriterNames = []
    Likes = []
    NumComments = []
    WriterIDs = []
    Titles = []
    AIDs = []
    Times = []
    for aid in AidReadList:  # 找出后面需要的全部信息
        article = Article.query.get(aid[0])  # aid对应的文章
        WriterIDs.append(article.UID)
        Titles.append(article.Title)
        AIDs.append(article.AID)
        Times.append(article.Time)
        user = User.query.get(article.UID)
        WriterNames.append(user.name)
        likes = Like.query.filter_by(AID=aid[0]).all()
        Likes.append(len(likes))
        comments = Comment.query.filter_by(AID=aid[0]).all()
        NumComments.append(len(comments))
    result = {
        "WriterIDs": WriterIDs,
        "WriterNames": WriterNames,
        "Titles": Titles,
        "AIDs": AIDs,
        "NumComments": NumComments,
        "Likes": Likes,
        "Times": Times,
        "len": len(aids)
    }
    return result


# 根据UID获得文章，按照时间排序
def getArticleByUID(Article, User, Like, Comment, UID):
    # 获得这个人的全部文章
    article = Article.query.filter_by(UID=UID).order_by(Article.Time.desc())
    # 获得一个文章的全部标签的内容
    aids = []
    for a in article:
        aids.append(a.AID)
    WriterNames = []
    Likes = []
    NumComments = []
    WriterIDs = []
    Titles = []
    AIDs = []
    Times = []
    for aid in aids:  # 找出后面需要的全部信息
        article = Article.query.get(aid)  # aid对应的文章
        WriterIDs.append(article.UID)
        Titles.append(article.Title)
        AIDs.append(article.AID)
        Times.append(article.Time)
        user = User.query.get(article.UID)
        WriterNames.append(user.name)
        likes = list(Like.query.filter_by(AID=aid).all())
        Likes.append(len(likes))
        comments = list(Comment.query.filter_by(AID=aid).all())
        NumComments.append(len(comments))
    result = {
        "WriterIDs": WriterIDs,
        "WriterNames": WriterNames,
        "Titles": Titles,
        "AIDs": AIDs,
        "NumComments": NumComments,
        "Likes": Likes,
        "Times": Times
    }
    return result


'''
- 下行数据格式：{
    - Title：文章的标题
    - AuthorName:作者用户名
    - AID：文章ID
    - Content：文章的markdown正文
    - Partitions：[文章的分区ID]
    - Tags：[文章的标签]
}
'''


# 根据AID获取一篇文章，记得更新用户信息
def getArticleByAID(db, Article, Partition, KeywordUser, ArticlePartition, Label, User, aid, uid):
    article = Article.query.get(aid)
    article.NumRead = article.NumRead+1
    db.session.commit()
    PartitionsRaw = ArticlePartition.query.filter_by(AID=aid).all()
    tags = Label.query.filter_by(AID=aid).all()
    Tags = []
    Partitions = []
    user = User.query.get(article.UID)
    for tag in tags:
        Tags.append(tag.content)
    for part in PartitionsRaw:
        Partitions.append(part.PID)
    result = {
        "Title": article.Title,
        "AuthorName": user.name,
        "AID": article.AID,
        "Content": article.Content,
        "Partitions": Partitions,
        "Tags": Tags
    }
    return result


# 根据aid获得文章作者uid
def getUIDByAID(Article, aid):
    a = Article.query.get(aid)
    return a.UID


# 用来调整文章的关键词以及系数，在内容相关修改完之后使用
def keywordManage(db, Article, KeywordArticle, Label, ArticlePartition, Partition, aid):
    article = Article.query.get(aid)
    keywordList_content = lcut_for_search(article.Content)
    keywordDict = {}
    article_keywords = KeywordArticle.query.filter_by(AID=aid).all()  # 先删除全部相关的关键字
    for item in article_keywords:
        db.session.delete(item)
    db.session.commit()
    for word in keywordList_content:  # 内容中每一个词加1
        if word in keywordDict.items():
            keywordDict[word] += 1
        else:
            keywordDict[word] = 1
    keywordList_title = lcut_for_search(article.Title)
    for word in keywordList_title:  # 题目中，每一个词加5
        if word in keywordDict:
            keywordDict[word] += 5
        else:
            keywordDict[word] = 5
    article_labels = Label.query.filter_by(AID=aid).all()  # 获取全部的相关标签
    for label in article_labels:  # 标签中，每一个词加8
        if label.content in keywordDict:
            keywordDict[label.content] += 8
        else:
            keywordDict[label.content] = 8
    article_partitions = ArticlePartition.query.filter_by(AID=aid).all()
    for part in article_partitions:
        p = Partition.query.get(part.PID)
        if p.name in keywordDict:
            keywordDict[Partition.query.get(part.PID).name] += 20
        else:
            keywordDict[Partition.query.get(part.PID).name] = 20
    for word, weight in keywordDict.items():
        ka = KeywordArticle(word, weight, aid)
        print(str(word)+","+str(weight)+","+str(aid))
        db.session.add(ka)
    db.session.commit()


# 搜索文章：根据输入的内容决定输出的顺序，先按照关键词权重排序，然后再加上浏览量，如果没有，就按照浏览量输出20篇文章
def searchForArticles(ArticleKeyword, Article, search_content):
    searched = lcut_for_search(search_content)  # 把输入内容分词
    article_weight = {}
    for words in searched:  # 按照每一个被搜索的单词进行查找
        print(f"Searching:{words}")
        included = ArticleKeyword.query.filter_by(word=words).all()  # 找出全部包含这个关键词的文章
        for aids in included:
            print("aid"+str(aids.AID))
            if aids.AID not in article_weight:  # 目前不包含
                article_weight[aids.AID] = aids.weight
            else:
                article_weight[aids.AID] += aids.weight
    if len(article_weight) != 0:
        print("Found!")
        aids = []
        for a, w in article_weight.items():
            article = Article.query.get(a)
            article_weight[a] += article.NumRead
            print(article_weight)
            weight_list = (list(article_weight.items()))
            weight_list.sort(key=lambda i: i[1], reverse=True)
            for item in weight_list:
                aids.append(item[0])
            print(aids)
            return aids
    else:
        print("Not Found")
        articles = Article.query.order_by(Article.NumRead.desc()).limit(20)
        aids_list = []
        for article in articles:
            aids_list.append(article.AID)
        return aids_list


# 根据aid列表输出搜索结果
def returnSearchResultByAID(Article, Like, Comment, User, aids):
    WriterNames = []
    Likes = []
    NumComments = []
    WriterIDs = []
    Titles = []
    AIDs = []
    Times = []
    for aid in aids:
        article = Article.query.get(aid)
        writer = User.query.get(article.UID)
        AIDs.append(aid)
        Times.append(article.Time)
        Titles.append(article.Title)
        WriterIDs.append(writer.UID)
        WriterNames.append(writer.name)
        Likes.append(len(Like.query.filter_by(AID=aid).all()))
        NumComments.append(len(Comment.query.filter_by(AID=aid).all()))
    result = {
        "WriterIDs": WriterIDs,
        "WriterNames": WriterNames,
        "Titles": Titles,
        "AIDs": AIDs,
        "NumComments": NumComments,
        "Likes": Likes,
        "Times": Times
    }
    return result


# 根据输入的字符串进行全文匹配的搜索
def searchForAll(Article, ArticleKeyword, Likes, Comment, User, InputString):
    aids = searchForArticles(ArticleKeyword, Article, InputString)
    return returnSearchResultByAID(Article, Likes, Comment, User, aids)


# 搜索文章：根据输入的内容，用标签搜索，找到AID集合
def searchForArticlesByTag(Label, Article, search_content):
    word_list = lcut_for_search(search_content)
    article_weight = {}
    for word in word_list:  # 找出全部的可能的标签记录
        records = Label.query.filter_by(content=word)
        for record in records:
            if record.AID in article_weight:
                article_weight[record.AID] += 1
            else:
                article_weight[record.AID] = 1
    article_list = list(article_weight.items())
    article_list.sort(key=lambda a: a[1], reverse=True)  # 对其权重进行排序
    aid_list = []
    for item in article_list:
        aid_list.append(item[0])
    if len(article_list) != 0:  # 找到了就返回
        return aid_list
    else:  # 找不到就按照浏览量
        articles = Article.query.order_by(Article.NumRead.desc()).limit(20)
        aids_list = []
        for article in articles:
            aids_list.append(article.AID)
        return aids_list


# 按照标签查询
def searchByTag(Article, Label, Like, Comment, User, search_content):
    aids = searchForArticlesByTag(Label, Article, search_content)
    return returnSearchResultByAID(Article, Like, Comment, User, aids)


# 获取动态列表
# 先获得一个人的全部关注者
# 再找出这些被关注者的活动（发文，评论，点赞，收藏）
'''
{
     "UID": "操作人",
     "AID": "目标文章",
     "TargetTitle": "目标文章题目",
     "Time": "动态发生时间",
     "Username": "操作人名字",
     "Type": "Like/Write/Collect/Comment"
}
'''


def getMovement(Article, User, Comment, Like, Collect, FollowBlogger, uid):
    concerned = []  # 被此人关注所有人的UID
    subscribed = FollowBlogger.query.filter_by(FanUID=uid)  # 被此人关注的所有人
    movements = []
    for p in subscribed:
        concerned.append(p.BloggerUID)
    for userID in concerned:  # 把被关注人的动态按照被关注人排列
        article_record = Article.query.filter_by(UID=userID)  # 这个被关注人全部的文章发表记录
        for article in article_record.all():
            record = {
                "UID": userID,
                "AID": article.AID,
                "TargetTitle": article.Title,
                "Time": article.Time,
                "Username": User.query.get(userID).name,
                "Type": "Write"
            }
            movements.append(record)
        comment_record = Comment.query.filter_by(UID=userID)  # 这个被关注人全部的评论记录
        for comment in comment_record.all():
            record = {
                "UID": userID,
                "AID": comment.AID,
                "TargetTitle": Article.query.get(comment.AID).Title,
                "Time": comment.time,
                "Username": User.query.get(userID).name,
                "Type": "Comment"
            }
            movements.append(record)
        like_record = Like.query.filter_by(UID=userID)  # 这个被关注人的点赞记录
        for like in like_record.all():
            record = {
                "UID": like.UID,
                "AID": like.AID,
                "TargetTitle": Article.query.get(like.AID).Title,
                "Time": like.time,
                "Username": User.query.get(userID).name,
                "Type": "Like"
            }
            movements.append(record)
        collect_record = Collect.query.filter_by(UID=userID)  # 该用户全部的收藏记录
        for collect in collect_record.all():
            record = {
                "UID": userID,
                "AID": collect.AID,
                "TargetTitle": Article.query.get(collect.AID).Title,
                "Time": collect.Time,
                "Username": User.query.get(userID).name,
                "Type": "Collect"
            }
            movements.append(record)
    movements.sort(key=lambda m: m['Time'])
    movements.reverse()
    UIDs = []
    AIDs = []
    TargetTitles = []
    Times = []
    Usernames = []
    Types = []
    for movement in movements:
        UIDs.append(movement['UID'])
        AIDs.append(movement['AID'])
        TargetTitles.append(movement['TargetTitle'])
        Times.append(movement['Time'])
        Usernames.append(movement['Username'])
        Types.append(movement['Type'])
    result = {
        "UID": UIDs,
        "AID": AIDs,
        "TargetTitle": TargetTitles,
        "Time": Times,
        "Username": Usernames,
        "Type": Types
    }
    return result

'''
{
     "UID": "操作人",
     "AID": "目标文章",
     "TargetTitle": "目标文章题目",
     "Time": "动态发生时间",
     "Username": "操作人名字",
     "Type": "Like/Write/Collect/Comment"
}
'''