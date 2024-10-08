import { createApp } from 'vue';
import App from './App.vue';
// //整体导入 ElementPlus 组件库
// import ElementPlus from 'element-plus'; //导入 ElementPlus 组件库的所有模块和功能
// import 'element-plus/dist/index.css'; //导入 ElementPlus 组件库所需的全局 CSS 样式
import * as ElementPlusIconsVue from '@element-plus/icons-vue'; //导入 ElementPlus 组件库中的所有图标
import 'virtual:windi.css';
import router from './router';
import './permission';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
//创建一个Pinia实例,用于在应用中集中管理状态(store)
const pinia = createPinia();

//将插件添加到 pinia 实例上
pinia.use(piniaPluginPersistedstate);
const app = createApp(App);
// app.use(ElementPlus); //将 ElementPlus 插件注册到 Vue 应用中
app.use(router);
//注册 ElementPlus 组件库中的所有图标到全局 Vue 应用中
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}
app.use(pinia); //将Pinia实例注册到Vue应用中
app.mount('#app');
