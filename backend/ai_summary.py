import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# DeepSeek 的 API key（你需要从 https://platform.deepseek.com/ 获取）
api_key = os.getenv("DEEPSEEK_API_KEY")

# 初始化 OpenAI 客户端，使用 DeepSeek 的 base_url
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"  # DeepSeek 的 API 基础地址
)

def summarize_news(news_list: list[str]) -> str:
    if not news_list:
        return "暂无新闻内容"

    prompt = (
        "请根据以下新闻标题，生成一段简洁的中文摘要，不超过150字：\n\n"
        + "\n".join(news_list)
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # DeepSeek 的模型名称（可替换）
            messages=[
                {"role": "system", "content": "你是一个擅长信息总结的助手"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ GPT 请求失败：", e)
        return "摘要生成失败（DeepSeek 错误）"
