from PIL import Image, ImageDraw, ImageFont
import random

def create_signatures(firstname: str, lastname: str, user_id: int):
    width, height = 400, 200
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    font_number = random.randint(1, 7)
    font_path = f"assets/{font_number}.ttf"
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)


    firstname = firstname[:1] + "." if random.randint(1, 2) == 2 else None
    if len(lastname) > 3:
        remove_count = random.randint(1, len(lastname) - 3)
        lastname = lastname[:-remove_count]

    text = f"{firstname if firstname else ''} {lastname}"
    text_bbox = draw.textbbox((0, 0), text, font=font)

    center_x = (image.width - (text_bbox[2] - text_bbox[0])) // 2
    center_y = (image.height - (text_bbox[3] - text_bbox[1])) // 2

    draw.text((center_x, center_y), text, font=font, fill="black")
    image.save(f"assets/users_signature/{user_id}_{font_number}.png")
    
    return font_number
