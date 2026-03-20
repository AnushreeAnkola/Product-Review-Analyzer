import json
from utils.llm_client import get_completion

def infer_sentiment(review):
    prompt = f"""What is the sentiment of the following product review?

Respond with ONLY one word: positive, negative, or mixed.

Review: \"\"\"{review}\"\"\"
"""
    return get_completion(prompt).strip().lower()

def infer_emotions(review):
    prompt = f"""Identify the key emotions expressed in the following product review.

Return your answer as a JSON array of emotion strings, e.g. ["joy", "frustration"].
Respond with ONLY the JSON array, nothing else.

Review: \"\"\"{review}\"\"\"
"""
    result = get_completion(prompt)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return [result.strip()]

def infer_topics(review):
    prompt = f"""Identify the main topics or themes discussed in the following product review.

Return your answer as a JSON array of short topic strings, e.g. ["battery life", "sound quality", "price"].
Respond with ONLY the JSON array, nothing else.

Review: \"\"\"{review}\"\"\"
"""
    result = get_completion(prompt)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return [result.strip()]

def infer_recommendation(review):
    prompt = f"""Based on the following product review, would the reviewer recommend this product?

Respond with ONLY one word: yes, no, or unclear.

Review: \"\"\"{review}\"\"\"
"""
    return get_completion(prompt).strip().lower()