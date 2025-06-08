import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

// 创建 axios 实例
const api = axios.create({
    baseURL: BASE_URL,
    timeout: 60000,  // 60 秒超时
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    withCredentials: false
});

// 添加请求拦截器
api.interceptors.request.use(
    config => {
        console.log('发送请求:', config.url);
        return config;
    },
    error => {
        console.error('请求错误:', error);
        return Promise.reject(error);
    }
);

// 添加响应拦截器
api.interceptors.response.use(
    response => {
        console.log('收到响应:', response.status);
        return response;
    },
    error => {
        console.error('响应错误:', error);
        if (error.code === 'ERR_NETWORK') {
            console.error('网络连接失败，请检查后端服务是否运行');
        }
        return Promise.reject(error);
    }
);

// 获取作文题目
export const getEssayQuestion = async () => {
    try {
        const response = await api.get('/api/essay/question');
        return response.data;
    } catch (error) {
        console.error('获取题目失败:', error);
        throw error;
    }
};

// 润色文章
export const polishEssay = async (essay) => {
    try {
        const response = await api.post('/api/essay/polish', { essay });
        return response.data;
    } catch (error) {
        console.error('润色文章失败:', error);
        throw error;
    }
}; 