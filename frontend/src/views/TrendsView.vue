<template>
  <div class="trends-page">
    <div class="trends-header">
      <el-button @click="router.push('/')">
        <el-icon><ArrowLeft /></el-icon> 返回对话
      </el-button>
      <h2>情绪趋势分析</h2>
    </div>
    <el-card v-loading="loading">
      <div ref="chartRef" style="width:100%; height:400px"></div>
    </el-card>
    <div class="stats" v-if="!loading && trends.length">
      <el-row :gutter="16">
        <el-col :span="6" v-for="(count, label) in emotionStats" :key="label">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-label">{{ emotionLabelMap[label] || label }}</div>
              <div class="stat-count">{{ count }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { emotionApi } from "@/api";
import * as echarts from "echarts";

const router = useRouter();
const loading = ref(false);
const trends = ref<any[]>([]);
const chartRef = ref<HTMLElement | null>(null);

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

const emotionStats = computed(() => {
  const counts: Record<string, number> = {};
  for (const t of trends.value) {
    counts[t.label] = (counts[t.label] || 0) + 1;
  }
  return counts;
});

function renderChart() {
  if (!chartRef.value || !trends.value.length) return;
  const chart = echarts.init(chartRef.value);
  const data = [...trends.value].reverse();
  chart.setOption({
    tooltip: { trigger: "axis" },
    xAxis: {
      type: "category",
      data: data.map((d) => d.created_at?.slice(5, 16) || ""),
      axisLabel: { rotate: 30 },
    },
    yAxis: { type: "value", min: 0, max: 1 },
    series: [
      {
        name: "情绪强度",
        type: "line",
        data: data.map((d) => d.score),
        smooth: true,
        areaStyle: { opacity: 0.15 },
        itemStyle: {
          color: (params: any) => {
            const map: Record<string, string> = {
              happy: "#67c23a",
              aggrieved: "#e6a23c",
              irritated: "#e6a23c",
              anxious: "#e6a23c",
              lonely: "#909399",
              tired: "#909399",
              angry: "#f56c6c",
              calm: "#409eff",
            };
            return map[data[params.dataIndex]?.label] || "#409eff";
          },
        },
      },
    ],
    grid: { left: 50, right: 20, bottom: 40, top: 20 },
  });
  window.addEventListener("resize", () => chart.resize());
}

onMounted(async () => {
  loading.value = true;
  try {
    const res = await emotionApi.trends();
    trends.value = res.data;
    await nextTick();
    renderChart();
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.trends-page {
  padding: 24px;
  max-width: 1000px;
  margin: 0 auto;
}
.trends-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}
.trends-header h2 { margin: 0; }
.stats { margin-top: 24px; }
.stat-item { text-align: center; }
.stat-label { font-size: 14px; color: #666; }
.stat-count { font-size: 28px; font-weight: bold; margin-top: 4px; }
</style>
