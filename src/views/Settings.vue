<template>
  <div class="settings-page">
    <div class="header">
      <h1>设置</h1>
    </div>

    <div class="settings-content">
      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>提醒设置</span>
          </div>
        </template>
        
        <div class="setting-item">
          <div class="setting-label">
            <div class="setting-title">提醒时间</div>
            <div class="setting-description">任务到期前多久提醒您</div>
          </div>
          <div class="setting-control">
            <el-select v-model="settings.reminderMinutes" @change="saveSettings">
              <el-option
                v-for="option in reminderOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </div>
        </div>
      </el-card>

      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>数据管理</span>
          </div>
        </template>
        
        <div class="setting-item">
          <div class="setting-label">
            <div class="setting-title">导出任务数据</div>
            <div class="setting-description">将您的任务数据导出为CSV或JSON格式</div>
          </div>
          <div class="setting-control">
            <el-button @click="exportData('csv')">导出CSV</el-button>
            <el-button @click="exportData('json')">导出JSON</el-button>
          </div>
        </div>
      </el-card>

      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>账户设置</span>
          </div>
        </template>
        
        <div class="setting-item">
          <div class="setting-label">
            <div class="setting-title">退出登录</div>
            <div class="setting-description">退出当前账户</div>
          </div>
          <div class="setting-control">
            <el-button type="danger" @click="logout">退出登录</el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '@/config/axios.js'
import { useRouter } from 'vue-router'
import notifierService from '@/services/notifier.js'
import API_CONFIG from '@/config/api.js'

export default {
  name: 'Settings',
  setup() {
    const router = useRouter()
    
    const settings = reactive({
      reminderMinutes: 30
    })
    
    const reminderOptions = [
      { label: '15分钟前', value: 15 },
      { label: '30分钟前', value: 30 },
      { label: '1小时前', value: 60 },
      { label: '2小时前', value: 120 }
    ]
    
    // 加载设置
    const loadSettings = () => {
      const savedSettings = localStorage.getItem('taskSettings')
      if (savedSettings) {
        const parsed = JSON.parse(savedSettings)
        settings.reminderMinutes = parsed.reminderMinutes || 30
      }
      
      // 更新提醒服务中的设置
      notifierService.setMinutesBefore(settings.reminderMinutes)
    }
    
    // 保存设置
    const saveSettings = () => {
      localStorage.setItem('taskSettings', JSON.stringify(settings))
      
      // 更新提醒服务中的设置
      notifierService.setMinutesBefore(settings.reminderMinutes)
      
      ElMessage.success('设置已保存')
    }
    
    // 导出数据
    const exportData = async (format) => {
      try {
        const response = await apiClient.get(`${API_CONFIG.BASE_URL}${API_CONFIG.TASKS.LIST}`)
        const tasks = response.data
        
        let content = ''
        let filename = ''
        let mimeType = ''
        
        if (format === 'csv') {
          // 创建CSV内容
          const headers = ['ID', '标题', '描述', '截止时间', '优先级', '状态', '创建时间']
          const rows = tasks.map(task => [
            task.id,
            `"${task.title}"`,
            `"${task.description || ''}"`,
            task.due_date ? new Date(task.due_date).toISOString() : '',
            getPriorityText(task.priority),
            getStatusText(task.status),
            task.created_at ? new Date(task.created_at).toISOString() : ''
          ])
          
          content = [headers, ...rows].map(row => row.join(',')).join('\n')
          filename = `tasks-${new Date().toISOString().slice(0, 10)}.csv`
          mimeType = 'text/csv;charset=utf-8;'
        } else {
          // 创建JSON内容
          content = JSON.stringify(tasks, null, 2)
          filename = `tasks-${new Date().toISOString().slice(0, 10)}.json`
          mimeType = 'application/json;charset=utf-8;'
        }
        
        // 创建下载链接
        const blob = new Blob([content], { type: mimeType })
        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)
        link.setAttribute('href', url)
        link.setAttribute('download', filename)
        link.style.visibility = 'hidden'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        ElMessage.success(`数据已导出为${format.toUpperCase()}格式`)
      } catch (error) {
        ElMessage.error('导出失败: ' + (error.response?.data?.detail || error.message))
      }
    }
    
    // 获取优先级文本
    const getPriorityText = (priority) => {
      const priorityMap = {
        1: '高',
        2: '中',
        3: '低'
      }
      return priorityMap[priority] || '中'
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待办',
        'in_progress': '进行中',
        'completed': '已完成'
      }
      return statusMap[status] || status
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
    
    // 组件挂载时加载设置
    onMounted(() => {
      loadSettings()
    })
    
    return {
      settings,
      reminderOptions,
      saveSettings,
      exportData,
      logout
    }
  }
}
</script>

<style scoped>
.settings-page {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
}

.settings-content {
  max-width: 800px;
}

.setting-card {
  margin-bottom: 20px;
}

.card-header {
  font-weight: bold;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-label {
  flex: 1;
}

.setting-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.setting-description {
  font-size: 14px;
  color: #666;
}

.setting-control {
  display: flex;
  gap: 10px;
}

.setting-control .el-select {
  width: 150px;
}
</style>