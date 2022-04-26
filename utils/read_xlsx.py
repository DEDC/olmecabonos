# Openpyxl
import openpyxl
from apps.bonos.models import Bono

def read_bonus():
    wb_obj = openpyxl.load_workbook('vitalicio.xlsx')
    sheet_obj = wb_obj.active
    max_row = sheet_obj.max_row
    max_col = sheet_obj.max_column
    
    for i in range(1, max_row+1):
        abonado = {
            'nombre': sheet_obj.cell(row = i, column = 2).value,
            'correo': '',
            'telefono': ''
        }
        tipo = sheet_obj.cell(row = i, column = 1).value
        centenario = {
            'seccion': sheet_obj.cell(row = i, column = 3).value,
            'fila': sheet_obj.cell(row = i, column = 4).value,
            'butaca': sheet_obj.cell(row = i, column = 5).value
        }
        macuspana = {
            'seccion': sheet_obj.cell(row = i, column = 6).value,
            'fila': sheet_obj.cell(row = i, column = 7).value,
            'butaca': sheet_obj.cell(row = i, column = 8).value
        }
        
        Bono.objects.create(
            tipo = tipo,
            abonado = abonado,
            ubicacion = {'centenario': centenario, 'macuspana': macuspana}
        )
        i = i+1