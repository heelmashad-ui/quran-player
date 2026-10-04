import streamlit as st
import requests

st.set_page_config(page_title="Quran Player", page_icon="📖", layout="centered")

st.title("📖 Quran Recitation Player")

# Cache the API response
@st.cache_data
def get_surahs():
    try:
        response = requests.get("https://api.alquran.cloud/v1/surah")
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.RequestException:
        return []

surahs = get_surahs()

if not surahs:
    st.error("Failed to load Surah data. Please check your internet connection.")
else:
    # Reciters with complete Quran recordings
    reciters = {
        "Mishary Rashid Alafasy": "ar.alafasy",
        "Maher Al Muaiqly": "ar.mahermuaiqly",
        "Abdur-Rahman As-Sudais": "ar.abdurrahmaansudais",
        "Saud Al-Shuraim": "ar.saoodshuraym",
        "Abdul Basit (Murattal)": "ar.abdulbasitmurattal",
        "Mahmoud Khalil Al-Husary": "ar.husary",
        "Muhammad Siddiq Al-Minshawi": "ar.minshawi",
        "Abu Bakr Al-Shatri": "ar.shaatree",
        "Ali Jaber": "ar.alijaber"
    }

    # UI Controls
    col1, col2 = st.columns(2)
    with col1:
        selected_reciter = st.selectbox("Select Reciter", list(reciters.keys()))
    with col2:
        surah_options = {f"{s['number']}. {s['englishName']}": s for s in surahs}
        selected_surah_key = st.selectbox("Select Surah", list(surah_options.keys()))

    surah_data = surah_options[selected_surah_key]
    surah_num = surah_data['number']
    
    st.markdown("---")
    
    # Display Arabic and English Surah Names
    st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{surah_data['name']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{surah_data['englishName']} ({surah_data['englishNameTranslation']})</h3>", unsafe_allow_html=True)
    
    # Direct Audio Stream URL
    audio_url = f"https://cdn.islamic.network/quran/audio-surah/128/{reciters[selected_reciter]}/{surah_num}.mp3"
    
    # Streamlit Audio Player
    st.audio(audio_url, format="audio/mp3")
    
    st.caption("Data and audio delivered via [Al Quran Cloud API](https://alquran.cloud/).")
