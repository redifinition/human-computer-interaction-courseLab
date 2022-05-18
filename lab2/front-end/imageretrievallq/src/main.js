import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'
import {VueAxios} from "./utils/request";
//+引入组件库及相关样式
import ElementUI from 'element-ui'
import axios from 'axios'
Vue.prototype.$axios = axios    //全局注册，使用方法为:this.$axios

Vue.use(Antd)
//让Vue使用ElementUI
Vue.use(ElementUI)


// mount axios to `Vue.$http` and `this.$http`
Vue.use(VueAxios)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
