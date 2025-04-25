import axios from 'axios';

// 创建全局axios实例，统一配置
const api = axios.create({
  baseURL: '/api',  // 使用相对路径作为基础URL
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true  // 支持跨域请求时发送cookies
});

// 请求拦截器：自动添加认证信息
api.interceptors.request.use(config => {
  const userData = localStorage.getItem('user');
  if (userData) {
    // 从localStorage获取用户信息，添加到请求头
    const user = JSON.parse(userData);
    // 添加JWT令牌到Authorization头
    if (user.token) {
      config.headers['Authorization'] = `Bearer ${user.token}`;
    }
  }
  return config;
}); 

// 响应拦截器：处理未认证
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 导出配置好的axios实例，供所有组件使用
export default api;

/**
 * 使用说明：
 * 
 * 1. 在组件中导入此api实例替代直接使用axios：
 * import api from '@/api';
 * 
 * 2. 使用相对路径调用API，无需添加/api前缀：
 * const response = await api.get('/create-exams/');
 * 
 * 3. 确保路径与后端路由完全匹配，包括尾部斜杠
 */