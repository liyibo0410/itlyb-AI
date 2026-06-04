from dotenv import load_dotenv, find_dotenv
import os
import sys
import time
import asyncio

# 自动找到项目根目录的 .env
load_dotenv(find_dotenv())

# ===================== 导入依赖 =====================
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# ===================== 1. 加载硅基流动配置 =====================
api_key = os.getenv("SILICON_API_KEY")
base_url = os.getenv("SILICON_BASE_URL")

# 初始化模型（免费、稳定）
llm = ChatOpenAI(
    model="Qwen/Qwen3-8B",
    api_key=api_key,
    base_url=base_url,
    temperature=0.7,
    max_tokens=1024
)

# ===================== 作业任务1：同步调用 invoke =====================
print("=" * 50)
print("【作业1】同步调用 invoke")
print("=" * 50)

resp1 = llm.invoke("什么是LangChain？")
print("回答：", resp1.content)
print()

# ===================== 作业任务2：流式输出 stream（打字机效果） =====================
print("=" * 50)
print("【作业2】流式调用 stream")
print("=" * 50)

print("AI：", end="")
full_ans = ""
for chunk in llm.stream("写一首关于夏天的短诗"):
    full_ans += chunk.content
    print(chunk.content, end="", flush=True)
print("\n")

# ===================== 作业任务3：批量调用 batch =====================
print("=" * 50)
print("【作业3】批量调用 batch")
print("=" * 50)

questions = [
    "Python是什么？",
    "什么是虚拟环境？",
    "什么是API？"
]

results = llm.batch(questions)
for q, a in zip(questions, results):
    print(f"问：{q}")
    print(f"答：{a.content[:50]}...")
    print("-" * 30)
print()

# ===================== 作业任务4：上下文对话（Message格式） =====================
print("=" * 50)
print("【作业4】上下文对话")
print("=" * 50)

messages = [
    SystemMessage(content="你是一个AI助手，回答简洁友好"),
    HumanMessage(content="你好，我叫小明"),
    AIMessage(content="你好小明！很高兴认识你！"),
    HumanMessage(content="我叫什么名字？")
]

resp4 = llm.invoke(messages)
print("AI回答：", resp4.content)