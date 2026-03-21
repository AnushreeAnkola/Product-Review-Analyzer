import streamlit as st
from utils.sample_reviews import reviews
from prompts.summarize import summarize_review, summarize_for_shipping, summarize_for_value
from prompts.infer import infer_sentiment, infer_emotions, infer_topics, infer_recommendation
from prompts.transform import translate_review, adjust_tone, fix_grammar
from prompts.expand import generate_reply

# ──────────────────────────────────────────────
# PAGE CONFIG & CUSTOM CSS
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Review Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,500;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f14 0%, #1a1a24 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown h1 {
        font-size: 1.3rem;
        letter-spacing: -0.02em;
    }

    /* ── Metric cards ── */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 16px 20px;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.6;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
    }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 24px;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: -0.01em;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 0.95rem;
    }

    /* ── Buttons ── */
    .stButton > button[kind="primary"] {
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: -0.01em;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(255,75,75,0.25);
    }

    /* ── Toast-style result cards ── */
    .result-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 12px;
    }
    .result-card h4 {
        margin: 0 0 8px 0;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        opacity: 0.5;
    }
    .result-card p {
        margin: 0;
        line-height: 1.65;
    }

    /* ── Sentiment badge ── */
    .sentiment-positive {
        display: inline-block;
        background: linear-gradient(135deg, #22c55e33, #22c55e11);
        border: 1px solid #22c55e55;
        color: #4ade80;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .sentiment-negative {
        display: inline-block;
        background: linear-gradient(135deg, #ef444433, #ef444411);
        border: 1px solid #ef444455;
        color: #f87171;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .sentiment-mixed {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b33, #f59e0b11);
        border: 1px solid #f59e0b55;
        color: #fbbf24;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* ── Topic pills ── */
    .topic-pill {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #a5b4fc;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 3px 4px 3px 0;
    }

    /* ── Comparison columns ── */
    .compare-header {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(255,255,255,0.08);
    }

    /* hide default streamlit footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ──────────────────────────────────────────────
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None


# ──────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────
def get_review_by_product(product_name):
    for r in reviews:
        if r["product"] == product_name:
            return r["review"]
    return ""


def render_sentiment_badge(sentiment):
    sentiment = str(sentiment)
    s = sentiment.strip().lower()
    if "positive" in s:
        css_class = "sentiment-positive"
        emoji = "😊"
    elif "negative" in s:
        css_class = "sentiment-negative"
        emoji = "😞"
    else:
        css_class = "sentiment-mixed"
        emoji = "😐"
    st.markdown(
        f'<span class="{css_class}">{emoji} {sentiment}</span>',
        unsafe_allow_html=True,
    )


def render_topic_pills(topics_input):
    if isinstance(topics_input, list):
        topics = [str(t).strip() for t in topics_input if str(t).strip()]
    else:
        topics = [t.strip() for t in str(topics_input).split(",") if t.strip()]
    pills_html = "".join(f'<span class="topic-pill">{t}</span>' for t in topics)
    st.markdown(pills_html, unsafe_allow_html=True)


def render_result_card(title, content):
    content = str(content)
    st.markdown(
        f'<div class="result-card"><h4>{title}</h4><p>{content}</p></div>',
        unsafe_allow_html=True,
    )


def run_full_analysis(review_text):
    """Run all analysis steps and return a results dict."""
    results = {}

    results["summary"] = summarize_review(review_text)
    results["shipping"] = summarize_for_shipping(review_text)
    results["value"] = summarize_for_value(review_text)
    results["sentiment"] = infer_sentiment(review_text)
    results["emotions"] = infer_emotions(review_text)
    results["topics"] = infer_topics(review_text)
    results["recommendation"] = infer_recommendation(review_text)
    results["grammar"] = fix_grammar(review_text)
    results["reply"] = generate_reply(review_text, results["sentiment"])

    return results


def run_selected_analysis(review_text, selected):
    """Run only the selected analysis features."""
    results = {}
    if "Summary" in selected:
        results["summary"] = summarize_review(review_text)
    if "Shipping Focus" in selected:
        results["shipping"] = summarize_for_shipping(review_text)
    if "Value Focus" in selected:
        results["value"] = summarize_for_value(review_text)
    if "Sentiment" in selected:
        results["sentiment"] = infer_sentiment(review_text)
    if "Emotions" in selected:
        results["emotions"] = infer_emotions(review_text)
    if "Topics" in selected:
        results["topics"] = infer_topics(review_text)
    if "Recommendation" in selected:
        results["recommendation"] = infer_recommendation(review_text)
    if "Grammar Fix" in selected:
        results["grammar"] = fix_grammar(review_text)
    if "Auto Reply" in selected:
        sentiment = results.get("sentiment") or infer_sentiment(review_text)
        results["reply"] = generate_reply(review_text, sentiment)
    return results


def display_results(results):
    """Render analysis results in a nice layout."""
    # ── Row 1: Metric cards ──
    if any(k in results for k in ("sentiment", "recommendation", "emotions")):
        cols = st.columns(3)
        with cols[0]:
            if "sentiment" in results:
                st.markdown("##### Sentiment")
                render_sentiment_badge(results["sentiment"])
        with cols[1]:
            if "recommendation" in results:
                rec = results["recommendation"]
                emoji = "✅" if "recommend" in rec.lower() else "⚠️"
                st.metric("Recommendation", f"{emoji} {rec}")
        with cols[2]:
            if "emotions" in results:
                st.markdown("##### Emotions")
                render_topic_pills(results["emotions"])

    st.divider()

    # ── Row 2: Summaries in tabs ──
    summary_keys = {"summary", "shipping", "value"} & results.keys()
    if summary_keys:
        tab_labels = []
        tab_data = []
        if "summary" in results:
            tab_labels.append("📝 Overview")
            tab_data.append(("Overall Summary", results["summary"]))
        if "shipping" in results:
            tab_labels.append("📦 Shipping")
            tab_data.append(("Shipping-Focused Summary", results["shipping"]))
        if "value" in results:
            tab_labels.append("💰 Value")
            tab_data.append(("Value-Focused Summary", results["value"]))

        tabs = st.tabs(tab_labels)
        for tab, (title, content) in zip(tabs, tab_data):
            with tab:
                render_result_card(title, content)

    # ── Row 3: Topics ──
    if "topics" in results:
        st.markdown("##### Detected Topics")
        render_topic_pills(results["topics"])
        st.markdown("")

    # ── Row 4: Grammar & Auto Reply side by side ──
    extras = {"grammar", "reply"} & results.keys()
    if extras:
        cols = st.columns(2 if len(extras) == 2 else 1)
        idx = 0
        if "grammar" in results:
            with cols[idx]:
                with st.expander("✏️ Grammar-Corrected Review", expanded=False):
                    st.write(results["grammar"])
            idx += 1
        if "reply" in results:
            with cols[min(idx, len(cols) - 1)]:
                with st.expander("💬 Auto-Generated Reply", expanded=True):
                    st.write(results["reply"])


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🔍 Review Analyzer")
    st.caption("AI-powered product review analysis")

    st.divider()

    # ── Input mode ──
    input_mode = st.radio(
        "Review source",
        ["Sample reviews", "Paste your own"],
        horizontal=True,
    )

    if input_mode == "Sample reviews":
        product = st.selectbox(
            "Product",
            [r["product"] for r in reviews],
        )
        review_text = get_review_by_product(product)
    else:
        review_text = ""

    st.divider()

    # ── Analysis toggles ──
    st.markdown("**Select analyses to run**")
    all_features = [
        "Summary",
        "Shipping Focus",
        "Value Focus",
        "Sentiment",
        "Emotions",
        "Topics",
        "Recommendation",
        "Grammar Fix",
        "Auto Reply",
    ]

    if st.button("Select All", use_container_width=True):
        st.session_state["selected_features"] = all_features

    selected_features = st.multiselect(
        "Features",
        all_features,
        default=st.session_state.get("selected_features", ["Summary", "Sentiment", "Topics", "Recommendation"]),
        label_visibility="collapsed",
    )
    st.session_state["selected_features"] = selected_features

    st.divider()

    # ── Transform options ──
    st.markdown("**Transform**")
    languages = ["Hindi", "Kannada", "French", "Spanish", "German", "Japanese", "Korean", "Portuguese"]
    chosen_lang = st.selectbox("Translate to", languages)

    tones = ["Business Formal", "Formal", "Casual", "Super Casual", "Enthusiastic", "Empathetic"]
    chosen_tone = st.selectbox("Adjust tone to", tones)

    st.divider()

    # ── History ──
    if st.session_state.analysis_history:
        st.markdown("**Recent Analyses**")
        for i, entry in enumerate(reversed(st.session_state.analysis_history[-5:])):
            st.caption(f"🕐 {entry['product'][:30]}…")


# ──────────────────────────────────────────────
# MAIN CONTENT
# ──────────────────────────────────────────────
st.markdown("## 📝 Review Input")

if input_mode == "Paste your own":
    review_text = st.text_area(
        "Paste a customer review",
        placeholder="Enter a product review to analyze…",
        height=180,
    )
else:
    review_text = st.text_area(
        "Customer Review",
        value=review_text,
        height=180,
    )

if not review_text.strip():
    st.info("Enter or select a review to get started.")
    st.stop()

# ── Word count bar ──
word_count = len(review_text.split())
st.caption(f"📊 {word_count} words  ·  {len(review_text)} characters")

st.markdown("")

# ── Action buttons ──
col_a, col_b, col_c = st.columns([1, 1, 1])

with col_a:
    run_analysis = st.button("🔍 Analyze Review", type="primary", use_container_width=True)
with col_b:
    run_translate = st.button(f"🌐 Translate → {chosen_lang}", use_container_width=True)
with col_c:
    run_tone = st.button(f"🎭 Adjust Tone → {chosen_tone}", use_container_width=True)

st.markdown("---")

# ──────────────────────────────────────────────
# ANALYSIS EXECUTION
# ──────────────────────────────────────────────
if run_analysis:
    if not selected_features:
        st.warning("Select at least one analysis feature in the sidebar.")
    else:
        progress_bar = st.progress(0, text="Starting analysis…")
        step_count = len(selected_features)

        # Run analysis
        results = {}
        for i, feature in enumerate(selected_features):
            progress_bar.progress(
                (i + 1) / step_count,
                text=f"Running: {feature}…",
            )
            partial = run_selected_analysis(review_text, [feature])
            results.update(partial)

        progress_bar.empty()

        st.session_state.last_analysis = results
        st.session_state.analysis_history.append({
            "product": review_text[:40],
            "results": results,
        })

        st.success("Analysis complete!")
        display_results(results)

        # ── Download report ──
        report_lines = []
        report_lines.append("# Product Review Analysis Report\n")
        report_lines.append(f"**Review:** {review_text[:100]}…\n")
        for key, val in results.items():
            report_lines.append(f"## {key.replace('_', ' ').title()}\n{val}\n")
        report_md = "\n".join(report_lines)

        st.download_button(
            "📥 Download Report (.md)",
            data=report_md,
            file_name="review_analysis_report.md",
            mime="text/markdown",
        )

elif run_translate:
    with st.spinner(f"Translating to {chosen_lang}…"):
        translated = translate_review(review_text, chosen_lang)
    st.markdown(f"### 🌐 Translation ({chosen_lang})")
    render_result_card(f"Translated to {chosen_lang}", translated)

elif run_tone:
    with st.spinner(f"Adjusting tone to {chosen_tone}…"):
        adjusted = adjust_tone(review_text, tone=chosen_tone)
    st.markdown(f"### 🎭 Tone: {chosen_tone}")
    render_result_card(f"Review in {chosen_tone} Tone", adjusted)

# ── Show last analysis if nothing new was run ──
elif st.session_state.last_analysis:
    st.markdown("### Previous Analysis Results")
    display_results(st.session_state.last_analysis)


# ──────────────────────────────────────────────
# COMPARISON MODE
# ──────────────────────────────────────────────
st.markdown("---")
with st.expander("⚖️ Compare Two Products", expanded=False):
    st.markdown("Select two products to compare their reviews side by side.")
    comp_cols = st.columns(2)

    product_names = [r["product"] for r in reviews]

    with comp_cols[0]:
        prod_a = st.selectbox("Product A", product_names, key="comp_a")
    with comp_cols[1]:
        prod_b = st.selectbox(
            "Product B",
            product_names,
            index=min(1, len(product_names) - 1),
            key="comp_b",
        )

    if st.button("🔍 Compare", use_container_width=True):
        review_a = get_review_by_product(prod_a)
        review_b = get_review_by_product(prod_b)

        with st.spinner("Analyzing both products…"):
            results_a = run_full_analysis(review_a)
            results_b = run_full_analysis(review_b)

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(f'<div class="compare-header">{prod_a}</div>', unsafe_allow_html=True)
            render_sentiment_badge(results_a["sentiment"])
            st.markdown("")
            render_topic_pills(results_a["topics"])
            st.markdown("")
            render_result_card("Summary", results_a["summary"])
            render_result_card("Recommendation", results_a["recommendation"])

        with col_right:
            st.markdown(f'<div class="compare-header">{prod_b}</div>', unsafe_allow_html=True)
            render_sentiment_badge(results_b["sentiment"])
            st.markdown("")
            render_topic_pills(results_b["topics"])
            st.markdown("")
            render_result_card("Summary", results_b["summary"])
            render_result_card("Recommendation", results_b["recommendation"])