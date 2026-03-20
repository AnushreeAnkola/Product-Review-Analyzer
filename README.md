# Product Review Analyzer
AI-powered product review analysis using prompt engineering techniques learned from DeepLearning.AI's **ChatGPT Prompt Engineering for Developers** course.

## About

This project applies prompt engineering concepts:
- summarizing, 
- inferring, 
- transforming, 
- and expanding 

to analyze product reviews and extract meaningful insights. 

## Features

1. Summarize : Generate concise summaries of reviews, with focused summaries for shipping and value
2. Infer : Detect sentiment, emotions, topics, and purchase recommendation
3. Transform : Translate reviews, adjust tone, and fix grammar
4. Expand : Auto-generate customer service replies tailored to review sentiment
5. Streamlit UI : Interactive web app with sample review selector (in progress)

## Tech Stack

>Python 3.12
>
>Anthropic Claude API
>
>Streamlit
>
>python-dotenv


## Setup

Clone the repo

```bash
    git clone https://github.com/AnushreeAnkola/Product-Review-Analyzer.git
```

```bash
    cd Product-Review-Analyzer
```

Create and activate a virtual environment

```bash
    python3.12 -m venv venv
```
```bash
   source venv/bin/activate
```

Install dependencies

```bash
    pip install -r requirements.txt
```

Add your Anthropic API key

```bash
    cp .env.example .env
   # Edit .env and add your key
```

Run the app

```bash
    streamlit run app.py
```

## What's Next

1. Complete the Streamlit UI with full analysis dashboard
2. Add prompt iteration notebook documenting the refinement process
3. Deploy to Streamlit Community Cloud