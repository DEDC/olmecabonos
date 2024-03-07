# Python
import zipfile
import io
import textwrap
from string import ascii_letters
# Django
from django.http import HttpResponse
# pillow
from PIL import Image, ImageFont, ImageDraw 
# qrcode
import qrcode

# class GenerateBonus():
#     def __init__(self, bonus_list = [], drawer = None):
#         self.bonus_list = bonus_list
#         self.drawer = drawer

# class DrawBonous:
    

def generate_bonus(bonus):
    b2 = io.BytesIO()
    zf = zipfile.ZipFile(b2, "w")
    images = []
    for obj in bonus:
        b1 = io.BytesIO()
        bonus_name = obj.abonado['name']
        if obj.fecha_reg.date().year == 2023:
            W, H = (1012,638)
            font = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 60)
            font_short = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 45)
            font_label = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 30)
            font_label_v2 = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 76)
            if obj.tipo == 'palco':
                # palco-v2-------------------
                img = Image.open("static/bonus/{}.png".format(obj.ubicacion['extra']), 'r')
                bonus = ImageDraw.Draw(img)
                bonus_label1 = obj.ubicacion['section']
                w, h = bonus.textsize(bonus_label1, font=font_label_v2)
                bonus.text((280, 468), bonus_label1, fill="white", font=font_label_v2)
                bonus_label1 = obj.ubicacion['seat']
                w, h = bonus.textsize(bonus_label1, font=font_label_v2)
                bonus.text((785, 466), bonus_label1, fill="white", font=font)
                qr_img = qrcode.make(obj.folio, border=0, box_size=8.5)
                qr_w, qr_h = qr_img.size
                offset = ((W-(qr_w))//7, 286)
                img.paste(qr_img, offset)
                img.save(b1, 'PNG', quality=100)
            else:
                # regular-v1--------------
                img = Image.open("static/bonus/bonus_v2.png", 'r')
                bonus = ImageDraw.Draw(img)
                avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
                max_char_count = int(img.size[0] * .70 / avg_char_width)
                text = textwrap.fill(text=bonus_name, width=max_char_count)
                if len(text.splitlines()) > 1:
                    bonus.text(xy=(256, img.size[1] / 3.3), text=text, font=font_short, fill='#000000')
                else:
                    bonus.text(xy=(256, img.size[1] / 3.3), text=text, font=font, fill='#000000')        
                bonus_label1 = 'SECCIÓN:'
                w, h = bonus.textsize(bonus_label1, font=font_label)
                bonus.text((258, 301), bonus_label1, fill="black", font=font_label)
                bonus_section = obj.ubicacion['section']
                w, h = bonus.textsize(bonus_section, font=font_label)
                bonus.text((380, 301), bonus_section, fill="#056b3d", font=font_label)
                bonus_label2 = 'FILA:'
                w, h = bonus.textsize(bonus_label2, font=font_label)
                bonus.text((480, 301), bonus_label2, fill="black", font=font_label)
                bonus_row = obj.ubicacion['row']
                w, h = bonus.textsize(bonus_row, font=font_label)
                bonus.text((550, 301), bonus_row, fill="#056b3d", font=font_label)
                bonus_label3 = 'ASIENTO:'
                w, h = bonus.textsize(bonus_label3, font=font_label)
                bonus.text((650, 301), bonus_label3, fill="black", font=font_label)
                bonus_seat = obj.ubicacion['seat']
                w, h = bonus.textsize(bonus_seat, font=font_label)
                bonus.text((770, 301), bonus_seat, fill="#056b3d", font=font_label)
                # QR
                qr_img = qrcode.make(obj.folio, border=0, box_size=6)
                qr_w, qr_h = qr_img.size
                offset = ((W-qr_w)//9, 208)
        if obj.fecha_reg.date().year == 2024:
            W, H = (638,1012)
            font = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 47)
            font_short = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 32)
            font_label = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 26)
            font_label_v2 = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 76)
            # regular-v1--------------
            img = Image.open("static/bonus/bonus_24.png", 'r')
            bonus = ImageDraw.Draw(img)
            avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int(img.size[0] * .90 / avg_char_width)
            text = textwrap.fill(text=bonus_name, width=max_char_count)
            if len(text.splitlines()) > 1:
                bonus.text(xy=(60, img.size[1] / 1.53), text=text, font=font_short, fill='#000000')
            else:
                bonus.text(xy=(60, img.size[1] / 1.53), text=text, font=font, fill='#000000')
            bonus_label1 = 'SECCIÓN:'
            w, h = bonus.textsize(bonus_label1, font=font_label)
            bonus.text((60, 739), bonus_label1, fill="black", font=font_label)
            bonus_section = obj.ubicacion['section']
            w, h = bonus.textsize(bonus_section, font=font_label)
            bonus.text((160, 739), bonus_section, fill="#056b3d", font=font_label)
            
            bonus_label2 = 'FILA:'
            w, h = bonus.textsize(bonus_label2, font=font_label)
            bonus.text((280+5, 739), bonus_label2, fill="black", font=font_label)
            bonus_row = obj.ubicacion['row']
            w, h = bonus.textsize(bonus_row, font=font_label)
            bonus.text((332+5, 739), bonus_row, fill="#056b3d", font=font_label)
            
            bonus_label3 = 'ASIENTO:'
            w, h = bonus.textsize(bonus_label3, font=font_label)
            bonus.text((400+50, 739), bonus_label3, fill="black", font=font_label)
            bonus_seat = obj.ubicacion['seat']
            w, h = bonus.textsize(bonus_seat, font=font_label)
            bonus.text((497+50, 739), bonus_seat, fill="#056b3d", font=font_label)
            # QR
            qr_img = qrcode.make(obj.folio, border=0, box_size=15)
            qr_w, qr_h = qr_img.size
            offset = (164, 264)
        img.paste(qr_img, offset)
        img.save(b1, 'PNG', quality=100)
        images.append(b1)
        b1.name = '{}_{}.png'.format(bonus_name, obj.folio)
    if len(images) > 1:
        for im in images:
            zf.writestr(im.name, im.getvalue())
        zf.close()
        response = HttpResponse(b2.getvalue(), content_type = 'application/application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=BONOS.zip'
    else:
        response = HttpResponse(b1.getvalue(), content_type = 'image/png')
        response['Content-Disposition'] = 'attachment; filename={}'.format(b1.name)
        b1.close()
    return response

def generate_qr(bonus):
    b2 = io.BytesIO()
    zf = zipfile.ZipFile(b2, "w")
    images = []
    for obj in bonus:
        b1 = io.BytesIO()
        qr_img = qrcode.make(obj.folio, border=1, box_size=12)
        qr_img.save(b1)
        images.append(b1)
        b1.name = '{}_{}.png'.format(obj.abonado['name'], obj.folio)
    if len(images) > 1:
        for im in images:
            zf.writestr(im.name, im.getvalue())
        zf.close()
        response = HttpResponse(b2.getvalue(), content_type = 'application/application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=BONOS_QR.zip'
    else:
        response = HttpResponse(b1.getvalue(), content_type = 'image/png')
        response['Content-Disposition'] = 'attachment; filename={}'.format(b1.name)
        b1.close()
    return response