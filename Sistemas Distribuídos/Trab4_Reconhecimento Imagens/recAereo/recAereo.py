import boto3
import json
from PIL import Image,ImageDraw,ImageFont
import io

client = boto3.client('rekognition', region_name='us-east-1')

imagem = "Imagens/ilhas.png"

with open(imagem,'rb') as arq_imagem:
    source_bytes = arq_imagem.read()


detectaObj = client.detect_labels(Image={'Bytes' : source_bytes})

image = Image.open(io.BytesIO(source_bytes))
draw = ImageDraw.Draw(image)


# detectaObj = client.detect_labels(
#     Image={
#         'S3Object': {
#             'Bucket': 'bucket-trabalho3',
#             'Name': 'mina.png'
#         }
#     },
#     MaxLabels=10,
#     MinConfidence=70
# )

print(json.dumps(detectaObj['Labels'], indent=2))

for objeto in detectaObj["Labels"]:
    nome = objeto["Name"]  
    precisao = objeto["Confidence"]
    print(f"{nome} - {precisao}")

    for instances in objeto["Instances"]:
        if 'BoundingBox' in instances:
            quadro = instances["BoundingBox"]

            left = image.width * quadro['Left']
            top = image.height * quadro['Top']
            width = image.width * quadro['Width']
            height = image.height * quadro['Height']

            pontos = (
                        (left, top),
                        (left + width, top),
                        (left + width, top + height),
                        (left,top + height),
                        (left,top)
                    )
            
            draw.line(pontos, width=5, fill = "#fa0202")

            retangulo = [(left - 2, top - 35),(width + 2 + left, top)]
            draw.rectangle(retangulo, fill = "#fa0202")

            fonte = ImageFont.truetype("arial.ttf",30)

            draw.text((left + 10,top - 30),nome, font=fonte, fill = "#000000")
            
image.show()  