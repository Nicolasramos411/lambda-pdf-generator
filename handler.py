import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from boto3 import client
import io
import uuid


def hello(event, context):

    # Datos de ejemplo
    datos_usuario = {
        "nombre": "Juan Pérez",
        "direccion": "Calle Principal 123",
        # ... Agrega más datos según tus necesidades
    }

    entrada_comprada = {
        "titulo": "Concierto",
        "fecha": "26 de mayo de 2023",
        # ... Agrega más datos según tus necesidades
    }

    # Crear un nuevo archivo PDF
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Configurar fuentes y tamaños de texto
    pdf.setFont("Helvetica", 12)
    pdf.setFont("Helvetica-Bold", 12)

    # Escribir los datos del usuario
    pdf.drawString(50, 700, "Datos del Usuario:")
    pdf.drawString(50, 680, f"Nombre: {datos_usuario['nombre']}")
    pdf.drawString(50, 660, f"Dirección: {datos_usuario['direccion']}")
    # ... Agrega más líneas según los datos que quieras mostrar

    # Escribir la entrada comprada
    pdf.drawString(50, 600, "Entrada Comprada:")
    pdf.drawString(50, 580, f"Título: {entrada_comprada['titulo']}")
    pdf.drawString(50, 560, f"Fecha: {entrada_comprada['fecha']}")
    # ... Agrega más líneas según los datos que quieras mostrar

    # Guardar y cerrar el archivo PDF
    pdf.save()
    pdf_buffer.seek(0)

    # Guardar pdf en S3 con permisos públicos

    s3 = client('s3')
    bucket_name = 'aws-python-pdf-generator-serverlessdeploymentbuck-1t99xs5ra2yn9'
    file_name = f'entrada-{uuid.uuid4()}.pdf'
    file = s3.put_object(Bucket=bucket_name, Key=file_name,
                         Body=pdf_buffer, ACL='public-read')

    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
        'file_url': f'https://{bucket_name}.s3.amazonaws.com/{file_name}'
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
