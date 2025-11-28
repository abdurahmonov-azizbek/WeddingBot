import qrcode
import uuid
from PIL import Image, ImageDraw, ImageFont
import os


def create_guest_qr(guest, lang: str = 'uz'):
    text = (
        f"Register raqami: {guest.reg_number}\n"
        f"FIO (UZ): {guest.full_name_uz}\n"
        f"FIO (RU): {guest.full_name_ru}\n"
        f"Stol raqami: {guest.table_number}\n"
        f"Qo'shimcha mehmonlar: {guest.persons_count}\n"
        f"Telefon raqam: {guest.phone_number}\n"
        f"Ro'yhatdan o'tganmi?: {'Ha' if guest.is_registered else 'Yo\'q'}\n"
        f"Mehmon bazmga kirganmi?: {'Ha' if guest.is_entered else 'Yo\'q'}\n"
    )

    if lang == 'ru':
        text = (
            f"Регистрационный номер: {guest.reg_number}\n"
            f"ФИО (UZ): {guest.full_name_uz}\n"
            f"ФИО (RU): {guest.full_name_ru}\n"
            f"Номер стола: {guest.table_number}\n"
            f"Количество : {guest.persons_count}\n"
            f"Номер телефона: {guest.phone_number}\n"
            f"Зарегистрирован?: {'Да' if guest.is_registered else 'Нет'}\n"
            f"Гость вошел на банкет?: {'Да' if guest.is_entered else 'Нет'}\n"
        )

    path = f"qrcodes/{str(uuid.uuid4())}.png"
    img = qrcode.make(text)
    img.save(path)

    return path


def create_invitation(qr_path: str, guest_name: str, table: int, persons: int = 0) -> str:
    # Load your huge background
    bg = Image.open("assets/bg.png")
    draw = ImageDraw.Draw(bg)
    w, h = bg.size
    print(f"Original size: {w}×{h}")  # you'll see it's massive

    # === PASTE QR CODE ===
    if os.path.exists(qr_path):
        qr = Image.open(qr_path).convert("RGBA")
        qr_size = 1600
        qr = qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        bg.paste(qr, (3900, 8250), qr)  # your exact spot

    # === FONT LOADER ===
    def font(size):
        try:
            if size >= 200:
                return ImageFont.truetype("assets/Lora[wght].ttf", size)
            elif size >= 100:
                return ImageFont.truetype("assets/GreatVibes-Regular.ttf", size)
            else:
                return ImageFont.truetype("assets/Cinzel[wght].ttf", size)
        except:
            return ImageFont.load_default().font_variant(size=int(size * 1.5))

    # === CENTERED TEXT ===
    def txt(text, y, size=60, color="#FFFFFF", stroke=0):
        f = font(size)
        bbox = draw.textbbox((0, 0), text, font=f)
        x = (w - (bbox[2] - bbox[0])) // 2
        if stroke:
            draw.text((x, y), text, font=f, fill=color,
                      stroke_width=stroke, stroke_fill="#1a1a1a")
        else:
            draw.text((x, y), text, font=f, fill=color)

    # === YOUR TEXT (kept your positions) ===
    guest_name = guest_name.upper() if persons == 0 else f"{guest_name.upper()} - {persons}"
    table_text = f"STOL RAQAMI: {table}"
    txt(guest_name, 3700, size=280, color="#FFFFFF", stroke=6)
    txt(table_text,         4450, size=200, color="#FFFFFF", stroke=5)  # Gold table number

    # === FINAL: RESIZE + CONVERT TO RGB + SAVE AS JPG (TELEGRAM WILL ACCEPT 100%) ===
    os.makedirs("invitations", exist_ok=True)
    output_path = f"invitations/invite_{uuid.uuid4()}.jpg"

    # Convert to RGB (remove transparency)
    if bg.mode in ("RGBA", "LA", "P"):
        bg = bg.convert("RGB")

    # Resize to safe Telegram limits (max 5000px height recommended)
    max_height = 5000
    if h > max_height:
        ratio = max_height / h
        new_size = (int(w * ratio), max_height)
        bg = bg.resize(new_size, Image.Resampling.LANCZOS)
        print(f"Resized to {new_size} for Telegram")

    # Save as JPG (small size, fast send, no errors)
    bg.save(output_path, quality=92, optimize=True, progressive=True)
    print(f"FINAL INVITATION READY → {output_path}")

    return output_path