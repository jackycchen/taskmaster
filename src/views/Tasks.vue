<template>
  <div class="tasks-page">
    <div class="header">
      <h1>任务管理</h1>
      <div class="actions">
        <el-button type="primary" @click="showTaskForm">新建任务</el-button>
        <el-button @click="switchView">
          {{ isListView ? '看板视图' : '列表视图' }}
        </el-button>
      </div>
    </div>

    <div class="filters">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable @change="loadTasks">
        <el-option label="全部" value=""></el-option>
        <el-option label="待办" value="pending"></el-option>
        <el-option label="进行中" value="in_progress"></el-option>
        <el-option label="已完成" value="completed"></el-option>
      </el-select>
      
      <el-select v-model="filterPriority" placeholder="优先级筛选" clearable @change="loadTasks">
        <el-option label="全部" value=""></el-option>
        <el-option label="高" :value="1"></el-option>
        <el-option label="中" :value="2"></el-option>
        <el-option label="低" :value="3"></el-option>
      </el-select>
    </div>

    <!-- 列表视图 -->
    <div v-if="isListView" class="list-view">
      <el-table :data="filteredTasks" style="width: 100%" @row-click="viewTask">
        <el-table-column prop="title" label="任务标题" min-width="200"></el-table-column>
        <el-table-column prop="description" label="描述" min-width="200">
          <template #default="scope">
            <span class="description">{{ scope.row.description }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="due_date" label="截止时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.due_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="scope">
            <el-tag :type="getPriorityType(scope.row.priority)">
              {{ getPriorityText(scope.row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click.stop="editTask(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click.stop="deleteTask(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 看板视图 -->
    <div v-else class="board-view">
      <div class="kanban-board">
        <div class="kanban-column" v-for="status in statusOptions" :key="status.value">
          <div class="column-header">
            <h3>{{ status.label }}</h3>
            <span class="task-count">({{ getTasksByStatus(status.value).length }})</span>
          </div>
          <div class="column-content"
               @drop="onDrop($event, status.value)"
               @dragover="onDragOver($event)">
            <div 
              v-for="task in getTasksByStatus(status.value)" 
              :key="task.id"
              class="task-card"
              draggable="true"
              @dragstart="onDragStart($event, task)"
              @click="viewTask(task)"
            >
              <div class="task-title">{{ task.title }}</div>
              <div class="task-description">{{ task.description }}</div>
              <div class="task-due-date">{{ formatDate(task.due_date) }}</div>
              <div class="task-priority">
                <el-tag :type="getPriorityType(task.priority)" size="small">
                  {{ getPriorityText(task.priority) }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务表单对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <TaskForm 
        :task="editingTask" 
        @submit="handleTaskSubmit" 
        @cancel="dialogVisible = false" 
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import apiClient from '@/config/axios.js'
import TaskForm from '@/components/TaskForm.vue'
import API_CONFIG from '@/config/api.js'

export default {
  name: 'Tasks',
  components: {
    TaskForm
  },
  setup() {
    const tasks = ref([])
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const editingTask = ref(null)
    const isListView = ref(true)
    const filterStatus = ref('')
    const filterPriority = ref('')
    
    const statusOptions = [
      { label: '待办', value: 'pending' },
      { label: '进行中', value: 'in_progress' },
      { label: '已完成', value: 'completed' }
    ]

    const priorityOptions = [
      { label: '高', value: 1 },
      { label: '中', value: 2 },
      { label: '低', value: 3 }
    ]

    // 加载任务列表
    const loadTasks = async () => {
      try {
        const response = await apiClient.get(`${API_CONFIG.BASE_URL}${API_CONFIG.TASKS.LIST}`)
        tasks.value = response.data
      } catch (error) {
        ElMessage.error('加载任务失败: ' + (error.response?.data?.detail || error.message))
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
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

    // 获取状态类型（用于标签颜色）
    const getStatusType = (status) => {
      const typeMap = {
        'pending': 'info',
        'in_progress': 'warning',
        'completed': 'success'
      }
      return typeMap[status] || 'info'
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

    // 获取优先级类型（用于标签颜色）
    const getPriorityType = (priority) => {
      const typeMap = {
        1: 'danger',
        2: 'warning',
        3: 'success'
      }
      return typeMap[priority] || 'warning'
    }

    // 显示任务表单
    const showTaskForm = () => {
      editingTask.value = null
      dialogTitle.value = '新建任务'
      dialogVisible.value = true
    }

    // 编辑任务
    const editTask = (task) => {
      editingTask.value = { ...task }
      dialogTitle.value = '编辑任务'
      dialogVisible.value = true
    }

    // 查看任务详情
    const viewTask = (task) => {
      editingTask.value = { ...task }
      dialogTitle.value = '任务详情'
      dialogVisible.value = true
    }

    // 处理任务提交
    const handleTaskSubmit = async (taskData) => {
      try {
        if (editingTask.value && editingTask.value.id) {
          // 更新任务
          await apiClient.put(`${API_CONFIG.BASE_URL}${API_CONFIG.TASKS.UPDATE}/${editingTask.value.id}`, taskData)
          ElMessage.success('任务更新成功')
        } else {
          // 创建任务
          await apiClient.post(`${API_CONFIG.BASE_URL}${API_CONFIG.TASKS.CREATE}`, taskData)
          ElMessage.success('任务创建成功')
        }
        
        dialogVisible.value = false
        loadTasks() // 重新加载任务列表
      } catch (error) {
        ElMessage.error('操作失败: ' + (error.response?.data?.detail || error.message))
      }
    }

    // 删除任务
    const deleteTask = async (taskId) => {
      try {
        const confirmResult = await ElMessageBox.confirm(
          '确定要删除这个任务吗？',
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        );
        
        if (confirmResult === 'confirm') {
          await apiClient.delete(`${API_CONFIG.BASE_URL}${API_CONFIG.TASKS.DELETE}/${taskId}`);
          ElMessage.success('任务删除成功');
          loadTasks(); // 重新加载任务列表
        }
      } catch (error) {
        // 处理取消操作或其他错误
        if (error !== 'cancel') {
          ElMessage.error('删除失败: ' + (error.response?.data?.detail || error.message));
        }
      }
    }

    // 切换视图
    const switchView = () => {
      isListView.value = !isListView.value
    }

    // 根据状态筛选任务
    const filteredTasks = computed(() => {
      let result = tasks.value
      
      if (filterStatus.value) {
        result = result.filter(task => task.status === filterStatus.value)
      }
      
      if (filterPriority.value !== '') {
        result = result.filter(task => task.priority === filterPriority.value)
      }
      
      return result
    })

    // 根据状态获取任务
    const getTasksByStatus = (status) => {
      return tasks.value.filter(task => task.status === status)
    }

    // 拖拽开始
    const onDragStart = (event, task) => {
      event.dataTransfer.setData('task', JSON.stringify(task))
    }

    // 拖拽经过
    const onDragOver = (event) => {
      event.preventDefault()
    }

    // 拖拽放置
    const onDrop = async (event, newStatus) => {
      event.preventDefault()
      const taskData = JSON.parse(event.dataTransfer.getData('task'))
      
      if (taskData.status !== newStatus) {
        try {
          await apiClient.put(`${API_CONFIG.BASE_URL}${API_CONFIG.TASKS.UPDATE}/${taskData.id}`, { status: newStatus })
          ElMessage.success('任务状态更新成功')
          loadTasks() // 重新加载任务列表
        } catch (error) {
          ElMessage.error('更新失败: ' + (error.response?.data?.detail || error.message))
        }
      }
    }

    // 组件挂载时加载任务
    onMounted(() => {
      loadTasks()
    })

    return {
      tasks,
      dialogVisible,
      dialogTitle,
      editingTask,
      isListView,
      filterStatus,
      filterPriority,
      statusOptions,
      priorityOptions,
      filteredTasks,
      loadTasks,
      formatDate,
      getStatusText,
      getStatusType,
      getPriorityText,
      getPriorityType,
      showTaskForm,
      editTask,
      viewTask,
      handleTaskSubmit,
      deleteTask,
      switchView,
      getTasksByStatus,
      onDragStart,
      onDragOver,
      onDrop
    }
  }
}
</script>

<style scoped>
.tasks-page {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.list-view {
  background: white;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.description {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.board-view {
  background: white;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.kanban-board {
  display: flex;
  gap: 20px;
  overflow-x: auto;
}

.kanban-column {
  flex: 1;
  min-width: 300px;
  background: #f5f5f5;
  border-radius: 4px;
}

.column-header {
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
}

.column-header h3 {
  margin: 0;
  flex: 1;
}

.task-count {
  font-size: 12px;
  color: #666;
}

.column-content {
  min-height: 200px;
  padding: 10px;
}

.task-card {
  background: white;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 10px;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}

.task-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.task-title {
  font-weight: bold;
  margin-bottom: 8px;
}

.task-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.task-due-date {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.task-priority {
  text-align: right;
}
</style>