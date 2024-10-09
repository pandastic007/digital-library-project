<template>
  <el-row class="login-container">
    <el-col :lg="16" :md="12" class="left">
      <div>
        <div>欢迎光临</div>
        <div>此站点是xxxxxxxxxxx</div>
      </div>
    </el-col>
    <el-col :lg="8" :md="12" class="right">
      <h2 class="title">欢迎回来</h2>
      <div class="title-text">
        <span class="line"></span>
        <span>账号密码登录</span>
        <span class="line"></span>
      </div>
      <el-form
        ref="formRef"
        :rules="rules"
        :model="form"
        class="w-[250px]"
        @keyup.enter="onSubmit()">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名">
            <template #prefix>
              <el-icon><user /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            v-model="form.password"
            placeholder="请输入密码"
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
            @click="onSubmit"
            >登 录</el-button
          >
        </el-form-item>
      </el-form>
      <div class="container">
        <el-button :type="info" text class="reg" @click="gotoReg">
          没有账号？点击注册
        </el-button>
      </div>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '@/api/manager'; // Updated import statement
import { useCookies } from '@vueuse/integrations/useCookies';
import { useLibStore } from '@/store/lib'; // Updated import statement

const router = useRouter();

// do not use same name with ref
const form = reactive({
  username: '',
  password: '',
});

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
  password: [
    {
      required: true,
      message: '密码不能为空',
      trigger: 'blur',
    },
  ],
};
const gotoReg = () => {
  router.push('/reg');
};
const formRef = ref(null);

const onSubmit = () => {
  formRef.value.validate((valid) => {
    if (!valid) {
      return false;
    }
    login(form.username, form.password)
      .then((res) => {
        console.log(res.data.data);

        // 提示成功
        ElNotification({
          title: 'Success',
          message: '登录成功',
          type: 'success',
          duration: 3000,
        });

        const cookie = useCookies();
        cookie.set('admin-token', res.data.data.token);
        const libStore = useLibStore();
        libStore.save(1);
        // 跳转到后台首页
        router.push('/');
      })
      .catch((err) => {
        ElNotification({
          title: 'Error',
          message: err.response.data.msg || '请求失败',
          type: 'error',
          duration: 3000,
        });
      });
  });
};
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
  position: relative;
  width: 260px;
  height: 25px;
}

.reg {
  position: absolute;
  top: 0;
  left: 0;
  color: #b3b3bd;
}
</style>
