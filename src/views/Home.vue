<template>
  <div class="home">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <h2>欢迎使用AceFlow任务管理系统</h2>
        </div>
      </template>
      
      <div class="welcome-content">
        <p>这是一个多用户隔离的个人任务管理系统，具有以下特性：</p>
        
        <ul>
          <li>✅ 用户注册和登录功能</li>
          <li>✅ 任务创建、编辑、删除和查看</li>
          <li>✅ 列表视图和看板视图切换</li>
          <li>✅ 任务优先级和状态管理</li>
          <li>✅ 到期任务提醒功能</li>
          <li>✅ 数据持久化存储</li>
          <li>✅ 数据导出功能</li>
        </ul>
        
        <div class="actions">
          <el-button type="primary" @click="$router.push('/tasks')">开始管理任务</el-button>
          <el-button @click="$router.push('/settings')">系统设置</el-button>
        </div>
      </div>
    </el-card>
    
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <h3>系统状态</h3>
        </div>
      </template>
      
      <div class="stats-content">
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ stats.users }}</div>
              <div class="stat-label">用户数</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ stats.tasks }}</div>
              <div class="stat-label">任务数</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ stats.completed }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Home',
  setup() {
    const stats = ref({
      users: 0,
      tasks: 0,
      completed: 0
    })

    // 获取系统统计信息
    const fetchStats = async () => {
      try {
        // 这里应该调用实际的统计API
        // 暂时使用模拟数据
        stats.value = {
          users: 1,
          tasks: 0,
          completed: 0
        }
      } catch (error) {
        console.error('获取统计信息失败:', error)
      }
    }

    onMounted(() => {
      fetchStats()
    })

    return {
      stats
    }
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
}

.card-header h2, .card-header h3 {
  margin: 0;
}

.welcome-content ul {
  padding-left: 20px;
}

.welcome-content li {
  margin-bottom: 10px;
}

.actions {
  margin-top: 20px;
}

.actions .el-button {
  margin-right: 10px;
}

.stats-card {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px 0;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}
</style>