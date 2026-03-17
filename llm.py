
import os
import google.generativeai as genai
import streamlit as st

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-flash-latest")

def generate_story(query, contexts):

    context_text = "\n".join([c.page_content for c in contexts])

    prompt = f"""
You are a storyteller narrating the Ramayana to people aged 7-20.

Scene:
{query}

Relevant verses from the Ramayana:
{context_text}

Write an engaging narrative explaining this event.
Make it feel like an engaging and imaginative story while remaining faithful to the verses .
"""

    response = model.generate_content(prompt)

    return response.text

# for m in genai.list_models():
#     print(m.name)