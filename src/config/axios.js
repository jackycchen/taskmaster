import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  // 可以在这里设置基础URL等配置
});

// 添加请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    
    // 如果有token，则添加到Authorization头部
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 如果是401错误，可能是token过期或无效
    if (error.response && error.response.status === 401) {
      // 清除本地token
      localStorage.removeItem('token');
      // 可以在这里添加跳转到登录页的逻辑
      // window.location.href = '/#/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;