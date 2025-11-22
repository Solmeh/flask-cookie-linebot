from PIL import Image, ImageDraw, ImageFont

def create_placeholder(filename, text, color):
    img = Image.new('RGB', (800, 800), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # Draw a circle
    d.ellipse([100, 100, 700, 700], outline=color, width=20)
    # Draw text (simplified, no font file needed for basic shapes, but text needs font)
    # We'll just draw a symbol '$'
    d.text((350, 300), "$", fill=color, align="center", font_size=300) # font_size might need Pillow 10+ or default font
    
    # Since default font is tiny, let's just draw a simple shape representing money
    d.rectangle([250, 300, 550, 500], outline=color, width=15)
    d.text((380, 350), "$", fill=color)
    
    img.save(filename)

if __name__ == "__main__":
    create_placeholder("assets/icon_rates.png", "$", (255, 215, 0)) # Gold color
