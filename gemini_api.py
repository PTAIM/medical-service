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


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    test_normal_image_path = "sample_images/chest-xray/normal/IM-1427-0001.jpeg"

    logger.info("Starting test analysis of a NORMAL chest X-ray image.")
    result = analyze_image(test_normal_image_path)

    if result:
        logger.info(f"Analysis complete. Result: {result.text}")
    else:
        logger.error("Analysis failed.")

    logger.info("Starting test analysis of a CHEST X-ray image with pneumonia.")
    test_pneumonia_image_path = (
        "sample_images/chest-xray/pneumonia/person1946_4874.jpeg"
    )
    result = analyze_image(test_pneumonia_image_path)

    if result:
        logger.info(f"Analysis complete. Result: {result.text}")
    else:
        logger.error("Analysis failed.")
