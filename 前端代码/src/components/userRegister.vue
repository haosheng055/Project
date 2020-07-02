<template lang="html">
  <div class="df-register">
    <div class="main-wrapper">
      <div class="alert">
        <el-alert
          title="注册成功)"
          type="success"
          v-show="alertVisible"
          v-if="isSuccess"
        ></el-alert>
        <el-alert
          title="注册失败"
          type="error"
          v-show="alertVisible"
          v-else
        ></el-alert>
      </div>
      <div class="main">
        <div class="form-wrapper">
          <el-form class="login-box" ref="form" :rules="rules" :model="form">
            <h3 class="login-title">欢迎注册</h3>
            <!--<el-form-item label="用户名" prop="name">
              <el-input
                placeholder="您的昵称"
                v-model="form.name"
                @blur="showPlaceholder"
                @focus="hidePlaceholder"
              ></el-input>
            </el-form-item> -->
            <el-form-item label="邮箱" prop="email">
              <el-input
                v-model="form.email"
                placeholder="建议使用邮箱"
                @blur="showPlaceholder"
                @focus="hidePlaceholder"
                :validate-event="false"
              ></el-input>
            </el-form-item>
            <el-form-item label="手机号" prop="mobile">
              <el-input
                v-model="form.mobile"
                placeholder="建议使用手机号"
                @blur="showPlaceholder"
                @focus="hidePlaceholder"
                :validate-event="false"
              ></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                placeholder="密码至少6位"
                type="password"
                v-model="form.password"
                @blur="showPlaceholder"
                @focus="hidePlaceholder"
                :validate-event="false"
              ></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="password_confirmation">
              <el-input
                placeholder="请再次输入您的密码"
                type="password"
                v-model="form.password_confirmation"
                @focus="hidePlaceholder"
                @blur="showPlaceholder"
                :validate-event="false"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                :loading="isLoading"
                :disabled="isRegistered"
                @click="submitForm"
                >立即注册
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import api from "@/api";
import QS from "qs";
export default {
  name: "userRegister",
  data() {
    return {
      form: {
        // 用户注册信息
        //name: "haoyu",
        email: "",
        mobile: "",
        password: "",
        password_confirmation: "",
        protocol: true,
      },
      rules: {
        // 表单验证规则
        email: [
          {
            //required: true,
            message: "此处不能为空。",
            trigger: "blur"
          },
          {
            max: 50,
            message: "此处不能大于50个字符。",
            trigger: "blur"
          },
          {
            type: "string",
            pattern: /(^(\w-*\.*)+@(\w-?)+(\.\w{2,})+)|(1\d{10})$/,
            message: "格式不正确。",
            trigger: "blur"
          },
          {
            validator: this.validateEmail,
            trigger: "blur"
          }
        ],
        mobile: [
          {
            //required: false,
            message: "手机号码不能为空。",
            trigger: "blur"
          },
          {
            len: 11,
            message: "手机号码必须是11个字符。",
            trigger: "blur"
          },
          {
            type: "string",
            pattern: /^1\d{10}$/,
            message: "格式不正确。",
            trigger: "blur"
          },
          {
            validator: this.validateMobile,
            trigger: "blur"
          }
        ],
        password: [
          {
            required: true,
            message: "密码不能为空。",
            trigger: "blur"
          },
          {
            min: 6,
            max: 20,
            message: "密码必须介于6-20个字符之间。",
            trigger: "blur"
          },
          {
            type: "string",
            pattern: /^[a-zA-Z0-9_-]{6,20}$/,
            message: "格式不正确。",
            trigger: "blur"
          }
        ],
        password_confirmation: [
          {
            validator: this.validatePassword,
            trigger: "blur"
          }
        ]
      },
      UID: "",
      name:"",
      dialogVisible: false, // 协议对话框可视度
      alertVisible: false, // 警告框可视度
      emailVisible: true, // email输入框可视度
      lastPlaceholder: "",
      isLoading: false, //  注册按钮是否正在加载
      isRegistered: false, // 是否已注册
      isSuccess: null, // 是否注册成功
      info:null
    };
  },
  methods: {
    validateEmail(r, v, cb) {
      this.$axios
        .post("/checkemail", QS.stringify(this.form))
        .then(response => {
          response.data.email ? cb(new Error("邮箱可能已经存在。")) : cb();
        })
        .catch(error => {
          this.$message({
            message: "该页面出了点状况11",
            type: "error",
            customClass: "c-msg",
            duration: 0,
            showClose: true
          });
          Promise.reject(error);
        });
    },
    validateMobile(r, v, cb) {
      this.$axios
        .post("/checkmobile", QS.stringify(this.form))
        .then(response => {
          response.data.mobile ? cb(new Error("手机号可能已经存在。")) : cb();
        })
        .catch(error => {
          this.$message({
            message: "",
            type: "error",
            customClass: "c-msg",
            duration: 0,
            showClose: true
          });
          Promise.reject(error);
        });
    },
    validatePassword(rule, value, cb) { 
      if (value === "") {
        cb(new Error("请再次输入密码。"));
      } else if(value !== this.form.password) {
        cb(new Error("两次输入密码不一致。"));
      } else cb();
    },
    // 提交表单
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          // 指定请求为正式提交表单
          this.form.is_submit = true;
          this.isLoading = true;
          this.$axios
            .post("/register", QS.stringify(this.form))
            .then(response => {
              this.isLoading = false;
              if (response.data.registered) {
                // 注册成功
                this.isSuccess = true;
                this.isRegistered = true;
                this.$store.commit('changeUserState',true);
                this.$store.commit('changeUID',response.data.uid);
                this.$store.commit('changeUserName',response.data.username);
                this.$router.replace("/");
                this.$message({
                    message: response.data.uid,
                    type: "success",
                    customClass: "c-msg",
                    showClose: true
                  }); 
              } else {
                // 注册失败
                this.isSuccess = false;
                  this.$message({
                    message: response.data.error,
                    type: "error",
                    customClass: "c-msg",
                    showClose: true
                  }); 
              }
              this.alertVisible = true;
            })
            .catch(error => {
              this.isLoading = false;
              this.$message({
                message: "该页面出了点状况44",
                type: "error",
                customClass: "c-msg",
                duration: 0,
                showClose: true
              });
              Promise.reject(error);
            });
        }
        return false;
      });
    },
    showDialog() {
      this.dialogVisible = !this.dialogVisible;
    },
    toggleEmail() {
      this.emailVisible = !this.emailVisible;
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
            line-height 2em
            color Silver
.login-box {
  border: 1px solid #dcdfe6;
  width: 350px;
  margin: 10px auto;
  padding: 35px 50px 15px 50px;
  border-radius: 5px;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  box-shadow: 0 0 25px #909399;
}
.login-title {
  text-align: center;
  margin: 0 auto 20px auto;
  color: #303133;
}
</style>
