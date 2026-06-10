import axios from "axios";
import { ElMessage } from "element-plus";

const API_BASE = import.meta.env.VITE_API_BASE || "/api/v1";

const http = axios.create({ baseURL: API_BASE, timeout: 60000 });

// Inject token + device_id
http.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = Bearer ;
  }
  const deviceId = localStorage.getItem("device_id");
  if (deviceId) {
    if (config.method === "get" || config.method === "GET") {
      config.params = { ...config.params, device_id: deviceId };
    } else if (config.data && typeof config.data === "object" && !(config.data instanceof FormData)) {
      config.data = { ...config.data, device_id: deviceId };
    }
  }
  return config;
});

// 401 redirect to login
http.interceptors.response.use(
  (resp) => resp,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default http;

// ===== Auth API =====
export const authApi = {
  login: (data: { username: string; password: string }) => http.post("/auth/login", data),
  me: () => http.get("/auth/me"),
};

// ===== Chat API =====
export const chatApi = {
  send: (data: { conversation_id?: number; message: string }) => http.post("/chat/send", data),
  conversations: () => http.get("/chat/conversations"),
  messages: (convId: number) => http.get(/chat/conversations//messages),
};

// ===== Emotion API =====
export const emotionApi = {
  trends: () => http.get("/emotion/trends"),
};
