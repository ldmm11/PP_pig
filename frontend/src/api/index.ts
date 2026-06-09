import axios from "axios";

const http = axios.create({
  baseURL: "/api/v1",
  timeout: 60000,
});

// Automatically inject device_id from localStorage
http.interceptors.request.use((config) => {
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

export default http;

// ===== Chat API =====
export const chatApi = {
  send: (data: { conversation_id?: number; message: string }) =>
    http.post("/chat/send", data),
  conversations: () => http.get("/chat/conversations"),
  messages: (convId: number) => http.get(`/chat/conversations/${convId}/messages`),
};

// ===== Emotion API =====
export const emotionApi = {
  trends: () => http.get("/emotion/trends"),
};
