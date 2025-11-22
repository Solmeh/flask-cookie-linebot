from game_service import GameService
from crawler_service import CrawlerService

game_service = GameService()
crawler_service = CrawlerService()

def handle_text_message(user_id, user_name, text):
    text = text.strip()
    
    # Game Commands
    if text == "領取":
        return game_service.collect_cookie(user_id, user_name)
    
    elif text == "查詢":
        return game_service.get_profile(user_id, user_name)
    
    elif text == "榜單":
        return game_service.get_leaderboard()
    
    elif text == "升級":
        return (
            "請輸入要購買的升級項目：\n"
            "1. 升級自動 (自動化烤箱)\n"
            "2. 升級冷卻 (時光機器)\n"
            "3. 升級幸運 (幸運餅乾)\n"
            "範例輸入：「升級自動」"
        )
        
    elif text.startswith("升級"):
        if "自動" in text:
            return game_service.buy_upgrade(user_id, user_name, "auto")
        elif "冷卻" in text:
            return game_service.buy_upgrade(user_id, user_name, "cooldown")
        elif "幸運" in text:
            return game_service.buy_upgrade(user_id, user_name, "lucky")
        else:
            return "未知的升級項目，請輸入「升級」查看列表。"

    # Crawler Commands
    elif text == "新聞":
        return crawler_service.get_news()
    
    elif text == "匯率":
        return crawler_service.get_exchange_rate()
        
    # Help
    elif text == "說明" or text == "help":
        return (
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
    
    return None # Don't reply if no command matched
