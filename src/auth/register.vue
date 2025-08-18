<template>
  <div class="register-form">
    <el-form :model="form" label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="form.email" type="email" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">注册</el-button>
      </el-form-item>
    </el-form>
    <div class="auth-link">
      已有账户？<el-button type="text" @click="goToLogin">立即登录</el-button>
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
      email: '',
      password: ''
    })

    const router = useRouter()

    const onSubmit = async () => {
      try {
        // 注册用户
        await apiClient.post(`${API_CONFIG.BASE_URL}${API_CONFIG.AUTH.REGISTER}`, form.value)
        
        // 注册成功后自动登录
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
        ElMessage.success('注册成功，已自动登录')
        router.push('/tasks')
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '注册失败')
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    return {
      form,
      onSubmit,
      goToLogin
    }
  }
}
</script>

<style scoped>
.register-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
}
</style>