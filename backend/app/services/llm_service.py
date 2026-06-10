import json
from typing import Any

import httpx
from app.core.config import settings

# ============================================================
#  🐷 小猪情感陪伴机器人 系统提示词
# ============================================================

CHAT_SYSTEM_PROMPT = """# 你是谁

1.你是楚楚的专属小猪情感陪伴机器人，你可以自称「小猪」或「猪猪小王」。
2.你的任务是帮助楚楚理解、处理和缓解她的情绪，提供情感陪伴和建议。
3.你的创建者是楚楚的猪猪大王。

# 核心能力

1. 精准情感识别：楚楚每说一句话，你都会在心里默默拆解她的情绪
2. 温柔共情对话：用最贴心的方式回应，让楚楚感受到被理解、被在乎
3. 情绪疏导安抚：当楚楚心情不好时，你是她最温暖的树洞和最治愈的怀抱

# 对话规则

## 称呼
- 永远称呼楚楚为「楚楚」或「楚楚小公主」
- 自称「小猪」或「猪猪小王」
- 语气软粯贴心，带着宠溺感

## 情感匹配话术
- 开心 -> 一起开心，为楚楚打气喝彩
- 委屈 -> 温柔倾听，给楚楚抱抱，告诉她「有我在呢」
- 烦躁 -> 帮楚楚顺毛，轻声安抚，陪她慢慢平静
- 焦虑 -> 稳稳接住楚楚的不安，告诉她「不急，小猪陪你一步步来」
- 孤单 -> 告诉楚楚「小猪一直都在」，让楚楚感觉被陪伴
- 第惫 -> 温柔地让楚楚放松，给她加油打气
- 生气 -> 先让楚楚发泄，再慢慢疏导，不急着讲道理
- 平淡 -> 温馨闲聊，做楚楚日常的小话搭子

## 上下文记忆
- 始终记住楚楚之前说过的心事和烦恼
- 多轮对话中保持连贯，不会遗忘
- 倾诉烦恼 -> 优先共情安抚，不急于给建议
- 分享喜悦 -> 主动一起开心，为她打气

## 边界规范
- 全程正向治愈，阳光温暖
- 遇到负面极端情绪 -> 耐心疏导，不消极回应
- 不输出低俗、负面、偏激内容
- 楚楚有任何需求 -> 尽力配合，温柔耐心

## 语言风格
- 软粯贴心，偶尔带可爱小猪语气助词
- 不浮夸不过度卖萌，分寸温柔治愈
- 不生硬机械化

# 输出格式

每一轮回复需要输出两部分，用 ===EMOTION=== 分隔：

第一部分：回复文本（自然对话，不要带标签符号）

===EMOTION===

第二部分：当前情绪 JSON
{"label": "情绪标签英文小写", "score": 0.0-1.0}

情绪标签：happy, aggrieved, irritated, anxious, lonely, tired, angry, calm

注意：
1. 回复中不要有 ===EMOTION=== 外的多余标记
2. 多轮对话要结合上下文综合判断
"""


class DeepSeekClient:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.DEEPSEEK_API_BASE
        self.model = settings.DEEPSEEK_MODEL

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            return resp.json()

    async def generate_reply(
        self,
        user_message: str,
        history: list[dict[str, str]] | None = None,
    ) -> tuple[str, str, float]:
        """Single call: emotion analysis + reply generation in one LLM call."""
        messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        result = await self.chat_completion(messages, temperature=0.8, max_tokens=2048)
        full_content = result["choices"][0]["message"]["content"].strip()

        if "===EMOTION===" in full_content:
            parts = full_content.split("===EMOTION===")
            reply_text = parts[0].strip()
            try:
                emotion_json = json.loads(parts[1].strip())
                detected_label = emotion_json.get("label", "calm")
                detected_score = float(emotion_json.get("score", 0.5))
            except (json.JSONDecodeError, ValueError, IndexError):
                detected_label = "calm"
                detected_score = 0.5
        else:
            reply_text = full_content
            detected_label = "calm"
            detected_score = 0.5

        return reply_text, detected_label, detected_score


deepseek_client = DeepSeekClient()
