<template>
  <LibHeader />
  <div class="search-container">
    <el-row type="flex" justify="center" align="middle">
      <el-col :span="10">
        <el-input
          placeholder="请输入搜索内容"
          v-model="searchQuery"
          :prefix-icon="Search"
          clearable
          @keyup.enter="handleSearch"
          input-style="font-size:20px">
          <template #prefix>
            <el-icon class="el-input__icon"><search /></el-icon>
          </template>
          <template #append>
            <el-button class="search-button" @click="handleSearch">
              搜索
            </el-button>
          </template>
        </el-input>
      </el-col>
    </el-row>
  </div>

  <div class="tabs">
    <el-tabs v-model="activeName" class="demo-tabs">
      <el-tab-pane label="All" name="first"><Cards label="All" /></el-tab-pane>
      <el-tab-pane label="AI" name="second"><Cards label="AI" /></el-tab-pane>
      <el-tab-pane label="NLP" name="third"><Cards label="NLP" /></el-tab-pane>
      <el-tab-pane label="CV" name="fourth"><Cards label="CV" /></el-tab-pane>
      <el-tab-pane label="CV1" name="fifth"><Cards label="CV1" /></el-tab-pane>
      <el-tab-pane label="CV2" name="sixth"><Cards label="CV2" /></el-tab-pane>
      <el-tab-pane label="CV3" name="seventh"><Cards label="CV3" /></el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCookies } from '@vueuse/integrations/useCookies';
import { useRouter } from 'vue-router';
import Cards from '../components/cards.vue';
import LibHeader from '../components/libHeader.vue';
import { useLibStore } from '@/store/lib'; // Updated from '~/store/lib' to '@/store/lib'

const libStore = useLibStore();
const id = libStore.data.id;
const searchQuery = ref('');
const activeName = ref('first');
const router = useRouter();

const handleSearch = () => {
  console.log('搜索内容:', searchQuery.value);
  // Add search logic here
};

const goBack = () => {
  // Add back navigation logic here
  console.log('返回上一页');
};

const exit1 = () => {
  const cookie = useCookies();
  cookie.remove('admin-token');
  router.push('/login');
};
</script>

<style scoped>
.header {
  padding-top: 25px;
  padding-bottom: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.page-container {
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
  font-size: 18px;
  height: 50px;
  line-height: 50px;
  padding: 0 30px;
}
.search-container .el-input__icon {
  font-size: 20px;
}
</style>
