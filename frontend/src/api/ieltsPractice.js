import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// 创建axios实例
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 120000, // 增加到120秒
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// 添加请求拦截器
api.interceptors.request.use(
    config => {
        // 确保URL是完整的
        if (!config.url.startsWith('http')) {
            config.url = `${API_BASE_URL}${config.url}`;
        }
        console.log('发送请求:', {
            url: config.url,
            method: config.method,
            headers: config.headers,
            data: config.data
        });
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
        console.log('收到响应:', {
            status: response.status,
            headers: response.headers,
            data: response.data
        });
        return response;
    },
    error => {
        if (error.code === 'ECONNABORTED') {
            console.error('请求超时，请稍后重试');
            return Promise.reject(new Error('请求超时，请稍后重试'));
        }
        console.error('响应错误:', {
            message: error.message,
            response: error.response ? {
                status: error.response.status,
                data: error.response.data,
                headers: error.response.headers
            } : 'No response'
        });
        return Promise.reject(error);
    }
);

// 获取指定版本的所有题目
export const getIeltsQuestions = async (version) => {
    try {
        console.log('正在获取题目，版本:', version);
        const response = await api.get(`/ielts/questions/${version}`);
        console.log('收到响应:', response);
        return response.data;
    } catch (error) {
        console.error('获取题目失败:', error);
        throw error;
    }
};

// 获取指定版本和测试号的题目
export const getIeltsQuestion = async (version, test) => {
    try {
        console.log(`正在获取题目，版本: ${version}, 测试: ${test}`);
        const response = await api.get(`/ielts/question/${version}/${test}`);
        console.log('收到响应:', response);
        return response.data;
    } catch (error) {
        console.error('获取题目失败:', error);
        throw error;
    }
};

// 评估作文并获取润色结果
export const evaluateEssay = async (essay, taskType, topic) => {
    try {
        console.log('正在评估作文...');
        const response = await api.post('/ielts/evaluate', {
            essay,
            task_type: taskType,
            topic
        });
        console.log('评估完成:', response.data);
        return response.data;
    } catch (error) {
        console.error('评估作文失败:', error);
        if (error.response) {
            console.error('错误响应:', error.response.data);
        }
        throw error;
    }
};

// 获取范文
export const getSampleEssay = async (version, test) => {
    try {
        console.log('正在获取范文...');
        const response = await api.get(`/ielts/sample/${encodeURIComponent(version)}/${encodeURIComponent(test)}`);
        console.log('获取范文完成:', response.data);
        return response.data;
    } catch (error) {
        console.error('获取范文失败:', error);
        if (error.response) {
            console.error('错误响应:', error.response.data);
        }
        throw error;
    }
}; 