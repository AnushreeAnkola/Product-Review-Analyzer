from utils.llm_client import get_completion

def translate_review(review, language):
    prompt = f"""
    Your task is to translate the following English review to {language}:
    review: ```{review}```
    """
    return get_completion(prompt)

def adjust_tone(review, tone):
    prompt = f"""
    Your task is to rephrase the following review to {tone} tone
    review: ```{review}```
    """
    return get_completion(prompt)

def fix_grammar(review):
    prompt = f"""
    Proof read and correct the grammer of the following review and rewrite the
    correct version. If you don't find any errors, just say "No error found". Do not
    use any punctuations around the text.
    review: ```{review}```
    """
    return get_completion(prompt)