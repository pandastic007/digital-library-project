import { createRouter, createWebHashHistory } from 'vue-router';
import Index from '@/pages/index.vue';
import Login from '@/pages/login.vue';
import NotFound from '@/pages/404.vue';
import Register from '@/pages/reg.vue';
import Abstract from '@/pages/abstract.vue';
import Test from '@/pages/test.vue';
import Preview from '@/pages/preview.vue';

const routes = [
  {
    path: '/',
    component: Index,
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/reg',
    component: Register,
  },
  {
    path: '/abstract',
    component: Abstract,
  },
  {
    path: '/test',
    component: Test,
  },
  {
    path: '/preview',
    component: Preview,
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
