# 必加：加载.env环境变量
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# 大模型配置（完美写法 ✅）
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0.7,
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY")
)

# 定义JSON结构
class Joke(BaseModel):
    title: str = Field(description='笑话的标题,简洁有趣')
    content: str = Field(description='笑话的正文内容,幽默诙谐')
    theme: str = Field(description='笑话的主题,比如 日常、职场、动物')

# JSON解析器
jsp = JsonOutputParser(pydantic_object=Joke)

# 调用模型
res = llm.invoke([
    ('system', jsp.get_format_instructions()),
    ('human', "请你给我讲一个笑话,幽默诙谐")
])

# 输出原始内容
print(res.content)
print(type(res.content))

# 解析成字典
pe = jsp.invoke(res.content)

print("---------------------")
print(type(pe))  # <class 'dict'>
print(pe['title'])
print(pe['content'])
print(pe['theme'])