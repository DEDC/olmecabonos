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
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from pdf2image import convert_from_path
from apps.bonos.models import Bono
import fitz  # PyMuPDF

# class GenerateBonus():
#     def __init__(self, bonus_list = [], drawer = None):
#         self.bonus_list = bonus_list
#         self.drawer = drawer

# class DrawBonous:


def ajustar_texto(canvas, text, x, y, max_width, font_name="Helvetica-Bold", max_font_size=12, min_font_size=6):
    """
    Dibuja texto en un canvas de reportlab ajustando el tamaño de fuente
    para que no se pase del ancho máximo.
    """
    font_size = max_font_size
    canvas.setFont(font_name, font_size)

    while font_size >= min_font_size:
        text_width = canvas.stringWidth(text, font_name, font_size)
        if text_width <= max_width:
            break
        font_size -= 1
        canvas.setFont(font_name, font_size)

    canvas.drawString(x, y, text)


def generate_bonus_server(bonus):
    zf = zipfile.ZipFile('BONOS.zip', 'w')
    W, H = (638,1012)
    c = 0
    for obj in bonus:
        c += 1
        print(c)
        print(obj.ubicacion)
        b1 = io.BytesIO()
        bonus_name = obj.abonado['name']
        font = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 47)
        font_short = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 32)
        font_label = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 26)
        font_label_v2 = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 76)
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
        b1.name = '{}_{}.png'.format(bonus_name, obj.folio)
        zf.writestr(b1.name, b1.getvalue())
    zf.close()
    # response = HttpResponse(b2.getvalue(), content_type = 'application/application/octet-stream')
    # response['Content-Disposition'] = 'attachment; filename=BONOS.zip'


def generate_pdf(file_front, file_back, bono: Bono):
    # Crear un nuevo PDF con ReportLab
    packet = io.BytesIO()

    # Tamaño de la credencial en cm
    width, height = 5.6 * cm, 8.7 * cm

    if  bono.tipo == "napoli":
        # Tamaño de la credencial en cm
        height, width = 5.6 * cm, 8.7 * cm

    bonus_name = bono.abonado['name']
    total_word = len(bonus_name.split())

    # Crear un objeto canvas
    pdf = canvas.Canvas('{}_{}.pdf'.format(bonus_name.replace("/", "_").replace('"',""), bono.folio), pagesize=(width, height))

    # Añadir la parte trasera
    pdf.drawImage(file_back, 0, 0, width=width, height=height)

    # Crear una nueva página para la parte trasera
    pdf.showPage()

    # Añadir la parte delantera
    pdf.drawImage(file_front, 0, 0, width=width, height=height)

    # Añadir el nombre de la persona
    pdf.setFont("Helvetica-Bold", 7)
    pdf.setFillColor(colors.black)
    text_x = 46
    qr_x = 48
    qr_y = 100
    qr_size = 3
    if total_word == 2:
        text_x = 50
    if total_word == 3:
        pdf.setFont("Helvetica-Bold", 6)
        text_x = 55
    if total_word > 3:
        pdf.setFont("Helvetica-Bold", 5)
        text_x = 65
    if total_word > 4:
        font = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 47)
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count = int(700 * .90 / avg_char_width)
        bonus_name = textwrap.fill(text=bonus_name, width=max_char_count)
    text_y = height - 1.5 * cm  # Ajusta esta posición según sea necesario
    if bono.tipo == "napoli":
        qr_x = 180
        qr_y = 62
        qr_size = 2.9

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(27, 90, bonus_name)
        bonus_row = bono.ubicacion['section']
        pdf.setFont("Helvetica-Bold", 10)
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(45, 72, "Zona")
        pdf.setFillColor("#056b3d")
        pdf.drawCentredString(60, 55, bonus_row)
    else:
        # if bono.tipo == "jaguares_sombra":
        if bono.tipo.startswith("jaguares"):
            qr_size = 3
            qr_x = 48
            qr_y = 133
            pdf.setFont("Helvetica-Bold", 7)
            pdf.drawCentredString(text_x + 10, 100, bonus_name)
            bonus_section = bono.ubicacion['section']
            pdf.setFont("Helvetica-Bold", 6)
            pdf.setFillColor("#056b3d")
            pdf.drawCentredString(50, 81, bonus_section)

            bonus_row = bono.ubicacion['row']
            pdf.drawString(92, 81, bonus_row)

            bonus_seat = bono.ubicacion['seat']
            pdf.drawCentredString(145, 81, bonus_seat)

        # elif bono.tipo == "jaguares_palco":
        #     qr_size = 3
        #     qr_x = 48
        #     text_x += 5
        #     if total_word > 3:
        #         pdf.setFont("Helvetica-Bold", 6)
        #         text_x += 8
        #
        #     pdf.setFont("Helvetica-Bold", 7)
        #     pdf.drawString(30, 67, bonus_name)
        #     bonus_row = bono.ubicacion['section']
        #     pdf.setFont("Helvetica-Bold", 6)
        #     pdf.setFillColor("#056b3d")
        #     pdf.drawCentredString(87, 48, bonus_row)
        #
        else:
            pdf.drawString(26, 71, bonus_name)

            bonus_label1 = 'SECC:'
            pdf.setFont("Helvetica-Bold", 5)
            pdf.setFillColor(colors.black)
            pdf.drawCentredString(34, 64, bonus_label1)

            bonus_section = bono.ubicacion['section']
            pdf.setFillColor("#056b3d")
            pdf.drawCentredString(54, 64, bonus_section)

            bonus_label2 = 'FILA:'
            pdf.setFillColor(colors.black)
            pdf.drawCentredString(75, 64, bonus_label2)

            bonus_row = bono.ubicacion['row']
            pdf.setFillColor("#056b3d")
            pdf.drawCentredString(86, 64, bonus_row)

            bonus_label3 = 'ASIENTO:'
            pdf.setFillColor(colors.black)
            pdf.drawCentredString(106, 64, bonus_label3)

            bonus_seat = bono.ubicacion['seat']
            pdf.setFillColor("#056b3d")
            pdf.drawCentredString(125, 64, bonus_seat)

    qr_img = qrcode.make(bono.folio, border=0, box_size=qr_size)
    qr_img_path = "{}_qr.png".format(bono.folio)
    qr_img.save(qr_img_path)
    pdf.drawImage(qr_img_path, qr_x, qr_y)

    # Guardar el PDF
    pdf.save()

    # Eliminar la imagen del código QR temporal
    os.remove(qr_img_path)
    print("PDF generado exitosamente")


def generate_pdf_olmeca(file_front, file_back, bono: Bono):
    # Crear un nuevo PDF con ReportLab
    packet = io.BytesIO()

    # Tamaño de la credencial en cm
    width, height = 8.7 * cm, 5.6 * cm

    if bono.tipo == "vitalicio":
        # Tamaño de la credencial en cm
        width, height = 5.6 * cm, 8.7 * cm


    bonus_name = bono.abonado['name']
    total_word = len(bonus_name.split())

    # Crear un objeto canvas
    pdf = canvas.Canvas('{}_{}.pdf'.format(bonus_name.replace("/", "_").replace('"',""), bono.folio), pagesize=(width, height))

    # Añadir la parte trasera
    pdf.drawImage(file_back, 0, 0, width=width, height=height)

    # Crear una nueva página para la parte trasera
    pdf.showPage()

    # Añadir la parte delantera
    pdf.drawImage(file_front, 0, 0, width=width, height=height)

    # Añadir el nombre de la persona
    pdf.setFont("Helvetica-Bold", 9)
    pdf.setFillColor(colors.white)
    text_x = 30
    qr_x = 160
    qr_y = 50
    qr_size = 3
    if total_word == 2:
        pdf.setFont("Helvetica-Bold", 14)
        text_x = 30
    # if total_word == 3:
    #     pdf.setFont("Helvetica-Bold", 12)
    #     text_x = 20
    # if total_word > 3:
    #     text_x = 20
    if total_word >= 3:
        # font = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 12)
        # avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        # max_char_count = int(700 * .90 / avg_char_width)
        pdf.setFont("Helvetica-Bold", 12)
        text_x = 30

    text_y = height - 1.5 * cm  # Ajusta esta posición según sea necesario

    if bono.tipo == "vitalicio":
        qr_size = 4
        qr_x = 37
        qr_y = 94
        pdf.setFont("Helvetica-Bold", 7)
        pdf.setFillColor("#000000")
        pdf.drawCentredString(65, 73, bonus_name.replace("\n", ""))
        bonus_section = bono.ubicacion['section']
        pdf.setFont("Helvetica-Bold", 6)
        pdf.setFillColor("#056b3d")
        pdf.drawCentredString(35, 60, bonus_section)

        bonus_row = bono.ubicacion['row']
        pdf.drawString(70, 60, bonus_row)

        bonus_seat = bono.ubicacion['seat']
        pdf.drawCentredString(65 + 50, 60, bonus_seat)

    elif bono.tipo == "palco":
        qr_size = 2
        qr_x = 37
        qr_y = 60
        pdf.setFont("Helvetica-Bold", 12)
        pdf.setFillColor("#ffffff")
        # pdf.setFillColor("#000000")
        pdf.drawCentredString(120, 130, bonus_name.replace("\n", ""))
        bonus_section = bono.ubicacion['section']
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawCentredString(110, 32, bonus_section)

        bonus_row = bono.ubicacion['seat']
        pdf.drawString(205, 32, bonus_row)
        #
        # bonus_seat = bono.ubicacion['seat']
        # pdf.drawCentredString(65 + 50, 60, bonus_seat)

    else:
        y_position = 70  # Posición inicial

        ajustar_texto(
            canvas=pdf,
            text=bonus_name,
            x=text_x,
            y=y_position,
            max_width=60  # en puntos (1 pulgada = 72 puntos)
        )

        pdf.setFont("Helvetica-Bold", 7)
        bonus_section = bono.ubicacion['section']
        # pdf.setFillColor("#056b3d")
        pdf.drawCentredString(110, 43, bonus_section)

        bonus_row = bono.ubicacion['row']
        # pdf.setFillColor("#056b3d")
        pdf.drawCentredString(110, 31, bonus_row)

        bonus_seat = bono.ubicacion['seat']
        # pdf.setFillColor("#056b3d")
        pdf.drawCentredString(110, 21, bonus_seat)

    qr_img = qrcode.make(bono.folio, border=0, box_size=qr_size)
    qr_img_path = "{}_qr.png".format(bono.folio)
    qr_img.save(qr_img_path)
    pdf.drawImage(qr_img_path, qr_x, qr_y)

    # Guardar el PDF
    pdf.save()

    # Eliminar la imagen del código QR temporal
    os.remove(qr_img_path)
    print("PDF generado exitosamente")


def generate_bonus(bonus):
    b2 = io.BytesIO()
    zf = zipfile.ZipFile(b2, "w")
    images = []
    img_flag = False
    for obj in bonus:
        b1 = io.BytesIO()
        bonus_name = obj.abonado['name']
        print("Folio: {}".format(obj.folio))
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
        else:
            W, H = (638,1012)
            font = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 47)
            font_short = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 32)
            font_short_medium = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 28)
            font_short_small = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 22)
            font_label = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 26)
            font_label_small = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 18)
            font_label_v2 = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 76)
            # regular-v1--------------
            img = None

            if obj.tipo.startswith("jaguares"):
                # front_path = "static/bonus/{}.jpg".format(obj.tipo)
                front_path = "static/bonus/jaguares_sombra.jpg".format(obj.tipo)
                back_path = "static/bonus/{}_back.jpg".format(obj.tipo)
                generate_pdf(front_path, back_path, obj)
                with open('{}_{}.pdf'.format(bonus_name.replace("/", "_").replace('"', ""), obj.folio), "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                    b1.write(pdf_data)
                images.append(b1)
                b1.name = '{}_{}.pdf'.format(bonus_name.replace("/", "_").replace('"', ""), obj.folio)

                # Devolver el PDF como respuesta HTTP
                # response = HttpResponse(pdf_data, content_type='application/pdf')
                # response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(b1.name)
                # return response

            elif obj.tipo.startswith("napoli"):
                front_path = "static/bonus/{}.png".format(obj.tipo)
                back_path = "static/bonus/{}_back.png".format(obj.tipo)
                generate_pdf(front_path, back_path, obj)
                with open('{}_{}.pdf'.format(bonus_name.replace("/", "_").replace('"', ""), obj.folio), "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                    b1.write(pdf_data)
                b1.name = '{}_{}.pdf'.format(bonus_name.replace("/", "_").replace('"', ""), obj.folio)
                images.append(b1)

                # Devolver el PDF como respuesta HTTP
                # response = HttpResponse(pdf_data, content_type='application/pdf')
                # response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(b1.name)
                # return response
            else:
                # if obj.tipo.startswith("jaguares"):
                #     img = Image.open("static/bonus/{}.jpg".format(obj.tipo), 'r')
                # else:
                #     img = Image.open("static/bonus/bonus_24.png", 'r')

                front_path = "static/bonus/bono_olmeca_black.jpg".format(obj.tipo)
                back_path = "static/bonus/bono_olmeca_black_back.jpg".format(obj.tipo)

                if obj.tipo == "vitalicio":
                    front_path = "static/bonus/vitalicio_olmeca.jpg".format(obj.tipo)
                    back_path = "static/bonus/vitalicio_olmeca_back.jpg".format(obj.tipo)

                if obj.tipo == "palco":
                    front_path = "static/bonus/palco_olmeca.jpg".format(obj.tipo)
                    back_path = "static/bonus/palco_olmeca_back.jpg".format(obj.tipo)

                generate_pdf_olmeca(front_path, back_path, obj)

                documento = fitz.open('{}_{}.pdf'.format(bonus_name.replace("/", "_").replace('"', ""), obj.folio))

                for i, pagina in enumerate(documento):
                    # Renderizar la página como pixmap
                    pix = pagina.get_pixmap(matrix=fitz.Matrix(3, 3))  # 3x3 para mejorar la calidad
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                    # Guardar la imagen
                    img.save('{}_{}.jpg'.format(bonus_name.replace("/", "_").replace('"', ""), obj.folio), "JPEG")

                with open('{}_{}.jpg'.format(bonus_name.replace("/", "_").replace('"', ""), obj.folio), "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                    b1.write(pdf_data)

                b1.name = '{}_{}.jpg'.format(bonus_name.replace("/", "_").replace('"', ""), obj.folio)
                images.append(b1)
                img_flag = True

                # Devolver el PDF como respuesta HTTP
                # response = HttpResponse(pdf_data, content_type='application/pdf')
                # response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(b1.name)
                # return response

                # bonus = ImageDraw.Draw(img)
                # avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
                # max_char_count = int(img.size[0] * .90 / avg_char_width)
                # text = textwrap.fill(text=bonus_name, width=max_char_count)
                # if len(text.splitlines()) > 1:
                #     bonus.text(xy=(90, img.size[1] / 1.45), text=text, font=font_short, fill='#000000')
                # else:
                #     bonus.text(xy=(60, img.size[1] / 1.53), text=text, font=font_short, fill='#000000')
                #
                # bonus_label1 = 'SECCIÓN:'
                # w, h = bonus.textsize(bonus_label1, font=font_label)
                # bonus.text((60, 739), bonus_label1, fill="black", font=font_label)
                # bonus_section = obj.ubicacion['section']
                # w, h = bonus.textsize(bonus_section, font=font_label)
                # bonus.text((160, 739), bonus_section, fill="#056b3d", font=font_label)
                #
                # bonus_label2 = 'FILA:'
                # w, h = bonus.textsize(bonus_label2, font=font_label)
                # bonus.text((280+5, 739), bonus_label2, fill="black", font=font_label)
                # bonus_row = obj.ubicacion['row']
                # w, h = bonus.textsize(bonus_row, font=font_label)
                # bonus.text((332+5, 739), bonus_row, fill="#056b3d", font=font_label)
                #
                # bonus_label3 = 'ASIENTO:'
                # w, h = bonus.textsize(bonus_label3, font=font_label)
                # bonus.text((400+50, 739), bonus_label3, fill="black", font=font_label)
                # bonus_seat = obj.ubicacion['seat']
                # w, h = bonus.textsize(bonus_seat, font=font_label)
                # bonus.text((497+50, 739), bonus_seat, fill="#056b3d", font=font_label)
                # # QR
                # qr_img = qrcode.make(obj.folio, border=0, box_size=15)
                # qr_w, qr_h = qr_img.size
                # offset = (164, 264)
                #
                # img.paste(qr_img, offset)
                # img.save(b1, 'PNG', quality=100)
                # images.append(b1)
                # b1.name = '{}_{}.png'.format(bonus_name, obj.folio)

    if len(images) > 1:
        for im in images:
            zf.writestr(im.name, im.getvalue())
        zf.close()
        response = HttpResponse(b2.getvalue(), content_type='application/application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=BONOS.zip'
    else:
        if img_flag:
            response = HttpResponse(b1.getvalue(), content_type='image/jpg')
        else:
            response = HttpResponse(b1.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename={}'.format(b1.name)
        b1.close()
    return response


def generate_bonus_resp(bonus):
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
            font_short_medium = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 28)
            font_short_small = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 22)
            font_label = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 26)
            font_label_small = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 18)
            font_label_v2 = ImageFont.truetype('static/fonts/Oswald-DemiBold.ttf', 76)
            # regular-v1--------------
            img = None
            if obj.tipo.startswith("jaguares"):
                img = Image.open("static/bonus/{}.png".format(obj.tipo), 'r')
            else:
                img = Image.open("static/bonus/bonus_24.png", 'r')

            if img.mode == "CMYK":
                img = img.convert("RGB")

            bonus = ImageDraw.Draw(img)
            avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int(img.size[0] * .90 / avg_char_width)
            text = textwrap.fill(text=bonus_name, width=max_char_count)

            if obj.tipo.startswith("jaguares"):
                if obj.tipo == "jaguares_sombra":
                    if len(text.splitlines()) > 1:
                        bonus.text(xy=(120, img.size[1] / 1.45), text=text.replace("\n", " "), font=font_short_medium, fill='#000000')
                    else:
                        bonus.text(xy=(120, img.size[1] / 1.45), text=text.replace("\n", " "), font=font_short_medium, fill='#000000')

                    bonus_section = obj.ubicacion['section']
                    bonus.text((190, 800), bonus_section, fill="#056b3d", font=font_label_small)

                    bonus_row = obj.ubicacion['row']
                    bonus.text((340, 800), bonus_row, fill="#056b3d", font=font_label_small)

                    bonus_seat = obj.ubicacion['seat']
                    bonus.text((530, 800), bonus_seat, fill="#056b3d", font=font_label_small)
                elif obj.tipo == "jaguares_palco":
                    if len(text.splitlines()) > 1:
                        bonus.text(xy=(120, img.size[1] / 1.45), text=text.replace("\n", " "), font=font_short_medium, fill='#000000')
                    else:
                        bonus.text(xy=(120, img.size[1] / 1.45), text=text.replace("\n", " "), font=font_short_medium, fill='#000000')

                    bonus_row = obj.ubicacion['section']
                    bonus.text((360, 790), bonus_row, fill="#056b3d", font=font_label_small)

                else:
                    if len(text.splitlines()) > 1:
                        bonus.text(xy=(120, img.size[1] / 1.45), text=text.replace("\n", " "), font=font_short_small,
                                   fill='#000000')
                    else:
                        bonus.text(xy=(120, img.size[1] / 1.45), text=text.replace("\n", " "), font=font_short_small, fill='#000000')

                    bonus_label1 = 'SECCIÓN:'
                    w, h = bonus.textsize(bonus_label1, font=font_label_small)
                    bonus.text((110, 739), bonus_label1, fill="black", font=font_label_small)
                    bonus_section = obj.ubicacion['section']
                    w, h = bonus.textsize(bonus_section, font=font_label_small)
                    bonus.text((180, 739), bonus_section, fill="#056b3d", font=font_label_small)

                    bonus_label2 = 'FILA:'
                    w, h = bonus.textsize(bonus_label2, font=font_label_small)
                    bonus.text((300, 739), bonus_label2, fill="black", font=font_label_small)
                    bonus_row = obj.ubicacion['row']
                    w, h = bonus.textsize(bonus_row, font=font_label_small)
                    bonus.text((340, 739), bonus_row, fill="#056b3d", font=font_label_small)

                    bonus_label3 = 'ASIENTO:'
                    w, h = bonus.textsize(bonus_label3, font=font_label_small)
                    bonus.text((400, 739), bonus_label3, fill="black", font=font_label_small)
                    bonus_seat = obj.ubicacion['seat']
                    w, h = bonus.textsize(bonus_seat, font=font_label_small)
                    bonus.text((470, 739), bonus_seat, fill="#056b3d", font=font_label_small)
                    # QR
                qr_img = qrcode.make(obj.folio, border=0, box_size=12)
                qr_w, qr_h = qr_img.size
                offset = (205, 355)
            else:
                if len(text.splitlines()) > 1:
                    bonus.text(xy=(90, img.size[1] / 1.45), text=text, font=font_short, fill='#000000')
                else:
                    bonus.text(xy=(60, img.size[1] / 1.53), text=text, font=font_short, fill='#000000')

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