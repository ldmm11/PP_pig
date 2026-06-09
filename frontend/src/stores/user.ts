import { defineStore } from "pinia";
import { ref } from "vue";

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
