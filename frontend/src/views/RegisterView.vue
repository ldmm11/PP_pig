<template>
  <div class="register-page">
    <el-card class="register-card">
      <template #header><h2>注册</h2></template>
      <el-form :model="form" label-width="80px" @keyup.enter="handleRegister">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="2-50个字符" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="至少6位" />
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" placeholder="选填" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading" style="width:100%">
            注 册
          </el-button>
        </el-form-item>
      </el-form>
      <div class="nav-link">
        已有账号？<router-link to="/login">去登录</router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { ElMessage } from "element-plus";

const router = useRouter();
const userStore = useUserStore();
const loading = ref(false);

const form = reactive({ username: "", password: "", nickname: "" });

async function handleRegister() {
  if (!form.username || !form.password) {
    ElMessage.warning("请填写用户名和密码");
    return;
  }
  loading.value = true;
  try {
    await userStore.register(form.username, form.password, form.nickname || undefined);
    ElMessage.success("注册成功");
    router.push("/");
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.register-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.register-card {
  width: 420px;
}
.nav-link {
  text-align: center;
  font-size: 14px;
  color: #666;
}
.nav-link a {
  color: #409eff;
  text-decoration: none;
}
</style>
