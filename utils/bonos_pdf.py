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

def generate_bonus(bonus):
    b2 = io.BytesIO()
    zf = zipfile.ZipFile(b2, "w")
    font = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 60)
    font_short = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 45)
    font_label = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 30)
    W, H = (1012,638)
    images = []
    for obj in bonus:
        img = Image.open("static/bonus/bonus_v2.png", 'r')
        b1 = io.BytesIO()
        bonus = ImageDraw.Draw(img)
        bonus_name = obj.abonado['name']
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
        qr_img = qrcode.make(obj.folio, border=0, box_size=6)
        qr_w, qr_h = qr_img.size
        offset = ((W-qr_w)//9, 208)
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


    # bonus_info1 = 'SECCIÓN'
    # bonus_info2 = 'FILA'
    # bonus_info3 = 'NO.BUTACA'
    # macuspana = 'EST. MACUSPANA'
    # centenario = 'EST. CENTENARIO'
    
    # for obj in bonus:
    #     img = Image.open("static/bonus/bonus_2.jpg", 'r')
    #     b1 = io.BytesIO()
    #     bonus = ImageDraw.Draw(img)
    #     # bonus info
    #     bonus_name = obj.abonado['nombre'].upper()
    #     bonus_type = obj.get_tipo_display().upper()
    #     # bonus name
    #     bonus_name = textwrap.fill(text=bonus_name, width=25)
    #     w, h = bonus.textsize(bonus_name, font=font)
    #     bonus.text(((W-w)/2, 180), bonus_name, fill="white", font=font)
    #     # bonus type
    #     w, h = bonus.textsize(bonus_type, font=font)
    #     bonus.text(((W-w)/2, 300), bonus_type, fill="white", font=font)
    #     # stadium info fields (centenario)
    #     w, h = bonus.textsize(centenario, font=font)
    #     bonus.text(((W-w)/2, 380), centenario, fill="#9e9e9e", font=font)
    #     w, h = bonus.textsize(bonus_info1, font=font)
    #     bonus.text(((W-w)/6, 440), bonus_info1, fill="white", font=font)
    #     w, h = bonus.textsize(bonus_info2, font=font)
    #     bonus.text(((W-w)/2-6, 440), bonus_info2, fill="white", font=font)
    #     w, h = bonus.textsize(bonus_info3, font=font)
    #     bonus.text(((W-w)/1-((W-w)/6), 440), bonus_info3, fill="white", font=font)
    #     # data
    #     w, h = bonus.textsize(obj.ubicacion['centenario']['seccion'], font=font)
    #     bonus.text(((W-w)/6, 486), obj.ubicacion['centenario']['seccion'], fill="white", font=font)
    #     w, h = bonus.textsize(obj.ubicacion['centenario']['fila'], font=font)
    #     bonus.text(((W-w)/2-6, 486), obj.ubicacion['centenario']['fila'], fill="white", font=font)
    #     w, h = bonus.textsize(str(obj.ubicacion['centenario']['butaca']), font=font)
    #     bonus.text(((W-w)/1-((W-w)/6), 486), str(obj.ubicacion['centenario']['butaca']), fill="white", font=font)
    #     # stadium info fields (macuspana)
    #     w, h = bonus.textsize(macuspana, font=font)
    #     bonus.text(((W-w)/2, 560), macuspana, fill="#9e9e9e", font=font)
    #     w, h = bonus.textsize(bonus_info1, font=font)
    #     bonus.text(((W-w)/6, 620), bonus_info1, fill="white", font=font)
    #     w, h = bonus.textsize(bonus_info2, font=font)
    #     bonus.text(((W-w)/2-6, 620), bonus_info2, fill="white", font=font)
    #     w, h = bonus.textsize(bonus_info3, font=font)
    #     bonus.text(((W-w)/1-((W-w)/6), 620), bonus_info3, fill="white", font=font)
    #     # data
    #     w, h = bonus.textsize(obj.ubicacion['macuspana']['seccion'] or '', font=font)
    #     bonus.text(((W-w)/6, 666), obj.ubicacion['macuspana']['seccion'] or '', fill="white", font=font)
    #     w, h = bonus.textsize(obj.ubicacion['macuspana']['fila'] or '', font=font)
    #     bonus.text(((W-w)/2-6, 666), obj.ubicacion['macuspana']['fila'] or '', fill="white", font=font)
    #     w, h = bonus.textsize(str(obj.ubicacion['macuspana']['butaca'] or ''), font=font)
    #     bonus.text(((W-w)/1-((W-w)/6), 666), str(obj.ubicacion['macuspana']['butaca'] or ''), fill="white", font=font)
    #     # add QR
    #     qr_img = qrcode.make(obj.folio, border=1, box_size=8)
    #     qr_w, qr_h = qr_img.size
    #     offset = ((W-qr_w)//2, 740)
    #     img.paste(qr_img, offset)
        # generate zip
    #     img.save(b1, 'PNG', quality=100)
    #     zf.writestr('{}_{}.png'.format(bonus_name, obj.folio), b1.getvalue())
    #     b1.close()
    # zf.close()