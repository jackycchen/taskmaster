<template>
  <div id="app">
    <el-container style="min-height: 100vh;">
      <!-- 侧边栏 -->
      <el-aside v-if="$route.path !== '/login' && $route.path !== '/register'" width="200px">
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical"
          router
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/">
            <i class="el-icon-house"></i>
            <span>任务管理</span>
          </el-menu-item>
          <el-menu-item index="/settings">
            <i class="el-icon-setting"></i>
            <span>设置</span>
          </el-menu-item>
          <el-menu-item index="" @click="logout">
            <i class="el-icon-switch-button"></i>
            <span>退出登录</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-container>
        <!-- 头部 -->
        <el-header v-if="$route.path !== '/login' && $route.path !== '/register'" style="background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,.05);">
          <div class="header-content">
            <h2>AceFlow任务管理</h2>
            <div class="user-info" v-if="currentUser">
              <span>欢迎, {{ currentUser }}</span>
            </div>
          </div>
        </el-header>

        <!-- 主体 -->
        <el-main>
          <router-view />
        </el-main>

        <!-- 底部 -->
        <el-footer v-if="$route.path !== '/login' && $route.path !== '/register'" style="text-align: center; background-color: #f5f5f5; padding: 20px;">
          <p>AceFlow任务管理系统 &copy; 2025</p>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import notifierService from '@/services/notifier.js'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const currentUser = ref('')

    // 获取当前用户信息
    const getCurrentUser = () => {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          // 解析JWT token获取用户名
          const payload = JSON.parse(atob(token.split('.')[1]))
          currentUser.value = payload.sub
        } catch (e) {
          console.error('解析token失败:', e)
        }
      }
    }

    // 退出登录
    const logout = () => {
      // 清除本地存储的token和设置
      localStorage.removeItem('token')
      localStorage.removeItem('taskSettings')
      
      // 停止提醒服务
      notifierService.stopChecking()
      
      // 跳转到登录页面
      router.push('/login')
      
      ElMessage.success('已退出登录')
    }

    // 组件挂载时初始化
    onMounted(() => {
      getCurrentUser()
      
      // 如果用户已登录，启动提醒服务
      if (localStorage.getItem('token')) {
        notifierService.startChecking()
      }
    })

    return {
      currentUser,
      logout
    }
  }
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-menu-vertical {
  height: 100%;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.user-info {
  font-size: 14px;
  color: #666;
}

.el-main {
  background-color: #f0f2f5;
}
</style>