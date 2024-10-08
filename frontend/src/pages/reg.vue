<template>
  <el-row class="login-container">
    <el-col :lg="16" :md="12" class="left">
      <div>
        <div>欢迎光临</div>
        <div>此站点是《vue3 + vite实战商城后台开发》视频课程的演示地址</div>
      </div>
    </el-col>
    <el-col :lg="8" :md="12" class="right">
      <h2 class="title">欢迎新用户</h2>
      <div class="title-text">
        <span class="line"></span>
        <span>注册</span>
        <span class="line"></span>
      </div>
      <el-form
        ref="ruleFormRef"
        :rules="rules"
        :model="ruleForm"
        class="w-[250px]"
        @keyup.enter="onSubmit()">
        <el-form-item prop="username">
          <el-input v-model="ruleForm.username" placeholder="请输入用户名">
            <template #prefix>
              <el-icon><user /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="pass">
          <el-input
            type="password"
            v-model="ruleForm.pass"
            placeholder="请输入密码"
            show-password>
            <template #prefix>
              <el-icon><lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="checkPass">
          <el-input
            type="password"
            v-model="ruleForm.checkPass"
            placeholder="请输入密码again"
            show-password>
            <template #prefix>
              <el-icon><lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            round
            color="#626aef"
            class="w-[250px]"
            type="primary"
            @click="submitForm(ruleFormRef)"
            >注 册</el-button
          >
        </el-form-item>
      </el-form>
      <div class="container">
        <el-button :type="info" text class="reg" @click="gotoLogin"
          >返回登录</el-button
        >
      </div>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref, reactive } from 'vue';

import { useRouter } from 'vue-router';
import { reg } from '~/api/manager';

const router = useRouter();

// do not use same name with ref
const ruleForm = reactive({
  username: '',
  pass: '',
  checkPass: '',
});
const gotoLogin = () => {
  router.push('/login');
};

const ruleFormRef = ref(null);
function validatePass(rule, value, callback) {
  if (value === '') {
    callback(new Error('Please input the password'));
  } else {
    if (ruleForm.checkPass !== '') {
      if (!ruleFormRef.value) return;
      ruleFormRef.value.validateField('checkPass');
    }
    callback();
  }
}

function validatePass2(rule, value, callback) {
  if (value === '') {
    callback(new Error('Please input the password again'));
  } else if (value !== ruleForm.pass) {
    callback(new Error("Two inputs don't match!"));
  } else {
    callback();
  }
}
const rules = {
  username: [
    {
      required: true,
      message: '用户名不能为空',
      trigger: 'blur',
    },
    {
      min: 3,
      max: 8,
      message: 'Length should be 3 to 8',
      trigger: 'blur',
    },
  ],
  pass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
};

function submitForm(formEl) {
  if (!formEl) return;
  formEl.validate(function (valid) {
    if (valid) {
      console.log('submit!');
      reg(form.username, form.pass)
        .then((res) => {
          console.log(res.data.data);

          // 提示成功
          ElNotification({
            title: 'Success',
            message: '注册成功',
            type: 'success',
            duration: 3000,
          });

          // 跳转到
          router.push('/login');
        })
        .catch((err) => {
          ElNotification({
            title: 'Error',
            message: err.response.data.msg || '请求失败',
            type: 'error',
            duration: 3000,
          });
        });
    } else {
      console.log('error submit!');
    }
  });
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background-color: #4f46e5;
}

.login-container .left,
.login-container .right {
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-container .right {
  background-color: #f9fafb;
  display: flex;
  flex-direction: column;
}

.left > div > div:first-child {
  font-weight: bold;
  font-size: 3rem;
  color: #f9fafb;
  margin-bottom: 1rem;
}

.left > div > div:last-child {
  color: #d1d5db;
  font-size: 0.875rem;
}

.right .title {
  font-weight: bold;
  font-size: 1.875rem;
  color: #4b5563;
}

.title-text {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1.25rem 0;
  color: #d1d5db;
  gap: 0.5rem;
}

.right .line {
  height: 1px;
  width: 4rem;
  background-color: #d1d5db;
}
.container {
  margin-top: 0;
  margin-bottom: 0;
  position: relative; /* 设置相对定位，作为子元素绝对定位的参考点 */
  width: 260px; /* 容器的宽度 */
  height: 25px; /* 容器的高度 */
  /* border: 1px solid #000; 边框，以便看到容器的范围 */
}

.reg {
  position: absolute; /* 绝对定位 */
  top: 0; /* 距离容器顶部0距离 */
  left: 0; /* 距离容器左边0距离 */
  color: #b3b3bd;
}
</style>
