import json
from typing import Any

import httpx
from app.core.config import settings


class DeepSeekClient:
    """DeepSeek OpenAI-compatible API client."""

    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.DEEPSEEK_API_BASE
        self.model = settings.DEEPSEEK_MODEL

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024,
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

    async def analyze_emotion(self, text: str) -> dict[str, Any]:
        """Analyze emotion using a system prompt."""
        system_prompt = """你是一个专业的情绪分析助手。请分析用户输入文本中的情绪，返回 JSON 格式结果：
{
    "label": "happy|sad|angry|anxious|neutral|surprised|fearful|disgusted",
    "score": 0.0-1.0,
    "explanation": "简短的中文解释（20字以内）"
}
只返回 JSON，不要多余内容。"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
        result = await self.chat_completion(messages, temperature=0.3, max_tokens=256)
        content = result["choices"][0]["message"]["content"].strip()
        # 去掉可能的 markdown 代码块标记
        content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(content)

    async def generate_reply(
        self,
        user_message: str,
        emotion_label: str,
        emotion_score: float,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        system_prompt = f"""你是一个温暖的机器人情绪对话助手。
你可以感知用户的情绪，并用富有同理心的方式回应。

当前检测到的用户情绪：{emotion_label}（强度：{emotion_score:.2f}）
- 如果用户情绪低落，请给予安慰和鼓励。
- 如果用户开心，请分享喜悦。
- 如果用户愤怒或焦虑，请保持冷静并帮助疏导。
- 始终保持友好、真诚的对话风格。"""

        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        result = await self.chat_completion(messages, temperature=0.8, max_tokens=1024)
        return result["choices"][0]["message"]["content"].strip()


deepseek_client = DeepSeekClient()
