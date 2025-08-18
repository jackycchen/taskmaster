import apiClient from '@/config/axios.js';
import API_CONFIG from '@/config/api.js';

class NotifierService {
  constructor() {
    this.checkInterval = null;
    this.minutesBefore = 30; // 默认提前30分钟提醒
  }

  // 开始定时检查到期任务
  startChecking() {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }
    
    this.checkInterval = setInterval(() => {
      this.checkDueTasks();
    }, 60000); // 每分钟检查一次
    
    // 立即检查一次
    this.checkDueTasks();
  }

  // 停止定时检查
  stopChecking() {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
    }
  }

  // 检查即将到期的任务
  async checkDueTasks() {
    try {
      const response = await apiClient.get(`${API_CONFIG.BASE_URL}${API_CONFIG.REMINDERS.DUE}?minutes_before=${this.minutesBefore}`);
      const dueTasks = response.data;
      
      // 为每个到期任务显示通知
      dueTasks.forEach(task => {
        this.showNotification(task);
        // 标记任务已提醒
        this.markTaskNotified(task.id);
      });
    } catch (error) {
      console.error('检查到期任务失败:', error);
    }
  }

  // 显示浏览器通知
  showNotification(task) {
    // 检查浏览器是否支持通知
    if (!("Notification" in window)) {
      console.warn("此浏览器不支持桌面通知");
      return;
    }

    // 请求通知权限
    if (Notification.permission === "granted") {
      this.createNotification(task);
    } else if (Notification.permission !== "denied") {
      Notification.requestPermission().then(permission => {
        if (permission === "granted") {
          this.createNotification(task);
        }
      });
    }
  }

  // 创建通知
  createNotification(task) {
    const title = `任务提醒: ${task.title}`;
    const options = {
      body: `任务截止时间: ${new Date(task.due_date).toLocaleString()}\n${task.description || ''}`,
      icon: '/favicon.ico',
      tag: `task-${task.id}`, // 避免重复通知
      requireInteraction: true // 需要用户交互才关闭
    };

    const notification = new Notification(title, options);

    // 设置通知点击事件
    notification.onclick = () => {
      // 跳转到任务详情页
      window.focus();
      window.location.hash = `#/tasks/${task.id}`;
      notification.close();
    };

    // 5秒后自动关闭通知
    setTimeout(() => {
      notification.close();
    }, 5000);
  }

  // 标记任务已提醒
  async markTaskNotified(taskId) {
    try {
      await apiClient.post(`${API_CONFIG.BASE_URL}${API_CONFIG.REMINDERS.MARK_NOTIFIED}/${taskId}`);
    } catch (error) {
      console.error('标记任务已提醒失败:', error);
    }
  }

  // 设置提醒提前时间
  setMinutesBefore(minutes) {
    this.minutesBefore = minutes;
  }

  // 获取提醒提前时间
  getMinutesBefore() {
    return this.minutesBefore;
  }
}

// 创建单例实例
const notifierService = new NotifierService();

export default notifierService;