from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_story(query, contexts):

    context_text = "\n".join([c.page_content for c in contexts])

    prompt = f"""
You are a storyteller narrating the Ramayana to children.

Scene:
{query}

Relevant verses from the Ramayana:
{context_text}

Write an engaging narrative explaining this event.
Make it feel like an engaging and imaginative story while remaining faithful to the verses .
"""

    response = model.generate_content(prompt)

    return response.text