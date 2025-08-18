<template>
  <div class="login-form">
    <el-form :model="form" label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">登录</el-button>
      </el-form-item>
    </el-form>
    <div class="auth-link">
      还没有账户？<el-button type="text" @click="goToRegister">立即注册</el-button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '@/config/axios.js'
import API_CONFIG from '@/config/api.js'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const form = ref({
      username: '',
      password: ''
    })
    const router = useRouter()

    const onSubmit = async () => {
      try {
        // 使用URLSearchParams来正确格式化表单数据
        const formData = new URLSearchParams();
        formData.append('username', form.value.username);
        formData.append('password', form.value.password);

        const response = await apiClient.post(`${API_CONFIG.BASE_URL}${API_CONFIG.AUTH.LOGIN}`, 
          formData,
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          }
        )
        localStorage.setItem('token', response.data.access_token)
        ElMessage.success('登录成功')
        router.push('/')
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '登录失败')
      }
    }

    const goToRegister = () => {
      router.push('/register')
    }

    return {
      form,
      onSubmit,
      goToRegister
    }
  }
}
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
}
</style>