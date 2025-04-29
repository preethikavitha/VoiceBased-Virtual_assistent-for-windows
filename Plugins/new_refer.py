import os
import re
import json
import tempfile
import time
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from dotenv import load_dotenv
from gtts import gTTS
import pygame  # For playing audio

# Load environment variables
load_dotenv(dotenv_path='..\\Data\\.env')

def get_news():
    try:
        api_key = os.getenv('NEWS_API')

        if not api_key:
            return "Error: NEWS_API key not found. Please set it as an environment variable."

        # Initialize NewsAPI client
        news = NewsApiClient(api_key=api_key)

        # Fetch top headlines from India
        top_headlines = news.get_top_headlines(language="en", country="us")

        if 'articles' not in top_headlines or not top_headlines['articles']:
            return "No news articles found. Try again later."

        # Extract and clean up titles
        articles = top_headlines['articles'][:5]  # Read only the top 5 headlines

        # Format the news for speech
        news_text = "Here are the top news headlines from India:\n\n" + "\n".join([
            f"Headline {i+1}: {article['title']}" for i, article in enumerate(articles)
        ])

        return news_text

    except NewsAPIException as e:
        return f"News API error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def speak_news(text):
    try:
        # Convert text to speech using gTTS
        tts = gTTS(text, lang="en", slow=False)
        
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
            temp_filename = temp_audio.name
            tts.save(temp_filename)
            
            # Initialize pygame mixer
            pygame.mixer.init()
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(1)

    except Exception as e:
        print(f"Error in speech synthesis: {e}")

if __name__ == "__main__":
    news_text = get_news()
    print(news_text)  # Display headlines
    speak_news(news_text)  # Speak headlines
