import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan Halaman
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Personal Assistant (Gemini)")
st.caption("Final Project - Chatbot Berbasis Google Gemini")

# 2. Sidebar Konfigurasi & Parameter
with st.sidebar:
    st.header("⚙️ Konfigurasi Parameter")
    api_key = st.text_input("Gemini API Key", type="password", help="Masukkan Gemini API Key Anda")
    
    persona = st.selectbox(
        "Gaya Bahasa / Persona",
        ["Formal & Profesional", "Santai & Ramah", "Edukatif & Detail"]
    )
    
    st.markdown("---")
    st.markdown("### 💡 Informasi")
    st.info("Aplikasi ini ditenagai oleh model Google Gemini (gemini-3.5-flash-lite).")

# 3. Inisialisasi Riwayat Percakapan (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Tampilkan Riwayat Percakapan di UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Area Input Pengguna & Pemrosesan Respon
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key di sidebar terlebih dahulu!")
        st.stop()

    # Tampilkan pesan user ke UI & simpan ke session state
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Panggil API Google Generative AI
    try:
        genai.configure(api_key=api_key)
        
        # Konfigurasi instruksi sistem berdasarkan persona yang dipilih
        system_instruction = f"Anda adalah asisten AI yang membantu. Jawablah dengan gaya bahasa {persona}."
        
        # Menggunakan gemini-1.5-flash dengan system_instruction
        model = genai.GenerativeModel(
            model_name="gemini-3.5-flash-lite",
            system_instruction=system_instruction
        )

        # Ubah format riwayat chat Streamlit agar sesuai dengan format history Gemini
        gemini_history = []
        for m in st.session_state.messages[:-1]: # Ambil riwayat sebelum pesan terbaru
            # Gemini menggunakan role 'user' dan 'model'
            role = "user" if m["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [m["content"]]})

        # Mulai sesi chat dengan membawa memori percakapan sebelumnya
        chat_session = model.start_chat(history=gemini_history)

        # Generate respon dari model dengan indikator loading
        with st.spinner("Sedang berpikir..."):
            response = chat_session.send_message(prompt)
            bot_response = response.text

        # Tampilkan respon bot ke UI & simpan ke session state
        st.chat_message("assistant").write(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memanggil API Gemini: {e}")
