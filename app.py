"""Offline Streamlit entry point for the fitness chatbot MVP."""

import streamlit as st

from src.dialogue import build_response, new_profile, profile_text, update_profile
from src.entity_extractor import extract_entities
from src.intent_classifier import classify_intent
from src.utils import load_exercises


st.set_page_config(page_title="Fitness Chatbot", page_icon="💪")
st.title("Personal Fitness Chatbot")
st.caption("Offline educational assistant — not a substitute for professional medical advice.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = new_profile()

with st.sidebar:
    st.header("Profile")
    st.write(profile_text(st.session_state.profile))
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.profile = new_profile()
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("How can I help with your fitness goals?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    intent = classify_intent(prompt)
    entities = extract_entities(prompt)
    update_profile(st.session_state.profile, entities)
    response = build_response(intent, entities, st.session_state.profile, load_exercises())

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
