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
    system_prompt = (
        f"You are a dictionary. Provide only concise definitions of the given text."
        f"Keep the response under 2 lines and avoid extra explanations."
        f"Do NOT include BOLD letters or asterics in you answers"
    )
    return call_gemini(selected_text, system_prompt)

def detailed_explanation(selected_text: str) -> str:
    """Return a detailed, context-aware explanation. Respond without using any asterisks and no bolding. 
    """
    system_prompt = (
        f"You are an explainer. Summarize the given text in clear, simple language."
        f"Keep the response under 10 lines, but make sure to explain key concepts so the reader fully understands them."
        f"Avoid unnecessary detail or repetition."
        f"Do NOT include BOLD letters or asterics in you answers"
    )
    return call_gemini(selected_text, system_prompt)


def question_text(selected_text, question):
    """Useful diagrams or visual aids."""
    print(question)
    system_prompt = (
        f"You are a knowledgeable tutor and assistant. Answer the user's questions about the given text clearly and accurately "
        f"that helps users understand selected text.  "
        f"Base your answer on the text first, and only add outside knowledge if it helps clarify the meaning. "
        f"Keep explanations concise, clear, and directly tied to the selected text."
        f"If the question is not related to text at all then just provide the best possible answer."
        f"Do NOT include BOLD letters or asterics in you answers"
        f"Do NOT ask back questions")
    return call_gemini(selected_text + "Question is: " + question , system_prompt)

