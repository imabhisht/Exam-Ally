import google.generativeai as genai
import logging
import os
from flask import current_app
genai.configure(api_key=os.getenv('GOOGLE_API_KEY')) 
model = genai.GenerativeModel('gemini-pro', generation_config={"max_output_tokens": 100000})


def generate_text(prompt):
    current_app.logger.info(f"[Co-Pilot] Generating text for prompt: {prompt}")
    reponse = model.generate_content(prompt,generation_config={
    "max_output_tokens": 100000,
    "temperature": 0.5,
    })

    return reponse.text