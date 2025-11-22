from PIL import Image, ImageDraw, ImageFont
import os

def create_rich_menu_image():
    # Canvas size (Standard Large Rich Menu)
    width = 2500
    height = 1686
    background_color = (240, 240, 240) # Light gray
    
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # Grid config
    rows = 2
    cols = 3
    cell_w = width // cols
    cell_h = height // rows
    
    icons = [
        ("assets/icon_collect.png", "領取餅乾"),
        ("assets/icon_profile.png", "我的資產"),
        ("assets/icon_upgrade.png", "升級工廠"),
        ("assets/icon_leaderboard.png", "排行榜"),
        ("assets/icon_news.png", "科技新聞"),
        ("assets/icon_rates.png", "即時匯率")
    ]
    
    # Try to load a Chinese font
    try:
        font_path = "C:\\Windows\\Fonts\\msjh.ttc" # Microsoft JhengHei
        font = ImageFont.truetype(font_path, 60)
    except:
        print("Chinese font not found, using default.")
        font = ImageFont.load_default()

    for i, (icon_path, label) in enumerate(icons):
        row = i // cols
        col = i % cols
        
        x = col * cell_w
        y = row * cell_h
        
        # Draw cell border (optional)
        draw.rectangle([x, y, x+cell_w, y+cell_h], outline=(200, 200, 200), width=2)
        
        # Load and resize icon
        if os.path.exists(icon_path):
            icon = Image.open(icon_path).convert("RGBA")
            # Resize icon to fit in cell (e.g., 500x500)
            icon_size = 500
            icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
            
            # Center icon
            icon_x = x + (cell_w - icon_size) // 2
            icon_y = y + (cell_h - icon_size) // 2 - 50 # Shift up slightly for text
            
            img.paste(icon, (icon_x, icon_y), icon)
        else:
            print(f"Warning: {icon_path} not found")
            
        # Draw Label
        # Calculate text size (rough estimation if font.getsize is deprecated in newer Pillow)
        try:
            bbox = draw.textbbox((0, 0), label, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except:
             text_w, text_h = 100, 50 # Fallback

        text_x = x + (cell_w - text_w) // 2
        text_y = y + cell_h - 150
        
        draw.text((text_x, text_y), label, fill=(50, 50, 50), font=font)

    output_path = "rich_menu.jpg"
    img.save(output_path, quality=95)
    print(f"Rich Menu image saved to {output_path}")

if __name__ == "__main__":
    create_rich_menu_image()
