import requests
import os
import json

class GameService:
    def __init__(self):
        self.gas_url = os.getenv('GAS_APP_URL', '')

    def _post(self, payload):
        if not self.gas_url:
            return "錯誤：未設定 GAS_APP_URL"
        try:
            response = requests.post(self.gas_url, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "message": f"HTTP Error {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def collect_cookie(self, user_id, user_name):
        payload = {
            "action": "collect",
            "userId": user_id,
            "userName": user_name
        }
        res = self._post(payload)
        if res.get("status") == "success":
            return f"{res['message']}\n目前餅乾：{res['current_cookies']}"
        else:
            return f"領取失敗：{res.get('message')}"

    def get_profile(self, user_id, user_name):
        payload = {
            "action": "get_profile",
            "userId": user_id,
            "userName": user_name
        }
        res = self._post(payload)
        if res.get("status") == "success":
            data = res['data']
            return (
                f"【{user_name} 的餅乾工廠】\n"
                f"🍪 餅乾：{data['cookies']}\n"
                f"🏭 自動產量等級：{data['autoRate']}\n"
                f"⏳ 冷卻縮減等級：{data['cooldownLevel']}\n"
                f"🍀 幸運加成等級：{data['collectLevel']}"
            )
        else:
            return "查詢失敗"

    def buy_upgrade(self, user_id, user_name, upgrade_type):
        payload = {
            "action": "upgrade",
            "userId": user_id,
            "userName": user_name,
            "type": upgrade_type
        }
        res = self._post(payload)
        if res.get("status") == "success":
            return f"{res['message']}\n剩餘餅乾：{res['current_cookies']}"
        else:
            return f"升級失敗：{res.get('message')}"

    def get_leaderboard(self):
        if not self.gas_url:
            return "錯誤：未設定 GAS_APP_URL"
        try:
            # GAS Web App GET request needs to follow redirects usually, but requests handles it
            response = requests.get(f"{self.gas_url}?action=leaderboard")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    leaders = data['data']
                    msg = "🏆 餅乾富豪榜 🏆\n"
                    for idx, user in enumerate(leaders):
                        msg += f"{idx+1}. {user['name']}: {user['cookies']} 🍪\n"
                    return msg
                else:
                    return "無法取得榜單"
            else:
                return "連線錯誤"
        except Exception as e:
            return f"發生錯誤：{str(e)}"
