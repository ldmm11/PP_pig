<template>
  <div
    class="pig-container"
    :style="{ width: size + 'px', height: size + 'px' }"
    @click="handleClick"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
    ref="containerRef"
  >
    <transition name="bubble">
      <div v-if="showBubble" class="emoji-bubble" :key="bubbleEmoji">
        {{ bubbleEmoji }}
      </div>
    </transition>

    <svg
      :viewBox="viewBox"
      class="pig-svg"
      :class="{ bouncing: isBouncing, talking: isTalking }"
    >
      <defs>
        <radialGradient id="bodyGrad" cx="40%" cy="35%" r="60%">
          <stop offset="0%" stop-color="#FFD1DC" />
          <stop offset="100%" stop-color="#FFB5C2" />
        </radialGradient>
        <radialGradient id="earGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#FFC8D4" />
          <stop offset="100%" stop-color="#FF9EB5" />
        </radialGradient>
        <radialGradient id="snoutGrad" cx="50%" cy="40%" r="50%">
          <stop offset="0%" stop-color="#FFC8D4" />
          <stop offset="100%" stop-color="#FF9EB5" />
        </radialGradient>
        <radialGradient id="cheekGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#FF8A9E" stop-opacity="0.6" />
          <stop offset="100%" stop-color="#FF8A9E" stop-opacity="0" />
        </radialGradient>
      </defs>

      <ellipse cx="70" cy="168" rx="14" ry="10" fill="#FFB5C2" />
      <ellipse cx="130" cy="168" rx="14" ry="10" fill="#FFB5C2" />

      <ellipse cx="100" cy="130" rx="58" ry="46" fill="url(#bodyGrad)" />

      <path
        d="M 155 125 Q 175 115 170 100 Q 165 85 175 90"
        stroke="#FF9EB5"
        stroke-width="4"
        fill="none"
        stroke-linecap="round"
      />

      <rect x="55" y="145" width="16" height="22" rx="8" fill="#FFB5C2" />
      <rect x="129" y="145" width="16" height="22" rx="8" fill="#FFB5C2" />

      <g class="ear left-ear">
        <ellipse cx="62" cy="50" rx="18" ry="24" fill="url(#earGrad)" />
        <ellipse cx="62" cy="50" rx="10" ry="16" fill="#FF8CA0" />
      </g>
      <g class="ear right-ear">
        <ellipse cx="138" cy="50" rx="18" ry="24" fill="url(#earGrad)" />
        <ellipse cx="138" cy="50" rx="10" ry="16" fill="#FF8CA0" />
      </g>

      <ellipse cx="100" cy="80" rx="52" ry="48" fill="url(#bodyGrad)" />

      <ellipse cx="60" cy="88" rx="12" ry="8" fill="url(#cheekGrad)" />
      <ellipse cx="140" cy="88" rx="12" ry="8" fill="url(#cheekGrad)" />

      <g class="eye-group">
        <ellipse
          :cx="leftEyeX"
          cy="72"
          :rx="eyeWidth"
          ry="10"
          fill="white"
          class="eye-white"
        />
        <ellipse
          :cx="rightEyeX"
          cy="72"
          :rx="eyeWidth"
          ry="10"
          fill="white"
          class="eye-white"
        />
        <circle :cx="leftPupilX" :cy="leftPupilY" r="5" fill="#333" class="pupil" />
        <circle :cx="rightPupilX" :cy="rightPupilY" r="5" fill="#333" class="pupil" />
        <circle :cx="leftPupilX - 2" :cy="leftPupilY - 2.5" r="2" fill="white" />
        <circle :cx="rightPupilX - 2" :cy="rightPupilY - 2.5" r="2" fill="white" />
      </g>

      <path :d="leftBrowPath" :stroke="browColor" stroke-width="3" fill="none" stroke-linecap="round" />
      <path :d="rightBrowPath" :stroke="browColor" stroke-width="3" fill="none" stroke-linecap="round" />

      <ellipse cx="100" cy="92" rx="22" ry="16" fill="url(#snoutGrad)" />
      <ellipse cx="94" cy="92" rx="4" ry="5" fill="#D46B7A" />
      <ellipse cx="106" cy="92" rx="4" ry="5" fill="#D46B7A" />

      <path :d="mouthPath" :stroke="mouthColor" stroke-width="2.5" fill="none" stroke-linecap="round" />
    </svg>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

const props = withDefaults(
  defineProps<{
    emotion?: string;
    size?: number;
  }>(),
  { emotion: "calm", size: 180 }
);

const emit = defineEmits<{ click: [] }>();

const containerRef = ref<HTMLElement | null>(null);
const isBouncing = ref(false);
const isTalking = ref(false);
const showBubble = ref(false);
const bubbleEmoji = ref("❤️");
const mouseX = ref(0.5);
const mouseY = ref(0.5);

const viewBox = "0 0 200 200";

const eyeWidth = computed(() => {
  switch (props.emotion) {
    case "happy": return 9;
    case "angry": return 8;
    case "tired": return 6;
    default: return 10;
  }
});

const leftEyeX = computed(() => 80);
const rightEyeX = computed(() => 120);

const pupilOffset = computed(() => {
  const maxOffset = 4;
  return {
    x: (mouseX.value - 0.5) * 2 * maxOffset,
    y: (mouseY.value - 0.5) * 2 * maxOffset,
  };
});

const leftPupilX = computed(() => leftEyeX.value + pupilOffset.value.x);
const leftPupilY = computed(() => 72 + pupilOffset.value.y);
const rightPupilX = computed(() => rightEyeX.value + pupilOffset.value.x);
const rightPupilY = computed(() => 72 + pupilOffset.value.y);

const browColor = computed(() => props.emotion === "angry" ? "#D46B7A" : "#666");

const leftBrowPath = computed(() => {
  switch (props.emotion) {
    case "aggrieved": return "M 66 58 Q 72 52 80 58";
    case "irritated": return "M 66 62 L 80 58";
    case "anxious": return "M 66 56 Q 73 50 80 56";
    case "lonely": return "M 66 62 Q 73 66 80 62";
    case "tired": return "M 66 64 L 80 62";
    case "angry": return "M 66 58 L 80 64";
    default: return "M 66 60 Q 73 56 80 60";
  }
});

const rightBrowPath = computed(() => {
  switch (props.emotion) {
    case "aggrieved": return "M 120 58 Q 127 52 134 58";
    case "irritated": return "M 120 58 L 134 62";
    case "anxious": return "M 120 56 Q 127 50 134 56";
    case "lonely": return "M 120 62 Q 127 66 134 62";
    case "tired": return "M 120 62 L 134 64";
    case "angry": return "M 120 64 L 134 58";
    default: return "M 120 60 Q 127 56 134 60";
  }
});

const mouthColor = computed(() => {
  switch (props.emotion) {
    case "happy": return "#FF6B81";
    default: return "#D46B7A";
  }
});

const mouthPath = computed(() => {
  switch (props.emotion) {
    case "happy": return "M 78 98 Q 100 120 122 98";
    case "aggrieved": return "M 82 104 Q 95 112 100 104 Q 105 96 118 104";
    case "irritated": return "M 82 100 L 118 100";
    case "anxious": return "M 85 98 Q 95 112 100 98 Q 105 84 115 98";
    case "lonely": return "M 82 98 Q 100 85 118 98";
    case "tired": return "M 88 100 Q 100 103 112 100";
    case "angry": return "M 82 94 L 95 100 L 100 94 L 105 100 L 118 94";
    default: return "M 85 96 Q 100 108 115 96";
  }
});

const emojiMap: Record<string, string> = {
  happy: "😊", aggrieved: "🥺", irritated: "😤",
  anxious: "😰", lonely: "😢", tired: "😴",
  angry: "😠", calm: "😌",
};

function handleClick() {
  isBouncing.value = true;
  setTimeout(() => (isBouncing.value = false), 500);
  bubbleEmoji.value = emojiMap[props.emotion] || "😌";
  showBubble.value = true;
  setTimeout(() => (showBubble.value = false), 1500);
  emit("click");
}

function handleMouseMove(event: MouseEvent) {
  if (!containerRef.value) return;
  const rect = containerRef.value.getBoundingClientRect();
  mouseX.value = (event.clientX - rect.left) / rect.width;
  mouseY.value = (event.clientY - rect.top) / rect.height;
}

function handleMouseLeave() {
  mouseX.value = 0.5;
  mouseY.value = 0.5;
}
</script>

<style scoped>
.pig-container {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
}
.pig-svg {
  width: 100%;
  height: 100%;
  overflow: visible;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pig-svg:hover { transform: scale(1.05); }
.pig-svg:not(.bouncing) { animation: breathe 3s ease-in-out infinite; }
@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}
.pig-svg.bouncing { animation: bounce 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes bounce {
  0% { transform: scale(1); }
  30% { transform: scale(1.15); }
  60% { transform: scale(0.95); }
  100% { transform: scale(1); }
}
.ear { transform-origin: center bottom; transition: transform 0.3s; }
.pig-container:hover .left-ear { transform: rotate(-10deg); }
.pig-container:hover .right-ear { transform: rotate(10deg); }
@keyframes blink { 0%, 95%, 100% { transform: scaleY(1); } 97% { transform: scaleY(0.1); } }
.eye-white { animation: blink 4s ease-in-out infinite; transform-origin: center center; }
.emoji-bubble {
  position: absolute; top: -10px; right: 10px; font-size: 28px;
  z-index: 10; pointer-events: none;
}
.bubble-enter-active { animation: float-up 1.5s ease-out forwards; }
.bubble-leave-active { animation: fade-out 0.3s ease-out forwards; }
@keyframes float-up {
  0% { opacity: 1; transform: translateY(0) scale(0.5); }
  30% { opacity: 1; transform: translateY(-10px) scale(1.2); }
  100% { opacity: 0; transform: translateY(-40px) scale(1); }
}
@keyframes fade-out { to { opacity: 0; transform: scale(0.5); } }
</style>
