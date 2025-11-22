# Flask LINE Bot Cookie Clicker 🍪🤖

這是一個結合 **Python Flask**、**LINE Messaging API** 與 **Google Apps Script (GAS)** 的智慧助理與餅乾點擊遊戲專案。

## ✨ 功能特色

### 🎮 餅乾點擊遊戲
- **領取餅乾**：每 10 分鐘可領取一次，累積你的財富！
- **升級系統**：
  - **自動化烤箱**：提升生產效率。
  - **時光機器**：減少領取冷卻時間。
  - **幸運餅乾**：增加每次領取的數量。
- **排行榜**：與其他玩家一較高下。
- **雲端存檔**：遊戲數據儲存於 Google Sheets，隨時隨地都能玩。

### 📰 智慧助理
- **即時新聞**：爬取最新科技新聞頭條。
- **匯率查詢**：提供台灣銀行即時匯率資訊。

## 🛠️ 技術架構
- **Backend**: Python Flask
- **Interface**: LINE Messaging API
- **Game Logic & DB**: Google Apps Script + Google Sheets
- **Crawler**: BeautifulSoup4

## 🚀 快速開始 (本地端)

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 設定環境變數
複製 `.env.example` 為 `.env` 並填入以下資訊：
```properties
LINE_CHANNEL_ACCESS_TOKEN=你的LINE_Token
LINE_CHANNEL_SECRET=你的LINE_Secret
GAS_APP_URL=你的GAS_WebApp_URL
```

### 3. 啟動伺服器
```bash
python app.py
```

### 4. 設定 LINE Webhook
使用 ngrok 讓 LINE 連線到本地伺服器：
```bash
ngrok http 5000
```
將 ngrok 網址 (例如 `https://xxxx.ngrok-free.app/callback`) 填入 LINE Developers Console 的 Webhook URL。

## ☁️ 部署 (Render)
本專案已準備好部署至 Render：
1. 將程式碼推送到 GitHub。
2. 在 Render 建立新的 Web Service。
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn -c gunicorn_config.py app:app`
5. 設定環境變數 (Environment Variables)。

## 📂 檔案結構
- `app.py`: Flask 應用程式入口。
- `bot_handler.py`: LINE Bot 訊息處理邏輯。
- `game_service.py`: 負責與 GAS 遊戲後端溝通。
- `crawler_service.py`: 負責爬蟲功能。
- `game_backend.js`: Google Apps Script 腳本 (需部署至 GAS)。

## 📖 詳細說明
請參閱 [walkthrough.md](walkthrough.md) 查看完整的使用者手冊與指令列表。
