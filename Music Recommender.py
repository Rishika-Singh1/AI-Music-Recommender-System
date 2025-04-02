import openai
import streamlit as st
import os
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud

# Set OpenAI API Key
api_key = os.getenv("API KEY")  # Ensure your API key is set
if not api_key:
    st.error("❌ OpenAI API key is missing! Set it as an environment variable or in the code.")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=api_key)

# Function to Get Music Recommendations
def get_mood_based_music_recommendation(user_mood):
    try:
        response = client.chat.completions.create(  
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that suggests songs based on mood."},
                {"role": "user", "content": f"Recommend 3 songs for someone feeling {user_mood}."}
            ]
        )
        return response.choices[0].message.content.strip().split("\n")  

    except openai.APIError as e:
        return [f"❌ OpenAI API error: {e}"]
    except openai.RateLimitError:
        return ["⚠️ API rate limit exceeded. Try again later."]
    except openai.AuthenticationError:
        return ["❌ Invalid OpenAI API key. Check your key and try again."]
    except Exception as e:
        return [f"❌ An unexpected error occurred: {e}"]

# Streamlit UI
st.title("🎵 AI Music Mood Recommender 🎵")
st.write("Tell me how you feel, and I'll recommend the perfect music for you!")

# User Input
user_mood = st.text_input("Describe your current mood:")
if st.button("Get Recommendation"):
    if user_mood:
        recommended_songs = get_mood_based_music_recommendation(user_mood)

        # Display Song Recommendations
        if recommended_songs:
            st.success("🎧 Recommended Songs:")
            for song in recommended_songs:
                st.write(f"- {song}")
            
            # **1️⃣ Word Cloud Visualization of Mood**
            st.subheader("🎭 Mood Word Cloud")
            wordcloud = WordCloud(width=500, height=300, background_color="white").generate(user_mood)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

            # **2️⃣ Bar Chart: Mood vs. Song Recommendations**
            st.subheader("📊 Mood vs. Song Recommendations")
            song_names = [song[:20] for song in recommended_songs if song]  # Filter valid songs
            y_pos = np.arange(len(song_names))
            plt.figure(figsize=(8, 5))
            plt.barh(y_pos, [5] * len(song_names), color="skyblue")
            plt.yticks(y_pos, song_names)
            plt.xlabel("Mood Influence Score")
            plt.title(f"Songs Recommended for Mood: {user_mood}")
            st.pyplot(plt)

        else:
            st.warning("⚠️ No recommendations found!")
    else:
        st.warning("⚠️ Please enter your mood to get recommendations.")
