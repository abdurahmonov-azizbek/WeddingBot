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


def create_invitation(qr_path, guest_name, table):
    bg = Image.open("assets/gpt.png")      # your exact background
    qr = Image.open(qr_path).convert("RGBA")

    w, h = bg.size
    draw = ImageDraw.Draw(bg)
    width, height = bg.size

    # STEP 1: COVER THE GRAY PLACEHOLDER WITH WHITE (so QR shows up)
    # Draw a white rounded rectangle exactly over the gray box
    draw.rounded_rectangle(
        [(1400, 2200), (1860, 2660)],   # exact coordinates of your gray box
        radius=60,
        fill="#FFFFFF"
    )


    if os.path.exists(qr_path):
        qr = Image.open(qr_path).convert("RGBA")
        qr_size = 250
        qr = qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        qr_bg = Image.new("RGBA", (qr_size+20, qr_size+20), (255, 255, 255, 230))
        qr_bg.paste(qr, (10, 10), qr)  # the qr itself has transparency mask
        
        # Paste onto invitation (bottom-right corner)
        bg.paste(qr_bg, (width - qr_size - 55, height - qr_size - 70), qr_bg)
        
    # Font function
    def font(size):
        try:
            if size >= 120: return ImageFont.truetype("assets/GreatVibes-Regular.ttf", size)
            if size >= 80:  return ImageFont.truetype("assets/Cinzel[wght].ttf", size)
            return ImageFont.truetype("assets/Lora[wght].ttf", size)
        except:
            return ImageFont.load_default().font_variant(size=int(size*1.4))

    def txt(text, y, size=55, color="#E8C07B", stroke=0):
        f = font(size)
        bbox = draw.textbbox((0,0), text, font=f)
        x = (w - (bbox[2]-bbox[0])) // 2
        if stroke:
            draw.text((x,y), text, font=f, fill=color, stroke_width=stroke, stroke_fill="#8B6914")
        else:
            draw.text((x,y), text, font=f, fill=color)

    # CHANGE ONLY THESE
    guest_name   = guest_name
    table_number = f"Table {table}"

    # FINAL PERFECT TEXT (no overlap, perfect size)
    txt("SAVE THE DATE",        100, 100, "#E8C07B", stroke=3)
    txt("to celebrate",         280,  46, "#FFFFFF")
    txt("GISELLE'S",            400, 100, "#E8C07B", stroke=2)
    txt("40TH BIRTHDAY",        510, 100, "#E8C07B", stroke=2)
    txt("SEP | 12 | 2024",      650,  70, "#F4E4BC")

    txt("Dear",                800,  48, "#FFFFFF")
    txt(guest_name,            880,  60, "#E8C07B", stroke=2)
    txt(f"YOUR {table_number}",985,  80, "#E8C07B", stroke=3)

    txt("7:30 PM 'till midnight", 1100, 35, "#FFFFFF")
    txt("539 brookside court, holloway", 1150, 35, "#FFFFFF")


    # Save
    invitations_folder = os.path.join("invitations")
    if not os.path.exists(invitations_folder):
        os.makedirs(invitations_folder)

    output = os.path.join(invitations_folder, f"{uuid.uuid4()}.jpg")
    bg.save(output, quality=98)

    return output