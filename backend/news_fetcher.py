def fetch_news(keywords):
    # 模拟抓取新闻标题
    news = []
    for kw in keywords:
        news.append(f"【{kw}】今天的头条新闻")
        news.append(f"【{kw}】技术进展迅速")
    return news
