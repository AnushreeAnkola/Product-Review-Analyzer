import os
import anthropic
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

try:
    client = anthropic.Anthropic(api_key=st.secrets['ANTHROPIC_API_KEY'])
    
except:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_completion(prompt, system_message="You are a helpful assistant.", model="claude-sonnet-4-20250514", temperature=0):
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_message,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.content[0].text