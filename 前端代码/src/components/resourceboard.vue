<template>

    <div id="list">
      <div
        class="each"
        v-for="(item,index) in this.resources"
        :key="index"
      >
        <p :class="fileName">文件名：{{ item.file_name }}</p><br>
        <a :href="item.getUrl" :class="link">下载</a>
        <div v-if="judgeMode()" :class="link" @click="deleteFile(index)">删除</div>
        <hr>
      </div>
      <div style="float:left; margin-top:20px">
        <form action="" method="POST" enctype="multipart/form-data" @submit.prevent="mysubmit" v-if="judgeMode()" class="form">
          <input type="file" :value=this.file ref="fileInput">
          <input type="submit">
        </form>
      </div>
    </div>
 
</template>

<script>
// @ is an alias to /src
import Navigator from "@/components/Navigator.vue";
import QS from "qs";
export default {
  name: "resourceboard",
  components: {
    Navigator
  },
  props:{
    cur_uid: Number,   //当前登录用户的UID
    tar_uid: Number,   //资源拥有者的UID
    //如果cur_uid!=tar_uid那就只能查看，不能新增和删除
  },
  data() {
    return {
      isEditable:this.cur_uid+this.tar_uid,
      file: null,
      resources:[
      ],
      rids:[

      ]
    };
  },
  mounted: function() {
    let data = new FormData();
    data.append("uid",this.tar_uid);
    this.$axios.post("/resourceList", data,{
      })
      .then((response) => 
      {
          //console.log("Mounted!");
          let resultList = response.data.list;
          //console.log(resultList);
          //console.log(resultList[0]);
          let i = 0;
          let len = resultList.length;
          console.log("mounted!");
          for(i=0;i<len;i++){
            this.resources.push({file_name:resultList[i].fileName,getUrl:resultList[i].url,deleteUrl:resultList[i].deleteUrl});
            //console.log(this.resources[i].deleteUrl);
            this.rids.push(resultList[i].RID);
          }
          //console.log(this.resources[0]);
      })
      .catch(error => {
          // 请求失败
          console.log(error);
      })
    },
  methods: {
    judgeMode(){
      console.log(this.isEditable);
      console.log("cur_id "+this.cur_uid);
      console.log("tar_id "+this.tar_uid);
      return this.cur_uid==this.tar_uid;
    },
    mysubmit(){
      const data = new FormData();
      data.append("fileInput",this.$refs.fileInput.files[0]);
      data.append("uid",this.tar_uid);
      console.log(this.tar_uid==this.cur_uid);
      this.$axios.post("/resourceCenter", data,{
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((response) => 
      {
          console.log("entered");
          //this.resources=response.data.list;
          let a=response.data.fileName;
          let b=response.data.url;
          let c=response.data.deleteUrl;
          this.resources.push({file_name:a,getUrl:b,deleteUrl:c});
          let rid = response.data.RID;
          this.rids.push(rid);
      })
      .catch(error => {
          // 请求失败
          console.log(error);
      })
    },
    deleteFile(index){
      let data = new FormData();
      data.append("RID",this.rids[index]);
      this.$axios.post("/deleteResource", data,{
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((response) => 
      {
          this.resources.splice(index,1);
          this.rids.splice(index,1);
      })
      .catch(error => {
          // 请求失败
          console.log(error);
      })
    }
  }
}
</script>

<style scoped>
.each {
  margin: 5px;
  cursor: pointer;
}
.fileName{
  text-align: center;
  float: right;
}
.link{
  text-align: center;
  float: right;
}
.form{
  float:right;
}
</style>