<template>
  <el-row class="login-container">
    <el-col :lg="16" :md="12" class="left">
      <div>
        <div>欢迎光临</div>
        <div>此站点是xxxxxxxxxxx</div>
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
        @keyup.enter="submitForm"
      >
        <el-form-item prop="email">
          <el-input v-model="ruleForm.email" placeholder="请输入邮箱">
            <template #prefix>
              <el-icon><user /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            v-model="ruleForm.password"
            placeholder="请输入密码"
            show-password
          >
            <template #prefix>
              <el-icon><lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input
            type="password"
            v-model="ruleForm.confirmPassword"
            placeholder="请再次输入密码"
            show-password
          >
            <template #prefix>
              <el-icon><lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="role">
          <el-radio-group v-model="ruleForm.role">
            <el-radio-button label="student">Student</el-radio-button>
            <el-radio-button label="teacher">Teacher</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button
            round
            color="#626aef"
            class="w-[250px]"
            type="primary"
            @click="submitForm"
          >
            注 册
          </el-button>
        </el-form-item>
      </el-form>
      <div class="container">
        <el-button :type="info" text class="reg" @click="gotoLogin">
          已有账号？点击登录
        </el-button>
      </div>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { db, auth } from '@/firebase'; // Import Firebase Firestore and Authentication
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { collection, query, where, getDocs, addDoc } from 'firebase/firestore';

const router = useRouter();

const ruleForm = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  role: '',
});

const rules = {
  email: [
    { required: true, message: '邮箱不能为空', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    {
      min: 8,
      message: '密码长度不能少于 8 位，并且包含大小写字母、数字和符号',
      trigger: 'blur',
    },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== ruleForm.password) {
          callback(new Error('两次输入的密码不一致'));
        } else {
          callback();
        }
      },
      trigger: 'blur',
    },
  ],
  role: [{ required: true, message: '请选择用户角色', trigger: 'change' }],
};

const ruleFormRef = ref(null);

const submitForm = async () => {
  ruleFormRef.value.validate(async (valid) => {
    if (!valid) return;

    try {
      // Check if email already exists
      const usersRef = collection(db, 'Users');
      const q = query(usersRef, where('email', '==', ruleForm.email));
      const querySnapshot = await getDocs(q);

      if (!querySnapshot.empty) {
        ElNotification({
          title: 'Error',
          message: '邮箱已存在，请更换其他邮箱',
          type: 'error',
          duration: 3000,
        });
        return;
      }

      // Register user with Firebase Auth
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        ruleForm.email,
        ruleForm.password
      );

      // Add user details to Firestore
      await addDoc(usersRef, {
        uid: userCredential.user.uid,
        email: ruleForm.email,
        role: ruleForm.role,
      });

      ElNotification({
        title: 'Success',
        message: '注册成功',
        type: 'success',
        duration: 3000,
      });

      // Redirect to login page after successful registration
      router.push('/login');
    } catch (error) {
      ElNotification({
        title: 'Error',
        message: error.message || '注册失败',
        type: 'error',
        duration: 3000,
      });
    }
  });
};

const gotoLogin = () => {
  router.push('/login');
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
