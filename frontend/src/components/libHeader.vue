<template>
  <div class="header">
    <el-page-header
      :icon="null"
      title="  Home"
      class="page-container"
      @back="goBack">
      <template #content>
        <div class="flex items-center">
          <el-avatar :size="32" class="mr-3" src="public/library.jpg" />
          <span class="text-large font-600 mr-3">文献查阅</span>
          <span
            class="text-sm mr-2"
            style="color: var(--el-text-color-regular)">
            内容管理与数字图书馆
          </span>
          <!-- <el-tag>Default</el-tag> -->
        </div>
      </template>

      <template #extra>
        <el-popconfirm title="Are you sure to EXIT?" @confirm="exit1">
          <template #reference>
            <div class="flex items-center">
              <el-button type="primary" plain>Exit</el-button>
              <!-- <el-button type="primary" class="ml-2">Edit</el-button> -->
            </div>
          </template>
        </el-popconfirm>
      </template>
    </el-page-header>
  </div>
</template>
<script setup>
import { useCookies } from '@vueuse/integrations/useCookies';
import { useRouter } from 'vue-router';

const router = useRouter();

const goBack = () => {
  // 在这里添加返回逻辑
  router.push('/');
};
const exit1 = () => {
  const cookie = useCookies();
  cookie.remove('admin-token');
  ElNotification({
    title: 'Success',
    message: '已退出',
    type: 'success',
    duration: 3000,
  });
  router.push('/login');
};
</script>

<style scoped>
.header {
  /* margin-top: 1%; */
  padding-top: 25px;
  padding-bottom: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.page-container {
  /* max-width: 1200px; */
  margin: 0 2%;
}
.header ::v-deep(.el-page-header__title) {
  font-size: 20px;
}
.search-container {
  margin: 20px 0;
}

.flex {
  display: flex;
  align-items: center;
}

.items-center {
  align-items: center;
}

.mr-3 {
  margin-right: 12px;
}

.text-large {
  font-size: 18px;
}

.font-600 {
  font-weight: 600;
}

.text-sm {
  font-size: 14px;
}

.ml-2 {
  margin-left: 8px;
}

.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.tabs {
  margin-left: 2%;
  margin-right: 2%;
}
::v-deep(.el-tabs__item) {
  font-size: 20px;
}
.search-button {
  font-size: 18px; /* 增加按钮上文字的字体大小 */
  height: 50px; /* 增加按钮的高度 */
  line-height: 50px; /* 使文字垂直居中 */
  padding: 0 30px; /* 增加按钮的左右padding */
}

/* 自定义prefix-icon图标大小 */
.search-container .el-input__icon {
  font-size: 20px; /* 调整图标大小 */
}
</style>
