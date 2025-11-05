import asyncio
import base64
from urllib import response
from faststream.rabbit import RabbitBroker
from faststream import FastStream
from pydantic import BaseModel

# Importa o TimeoutError do asyncio
from asyncio import TimeoutError


# Schemas
class ImageAnalysisRequest(BaseModel):
    image_bytes: bytes
    mime_type: str


class ImageAnalysisResponse(BaseModel):
    analysis_text: str


# --- CONFIGURAÇÃO ---
IMAGE_PATH = "sample_images/chest-xray/pneumonia/person1946_4874.jpeg"
MIME_TYPE = "image/jpeg"
# ---------------------

# 1. Configurar o Broker (igual ao seu consumer)
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(broker)

# --- SINCRONIZAÇÃO (A MÁGICA) ---
# Criamos um "Evento" do asyncio.
# A função main() vai esperar por ele.
# O subscriber vai "ativar" ele quando receber a resposta.
response_received = asyncio.Event()
# ---------------------------------


# 2. Seu publisher (não usado no main, mas pode ficar)
@broker.publisher(queue="image_analysis")
async def send_analysis_request(msg: ImageAnalysisRequest):
    pass


# 3. Seu subscriber (Ouvinte da Resposta)
@broker.subscriber(queue="image_analysis_response")
async def receive_analysis_response(msg: ImageAnalysisResponse) -> None:
    """
    Escuta a fila de respostas de análise de imagem.
    """
    print(f"\n--- Resposta Recebida ---")
    print(f"Análise: {msg.analysis_text}")
    print("--------------------------\n")

    # *** MUDANÇA AQUI ***
    # Avisa à função main() que a resposta chegou
    response_received.set()


async def main():
    """
    Função principal para carregar a imagem e chamar o RPC.
    """

    # 3. Ler e codificar a imagem
    print(f"Carregando imagem de: {IMAGE_PATH}...")
    try:
        with open(IMAGE_PATH, "rb") as f:
            image_bytes_raw = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{IMAGE_PATH}'.")
        print("Por favor, atualize a variável IMAGE_PATH no script.")
        return

    # Codificar os bytes para base64 (como string)
    image_b64_string = base64.b64encode(image_bytes_raw)

    # 4. Criar a mensagem de requisição
    request_message = ImageAnalysisRequest(
        image_bytes=image_b64_string, mime_type=MIME_TYPE
    )

    print("Conectando ao broker e registrando subscribers...")

    # 5. Conectar e iniciar os ouvintes (incluindo o receive_analysis_response)
    await broker.start()

    try:
        # Publica a mensagem exatamente como você fez
        await broker.publish(
            request_message,
            queue="image_analysis",
            reply_to="image_analysis_response",
        )
        print("Pedido enviado. Aguardando resposta do worker...")

    except TimeoutError:
        print("\nErro: O pedido expirou (Timeout).")
        print("Verifique se o seu 'consumer' (worker) está rodando.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

    while response_received.is_set() is False:
        # Espera até que o evento seja setado pelo subscriber
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
