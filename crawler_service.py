import requests
from bs4 import BeautifulSoup

class CrawlerService:
    def get_news(self):
        try:
            # Example: Yahoo News TW Technology section
            url = "https://tw.news.yahoo.com/technology"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This selector might need adjustment based on Yahoo's actual structure
            # Looking for headlines
            headlines = []
            # Yahoo News structure changes often, trying a generic approach for list items
            # This is a simplified example. In production, use robust selectors.
            items = soup.find_all('li', class_='js-stream-content', limit=5)
            
            if not items:
                # Fallback or try another selector
                return "目前無法抓取新聞，請稍後再試。"
                
            msg = "📰 最新科技新聞：\n"
            for item in items:
                title_tag = item.find('h3')
                if title_tag:
                    title = title_tag.get_text()
                    link_tag = item.find('a')
                    link = link_tag['href'] if link_tag else ""
                    if not link.startswith('http'):
                        link = 'https://tw.news.yahoo.com' + link
                    msg += f"- {title}\n{link}\n\n"
            
            return msg.strip()
        except Exception as e:
            return f"抓取新聞失敗：{str(e)}"

    def get_exchange_rate(self):
        try:
            # Bank of Taiwan
            url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            rows = soup.find('tbody').find_all('tr')
            
            target_currencies = ['USD', 'JPY', 'EUR', 'CNY']
            msg = "💱 即時匯率 (台灣銀行)：\n"
            
            for row in rows:
                currency_tag = row.find('div', class_='visible-phone print_hide')
                if currency_tag:
                    currency_code = currency_tag.get_text().strip().split(' ')[0] # e.g. "美金 (USD)" -> "美金" -> wait, usually format is "USD" in hidden tag or similar
                    # Actually the text is like "美金 (USD)"
                    full_text = currency_tag.get_text().strip()
                    
                    found = False
                    for target in target_currencies:
                        if target in full_text:
                            found = True
                            break
                    
                    if found:
                        # Buying/Selling rates are usually in specific tds
                        # 0: Currency, 1: Cash Buy, 2: Cash Sell, 3: Spot Buy, 4: Spot Sell
                        cells = row.find_all('td')
                        cash_sell = cells[2].get_text().strip()
                        spot_sell = cells[4].get_text().strip()
                        
                        msg += f"{full_text}:\n現金賣出: {cash_sell} | 即期賣出: {spot_sell}\n"
            
            return msg.strip()
        except Exception as e:
            return f"抓取匯率失敗：{str(e)}"
