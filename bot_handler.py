from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction, FlexSendMessage
from game_service import GameService
from crawler_service import CrawlerService

game_service = GameService()
crawler_service = CrawlerService()

def handle_text_message(user_id, user_name, text):
    text = text.strip()
    
    # Game Commands
    if text == "領取":
        msg = game_service.collect_cookie(user_id, user_name)
        return TextSendMessage(text=msg)
    
    elif text == "查詢":
        msg = game_service.get_profile(user_id, user_name)
        return TextSendMessage(text=msg)
    
    elif text == "榜單":
        msg = game_service.get_leaderboard()
        return TextSendMessage(text=msg)
    
    elif text == "升級":
        return FlexSendMessage(
            alt_text='請選擇升級項目',
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://cdn-icons-png.flaticon.com/512/3100/3100528.png",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                        "type": "uri",
                        "uri": "http://linecorp.com/"
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "工廠升級",
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "text",
                            "text": "請選擇要升級的項目：",
                            "margin": "md",
                            "size": "sm",
                            "color": "#666666"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "升級自動化 (每小時+10)",
                                "text": "升級自動"
                            },
                            "color": "#1DB446"
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "升級冷卻 (時間-1分)",
                                "text": "升級冷卻"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "升級幸運 (每次+1)",
                                "text": "升級幸運"
                            }
                        }
                    ],
                    "flex": 0
                }
            }
        )
        
    elif text.startswith("升級"):
        if "自動" in text:
            msg = game_service.buy_upgrade(user_id, user_name, "auto")
        elif "冷卻" in text:
            msg = game_service.buy_upgrade(user_id, user_name, "cooldown")
        elif "幸運" in text:
            msg = game_service.buy_upgrade(user_id, user_name, "lucky")
        else:
            msg = "未知的升級項目，請輸入「升級」查看列表。"
        return TextSendMessage(text=msg)

    # Crawler Commands
    elif text == "新聞":
        msg = crawler_service.get_news()
        return TextSendMessage(text=msg)
    
    elif text == "匯率":
        msg = crawler_service.get_exchange_rate()
        return TextSendMessage(text=msg)
        
    # Help
    elif text == "說明" or text == "help":
        msg = (
            "【指令列表】\n"
            "🍪 遊戲指令：\n"
            "- 領取：獲得餅乾\n"
            "- 查詢：查看目前資產\n"
            "- 升級：查看與購買升級\n"
            "- 榜單：查看排行榜\n\n"
            "📰 助理指令：\n"
            "- 新聞：最新頭條\n"
            "- 匯率：即時匯率"
        )
        return TextSendMessage(text=msg)
    
    return None # Don't reply if no command matched
