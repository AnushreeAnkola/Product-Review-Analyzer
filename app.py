import streamlit as st
from utils.sample_reviews import reviews
from prompts.summarize import summarize_review, summarize_for_shipping, summarize_for_value
from prompts.infer import infer_sentiment, infer_emotions, infer_topics, infer_recommendation
from prompts.transform import translate_review, adjust_tone, fix_grammar
from prompts.expand import generate_reply

st.title("Product Review Analyzer")
st.markdown("AI-powered product review analysis using prompt engineering techniques")


option = st.selectbox("Pick review of a product",
                          [r['product'] for r in reviews])


def get_review(reviews):
    for r in reviews:
        product = r['product']
        if product == option:
            review = r['review']
            return review

txt = st.text_area(
    "Customer Reviews",
    get_review(reviews), height=200  
)


review = get_review(reviews)

if st.button("Analyze the Review", type="primary"):
    with st.spinner("Wait for it...", show_time=True):
        st.write('Summary of the review is')
        st.write(summarize_review(review))
        st.write('Shipping Summary')
        st.write(summarize_for_shipping(review))
        st.write('Price Summary')
        st.write(summarize_for_value(review))
        st.write('Infer Sentiment')
        sentiment = infer_sentiment(review)
        st.write(sentiment)
        st.write("Add an auto reply to the review")
        st.write(generate_reply(review,sentiment))
        st.write('Infer Emotion')
        st.write(infer_emotions(review))
        st.write('Infer Topic')
        st.write(infer_topics(review))
        st.write('Infer Recommendation')
        st.write(infer_recommendation(review))
        st.write('Fix Grammar')
        st.write(fix_grammar(review))

languages = ['Hindi', 'Kannada', 'French', 'Spanish']
chosen_lang = st.selectbox("Pick a language", languages)
if st.button("Translate Review to a language of your choice", type="primary"):
    with st.spinner("Translating.."):
        st.write(translate_review(review, chosen_lang))

tones = ['Business Formal', 'Formal', 'Casual', 'Super Casual']
tone = st.selectbox("Pick a tone", tones)

if st.button("Adjust the tone of the review", type="primary"):
    with st.spinner("Adjusting the tone.."):
        st.write(adjust_tone(review, tone=tone))


