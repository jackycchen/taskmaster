// API配置文件
const API_CONFIG = {
  BASE_URL: 'http://localhost:8001',
  AUTH: {
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register'
  },
  TASKS: {
    LIST: '/api/tasks',
    CREATE: '/api/tasks',
    UPDATE: '/api/tasks',
    DELETE: '/api/tasks'  // 删除任务的路径
  },
  REMINDERS: {
    DUE: '/api/reminders/due',
    MARK_NOTIFIED: '/api/reminders/mark-notified'
  }
}

export default API_CONFIG