import router from '~/router';
import { useCookies } from '@vueuse/integrations/useCookies';
// 全局前置守卫，引入到mian.js的
router.beforeEach((to, from, next) => {
  const token = useCookies().get('admin-token');

  // 没有登录，强制跳转回登录页
  const isLoginOrReg = to.path === '/login' || to.path === '/reg';
  if (!token && !isLoginOrReg) {
    return next({ path: '/login' });
  }

  // 防止重复登录
  if (token && isLoginOrReg) {
    return next({ path: from.path ? from.path : '/' });
  }

  next();
});
