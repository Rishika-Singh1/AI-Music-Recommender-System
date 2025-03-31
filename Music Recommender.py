import openai
import streamlit as st
import os
# Set OpenAI API Key (Replace with your actual key)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to Get Music Recommendations
def get_mood_based_music_recommendation(user_mood):
    try:
        client = openai.OpenAI()  # ✅ New API client
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ✅ Free-tier compatible
            messages=[
                {"role": "system", "content": "You are an AI that suggests songs based on mood."},
                {"role": "user", "content": f"Recommend 3 songs for someone feeling {user_mood}."}
            ]
        )
        return response.choices[0].message.content.strip()  # ✅ Extract response

    except openai.APIError as e:  # ✅ Handles API errors
        return f"OpenAI API error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Streamlit UI
st.title("🎵 AI Music Mood Recommender 🎵")
st.write("Tell me how you feel, and I'll recommend the perfect music for you!")

# User Input
user_mood = st.text_input("Describe your current mood:")
if st.button("Get Recommendation"):
    if user_mood:
        recommendation = get_mood_based_music_recommendation(user_mood)
        st.success(f"🎧 Recommended Songs: {recommendation if recommendation else 'No songs found'}")
    else:
        st.warning("Please enter your mood to get recommendations.")
