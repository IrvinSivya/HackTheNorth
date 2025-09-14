from google import genai
from dotenv import load_dotenv
from google.genai import types
import os

def define_text(selected_text):
  # The client gets the API key from the environment variable `GEMINI_API_KEY`.
  load_dotenv()
  api_key = os.getenv('GEMINI_API_KEY')
  if (api_key == None):
    print("Unable to get API Key")
    exit()

  client = genai.Client()

  response = client.models.generate_content(
    model="gemini-2.5-flash", 
    config=types.GenerateContentConfig (
	  system_instruction="You are a dictionary. Provide only concise definitions of the given text." \
    "Keep the response under 2 lines and avoid extra explanations."),
	  contents=selected_text)
  
  return(response.text)

def summarize_text(selected_text):
  # The client gets the API key from the environment variable `GEMINI_API_KEY`.
  load_dotenv()
  api_key = os.getenv('GEMINI_API_KEY')
  if (api_key == None):
    print("Unable to get API Key")
    exit()

  client = genai.Client()

  response = client.models.generate_content(
    model="gemini-2.5-flash", 
    config=types.GenerateContentConfig(
	  system_instruction="You are an explainer. Summarize the given text in clear, simple language." \
    "Keep the response under 10 lines, but make sure to explain key concepts so the reader fully understands them."\
    "Avoid unnecessary detail or repetition."),
	  contents=selected_text)
  
  return(response.text)