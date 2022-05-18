import axios from 'axios'
import notification from 'ant-design-vue/es/notification'
import { VueAxios } from './axios'


// 创建 axios 实例
const request = axios.create({
    // API 请求的默认前缀
    baseURL: 'http://100.80.144.51:5000',
    // baseURL: 'http://localhost:8080',
    timeout: 6000, // 请求超时时间
    withCredentials: true
})

// 异常拦截处理器
const errorHandler = (error) => {
    //console.log('error:')
    //console.log(error)
    if (error.response) {
        const data = error.response.data

        if (error.response.status === 403) {
            notification.error({
                message: 'Forbidden',
                description: data.message
            })
        }
        if (error.response.status === 401) {
            notification.error({
                message: 'Unauthorized',
                description: 'Authorization verification failed'
            })
        }
    }
    return Promise.reject(error)
}

// request interceptor
request.interceptors.request.use(config => {
    return config
}, errorHandler)

// response interceptor
request.interceptors.response.use((response) => {
    return response.data
}, errorHandler)

const installer = {
    vm: {},
    install (Vue) {
        Vue.use(VueAxios, request)
    }
}

export default request

export {
    installer as VueAxios,
    request as axios
}
