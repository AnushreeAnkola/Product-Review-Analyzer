from utils.sample_reviews import reviews
from prompts.summarize import summarize_review, summarize_for_shipping, summarize_for_value
from prompts.infer import infer_sentiment, infer_emotions, infer_topics, infer_recommendation
from prompts.transform import translate_review, adjust_tone, fix_grammar
from prompts.expand import generate_reply

review = reviews[0]['review']
print('Product:', reviews[0]['product'])
print('Summary:', summarize_review(review))
print("Summary for shipping:", summarize_for_shipping(review))
print("Summary for value:", summarize_for_value(review))
print("Infer Sentiment:", infer_sentiment(review))
print("Infer Emotion:", infer_emotions(review))
print("Infer Topic:", infer_topics(review))
print("Infer Recommendation:", infer_recommendation(review))
print("Translate Review", translate_review(review, language="French"))
print("Adjust Tone", adjust_tone(review, tone="Super Casual"))
print("Fix Grammar", fix_grammar(review))

print("Auto reply: Positive review", generate_reply(reviews[0]['review'],"positive"))
print("Auto reply: Negative review", generate_reply(reviews[1]['review'], "negative"))