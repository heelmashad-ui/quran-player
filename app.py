import streamlit as st
import requests

st.set_page_config(page_title="Al-Quran Al-Kareem", page_icon="📖", layout="wide")

# Custom CSS for modern design
st.markdown("""
<style>
.main { background-color: #f7f9fc; }
h1, h2, h3 { color: #2c3e50; font-family: 'serif'; }
.arabic-name { text-align: center; color: #4CAF50; font-size: 50px; margin-bottom: 5px; font-family: 'Arial', sans-serif; }
.english-title { margin-top: 0; color: #333; text-align: center; }
.reading-panel {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# 1. Fetch Surahs from the API
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
    # 2. Reciters and Surah Options
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
    
    surah_options = {f"{s['number']}. {s['englishName']}": s for s in surahs}

    # Public image URLs for the aesthetic look
    sidebar_image_url = "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?auto=format&fit=crop&w=600&q=80"
    reading_image_url = "https://images.unsplash.com/photo-1601287132924-4061a99eb2a0?auto=format&fit=crop&w=1000&q=80"

    # 3. Sidebar UI and General App Visuals
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>✨ Al-Quran Al-Kareem</h2>", unsafe_allow_html=True)
        # Display Sidebar Image directly from URL
        st.image(sidebar_image_url, use_container_width=True)

        st.markdown("---")
        st.markdown("### Selection Panel")
        selected_reciter_name = st.selectbox("Select Reciter", list(reciters.keys()))
        selected_surah_key = st.selectbox("Select Surah", list(surah_options.keys()))
        
        st.markdown("---")
        st.markdown("<p style='color: gray; font-size: 11px; text-align:center;'>Immerse yourself in the divine recitations of world-renowned Qaris.</p>", unsafe_allow_html=True)

    # 4. Main Page Visuals and Data
    st.title("📖 Divine Recitations")

    # Fetch dynamic data
    selected_reciter_id = reciters[selected_reciter_name]
    surah_data = surah_options[selected_surah_key]
    surah_num = surah_data['number']

    # Display dynamic header in a stylized panel
    st.markdown(f"<div class='reading-panel'>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='arabic-name'>{surah_data['name']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 class='english-title'>{surah_data['englishName']} ({surah_data['englishNameTranslation']})</h3>", unsafe_allow_html=True)
    
    # Construct and display Audio Player
    audio_url = f"https://cdn.islamic.network/quran/audio-surah/128/{selected_reciter_id}/{surah_num}.mp3"
    st.audio(audio_url, format="audio/mp3")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual 3: "Page that is read" visual directly from URL
    st.image(reading_image_url, caption="The Noble Qur'an", use_container_width=True)
    
    st.markdown(f"</div>", unsafe_allow_html=True)

    st.markdown("<p style='color: gray; font-size: 12px; text-align: center; margin-top: 30px;'>Data and audio delivered via <a href='https://alquran.cloud/'>Al Quran Cloud API</a>.</p>", unsafe_allow_html=True)
