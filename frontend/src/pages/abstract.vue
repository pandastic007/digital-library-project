<template>
  <LibHeader />
  <el-container>
    <el-aside width="200px" class="left">
      <el-row>
        <el-col>
          <h5 class="mb-2">标题</h5>
          <el-menu class="el-menu-vertical-demo">
            <el-sub-menu index="1">
              <template #title>
                <span>第1章</span>
              </template>
              <el-menu-item index="1-1">1.1</el-menu-item>
              <el-menu-item index="1-2">1.2</el-menu-item>
              <el-menu-item index="1-3">1.3</el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="2">
              <template #title>
                <span>第2章</span>
              </template>
              <el-menu-item index="2-1">2.1</el-menu-item>
              <el-menu-item index="2-2">2.2</el-menu-item>
              <el-menu-item index="3-3">2.3</el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="3">
              <template #title>
                <span>第3章</span>
              </template>
              <el-menu-item index="3-1">3.1</el-menu-item>
              <el-menu-item index="3-2">3.2</el-menu-item>
              <el-menu-item index="3-3">3.3</el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="4">
              <template #title>
                <span>第4章</span>
              </template>
              <el-menu-item index="4-1">4.1</el-menu-item>
              <el-menu-item index="4-2">4.2</el-menu-item>
              <el-menu-item index="4-3">4.3</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-col>
      </el-row>
    </el-aside>
    <el-main class="body">
      <div>
        <el-descriptions
          class="margin-top"
          title="With border"
          :column="3"
          border>
          <template #extra>
            <el-button type="primary" @click="gotoPre"
              >preview & dialog</el-button
            >
          </template>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <user />
                </el-icon>
                Username
              </div>
            </template>
            kooriookami
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <iphone />
                </el-icon>
                Telephone
              </div>
            </template>
            18100000000
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <location />
                </el-icon>
                Place
              </div>
            </template>
            Suzhou
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <tickets />
                </el-icon>
                Remarks
              </div>
            </template>
            <el-tag size="small">School</el-tag>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <office-building />
                </el-icon>
                Address
              </div>
            </template>
            No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
          </el-descriptions-item>
        </el-descriptions>

        <el-descriptions
          class="margin-top"
          title="Without border"
          :column="3"
          :style="blockMargin">
          <template #extra>
            <el-button type="primary" class="custom-button">
              <el-icon><Download /></el-icon>
              Download
            </el-button>
          </template>
          <el-descriptions-item label="Num">{{ num }}</el-descriptions-item>
          <el-descriptions-item label="Telephone"
            >18100000000</el-descriptions-item
          >
          <el-descriptions-item label="Place">Suzhou</el-descriptions-item>
          <el-descriptions-item label="Remarks">
            <el-tag size="small">School</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Address">
            No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <div class="demo-collapse">
        <el-collapse v-model="activeName" accordion>
          <el-collapse-item title="全文总结" name="1">
            <div>
              Consistent with real life: in line with the process and logic of
              real life, and comply with languages and habits that the users are
              used to;
            </div>
            <div>
              Consistent within interface: all elements should be consistent,
              such as: design style, icons and texts, position of elements, etc.
            </div>
          </el-collapse-item>
          <el-collapse-item title="第1章总结" name="2">
            <div>
              Operation feedback: enable the users to clearly perceive their
              operations by style updates and interactive effects;
            </div>
            <div>
              Visual feedback: reflect current state by updating or rearranging
              elements of the page.
            </div>
          </el-collapse-item>
          <el-collapse-item title="第2章总结" name="3">
            <div>
              Simplify the process: keep operating process simple and intuitive;
            </div>
            <div>
              Definite and clear: enunciate your intentions clearly so that the
              users can quickly understand and make decisions;
            </div>
            <div>
              Easy to identify: the interface should be straightforward, which
              helps the users to identify and frees them from memorizing and
              recalling.
            </div>
          </el-collapse-item>
          <el-collapse-item title="第3章总结" name="4">
            <div>
              Decision making: giving advices about operations is acceptable,
              but do not make decisions for the users;
            </div>
            <div>
              Controlled consequences: users should be granted the freedom to
              operate, including canceling, aborting or terminating current
              operation.
            </div>
          </el-collapse-item>
          <el-collapse-item title="第4章总结" name="5">
            <div>
              Decision making: giving advices about operations is acceptable,
              but do not make decisions for the users;
            </div>
            <div>
              Controlled consequences: users should be granted the freedom to
              operate, including canceling, aborting or terminating current
              operation.
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import LibHeader from '../components/libHeader.vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const num = route.query.num;
const router = useRouter();
// console.log(num);
const gotoPre = () => {
  router.push('/preview');
};
</script>

<style scoped>
.el-descriptions {
  margin-top: 20px;
}
.cell-item {
  display: flex;
  align-items: center;
}
.margin-top {
  margin-top: 20px;
}
.body {
  margin-top: 2%;
  padding: 1% 2%;
  /* background-color: #f0f0f0; */
  box-shadow: 10px 0px 10px 0px rgba(0, 0, 0, 0.1);
}
.left {
  margin-top: 2%;
  padding: 1% 0;
  box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.1);
}
.el-descriptions {
  margin-top: 20px;
}
.cell-item {
  display: flex;
  align-items: center;
}
.margin-top {
  margin-top: 20px;
}
.mb-2 {
  margin-bottom: 0.5rem; /* 保留原有的外边距 */
  padding-left: 20px; /* 添加左边的内边距 */
}
.el-menu-vertical-demo .el-menu-item {
  height: 40px; /* 修改高度为60px */
  line-height: 40px; /* 调整行高以垂直居中 */
}
.demo-collapse {
  padding-top: 3%;
} /* 增加图标和文字之间的距离 */
.custom-button .el-icon {
  margin-right: 8px; /* 可以根据需要调整距离 */
}

/* 调整按钮的左右内边距 */
.custom-button {
  padding-left: 10px; /* 调整左侧内边距 */
  padding-right: 10px; /* 调整右侧内边距 */
}
</style>
