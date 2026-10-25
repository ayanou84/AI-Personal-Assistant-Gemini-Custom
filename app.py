import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Set Halaman Streamlit
st.set_page_config(page_title="AI Chatbot Assistant", page_icon="🤖")
st.title("🤖 AI Personal Assistant")
st.caption("Final Project - Chatbot Berbasis LLM")

# Sidebar untuk Konfigurasi Parameter Kreatif
with st.sidebar:
    st.header("⚙️ Konfigurasi Parameter")
    api_key = st.text_input("Groq API Key", type="password")
    persona = st.selectbox(
        "Gaya Bahasa / Persona",
        ["Formal & Profesional", "Santai & Ramah", "Edukatif & Detail"]
    )
    temperature = st.slider("Kreativitas (Temperature)", 0.0, 1.0, 0.7)

# Inisialisasi History Percakapan (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan History Chat
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

# Input Pesan Pengguna
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    if not api_key:
        st.info("Masukkan Groq API Key terlebih dahulu di sidebar.")
        st.stop()

    # Tambah pesan pengguna ke history
    st.chat_message("user").write(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # System Prompt berdasarkan persona
    system_instruction = f"Anda adalah asisten AI yang membantu. Jawablah dengan gaya bahasa {persona}."

    # Panggil Model LLM
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=temperature
    )

    # Kirim percakapan ke model
    messages_to_send = [SystemMessage(content=system_instruction)] + st.session_state.messages
    with st.spinner("Sedang mengetik..."):
        response = llm.invoke(messages_to_send)

    # Tampilkan dan simpan respon bot
    st.chat_message("assistant").write(response.content)
    st.session_state.messages.append(AIMessage(content=response.content))