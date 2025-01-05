import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    headers: {
      'Content-Type': 'application/json',
    },
  });
const app = createApp(App);
app.provide('$api', apiClient);
app.use(ElementPlus);
app.mount('#app');
