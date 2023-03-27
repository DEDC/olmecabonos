# Django
from django import template
# qrcode
import qrcode
import qrcode.image.svg
from io import BytesIO

register = template.Library()

@register.inclusion_tag('templatetags/qr_generator.html')
def generate_qr(text):
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(text, image_factory=factory, box_size=10, border=0)
    stream = BytesIO()
    img.save(stream)
    return {'qr': stream.getvalue().decode()}