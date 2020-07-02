<template>
  <div class="home" style="width=100%">
    <div
      id="topline"
      style="height: 90px;width: 100%; position: fixed;
     top: 10px"
    >
      <div id="munuOfTopline" style="height: 90px;">
        <div class="df-header" id="navigator" style="width: 100%; height:70px">
          <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            background-color="#ffffff"
            text-color="#000000"
            active-text-color="#FF6600"
          >
            <div
              id="buttonOfTopline"
              style="float:left; padding-left:100px;padding-right:100px"
            >
              <h3>01 Cafe</h3>
            </div>
            <div
              id="searchOfTopline"
              style="float:left; height: 50px; padding-top:8px"
            >
              <el-input
                placeholder="请输入内容"
                v-model="search.Value"
                class="input-with-select"
                @change="changeEvent"
              >
                <el-button
                  slot="append"
                  icon="el-icon-search"
                  @click="Search(2)"
                >全局</el-button>
                <el-button
                  slot="append"
                  icon="el-icon-search"
                  @click="Search(1)"
                >分区</el-button>-
              </el-input>
            </div>
            <div style="float:left; margin-right:50px; margin-left:50px; padding-top:8px;" v-if="this.$store.state.isRegister">
              <el-button @click="toArticle(xiba,-1)" icon="el-icon-circle-plus-outline">创作</el-button>
            </div>
            <div  style="float :left;margin-right:0px; margin-top:8px;"  v-if="this.$store.state.isRegister">
              <el-button @click.native="toProfile"
                ><i class="el-icon-user-solid"></i>个人</el-button
              >
              <el-button  @click.native="toUserModify"
                ><i class="el-icon-s-tools"></i>修改</el-button
              >
              <el-button  @click.native="logout"
                ><i class="el-icon-s-release"></i>注销</el-button
              >
            </div>
              <el-menu-item style="float:right; " @click="toHome" >主页</el-menu-item>
              <el-menu-item  style="float:right" @click="toRegister" v-if="!this.$store.state.isRegister">注册</el-menu-item>
              <el-menu-item  style="float:right;" @click="toLogin" v-if="!this.$store.state.isRegister">登录</el-menu-item>
              <el-menu-item v-if="this.$store.state.isRegister" style="float:right; " @click="getDynamicData" >动态</el-menu-item>
          </el-menu>
        </div>
      </div>
    </div>
    <div
      id="leftOfMain"
      style="position:fixed; height:300px; margin-left:100px; margin-right:170px;"
    >
      <div class="df-register">
        <div class="main">
          <div class="form-wrapper">
            <el-form class="login-box" ref="form"  label-position="left" label-width="90px" :model="form">
              <h3 class="login-title">分区列表</h3>
              <el-col :span="12">
                <el-menu default-active="2" class="el-menu-vertical-demo">
                <div v-for="(item,i) in getpart" :key="i" >
                  <el-menu-item index=item.partition_pid  @click="PIDSummit(item.partition_pid)">
                    <img :src= "geturl(item.partition_icon_url)" width="25" height="25">
                    <span slot="title">{{item.partition_name}}</span>
                  </el-menu-item>
                </div>
                </el-menu>
              </el-col>
            </el-form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="this.$store.state.isCurrentBlog && this.isDynamic!=true" 
    style="height:auto; min-height:700px; margin-left:250px; margin-right:170px; margin-top:100px">
      <ArticleList :Articles11="this.localData"></ArticleList>
    </div>
    <div v-else-if="this.isDynamic!=true" style="height:auto; min-height:700px; margin-left:250px; margin-right:170px; margin-top:100px">
      <ArticleList :Articles11="this.localData"></ArticleList></div>
    <div v-if="this.isDynamic" style="height:auto; min-height:700px; margin-left:250px; margin-right:170px; margin-top:100px">
      <Dynamic :DynamicInfo="this.Movement"></Dynamic>
    </div>
    <div
      id="bottom"
      style="background-color:#F0F0F0;height:300px; margin-top:35px"
    >
      <div style="margin-left:500px">
        <table border="0" cellspacing="30px">
          <tr>
            <td>关于我们</td>
            <td>加入我们</td>
          </tr>
          <tr>
            <td>用户协议</td>
            <td>隐私政策</td>
          </tr>
          <tr>
            <td>网页反馈</td>
            <td>侵权申诉</td>
          </tr>
        </table>
      </div>
      <div style="">
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Navigator from "@/components/Navigator.vue";
import axios from "axios";
import ArticleList from "@/components/ArticleList.vue"
import Dynamic from "@/components/Dynamic.vue"
import QS from "qs";
export default {
  name: "Home",
  components: {
    Navigator,
    ArticleList,
    Dynamic
  },
  data() {
    return {
      isDynamic:false,
      localData: {
        Titles: [],
        Likes: [],
        NumComments:[],
        Times:[],
        WriterNames:[]
      },
      Movement:{
        UID: [],
        AID: [],
        Titles: [],
        Time :[],
        Username : [],
        Type : []
      },
      form: {
        UID: this.$store.state.userProfile.UID,
        Type:"Sector",//,"User"
        Value:-1
      },
      activeIndex: "1",
      search: {
        Type:"Tag",//,"All"
        Value:""
      },
      xiba: this.$store.state.userProfile.UID,
      getpart: []
    };
  },
  props: ['Article'],
  created() {
    this.getPartition();
    this.getLocalData(-1)
  },
  methods: {
    geturl(url){
      return "http://182.92.223.226"+url;
    },
    PIDSummit(_sectorID) {
      this.isDynamic=false;
      this.form.Value=_sectorID;
      this.form.UID=this.$store.state.userProfile.UID;
      this.$axios
        .post("/getArticle", QS.stringify(this.form))
        .then(response => {
          this.localData.Titles = response.data.Titles
          this.localData.Likes = response.data.Likes
          this.localData.NumComments = response.data.NumComments
          this.localData.Times = response.data.Times
          this.localData.WriterNames = response.data.WriterNames
          this.localData.WriterIDs=response.data.WriterIDs
          this.localData.AIDs=response.data.AIDs
          this.$store.commit('changeCurrentBlog',true);
        })
        .catch(error => {
          this.$message({
            message: "该页面出了点状况",
            type: "error",
            customClass: "c-msg",
            duration: 0,
            showClose: true,
            duration: 1000
          });
          Promise.reject(error);
        });
    },
    getPartition(){
      this.isDynamic=false;
      this.$axios
      .post("/getPartition", QS.stringify(this.form))
      .then(response => {
        this.getpart=response.data.partition_data;
        console.log(this.getpart);
      })
      .catch(error => {
        this.$message({
          message: "该页面出了点状况",
          type: "error",
          customClass: "c-msg",
          duration: 0,
          showClose: true,
          duration: 1000
        });
        Promise.reject(error);
      });
    },
    getLocalData(_sectorID) {
      this.isDynamic=false;
      this.form.UID=this.$store.state.userProfile.UID;
      this.form.Value=_sectorID;
      this.$axios
      .post('/getArticle',QS.stringify(this.form)).then(response => {
        this.localData.Titles = response.data.Titles
        this.localData.Likes = response.data.Likes
        this.localData.NumComments = response.data.NumComments
        this.localData.Times = response.data.Times
        this.localData.WriterNames = response.data.WriterNames
        this.localData.WriterIDs=response.data.WriterIDs
        this.localData.AIDs=response.data.AIDs
        console.log(this.localData)
      }).catch(error => {
        this.$message({
          message: '页面出了一点问题dgdf',
          type: 'error',
          customClass: 'c-msg',
          duration: 0,
          showClose: true,
          duration: 1000
        })
        Promise.reject(error)
      })
    },
    getDynamicData() {
      console.log(this.isDynamic);
      this.isDynamic=true;
      console.log(this.isDynamic);
      var movePara={
        UID:this.$store.state.userProfile.UID
      }
      this.$axios
      .post('/MovementList',QS.stringify(movePara)).then(response => {
        this.Movement.UID=response.data.UID
        this.Movement.AID=response.data.AID
        this.Movement.Titles = response.data.TargetTitle
        this.Movement.Time = response.data.Time
        this.Movement.Username = response.data.Username
        this.Movement.Type = response.data.Type
      }).catch(error => {
        this.$message({
          message: 'Dynamic页面出了一点问题',
          type: 'error',
          customClass: 'c-msg',
          duration: 0,
          showClose: true,
          duration: 1000
        })
        Promise.reject(error)
      })
    },
    logout(){
      this.$store.commit('changeUserState',false);
      this.$store.commit('changeUID','');
      return this.$message({
        message: "注销成功",
        type: "success",
        customClass: "c-msg",
        showClose: true,
        duration: 1000
      });
    },
    Search(_type){
      this.isDynamic=false;
        if(_type==1){
          this.search.Type="Tag";
        }
        if(_type==2){
          this.search.Type="All";
        }
        this.$axios
        .post("/Search", QS.stringify(this.search))
        .then(response => {
          this.localData.Titles = response.data.Titles
          this.localData.Likes = response.data.Likes
          this.localData.NumComments = response.data.NumComments
          this.localData.Times = response.data.Times
          this.localData.WriterNames = response.data.WriterNames
          this.localData.WriterIDs=response.data.WriterIDs
          this.localData.AIDs=response.data.AIDs
        })
        .catch(error => {
          this.$message({
            message: "该页面出了点状况",
            type: "error",
            customClass: "c-msg",
            duration: 0,
            showClose: true,
            duration: 1000
          });
          Promise.reject(error);
        });
    },
    changeToDynamic(){
      this.$store.commit('changeCurrentBlog',false);
    },
    changeToBlog(){
      this.$store.commit('changeCurrentBlog',true);
    },
    changeEvent() {
      this.$forceUpdate();
    },
    toHome() {
      this.getLocalData(-1);
      this.$router.push({ path: "/home" });
    },
    toRegister() {
      this.$router.push({ path: "/user/register" });
    },
    toLogin() {
      this.$router.push({ path: "/user/login" });
    },
    toProfile() {
      this.$router.push({ 
        path : "/user/profile",
        query: {
          UID : parseInt(this.$store.state.userProfile.UID ),
          Judge:1
        }
      });
    },
    toUserModify() {
      this.$router.push({ path: "/user/modify"});
    },
    toArticle(_Author_ID,_AID){
      this.$router.push({
        path:`/ArticleEditor/${_Author_ID}/${_AID}`,
        params:{
          Author_ID:_Author_ID,
          AID:_AID,
        }
      })
    },
  }
};
</script>

<style scoped lang="stylus">
.each {
  width: 30%;
  border: 1px solid black;
  margin: 5px;
  cursor: pointer;
}
.df-register
  height 100%
  .main-wrapper
    width 100%
    .alert
      margin-top 10px
      text-align center
    .main
      fj(center,center)
      .form-wrapper
        width 33.3%
        .form
          .publish
            width 100%
      .register-dialog
        .about-user,.copyright
          &>span
            display inline-block
            line-height 1em
            color Silver
.df-header
  font-weight bold
  background-color White !important
  .el-menu-item
    font-size 1em
    transition all .2s ease
    &:hover
      border-bottom 3px solid Blue
      bc(White !important,Blue)
      transform translateY(-10px)
    &.is-active
      border-bottom-left-radius 80%
      border-bottom-right-radius 10%
      border-bottom 3px solid Blue
      color Blue
  .searchbar-wrapper
    padding-top 15px
    .searchbar-act
      width 100% !important
      transition all .5s
      &+button
        position absolute
        zoom .001
        transform scale(0)
        transition all .5s
    .searchbar
      width 70%
      &>i
        &:focus,&:hover
          color Blue !important
    .create
      margin-left 10px
      color Silver
      text-align center
      &:hover, &:focus
        bdco(Blue,Blue)
  .actions
    fj()
    .menu
      border 0
      .el-submenu__title
        &:hover
          background-color White
        .avatar
          wh(40px,40px)
          margin-top 10px
          border-radius 40px
        &>i
          display none
      .el-menu-item
        border 0
        font(.8em,Light-Silver)
        text-align center
        &>i
          padding-right 5px
          color Light-Blue
          &:hover
            color Blue
        &:hover
          border-bottom 0
          transform translateY(-3px)
    .inbox
      z-index 999
      .el-badge
        &>sup
          top 20px
          background-color Blue
        &>i
          font-size 1.8em
    .is-active
      .el-submenu__title
        border-bottom-left-radius 70%
        border-bottom-right-radius 70%
        border-bottom 3px solid Blue
        color Blue
        transition all .2s
      i
        color Blue
.login-box {
  label-width: 50px ;
  size: mini;
  border: 1px 
  width: 120px;
  height: 450px;
  margin: 0px auto;
  padding: 10px 25px 10px 25px;
  border-radius: 5px;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
}
.el-menu-vertical-demo{
  height: 40px;
  width: 120px;
}
.df-subPoem
  fj()
  margin 20px 0
  border-bottom 1px solid Extra-Light-Grey
  &:hover
    transform translateY(-3px)
    background-color 	#D8D8D8
  .main-left
    margin-right 20px
    .avatar
      wh(120px,120px)
      border-radius 10px
      box-shadow 0 1px 1px rgba(0,0,0,.2)
  .main-right
    position relative
    margin 0 !important
    width 100%
    .header
      .title
        display inline-block
        font(1.5em,mgreen(.8))
        text-decoration none
        transition all .3s
        &:hover
          transform translateY(-1px)
      .favor,.trash
        float right
    .info
      margin 0px 0
      &>span:first-child
        &>a
          text-decoration none
          color Green
      span
       margin-right 5px
       font(.8em,Silver)
       &>i
         margin-right 5px
    .body
      margin 10px 0 20px 0
      font(.8em,Silver)
      .content
        max-height 120px
        overflow hidden
        padding-bottom 20px
        word-break break-all
        line-height 2em
        cursor pointer
        .ellipsis
          color Green
        *
          display inline-block
          margin 0
     .footer
      fj(space-between)
      position absolute
      bottom 5px
      left 0
      width 100%
      .feedback
        float right
        margin-bottom 5px
        &>a
          margin-left 10px
          font(.7em,Silver)
          text-decoration none
          transition all .2s
          &:hover,&:focus
            color Green
            cursor pointer
          &>i
            margin-right 5px

Green = #42b983
Light-Green = #87d86b
White = #FFF
Dark-White = #F9FAFC
Red = #FF7352
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

bc(bgC=Green,c=Write)
  color c
  background-color bgC

bdco(bdc=Green,c=Green)
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
  color Green
  &::before
    position absolute
    top 50%
    left 0
    wh(w,1px)
    background-color Light-Green
    content ''
  &::after
    position absolute
    top 50%
    right 0
    wh(w,1px)
    background-color Light-Green
    content ''

mgreen(o=1)
  rgba(66,185,131,o)


/* 标签动画 */
@keyframes skTag
  33%
    margin-right 0 10px
    transform rotateY(90deg)
  50%
    border 0
    border-radius 50%
    font-size 1.5em
    color Green
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
</style>
