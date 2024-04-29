import google.generativeai as genai
import os
from flask import current_app
import random



def generate_text(prompt):
    google_api_key = (os.getenv('GOOGLE_API_KEY')).split(";")
    google_api_key = random.choice(google_api_key)
    genai.configure(api_key=google_api_key) 
    model = genai.GenerativeModel('gemini-pro', generation_config={"max_output_tokens": 100000})
    current_app.logger.info(f"[Co-Pilot] Generating text for prompt: {prompt}")
    ## Mask API Key while logging and just log the last 5 characters
    current_app.logger.info(f"[Co-Pilot] Using API Key: {'*'*(len(google_api_key)-5)}{google_api_key[-5:]}")
    reponse = model.generate_content(prompt,generation_config={
    "max_output_tokens": 100000,
    "temperature": 0.5,
    })

    return reponse.text