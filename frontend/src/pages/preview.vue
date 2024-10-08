<template>
  <el-row class="login-container">
    <el-col :lg="16" :md="12" class="left">
      <div>
        <iframe
          src="test_pdf/课程说明.pdf"
          style="width: 100%; height: 100vh"
          frameborder="0"></iframe>
      </div>
    </el-col>
    <el-col :lg="8" :md="12" class="right">
      <el-page-header title=" " :icon="null" class="qaheader">
        <template #content>
          <span class="text-large font-600">Q&A</span>
        </template>
      </el-page-header>
      <div class="content">
        <div class="container">
          <!--简介： scroll-with-animation:动画，开启有一个过渡效果；scroll-into-view：向指定id滚动 -->
          <el-scrollbar class="Scroll" scroll-y="true" ref="scrollbar">
            <div
              class="box"
              v-for="(item, index) in dialogList"
              :key="index"
              :id="`item-${index}`">
              <div class="input">
                <el-text class="i">{{ item.input }}</el-text>
              </div>
              <div class="output">
                <el-text class="o">{{ item.output }}</el-text>
              </div>
            </div>
          </el-scrollbar>
        </div>
        <div class="footer">
          <div class="ipt">
            <el-input
              placeholder="请输入内容"
              type="textarea"
              class="IPT"
              v-model="sendInfo"
              @keyup.enter="send()">
            </el-input>
          </div>
          <div class="btn">
            <el-button type="primary" @click="send()">Send</el-button>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>
<script setup>
import { ref, watch, nextTick } from 'vue';

// scroll-into-view指向的id值
let item = ref('');

// 发送的内容
let sendInfo = ref('');
const scrollbar = ref(null);
//模拟的虚拟数据
const dialogList = ref([
  {
    input: '你好',
    output: '你好，很高兴认识你！',
  },
]);

// 动态更新item的值
watch(
  dialogList,
  (newval, oldval) => {
    // 重新赋值item,延迟到dom更新之后进行，否则没效果
    nextTick(() => {
      item.value = 'item-' + (newval.length - 1);
    });
  },
  {
    deep: true, //深度监视
    immediate: true, //初始化立即执行
  }
);

// 发送
const send = () => {
  if (!sendInfo.value) return;
  let obj = {
    input: sendInfo.value,
    output: '......',
  };
  // 追加数据
  dialogList.value.push(obj);
  // 清空输入框
  sendInfo.value = '';

  dialogList.value[
    dialogList.value.length - 1
  ].output = `In the Garden of Solitude

Alone amidst the whispering trees,
I find my solace, calm and free.
The garden of solitude holds my key,
To moments of tranquility.

Beneath the azure sky's vast expanse,
I walk where no one else can see.
Each petal, leaf, and blade of grass,
Speaks softly in poetry.

The sun dips low beyond the hill,
And twilight's hues begin to spill.
In this secret place, where time stands still,
I find my heart's true will.

Here, life's cacophony subsides,
In favor of the quiet tides.
The garden of solitude, it guides
My soul to peaceful sides.`;

  // 确保消息被添加到列表后滚动到底部
  nextTick(() => {
    // 使用 Element Plus 的滚动方法
    if (scrollbar.value) {
      const wrapper = scrollbar.value.wrapRef;
      if (wrapper) {
        console.log('wrapper');
        wrapper.scrollTop = wrapper.scrollHeight;
      }
    }
  });
};

// 触顶加载更多
</script>
<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
}
.left {
  background-color: #f5f5f5;
}
.login-container .right {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.login-container .right {
  background-color: #f9fafb;
  display: flex;
  flex-direction: column;
}
.chat-content {
  flex-grow: 1;
  overflow-y: auto;
}

.content {
  max-height: 100vh;
  background: rgb(245, 245, 245);
  .container {
    height: 85vh;
    padding: 10rpx 10rpx 10rpx 20rpx;
    box-sizing: border-box;
    .Scroll {
      height: 85vh;
      .box {
        padding: 0 10rpx 0 0;
        box-sizing: border-box;
        .output {
          display: flex;
          justify-content: flex-start;
          margin: 30rpx 0;
          .o {
            margin-top: 15px;
            margin-bottom: 10px;
            padding: 5px 5px 5px 10px; /* 上 右 下 左 */
            max-width: 20vw;
            height: auto;
            padding: 10rpx;
            background-color: rgb(255, 255, 255);
            border-top-left-radius: 10rpx;
            border-top-right-radius: 10rpx;
            border-bottom-right-radius: 10rpx;
          }
        }
        .input {
          display: flex;
          justify-content: flex-end;
          margin: 20rpx 0;
          .i {
            margin-top: 15px;
            padding: 5px;
            max-width: 15vw;
            height: auto;
            padding: 10rpx;
            background-color: rgb(28, 217, 128);
            border-top-left-radius: 10rpx;
            border-top-right-radius: 10rpx;
            border-bottom-left-radius: 10rpx;
          }
        }
      }
    }
  }
  .footer {
    height: 10vh;
    margin-top: 20rpx;
    background-color: #e3f9fd;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10rpx 20rpx 0 20rpx;
    box-sizing: border-box;
    .ipt {
      flex: 6;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      .IPT {
        margin-left: 5%;
        line-height: 80rpx;
        background-color: white;
        border-radius: 10rpx;
        margin-right: 10rpx;
        padding-left: 10rpx;
      }
    }
    .btn {
      flex: 1.5;

      height: 80rpx;
      line-height: 80rpx;
      border-radius: 10rpx;
      margin-left: 2%;
      margin-right: 10rpx;
    }
  }
}
.qaheader {
  padding-top: 2%;
  margin-bottom: 1%;
}
.el-text {
  font-size: 18px;
}
</style>
