from google import genai
from dotenv import load_dotenv
from google.genai import types
import os

# Load API key once at import
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if api_key is None:
    raise ValueError("Unable to get API Key. Make sure GEMINI_API_KEY is set in .env")

client = genai.Client()

def call_gemini(selected_text, role_instruction):
    """Helper to call Gemini with different instructions."""
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        config=types.GenerateContentConfig(
            system_instruction=role_instruction
        ),
        contents=selected_text
    )
    return response.text

def define_text(selected_text: str) -> str:
    """Return a simplified, context-aware definition in jot note style 
    
    (Format:)
    • Point 1....
    • Point 2....
    
    """
    prompt = (
        f"Act as a professional dictionary. Define the following text in **i-jot note format**: "
        f"short bullet points, dashes, very concise. Use relevant context or related info. "
        f"No full sentences unless essential. Avoid extra explanations.\n\n"
        f"Text: {selected_text}"
    )
    return call_gemini(selected_text, prompt)

def detailed_explanation(selected_text: str) -> str:
    """Return a detailed, context-aware explanation in i-jot note style 
    
    (Format:)
    • Point 1....
    • Point 2.... 
    
    """
    prompt = (
        f"Act as an expert tutor. Explain the following text in **i-jot note format**: "
        f"short bullet points, dashes, concise phrases. Include relevant context, examples, "
        f"analogies, and connections to related concepts. Avoid long sentences.\n\n"
        f"Text: {selected_text}"
    )
    return call_gemini(selected_text, prompt)


def diagram_text(selected_text):
    """Useful diagrams or visual aids."""
    return call_gemini(
        selected_text,
        "You are a visual teacher. Provide useful diagrams or schematic descriptions. "
        "If diagrams cannot be drawn directly, use ASCII art or describe clearly what the diagram should look like. "
        "Format your response in Markdown, using code blocks (```) for ASCII art."
    )
