from google import genai
from dotenv import load_dotenv
import os

def define_text(selected_text):
  
  # The client gets the API key from the environment variable `GEMINI_API_KEY`.
  load_dotenv(dotenv_path='./extensions/.env')
  api_key = os.getenv('GEMINI_API_KEY')
  if (api_key == None):
    print("Unable to get API Key")
    exit()

  client = genai.Client()

  response = client.models.generate_content(
	  model="gemini-2.5-flash", 
	  system_instruction="You need to provide definitions/short summaries of inputed text. " \
	  "Make it no longer than 2 or 3 lines",
	  contents=selected_text)
  
  return(response.text)