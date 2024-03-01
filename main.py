import streamlit as st
from openai import OpenAI

key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Personal Moderation Assistant")

st.header("📱 Personal Moderation Assistant")
st.subheader('Science Fair Project by Wafaa in Grade 8', divider='rainbow')

if "user_messages" not in st.session_state:
    st.session_state["user_messages"] = [
        {"role": "assistant", "content": "Hi, how can I help you?"}]

for user_msg in st.session_state.user_messages:
    st.chat_message(user_msg["role"]).write(user_msg["content"])

if user_prompt := st.chat_input():
    st.session_state.user_messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    client = OpenAI(api_key=key)
    response = client.chat.completions.create(model="gpt-4",
                                                                          messages=[
                                                                              {"role": "system",
                                                                               "content": f"YOU MUST FOLLOW THE SCRIPT AT THE END OF THE PROMPT.\\n\\nBACKGROUND INFO:\\n\\nYou are a chatbot designed to help with cause and prevention of video games addiction. Your job is to provide rehablitation in video games addiction and steps to reduce screen time. Ask user about their name, age and screen time the provide treatment what suits best to them. If someone inquires about anything else other than screen time, video games, Video games addiction respond with 'I am a chatbot designed to help with cause and prevention of video games addiction. could you please try relevant questions."},
                                                                              {"role": "user",
                                                                               "content": user_prompt}
                                                                          ],
                                                                          temperature=0.5,
                                                                          max_tokens=360,
                                                                          top_p=1
                                                                          )
    user_msg = response.choices[0].message.content
    st.session_state.user_messages.append({"role": "assistant", "content": user_msg})
    st.chat_message("assistant").write(user_msg)
