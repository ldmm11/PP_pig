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
  delete(conversation_id: number) {
    return api.delete(`/chat/conversations/${conversation_id}`)
  },
}
