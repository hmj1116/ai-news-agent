```python
import datetime
import os
import requests

class AINewsAgent:
    def __init__(self):
        self.today = datetime.date.today().strftime("%Y-%m-%d")
        # 你的报告保存路径
        self.report_path = "ai-news-agent/index.html"
        # 钉钉 Webhook 地址 (从环境变量读取)
        self.webhook_url = os.getenv("DINGTALK_WEBHOOK")

    def fetch_mock_news(self):
        """
        模拟抓取最新资讯。
        在实际运行中，你可以通过搜索 API 获取真实数据。
        """
        return [
            {
                "time": "2026-02-19",
                "title": "谷歌发布了更聪明的“大脑”：Gemini 3.1 Pro",
                "source": "Google",
                "desc": "谷歌最近升级了他们的 AI 模型。这个新版本比以前聪明了一倍，能听懂更难的指令了。",
                "easy_talk": "就像你的手机系统从 1.0 升级到了 3.1，它现在不仅跑得快，而且能听懂更难的指令了。"
            },
            {
                "time": "2026-02-17",
                "title": "机器人也能自己买东西了？Agentic Commerce 协议发布",
                "source": "Stripe & OpenAI",
                "desc": "支付巨头 Stripe 和 OpenAI 联手制定了一个新规。以后，你的 AI 助手可以被你授权，直接去网上帮你下单买东西。",
                "easy_talk": "以前 AI 只能告诉你哪双鞋好看，现在你可以直接跟它说“帮我买这双鞋”，它就能自己付钱下单送到你家。"
            }
        ]

    def generate_html(self, news_list):
        """
        生成百科词典风格的 HTML 简报
        """
        html_template = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>AI 智能体百科简报 - {self.today}</title>
            <script src="https://cdn.tailwindcss.com/3.4.17"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
                body {{ font-family: 'Noto+Sans+SC', sans-serif; background-color: #f0f4f8; }}
                .dictionary-tag {{ background: #e2e8f0; color: #475569; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }}
                .explanation-box {{ border-left: 4px solid #3b82f6; background: #eff6ff; padding: 12px; margin: 10px 0; border-radius: 0 8px 8px 0; }}
            </style>
        </head>
        <body class="text-slate-800">
            <header class="bg-white border-b-4 border-blue-500 sticky top-0 z-50 shadow-md">
                <div class="max-w-6xl mx-auto px-4 h-20 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white shadow-lg">
                            <i class="fas fa-book-open text-2xl"></i>
                        </div>
                        <h1 class="font-bold text-xl text-blue-900">AI 行业“大白话”日报</h1>
                    </div>
                    <div class="text-right">
                        <p class="text-sm font-bold text-slate-700">{self.today}</p>
                    </div>
                </div>
            </header>
            <main class="max-w-6xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-4 gap-8">
                <div class="lg:col-span-3 space-y-8">
        """
        
        for item in news_list:
            html_template += f"""
                    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
                        <div class="flex justify-between items-center mb-3">
                            <span class="px-2 py-1 bg-blue-100 text-blue-600 text-xs font-bold rounded">{item['source']}</span>
                            <span class="text-slate-400 text-xs"><i class="far fa-clock mr-1"></i> {item['time']}</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3">{item['title']}</h3>
                        <p class="text-slate-600 leading-relaxed mb-4">{item['desc']}</p>
                        <div class="explanation-box">
                            <p class="text-sm font-bold text-blue-800 mb-1">💡 通俗解释：</p>
                            <p class="text-sm text-blue-700">{item['easy_talk']}</p>
                        </div>
                    </div>
            """

        html_template += """
                </div>
                <div class="lg:col-span-1">
                    <div class="bg-white rounded-2xl p-6 shadow-md border-t-4 border-blue-500 sticky top-28">
                        <h2 class="text-lg font-black text-slate-900 mb-4">📖 AI 小词典</h2>
                        <div class="space-y-4 text-xs">
                            <p><strong>Agent (智能体)</strong>：不仅能说话，还能自主干活的 AI。</p>
                            <p><strong>Google (谷歌)</strong>：全球搜索引擎老大。</p>
                            <p><strong>OpenAI</strong>：开发了 ChatGPT 的公司。</p>
                        </div>
                    </div>
                </div>
            </main>
        </body>
        </html>
        """
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write(html_template)

    def send_dingtalk(self, news_list):
        if not self.webhook_url:
            print("未配置钉钉 Webhook，跳过推送。")
            return

        first_news = news_list[0]
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "今日 AI 简报",
                "text": f"### 🤖 今日 AI 行业简报 ({self.today})\n\n" + \
                        f"**🔥 核心消息：**\n> {first_news['title']}\n\n" + \
                        f"**💡 大白话解释：**\n{first_news['easy_talk']}\n\n" + \
                        f"👉 [点击查看完整百科简报](https://你的github用户名.github.io/ai-news-agent/ai-news-agent/index.html)"
            }
        }
        requests.post(self.webhook_url, json=payload)

    def run(self):
        news = self.fetch_mock_news()
        self.generate_html(news)
        self.send_dingtalk(news)

if __name__ == "__main__":
    AINewsAgent().run()
```

---
