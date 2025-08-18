import axios from 'axios'

const API_URL = '/api/tasks'

const createTask = async (taskData) => {
  const response = await axios.post(API_URL, taskData)
  return response.data
}

const getTasks = async () => {
  try {
    const response = await axios.get(API_URL)
    return response.data
  } catch (error) {
    console.log('API请求失败，返回模拟数据')
    return [
      {
        id: 1,
        title: '示例任务1',
        description: '这是一个示例任务',
        status: 'pending'
      },
      {
        id: 2,
        title: '示例任务2',
        description: '已完成的任务示例',
        status: 'completed'
      }
    ]
  }
}

const updateTask = async (taskId, taskData) => {
  const response = await axios.put(`${API_URL}/${taskId}`, taskData)
  return response.data
}

const deleteTask = async (taskId) => {
  const response = await axios.delete(`${API_URL}/${taskId}`)
  return response.data
}

export default {
  createTask,
  getTasks,
  updateTask,
  deleteTask
}
