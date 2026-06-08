import axios from "axios";
import { ElMessage } from "element-plus";

const http = axios.create({
  baseURL: "/api/v1",
  timeout: 60000,
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    const msg = error.response?.data?.detail || error.message || "请求失败";
    ElMessage.error(msg);
    return Promise.reject(error);
  }
);

export default http;

// ===== Auth API =====
export const authApi = {
  login: (data: { username: string; password: string }) =>
    http.post("/auth/login", data),
  register: (data: { username: string; password: string; nickname?: string }) =>
    http.post("/auth/register", data),
  me: () => http.get("/auth/me"),
};

// ===== Chat API =====
export const chatApi = {
  send: (data: { conversation_id?: number; message: string }) =>
    http.post("/chat/send", data),
  conversations: () => http.get("/chat/conversations"),
  messages: (convId: number) => http.get(`/chat/conversations/${convId}/messages`),
};

// ===== Emotion API =====
export const emotionApi = {
  analyze: (data: { text: string }) => http.post("/emotion/analyze", data),
  trends: () => http.get("/emotion/trends"),
};
