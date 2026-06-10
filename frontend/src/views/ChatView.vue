<template>
  <div class="chat-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h3>楚楚的猪猪小王</h3>
      </div>
      <div class="new-chat">
        <el-button type="primary" style="width:100%" @click="startNewChat">
          <el-icon><Plus /></el-icon> 新对话
        </el-button>
      </div>
      <div class="conv-list">
        <div
          v-for="conv in conversations"
          :key="conv.id"
          class="conv-item"
          :class="{ active: conv.id === currentConvId }"
          @click="switchConversation(conv.id)"
        >
          <el-icon style="margin-right:6px"><ChatDotRound /></el-icon>
          <span class="conv-title">{{ conv.title }}</span>
          <el-icon class="conv-delete" @click.stop="removeConversation(conv.id)"><Delete /></el-icon>
        </div>
      </div>
      <div class="sidebar-footer">
        <span @click="router.push('/trends')" style="cursor:pointer">
          <el-icon><DataAnalysis /></el-icon> 情绪趋势
        </span>
      </div>
    </div>

    <!-- Main Chat Area -->
    <div class="main-area">
      <div class="messages" ref="messagesRef">
        <div v-if="messages.length === 0" class="empty-hint">
          <el-icon :size="48" color="#c0c4cc"><ChatLineSquare /></el-icon>
          <p>开始一段新的对话吧</p>
        </div>
        <div v-for="msg in messages" :key="msg.id" class="message-row" :class="msg.role">
          <el-avatar :size="36" :class="msg.role">
            {{ msg.role === "user" ? "楚楚" : "🤖" }}
          </el-avatar>
          <div class="bubble">
            <div class="text">{{ msg.content }}</div>
            <div v-if="msg.emotion_label" class="emotion-tag">
              <el-tag :type="emotionTagType(msg.emotion_label)" size="small">
                {{ emotionLabelMap[msg.emotion_label] || msg.emotion_label }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <div class="input-area">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="3"
          placeholder="说点什么吧..."
          @keydown.enter.prevent="sendMessage"
          :disabled="sending"
        />
        <el-button type="primary" @click="sendMessage" :loading="sending" style="margin-left:12px">
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useDeviceStore } from "@/stores/user";
import { chatApi } from "@/api";

const router = useRouter();
const deviceStore = useDeviceStore();

const conversations = ref<any[]>([]);
const messages = ref<any[]>([]);
const currentConvId = ref<number | null>(null);
const inputText = ref("");
const sending = ref(false);
const messagesRef = ref<HTMLElement | null>(null);

const emotionLabelMap: Record<string, string> = {
  happy: "开心",
  aggrieved: "委屈",
  irritated: "烦躁",
  anxious: "焦虑",
  lonely: "孤单",
  tired: "第惫",
  angry: "生气",
  calm: "平淡",
};

function emotionTagType(label: string): string {
  const map: Record<string, string> = {
    happy: "success",
    aggrieved: "warning",
    irritated: "warning",
    anxious: "warning",
    lonely: "info",
    tired: "info",
    angry: "danger",
    calm: "",
  };
  return map[label] || "";
}

async function loadConversations() {
  try {
    const res = await chatApi.conversations(deviceStore.deviceId);
    conversations.value = res.data;
  } catch { /* ignore */ }
}

async function loadMessages(convId: number) {
  try {
    const res = await chatApi.messages(convId);
    messages.value = res.data;
    await scrollToBottom();
  } catch { /* ignore */ }
}

async function switchConversation(convId: number) {
  currentConvId.value = convId;
  await loadMessages(convId);
}

async function startNewChat() {
  currentConvId.value = null;
  messages.value = [];
  inputText.value = "";
  await loadConversations();
}

async function removeConversation(convId: number) {
  try {
    await chatApi.delete(convId);
    if (currentConvId.value === convId) {
      currentConvId.value = null;
      messages.value = [];
    }
    await loadConversations();
  } catch { /* ignore */ }
}

async function sendMessage() {
  const text = inputText.value.trim();
  if (!text) return;
  sending.value = true;
  try {
    const res = await chatApi.send({
      device_id: deviceStore.deviceId,
      conversation_id: currentConvId.value ?? undefined,
      message: text,
    });
    currentConvId.value = res.data.conversation_id;
    inputText.value = "";
    if (currentConvId.value !== null) await loadMessages(currentConvId.value);
    await loadConversations();
  } finally {
    sending.value = false;
  }
}

async function scrollToBottom() {
  await nextTick();
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
  }
}

onMounted(async () => {
  deviceStore.getDeviceId();
  await loadConversations();
});
</script>

<style scoped>
.chat-layout {
  display: flex;
  height: 100vh;
}
.sidebar {
  width: 260px;
  background: #fff;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}
.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
}
.sidebar-header h3 { margin: 0; font-size: 16px; }
.new-chat { padding: 12px 16px; }
.conv-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px;
}
.conv-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}
.conv-item:hover { background: #f5f7fa; }
.conv-item.active { background: #ecf5ff; color: #409eff; }
.conv-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.conv-delete {
  display: none;
  margin-left: auto;
  font-size: 14px;
  color: #c0c4cc;
  cursor: pointer;
  flex-shrink: 0;
}
.conv-item:hover .conv-delete {
  display: inline-flex;
}
.conv-delete:hover {
  color: #f56c6c;
}
.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #409eff;
}
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
.empty-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}
.empty-hint p { margin-top: 12px; font-size: 16px; }
.message-row {
  display: flex;
  margin-bottom: 20px;
  gap: 10px;
}
.message-row.user { flex-direction: row-reverse; }
.bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  line-height: 1.6;
}
.message-row.user .bubble { background: #409eff; color: #fff; }
.emotion-tag { margin-top: 6px; }
.input-area {
  display: flex;
  align-items: flex-end;
  padding: 16px 20px;
  background: #fff;
  border-top: 1px solid #e4e7ed;
}
.input-area .el-textarea { flex: 1; }
</style>
