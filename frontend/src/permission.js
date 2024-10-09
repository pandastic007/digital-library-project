import router from '@/router';
import { useCookies } from '@vueuse/integrations/useCookies';

// Global guard, used in main.js
router.beforeEach((to, from, next) => {
  const token = useCookies().get('admin-token');

  // If not logged in, redirect to login page
  const isLoginOrReg = to.path === '/login' || to.path === '/reg';
  if (!token && !isLoginOrReg) {
    return next({ path: '/login' });
  }

  // Prevent redundant login
  if (token && isLoginOrReg) {
    return next({ path: from.path ? from.path : '/' });
  }

  next();
});
