# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from apscheduler.schedulers.background import BackgroundScheduler
from news_fetcher import fetch_news
from ai_summary import summarize_news
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# 设置允许跨域的源（前端本地开发端口）
origins = [
    "http://localhost:5173",  # Vite 开发服务器默认端口
    # 你也可以加其他地址，比如部署后的域名
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 允许的源
    allow_credentials=True,
    allow_methods=["*"],              # 允许所有 HTTP 方法
    allow_headers=["*"],              # 允许所有 Header
)


# 全局变量：关键词配置与摘要内容
keyword_config = {"keywords": []}
latest_summary = {"text": "暂无摘要"}

# 接受关键词请求体模型
class KeywordConfig(BaseModel):
    keywords: List[str]

@app.get("/status")
def status():
    return {"message": "hello world"}

@app.post("/config")
def set_config(config: KeywordConfig):
    keyword_config["keywords"] = config.keywords
    return {"message": "配置成功", "keywords": config.keywords}

@app.get("/summary")
def get_summary():
    return {
        "keywords": keyword_config["keywords"],
        "summary": latest_summary["text"]
    }

# 定时任务逻辑
def scheduled_task():
    keywords = keyword_config["keywords"]
    if not keywords:
        print("❌ 无关键词，跳过新闻抓取")
        return

    print("⏰ 正在抓取新闻...")
    news_list = fetch_news(keywords)
    print("✅ 抓取到：", news_list)

    print("🧠 正在调用 GPT 总结...")
    summary = summarize_news(news_list)
    latest_summary["text"] = summary
    print("✅ 摘要已更新")

# 启动定时器（默认1小时一次）
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', hours=1)
scheduler.start()

import atexit
atexit.register(lambda: scheduler.shutdown())


# 添加手动触发接口
@app.get("/trigger")
def trigger_task():
    scheduled_task()
    return {"message": "已手动触发"}
    