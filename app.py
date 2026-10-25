import streamlit as st
from groq import Groq

# 1. Konfigurasi Tampilan Halaman
st.set_page_config(
    page_title="AI Chatbot Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Personal Assistant")
st.caption("Final Project Data Scientist - Chatbot Berbasis LLM")

# 2. Sidebar Konfigurasi & Parameter Kreatif
with st.sidebar:
    st.header("⚙️ Konfigurasi Parameter")
    api_key = st.text_input("Groq API Key", type="password", help="Masukkan API Key Groq Anda")
    
    persona = st.selectbox(
        "Gaya Bahasa / Persona",
        ["Formal & Profesional", "Santai & Ramah", "Edukatif & Detail"]
    )
    
    temperature = st.slider("Kreativitas (Temperature)", 0.0, 1.0, 0.7)
    
    st.markdown("---")
    st.markdown("### 💡 Informasi")
    st.info("Aplikasi ini ditenagai oleh model Llama via Groq API.")

# 3. Inisialisasi Riwayat Percakapan (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Tampilkan Riwayat Percakapan
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Area Input Pengguna & Pemprosesan Respon
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    if not api_key:
        st.error("Silakan masukkan Groq API Key terlebih dahulu di sidebar!")
        st.stop()

    # Tampilkan pesan user di UI & simpan di memory
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Panggil API Groq
    try:
        client = Groq(api_key=api_key)
        system_instruction = f"Anda adalah asisten AI yang membantu. Jawablah dengan gaya bahasa {persona}."

        # Susun payload percakapan
        messages_payload = [{"role": "system", "content": system_instruction}] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]

        # Generate respon dari model Llama yang aktif
        with st.spinner("Sedang berpikir..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_payload,
                temperature=temperature,
            )
            bot_response = response.choices[0].message.content

        # Tampilkan respon bot di UI & simpan di memory
        st.chat_message("assistant").write(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memanggil API: {e}")
