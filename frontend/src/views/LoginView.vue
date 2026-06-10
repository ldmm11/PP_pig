<template>
  <div class="login-page">
    <el-card class="login-card">
      <template #header><h2 style="text-align:center">情绪对话助手</h2></template>
      <el-form :model="form" label-width="0" @keyup.enter="handleLogin">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" show-password placeholder="密码" :prefix-icon="Lock" size="large" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" style="width:100%" size="large">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { User, Lock } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

const router = useRouter();
const userStore = useUserStore();
const loading = ref(false);

const form = reactive({ username: "root", password: "" });

async function handleLogin() {
  if (!form.username || !form.password) {
    ElMessage.warning("请输入用户名和密码");
    return;
  }
  loading.value = true;
  try {
    await userStore.login(form.username, form.password);
    ElMessage.success("登录成功");
    router.push("/");
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || "登录失败");
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card { width: 380px; }
</style>
