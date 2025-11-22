from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, MessageAction
import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
if not CHANNEL_ACCESS_TOKEN:
    print("Error: LINE_CHANNEL_ACCESS_TOKEN not found in .env")
    exit(1)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def create_rich_menu():
    # 1. Define Rich Menu
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=True,
        name="CookieGameMenu",
        chat_bar_text="開啟選單",
        areas=[
            # Row 1
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                action=MessageAction(label="領取", text="領取")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                action=MessageAction(label="查詢", text="查詢")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1666, y=0, width=834, height=843),
                action=MessageAction(label="升級", text="升級")
            ),
            # Row 2
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=843, width=833, height=843),
                action=MessageAction(label="榜單", text="榜單")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=843, width=833, height=843),
                action=MessageAction(label="新聞", text="新聞")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1666, y=843, width=834, height=843),
                action=MessageAction(label="匯率", text="匯率")
            )
        ]
    )

    # 2. Create Rich Menu
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    print(f"Rich Menu created. ID: {rich_menu_id}")

    # 3. Upload Image
    image_path = "rich_menu.jpg"
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Please generate it first.")
        return

    with open(image_path, 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)
    print("Rich Menu image uploaded.")

    # 4. Set as Default
    line_bot_api.set_default_rich_menu(rich_menu_id)
    print("Rich Menu set as default successfully!")

if __name__ == "__main__":
    try:
        create_rich_menu()
    except Exception as e:
        print(f"Error: {e}")
