from google import genai
from get_logger import app_logger

# Use google/medgemma-4b-it model from Google GenAI API to analyze medical images
client = genai.Client(api_key="AIzaSyDGWLIXBvYHdsXfuVTfVy3r0CjoZMJsfOk")
PROMPT = "Describe this X-ray"
SYSTEM_PROMPT = (
    "You are an expert multimodal medical imaging assistant trained on medical texts and images. "
    "Your primary task is to analyze the provided image and patient data to generate a structured, objective report. "
    "CRITICAL RULE: You must NEVER provide definitive diagnoses or treatment recommendations. "
)


def analyze_image(image_path: str) -> dict:
    # Implement the logic to analyze the image using Google GenAI API
    app_logger.info(f"Analyzing image at {image_path} using Google GenAI API.")
    # list_response = client.models.list()  # Just to ensure the client is working
    # return list_response
    try:
        uploaded_file = client.files.upload(file=image_path)
        app_logger.info(f"   -> Upload successful. URI: {uploaded_file.uri}")
    except Exception as e:
        app_logger.error(f"Error during file upload: {e}")
        return

    contents = [uploaded_file, PROMPT]
    app_logger.info("   -> Generating content using Google GenAI API.")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=contents,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=200, system_instruction=SYSTEM_PROMPT
            ),
        )
    except Exception as e:
        app_logger.error(f"Error during content generation: {e}")
        return

    return response
