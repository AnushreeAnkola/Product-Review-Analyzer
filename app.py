import streamlit as st
from utils.sample_reviews import reviews

st.title("Product Review Analyzer")
st.markdown("AI-powered product review analysis using prompt engineering techniques")


option = st.selectbox("Pick a review",
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