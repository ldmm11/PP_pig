import axios from "axios"

const api = axios.create({
  baseURL: "/api/v1",
  timeout: 30000,
})

export const chatApi = {
  send(data: { device_id: string; conversation_id?: number; message: string }) {
    return api.post("/chat/send", data)
  },
  conversations(device_id: string) {
    return api.get("/chat/conversations", { params: { device_id } })
  },
  messages(conversation_id: number) {
    return api.get(`/chat/conversations/${conversation_id}/messages`)
  },
  delete(conv_id: number) {
    return api.delete(`/chat/conversations/${conv_id}`)
  },
}

export const emotionApi = {
  trends(device_id: string) {
    return api.get("/emotion/trends", { params: { device_id } })
  },
  analyze(data: { device_id: string; text: string }) {
    return api.post("/emotion/analyze", data)
  },
}
