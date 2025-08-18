import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Tasks from '@/views/Tasks.vue'
import Settings from '@/views/Settings.vue'
import Login from '@/auth/login.vue'
import Register from '@/auth/register.vue'

// 路由守卫 - 检查用户是否已登录
const requireAuth = (to, from, next) => {
  const token = localStorage.getItem('token')
  if (token) {
    next()
  } else {
    next('/login')
  }
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: requireAuth
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: Tasks,
    beforeEnter: requireAuth
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    beforeEnter: requireAuth
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // 如果用户已登录且尝试访问登录或注册页面，则重定向到首页
  const token = localStorage.getItem('token')
  if (token && (to.path === '/login' || to.path === '/register')) {
    next('/')
  } else {
    next()
  }
})

export default router