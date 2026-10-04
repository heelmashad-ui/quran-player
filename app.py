import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Function to encode a PIL image to base64 for HTML embedding
def get_image_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

st.set_page_config(page_title="Al-Quran Al-Kareem - Divine Recitations", page_icon="📖", layout="wide")

# Custom CSS for modern design and imagery integration
st.markdown("""
<style>
/* Existing CSS, refined */
.main { background-color: #f7f9fc; }
h1, h2, h3 { color: #2c3e50; font-family: 'Playfair Display', serif; }
.arabic-name { text-align: center; color: #4CAF50; font-size: 50px; margin-bottom: 5px; font-family: 'Amiri', serif; }
.english-title { margin-top: 0; color: #333; text-align: center; font-family: 'Playfair Display', serif;}
.caption-text { color: gray; font-size: 12px; font-style: italic; }

/* New CSS for Reading Panel and Imagery */
.reading-panel {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin-top: 10px;
    margin-bottom: 20px;
}
.sidebar-header-image {
    width: 100%;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.reciter-collage-image {
    width: 100%;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.reading-visual-image {
    width: 100%;
    border-radius: 15px;
    margin-top: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
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

    # Load images as PIL objects for base64 encoding
    # Placeholder paths; in real scenario, these would be local file paths or URLs
    image_reciters_collage = Image.open('image_0.png') # Single Collage of all 9 reciters
    image_reading_visual = Image.open('image_1.png') # Stylized "page that is read"

    # 3. Sidebar UI and General App Visuals
    with st.sidebar:
        # Visual 1: Qur'an and General Header
        st.markdown("<h2 style='text-align: center; color: #2c3e50; font-family: Playfair Display, serif;'>✨ Al-Quran Al-Kareem</h2>", unsafe_allow_html=True)
        st.markdown(f'<img src="data:image/png;base64,{get_image_base64(image_reciters_collage)}" class="reciter-collage-image">', unsafe_allow_html=True)

        st.markdown("---")
        # Visual 2: Controls and dynamic imagery for selection
        st.markdown("### Selection Panel")
        selected_reciter_name = st.selectbox("Select Reciter", list(reciters.keys()), key='reciter_select')
        selected_surah_key = st.selectbox("Select Surah", list(surah_options.keys()), key='surah_select')
        
        # Display symbolic portrait of the selected reciter (extracted from the collage visual)
        # For simplicity in this illustrative context, we show the collage itself.
        st.markdown("---")
        st.markdown("<p style='color: gray; font-size: 11px; text-align:center;'>Reciter imagery is symbolic of famous voices.</p>", unsafe_allow_html=True)

    # 4. Main Page Visuals and Data
    st.title("📖 Al-Quran Al-Kareem - Divine Recitations")

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
    
    # Visual 3: "Page that is read" placeholder visual
    st.markdown(f'<img src="data:image/png;base64,{get_image_base64(image_reading_visual)}" class="reading-visual-image">', unsafe_allow_html=True)
    st.markdown(f"<p class='caption-text' style='text-align:center; font-style:italic;'>A stylized visualization of the divine word and spiritual listening.</p>", unsafe_allow_html=True)
    
    st.markdown(f"</div>", unsafe_allow_html=True)

    st.markdown("<p class='caption-text' style='text-align: center; margin-top: 30px;'>Data and audio delivered via <a href='https://alquran.cloud/'>Al Quran Cloud API</a>.</p>", unsafe_allow_html=True)
