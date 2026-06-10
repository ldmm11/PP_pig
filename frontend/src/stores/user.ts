import { defineStore } from "pinia";
import { ref } from "vue";
import { authApi } from "@/api";

export const useUserStore = defineStore("user", () => {
  const token = ref(localStorage.getItem("token") || "");
  const username = ref(localStorage.getItem("username") || "");
  const isAdmin = ref(localStorage.getItem("is_admin") === "true");

  function setAuth(t: string, u: string, admin: boolean) {
    token.value = t;
    username.value = u;
    isAdmin.value = admin;
    localStorage.setItem("token", t);
    localStorage.setItem("username", u);
    localStorage.setItem("is_admin", String(admin));
  }

  function logout() {
    token.value = "";
    username.value = "";
    isAdmin.value = false;
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("is_admin");
    window.location.href = "/login";
  }

  async function login(user: string, pass: string) {
    const res = await authApi.login({ username: user, password: pass });
    setAuth(res.data.access_token, res.data.username, res.data.is_admin);
  }

  return { token, username, isAdmin, login, logout, setAuth };
});

export const useDeviceStore = defineStore("device", () => {
  const deviceId = ref(localStorage.getItem("device_id") || "");

  function getDeviceId(): string {
    if (!deviceId.value) {
      const id = "device_" + Date.now() + "_" + Math.random().toString(36).substring(2, 10);
      deviceId.value = id;
      localStorage.setItem("device_id", id);
    }
    return deviceId.value;
  }

  return { deviceId, getDeviceId };
});
