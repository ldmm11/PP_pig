import { defineStore } from "pinia";
import { ref } from "vue";
import { authApi } from "@/api";
import type { AxiosResponse } from "axios";

interface UserInfo {
  id: number;
  username: string;
  nickname: string;
  avatar_url: string;
}

export const useUserStore = defineStore("user", () => {
  const token = ref(localStorage.getItem("token") || "");
  const userInfo = ref<UserInfo | null>(null);

  async function login(username: string, password: string) {
    const res: AxiosResponse = await authApi.login({ username, password });
    token.value = res.data.access_token;
    localStorage.setItem("token", token.value);
    await fetchUserInfo();
  }

  async function register(username: string, password: string, nickname?: string) {
    const res: AxiosResponse = await authApi.register({ username, password, nickname });
    token.value = res.data.access_token;
    localStorage.setItem("token", token.value);
    await fetchUserInfo();
  }

  async function fetchUserInfo() {
    try {
      const res: AxiosResponse = await authApi.me();
      userInfo.value = res.data;
    } catch {
      logout();
    }
  }

  function logout() {
    token.value = "";
    userInfo.value = null;
    localStorage.removeItem("token");
  }

  return { token, userInfo, login, register, fetchUserInfo, logout };
});
