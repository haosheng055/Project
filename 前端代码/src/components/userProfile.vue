<template lang="html">
<div>
  <div
      id="topline"
      style="height: 90px;width: 100%; position: fixed;
     top: 10px"
    >
      <Navigator />
  </div>
  <div class="df-profile">
    <div class="header">
      <div class="mid">
        <div>
          <h1 class="name">{{ this.userProfile1.nickname }}</h1>
        </div>
        <div class="info">
          <div class="box" @click="works">
            <span>文章</span>
            <span>{{ this.userProfile1.likeNum }}</span>
          </div>
          <div class="box" @click="followers">
            <span>关注</span>
            <span>{{ this.userProfile1.follow }}</span>
          </div>
          <div class="box" @click="followings">
            <span>粉丝</span>
            <span>{{ this.userProfile1.fans }}</span>
          </div>
          <!--<el-button slot="append" icon="el-icon-upload2"  v-if="isOwns">上传资源</el-button>-->
        </div>
      </div>
    </div>
    <div class="body" style="border:1px solid">
      <dot></dot>
      <div id="leftOfBody" style="float:left; border:1px solid; width:60%; height:auto; min-height:500px; ">
        <ArticleList :Articles11="this.userArticles"></ArticleList>
      </div>
      <div id="rightOfBody" style="float:right; margin-left:200px;  border:1px solid; ">
        <resourceboard :tar_uid="parseInt(this.$route.query.UID)" :cur_uid="this.$store.state.userProfile.UID"></resourceboard>
      </div>
    </div>
  </div>
</div>
</template>

<script>
//import api from "@/api";
import Dot from "@/components/dot"
import resourceboard from "@/components/resourceboard.vue"
import ArticleList from "@/components/ArticleList.vue"
import QS from "qs"
import Navigator from "@/components/Navigator.vue"
export default {
  name: "userProfile",
  components: {
    Dot,
    resourceboard,
    ArticleList,
    Navigator
  },
  data() {
    return {
      placeholder: {
        nickname: "行不更名坐不改姓",
        birthday: "生日格式：1996-07-21",
        signature: "私人语录即一句话显逼格，最长为140个字符",
        poet: "想被推荐的博文类型"
      },
      userArticles: {
          Titles: [],
          Likes: [],
          NumComments:[],
          Times:[],
          WriterNames:[],
          AID:[],
          WriterIDs:[]
        },
        // 个人信息 or 用户信息
      userProfile1:{
          nickname: '',
          likeNum:0,//点赞数
          follow:0,//关注数
          fans:0,//被关注数
      },
      dialogVisible: false,
      isOwns: true,
      rules: {
        nickname: [
          {
            min: 2,
            max: 20,
            message: "昵称必须介于2-20个字符之间。",
            trigger: "blur"
          },
          {
            type: "string",
            pattern: /^[\u4E00-\u9FFFa-zA-Z0-9_-]{2,20}$/,
            message: "格式不正确。",
            trigger: "blur"
          }
        ],
      },
    };
  },
  mounted() {
    // 检查是否是个人信息页面
    console.log(this.$route.query.UID);
    var ret=this.checkoutOwns();
    if(ret===true){
      this.getUserInfomation(this.$store.state.userProfile.UID)
      this.getUserArticles(this.$store.state.userProfile.UID)
    }
    else{
      this.getUserInfomation(this.$route.query.UID)
      this.getUserArticles(this.$route.query.UID);
    }
  },
  methods: {
    // 检查该页面属于个人信息页面 or 用户信息页面
    checkoutOwns() {
      if(this.$route.query.UID==this.$store.state.userProfile.UID){
        this.isOwns = true;
        return true;
      }
      else{
        this.isOwns=false;
        return false;
      }
    },
    getUserInfomation(_UID) {
      var toSubmit={
        UID:_UID
      };
      this.$axios
      .post('/personInfo',QS.stringify(toSubmit)).then(response => {
        this.userProfile1.nickname = response.data.Username
        this.userProfile1.likeNum = response.data.NumArticle
        this.userProfile1.follow = response.data.NumSubscribed
        this.userProfile1.fans = response.data.NumFans
      }).catch(error => {
        this.$message({
          message: 'getUserInfo页面出了一点问题',
          type: 'error',
          customClass: 'c-msg',
          duration: 0,
          showClose: true
        })
        Promise.reject(error)
      })
    },
    getUserArticles(_UID) {
      var from={
        UID: this.$store.state.userProfile.UID,
        Type:"User",
        Value:this.$route.query.UID
      }
      this.$axios
      .post('/getArticle',QS.stringify(from)).then(response => {
        this.userArticles.AIDs=response.data.AIDs
        this.userArticles.WriterIDs=response.data.WriterIDs
        this.userArticles.Titles = response.data.Titles
        this.userArticles.Likes = response.data.Likes
        this.userArticles.NumComments = response.data.NumComments
        this.userArticles.Times = response.data.Times
        this.userArticles.WriterNames = response.data.WriterNames
      }).catch(error => {
        this.$message({
          message: 'getArticle页面出了一点问题',
          type: 'error',
          customClass: 'c-msg',
          duration: 0,
          showClose: true
        })
        Promise.reject(error)
      })
    },
    works() {
      this.$router.push(`/user/${this.userProfile.name}/works`);
    },
    followings() {
      this.$router.push(`/user/${this.userProfile.name}/followings`);
    },
    followers() {
      this.$router.push(`/user/${this.userProfile.name}/followers`);
    },
    dateFormatter(date) {
      return new Date(date).toLocaleDateString();
    },
    toggleProfileDialog() {
      this.dialogVisible = !this.dialogVisible;
    },
    showPlaceholder(e) {
      e.target.placeholder = this.lastPlaceholder;
    },
    hidePlaceholder(e) {
      this.lastPlaceholder = e.target.placeholder;
      e.target.placeholder = "";
    }
  }
};
</script>
<style lang="stylus" scoped>
Blue = #42b983
Light-Blue = #87d86b
White = #FFF
Dark-White = #F9FAFC
Green = #FF7352
Blue = #64c0ff
Orange = #F7BA2A
Light-Orange = #ffc741
Silver = #8492A6
Light-Silver = #99A9BF
Extra-Light-Silver = #C0CCDA
Grey = #D3DCE6
Light-Grey = #E5E9F2
Extra-Light-Grey = #EFF2F7
Black = #1F2D3D
Light-Black = #324057
Extra-Light-Black = #475669

fj(x=flex-start,y=stretch)
  display flex
  justify-content x
  align-items y

wh(w,h)
  width w
  height h

bc(bgC=Blue,c=Write)
  color c
  background-color bgC

bdco(bdc=Blue,c=Blue)
  border-color bdc
  color c

font(s,c)
  font-size s
  color c


txtline(w=40%)
  position relative
  font-size .8em
  letter-spacing 1px
  text-align center
  color Blue
  &::before
    position absolute
    top 50%
    left 0
    wh(w,1px)
    background-color Light-Blue
    content ''
  &::after
    position absolute
    top 50%
    right 0
    wh(w,1px)
    background-color Light-Blue
    content ''

mBlue(o=1)
  rgba(66,185,131,o)

@keyframes skTag
  33%
    margin-right 0 10px
    transform rotateY(90deg)
  50%
    border 0
    border-radius 50%
    font-size 1.5em
    color Blue
    transform rotateZ(90deg)
  100%
    zoom 1.2
/* 收藏、写赏析、点赞、分享动画 */
@keyframes skAct
  33%
    zoom 1.1
    margin-right 0 10px
    opacity .899
    transform rotateZ(-80deg)
  50%
    zoom 1.2
    border 0
    opacity .5
    transform rotateZ(-120deg)
  77%
    zoom 1.3
    opacity 0
/* 点击评论框显示按钮 */
@keyframes showBtn
  0%
    border-radius 50%
    zoom .001
    transform scale(0)
  100%
    border-radius 4px
    zoom 1
    transform scale(1)
/* 评论文本框无内容时动画 */
@keyframes skTxta
  0%
    opacity .7
    transform scale(1)
  33%
    padding-left 1px
    opacity .765
    transform scale(.999)
  50%
    padding-top 1px
    opacity .8
    transform scale(.997)
  80%
    opacity .765
    transform scale(.998)
  100%
    opacity .7
    transform scale(1)
/* 私信小圆球动画 */
@keyframes drpGlobe
  33%
    transform rotateZ(90deg)
    opacity .9
  50%
    top 50%
    font-size 1.5em
    opacity .7
    transform rotateY(90deg)
  77%
    opacity .9
    transform rotateX(90deg)
  100%
    opacity 1
/* 无内容动画 */
@keyframes showHint
  0%
    zoom 1
    opacity .999
    transform skew(20deg)
  33%
    transform translateX(20px)
  50%
    zoom .999
    color Dark-White
    opacity .8
    transform translateX(10px)
  77%
    transform rotate(4deg)
  80%
    color Light-Silver
    transform scale(.9)
  100%
    zoom 1
    opacity .1
    transform skew(30deg)
/* intro icon动画 */
@keyframes tfIcon
  50%
    font-size 1em
    opacity 0

.clearfix::after
  display block
  clear both
  visibility hidden
  height 0
  overflow hidden
  content '.'
.clearfix
  zoom 1

.line
  clear both
  height 1px
  background-color Blue

.light-line
  clear both
  height 1px
  background-color Light-Blue

.text-line-40
  txtline(40%)

.text-line-35
  txtline(35%)

.tdu
  color Blue
  text-decoration none
  &:hover
    text-decoration underline

.btn-default
  color Silver !important
  text-align center
  &:hover, &:focus
    bdco(Blue !important, Blue !important)

.btn-act
  bdco(mBlue(.8) !important, mBlue(.8) !important,)
  &:focus, &:hover
    border-color mBlue(.8) !important
  i
    color mBlue(.8)

.btn-can
  bc(White !important,Light-Silver !important)
  transition all .15s
  &:hover,&:focus
    bdco(Light-Silver !important,Silver !important)

.btn-pub
  bc(Blue !important, White !important)
  border-color Blue !important
  transition all .2s
  &:hover,&:focus
    bc(Orange !important, White !important)
    border-color Orange !important

/* ------------    ~~~   -------------- /*

/* 表单 */
.c-form
  input, textarea
    color Blue
    &:hover, &:focus
      border-color Blue
    &::placeholder
      font-size .8em
  button
    font-size .8em
    color Silver
    transition all .2s
    &:hover,&:focus
      border-color Blue
      color Blue
  .is-error input, .is-error textarea
    border-color Green !important
  .el-form-item__error
    color Green
  .el-form-item__label
    &::before
      content '' !important
  .is-checked
    span
      border-color Blue !important
      background-color Blue !important
      transition all .3s ease
  .el-radio__inner:hover,.el-radio__inner:focus
    border-color Blue !important
  .el-checkbox__inner:hover,.el-checkbox__inner:focus,.el-checkbox__inner:visited
    border-color Blue !important
  .is-focus
    span
      border-color Blue !important
      &:hover,&:focus
        border-color Blue !important

/* quill 编辑器 */
.c-quill
  .ql-editor
    min-height 300px
    border 1px solid Extra-Light-Silver
    border-radius 5px
    color Blue

/* 消息提示 */
.c-msg
  .el-message__closeBtn:hover
    color Blue

.c-confirm
  .el-message-box__header
    i
      &:hover,&:focus
        color Blue

/* el-autocomplete 下拉框 */
.c-popper
  .hover
    color Dark-White
    background-color Blue !important
  .selected
    background-color Blue !important
  li:hover
    color Dark-White
    background-color Blue !important
  li:focus
    background-color Blue !important

/* 私信对话框 */
.c-reply
  .el-dialog__header
    &>span
      color Silver
    i
      &:hover,&:focus
        color Blue
  .header
    color Silver
    margin-bottom 10px
    .receiver
      font-weight bold
      letter-spacing 2px
      color Blue
.c-tags
  display inline-block
  &>i
    color mBlue(.8)
  .tag
    margin-right 5px
    border-color Extra-Light-Silver
    bc(inherit,Silver)
    cursor pointer
    &:hover
      animation skTag 1s cubic-bezier(1,.8,.5,1)


.df-profile
  .header
    margin-right 100px
    margin-left 100px
    fj(space-around)
    margin-top 20px
    padding-top 20px
    background-color Extra-Light-Grey
    .mid
      height 100px
      height auto
      min-height 100px
      width 100%
      text-align center
      letter-spacing 3px
      color Blue
      .name
        &::before
          margin-right 20px
          content '\5B'
        &::after
          margin-left 20px
          content '\5D'
      .info
        margin-top 5px
        margin-bottom 10px
        .box
          display inline-block
          margin-left 20px
          transition color .1s
          &:hover
            color Green
            cursor pointer
          span
            display block
            font-size 1.3em
          & span:nth-child(1)
            margin-bottom 10px
            font-weight bold
          & span:nth-child(2)
            font-size 1.1em
        button
          margin-top 10px
    .right
      width 16.6%
      &:hover
        cursor pointer
  .body
    margin-right 100px
    margin-left 100px
    z-index 1
    fj(left ,left )
    padding 20px 0
  .profile-dialog
    .form-wrapper
      fj(center)
      .form
        width 75%
        .publish
          width 100%
</style>
