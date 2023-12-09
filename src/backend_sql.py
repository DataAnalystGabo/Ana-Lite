import os
import pymysql.cursors
from dotenv import load_dotenv
from aiogram.utils.markdown import hbold

load_dotenv()

def querySQL(input_address):

    connection   = pymysql.connect(
        host     = os.getenv('MYSQLDB_HOST'),
        user     = os.getenv('MYSQLDB_USER'),
        password = os.getenv('MYSQLDB_ROOT_PASSWORD'),
        database = os.getenv('MYSQLDB_DATABASE'),
        port     = os.getenv('MYSQLDB_PORT'),
        cursorclass=pymysql.cursors.DictCursor
    )


    input_address = input_address.upper()
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM Permisos WHERE DIRECCION LIKE '{input_address}' LIMIT 10")

    records = cursor.fetchall()

    if len(records) == 1:
        response = f"Ey, encontré un permiso para {input_address}. Acá esta la información para la dirección:\n\n"
    if len(records) > 1:
        response = f"¡Qué suerte! encontré más de un permiso para la dirección {input_address}. Acá está la información:\n\n"
    else:
        response = f"¡Ups! No se encontraron permisos para la dirección {input_address}"

    for data in records:
        response += f"""
{hbold('ID:  ')} {data['ID']}
{hbold('CLASE DE AVISO:  ')} {data['CLASE_AVISO']}
{hbold('EMPRESA:  ')} {data['EMPRESA']}
{hbold('CONTRATISTA:  ')} {data['CONTRATISTA']}
{hbold('DIRECCION:  ')} {data['DIRECCION']}
{hbold('COMUNA:  ')} {data['COMUNA']}
{hbold('BARRIO:  ')} {data['BARRIO']}
{hbold('TIPO DE OBRA:  ')} {data['TIPO_OBRA']}
{hbold('TIPO DE CONTROL:  ')} {data['TIPO_CONTROL']}
{hbold('ESTADO DE LA INCIDENCIA:  ')} {data['ESTADO_INCIDENCIA']}
{hbold('OBSERVACIONES:  ')} {data['OBSERVACIONES;']}

-----------------------------------------------------
"""

    cursor.close()
    connection.close()

    return response
