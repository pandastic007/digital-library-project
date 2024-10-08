import { reactive, ref } from 'vue';
import { defineStore } from 'pinia';

/*
  定义一个基于 Pinia 的 Store
  第1个参数 lib 是 useLibStore 在应用中的唯一标识符(ID)
  第2个参数是 Setup函数 或 Option对象
*/
export const useLibStore = defineStore(
  'lib',
  () => {
    //定义一个响应式对象，存储网站信息
    const data = reactive({
      id: Number,
    });
    const save = (id) => {
      data.id = id;
    };
    return {
      data,
      save,
    };
  },
  {
    //持久化存储到 localStorage 中
    persist: true,
  }
);
