import requests
import ipywidgets as widgets
from IPython.display import display, HTML, Audio, clear_output

# 1. Fetch Surahs from the API
def get_surahs():
    try:
        response = requests.get("https://api.alquran.cloud/v1/surah")
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.RequestException:
        return []

surahs = get_surahs()

if not surahs:
    print("Failed to load Surah data. Please check your internet connection.")
else:
    # 2. Verified Reciters with Complete 114 Surah Audio (Murattal)
    reciters = {
        "Mishary Rashid Alafasy": "ar.alafasy",
        "Maher Al Muaiqly": "ar.mahermuaiqly",  # Added
        "Abdur-Rahman As-Sudais": "ar.abdurrahmaansudais",
        "Saud Al-Shuraim": "ar.saoodshuraym",
        "Abdul Basit (Murattal)": "ar.abdulbasitmurattal",
        "Mahmoud Khalil Al-Husary": "ar.husary",
        "Muhammad Siddiq Al-Minshawi": "ar.minshawi",
        "Abu Bakr Al-Shatri": "ar.shaatree",
        "Ali Jaber": "ar.alijaber"            # Added
    }
    
    surah_options = {f"{s['number']}. {s['englishName']}": s for s in surahs}
    
    # 3. Create Interactive Jupyter Widgets
    reciter_dropdown = widgets.Dropdown(
        options=list(reciters.keys()),
        value='Mishary Rashid Alafasy',
        description='Reciter:',
        layout={'width': '300px'}
    )
    
    surah_dropdown = widgets.Dropdown(
        options=list(surah_options.keys()),
        value=list(surah_options.keys())[0], # Defaults to Al-Fatihah
        description='Surah:',
        layout={'width': '300px'}
    )
    
    out = widgets.Output()

    # 4. Update Function
    def update_player(change=None):
        with out:
            clear_output(wait=True)
            
            selected_reciter_id = reciters[reciter_dropdown.value]
            surah_data = surah_options[surah_dropdown.value]
            surah_num = surah_data['number']
            
            # UI Styling
            html_content = f"""
            <div style="text-align: center; margin: 20px; border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: #f9f9f9; max-width: 600px;">
                <h1 style="color: #2E7D32; font-size: 32px; margin-bottom: 5px;">{surah_data['name']}</h1>
                <h3 style="margin-top: 0; color: #333;">{surah_data['englishName']} <i>({surah_data['englishNameTranslation']})</i></h3>
            </div>
            """
            display(HTML(html_content))
            
            # Construct the audio URL
            audio_url = f"https://cdn.islamic.network/quran/audio-surah/128/{selected_reciter_id}/{surah_num}.mp3"
            
            # Display Audio Player
            display(Audio(url=audio_url, autoplay=False))
            display(HTML("<p style='color:gray; font-size:12px;'>Audio provided via Al Quran Cloud</p>"))

    # 5. Bind functions
    reciter_dropdown.observe(update_player, names='value')
    surah_dropdown.observe(update_player, names='value')

    # 6. Display UI
    display(HTML("<h2>📖 Jupyter Quran Player</h2>"))
    ui = widgets.VBox([reciter_dropdown, surah_dropdown]) # Stacked vertically for better mobile viewing
    display(ui)
    display(out)
    
    update_player()
