
import streamlit as st
import requests
from transformers import pipeline

# Load API key securely from Streamlit secrets
API_KEY = st.secrets["NEWS_API_KEY"]

# Set page title
st.set_page_config(page_title="🧠 NewsMind – Real-Time News Sentiment", layout="centered")
st.title("🧠 NewsMind – Real-Time News Sentiment Predictor")
st.write("Get live news headlines and predict their sentiment using a Hugging Face ML model.")

# Country mapping with full names
country_mapping = {
    "India 🇮🇳": "in",
    "United States 🇺🇸": "us",
    "United Kingdom 🇬🇧": "gb",
    "Australia 🇦🇺": "au",
    "Canada 🇨🇦": "ca",
    "Singapore 🇸🇬": "sg",
    "France 🇫🇷": "fr",
    "Germany 🇩🇪": "de",
    "Italy 🇮🇹": "it",
    "Japan 🇯🇵": "jp",
    "Brazil 🇧🇷": "br",
    "New Zealand 🇳🇿": "nz",
    "South Africa 🇿🇦": "za",
    "United Arab Emirates 🇦🇪": "ae",
    "China 🇨🇳": "cn",
    "Russia 🇷🇺": "ru"
}

# News categories
categories = [
    "general", "business", "entertainment",
    "health", "science", "sports", "technology"
]

# UI dropdowns
selected_country_name = st.selectbox("🌍 Select Country", list(country_mapping.keys()))
selected_country_code = country_mapping[selected_country_name]
selected_category = st.selectbox("🗂 Select News Category", categories)

# Load sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

# Button click
if st.button("🧠 Fetch News & Predict Sentiment"):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": API_KEY,
        "country": selected_country_code,
        "category": selected_category,
        "pageSize": 5
    }

    response = requests.get(url, params=params).json()

    if response["status"] == "ok":
        articles = response.get("articles", [])
        if not articles:
            st.warning("No articles found.")
        for i, article in enumerate(articles):
            title = article["title"]
            result = sentiment_pipeline(title)[0]
            label = result["label"]
            confidence = round(result["score"] * 100, 2)
            emoji = "😊" if label == "POSITIVE" else "☹"

            st.subheader(f"{i+1}. {title}")
            st.write(f"{emoji} *Sentiment:* {label} ({confidence}%)")
            st.markdown(f"[🔗 Read more]({article['url']})")
            st.write("---")
    else:
        st.error("❌ Failed to fetch news. Please check your API key or try again later.")
