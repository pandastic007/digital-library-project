<template>
  <div class="card-container">
    <el-card v-for="(card, index) in cards" :key="index" class="card-item">
      <!-- 卡片内容 -->
    </el-card>
  </div>
</template>

<script></script>

<style scoped>
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px; /* 卡片之间的间距 */
}

.card-item {
  flex: 1 1 200px; /* 每张卡片的基础宽度，根据实际情况调整 */
  margin: 5px; /* 卡片的外边距，也可以增加间距 */
}
</style>
