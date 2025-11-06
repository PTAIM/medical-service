import os
from faststream import FastStream
import uvicorn
import base64
from typing import Dict, Any
from dotenv import load_dotenv
from faststream.rabbit import RabbitBroker
from gemini_api import analyze_image_from_bytes
from schemas import ImageAnalysisRequest, ImageAnalysisResponse

# Carrega variáveis de ambiente
load_dotenv()

# 1. Configurar o Broker do FastStream
rabbit_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

broker = RabbitBroker(rabbit_url)
app = FastStream(broker)


@broker.subscriber(queue="image_analysis")
@broker.publisher(queue="image_analysis_response")
async def analyze_consumer(msg: ImageAnalysisRequest) -> ImageAnalysisResponse:
    """
    Escuta a fila "image_analysis", recebe os dados da imagem,
    e chama a função de análise.
    """
    print("Recebido pedido de análise de imagem.")
    # Decodificar a imagem de base64
    image_bytes = base64.b64decode(msg.image_bytes)

    # Chamar a função de análise demorada
    result = analyze_image_from_bytes(image_bytes=image_bytes, mime_type=msg.mime_type)

    # Imprimir o resultado no console do worker
    print(f"Análise completa:\n{result}")
    return ImageAnalysisResponse(analysis_text=result)
