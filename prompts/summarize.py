from utils.llm_client import get_completion

def summarize_review(review, max_words = 30):
    prompt = f"""
    Your task is to generate a short summary of a product review from 
    an ecommerce site. 

    Summarize the review below, delimited by triple backticks in at
    most {max_words} words.

    Review: ```{review}```
    """
    return get_completion(prompt)


def summarize_for_shipping(review):
    prompt = f"""
    Your task is to generate a short summary of a product review from an 
    ecommerce site to give feedback to the Shipping department.

    Summarize the review below in at most 30 words, delimited by triple backticks focusing on any
    aspect that mention the shipping and delivery of the product. 

    If no shipping review found, just mention so and do not make it up.

    Review: ```{review}```
    """
    return get_completion(prompt)

def summarize_for_value(review):
    prompt = f"""
    Your task is to generate a short summary of a product review from an
    ecommerce site, focusing on price and perceived value for money. 

    Summarize the review below in at most 30 words, focusing on value and
    pricing.
    
    Review: ```{review}```
    """
    return get_completion(prompt)