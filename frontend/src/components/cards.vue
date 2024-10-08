<template>
  <div class="card-container">
    <el-card
      v-for="n in 100"
      :key="n"
      shadow="hover"
      class="card-item"
      @click="gotoAbstract(n)">
      <template #header>
        <div class="card-header">
          <span>{{ label }}</span>
        </div>
      </template>
      <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
      <template #footer>Footer content</template>
    </el-card>

    <el-pagination
      class="page"
      background
      layout="prev, pager, next"
      size="large"
      :total="1000" />
  </div>
</template>
<script setup>
import { ref, defineProps } from 'vue';
import { useCookies } from '@vueuse/integrations/useCookies';
import { useRouter } from 'vue-router';
const router = useRouter();

defineProps(['label']);

const gotoAbstract = (num) => {
  const url = router.resolve({
    path: '/abstract',
    query: { num: num },
  });
  window.open(url.href);
};
</script>

<style scoped>
.card-container {
  display: flex;
  width: 480;
  flex-wrap: wrap;
  gap: 10px; /* 卡片之间的间距 */
}

.card-item {
  flex: 1 1 300px; /* 每张卡片的基础宽度，根据实际情况调整 */
  margin: 5px; /* 卡片的外边距，也可以增加间距 */
}
.page {
  padding-top: 2%;
  padding-bottom: 5%;
  margin: 0 auto;
}
</style>
