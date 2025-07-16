import streamlit as st
import requests
import os

API_KEY = st.secrets["NEWS_API_KEY"]  # 👈 Secure way

st.set_page_config(page_title="📰 NewsSnap", layout="centered")
st.title("📰 Live News App")
st.write("Get the latest news by category and country.")

BASE_URL = "https://newsapi.org/v2/top-headlines"
categories = ["general", "business", "entertainment", "health", "science", "sports", "technology"]
country = st.selectbox("Select Country:", ["in", "us", "gb", "au", "ca", "sg"])
selected_category = st.selectbox("Choose Category:", categories)

if st.button("Get News"):
    if not API_KEY:
        st.error("API Key not found in secrets.")
    else:
        params = {
            "apiKey": API_KEY,
            "country": country,
            "category": selected_category,
            "pageSize": 5
        }
        response = requests.get(BASE_URL, params=params).json()
        if response["status"] == "ok":
            for i, article in enumerate(response["articles"]):
                st.subheader(f"{i+1}. {article['title']}")
                st.write(article.get("description", "No description available."))
                st.markdown(f"[🔗 Read more]({article['url']})")
                st.write("---")
        else:
            st.error("Failed to fetch news.")
