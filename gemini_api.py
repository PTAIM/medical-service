from google import genai

import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GEMINI_API_LOGGER")


PROMPT = "Describe this image"
SYSTEM_PROMPT = (
    "You are an expert multimodal medical imaging assistant trained on medical texts and images. "
    "Your primary task is to analyze the provided image and patient data to generate a structured, objective report. "
    "CRITICAL RULE: You must NEVER provide definitive diagnoses or treatment recommendations. "
)


def analyze_image(image_path: str) -> dict:
    client = genai.Client()

    logger.info(f"Analyzing image at {image_path} using Google GenAI API.")
    try:
        uploaded_file = client.files.upload(file=image_path)
        logger.info(f"   -> Upload successful. URI: {uploaded_file.uri}")
    except Exception as e:
        logger.error(f"Error during file upload: {e}")
        return

    contents = [uploaded_file, PROMPT]
    logger.info("   -> Generating content using Google GenAI API.")

    response = None

    attemps = 3

    while attemps > 0:
        attemps -= 1
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=genai.types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )
            return response.text
        except Exception as e:
            logger.error(f"Error during content generation: {e}")
            time.sleep(1)


def analyze_image_from_bytes(image_bytes: bytes, mime_type: str) -> str:
    """
    Analisa uma imagem a partir de seus bytes e mime_type.
    """
    client = genai.Client()

    logger.info(
        f"Analyzing image ({mime_type}, {len(image_bytes)} bytes) using Google GenAI API."
    )

    # --- Início da Mudança Principal ---

    # 1. Crie a "parte" da imagem diretamente dos bytes.
    #    Não é mais necessário fazer o upload do arquivo primeiro.
    try:
        image_part = genai.types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    except Exception as e:
        logger.error(f"Erro ao criar a 'Part' da imagem: {e}")
        return None

    # 2. Construa o 'contents' com a parte da imagem e o prompt
    contents = [image_part, PROMPT]

    # --- Fim da Mudança Principal ---

    logger.info("   -> Generating content using Google GenAI API.")

    response = None
    attempts = 3  # Corrigi o "attemps" para "attempts"

    while attempts > 0:
        attempts -= 1
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=genai.types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )
            # Retorna o texto diretamente
            return response.text

        except Exception as e:
            logger.error(f"Error during content generation: {e}")
            time.sleep(1)

    logger.error("Falha ao gerar conteúdo após 3 tentativas.")
    return None  # Retorna None se todas as tentativas falharem


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    test_normal_image_path = "sample_images/chest-xray/normal/IM-1427-0001.jpeg"

    logger.info("Starting test analysis of a NORMAL chest X-ray image.")

    with open(test_normal_image_path, "rb") as image_file:
        image_bytes = image_file.read()
        result = analyze_image_from_bytes(image_bytes, "image/jpeg")

    if result:
        logger.info(f"Analysis complete. Result: {result}")
    else:
        logger.error("Analysis failed.")

    logger.info("Starting test analysis of a CHEST X-ray image with pneumonia.")
    test_pneumonia_image_path = (
        "sample_images/chest-xray/pneumonia/person1946_4874.jpeg"
    )
    with open(test_pneumonia_image_path, "rb") as image_file:
        image_bytes = image_file.read()
        result = analyze_image_from_bytes(image_bytes, "image/jpeg")

    if result:
        logger.info(f"Analysis complete. Result: {result}")
    else:
        logger.error("Analysis failed.")
