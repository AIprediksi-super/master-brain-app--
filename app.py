import streamlit as st
import numpy as np
import easyocr
from PIL import Image
import streamlit.components.v1 as components
from collections import Counter

# 1. Inisialisasi AI OCR
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'id'])

reader = load_ocr()

# 2. Pengaturan Halaman & Tema
st.set_page_config(page_title="Master Brain v12.2: Ultra Contrast", layout="wide")

if 'global_history' not in st.session_state:
    st.session_state.global_history = []

# --- SIDEBAR TEMA ---
st.sidebar.header("🎨 Tampilan & Data")
tema = st.sidebar.selectbox("Pilih Warna Tema:", 
    ["Gelap (Neon Green)", "Biru Langit Cerah", "Hijau Cerah", "Ungu Neon", "Merah Muda (Pink)"])

themes = {
    "Gelap (Neon Green)": {"bg": "#0E1117", "txt": "#00FF00", "akurat": "#006400", "mid": "#8B8000", "kontra": "#8B0000", "btn": "#00FF00", "btn_txt": "black"},
    "Biru Langit Cerah": {"bg": "#E0F7FA", "txt": "#01579B", "akurat": "#0288D1", "mid": "#FBC02D", "kontra": "#D32F2F", "btn": "#0288D1", "btn_txt": "white"},
    "Hijau Cerah": {"bg": "#F1F8E9", "txt": "#33691E", "akurat": "#388E3C", "mid": "#FBC02D", "kontra": "#D32F2F", "btn": "#558B2F", "btn_txt": "white"},
    "Ungu Neon": {"bg": "#2D004D", "txt": "#BF00FF", "akurat": "#7B1FA2", "mid": "#9C27B0", "kontra": "#4A148C", "btn": "#BF00FF", "btn_txt": "black"},
    "Merah Muda (Pink)": {"bg": "#FCE4EC", "txt": "#880E4F", "akurat": "#C2185B", "mid": "#FBC02D", "kontra": "#AD1457", "btn": "#D81B60", "btn_txt": "white"}
}
t = themes[tema]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; transition: all 0.6s ease-in-out; }}
    div[data-baseweb="textarea"] {{ border: 3px solid {t['txt']} !important; background-color: white !important; border-radius: 12px; }}
    textarea {{ color: black !important; font-size: 22px !important; font-family: 'Consolas', monospace; }}
    .stButton>button {{ background-color: {t['btn']} !important; color: {t['btn_txt']} !important; font-size: 20px !important; font-weight: bold; border-radius: 12px; width: 100%; height: 3.5em; }}
    
    /* Style Tabel Prediksi */
    .predict-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 30px;
        color: white;
    }}
    .predict-table th {{
        border: 2px solid {t['txt']};
        padding: 10px;
        background-color: rgba(0,0,0,0.3);
        font-size: 16px;
        color: {t['txt']};
    }}
    .predict-table td {{
        border: 1px solid rgba(255,255,255,0.3);
        padding: 10px;
        text-align: center;
        font-size: 28px;
        font-weight: 900;
        /* EFEK LES HITAM PADA HURUF/ANGKA PUTIH */
        color: white;
        text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
    }}
    .bg-akurat {{ background-color: {t['akurat']} !important; }}
    .bg-mid {{ background-color: {t['mid']} !important; }}
    .bg-kontra {{ background-color: {t['kontra']} !important; }}
    
    h1, h2, h3 {{ color: {t['txt']} !important; text-transform: uppercase; letter-spacing: 2px; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V12.2: LES HITAM EDITION")

# --- PANEL INPUT ---
st.sidebar.markdown("---")
input_mode = st.sidebar.selectbox("Metode Input:", ["Input Manual / Paste", "Upload Screenshot"])
if st.sidebar.button("🗑️ RESET DATA"):
    st.session_state.global_history = []
    st.rerun()

if input_mode == "Input Manual / Paste":
    manual_input = st.text_area("Paste Data (0-9, A, B):", height=200)
    if st.button("🚀 ANALISA GLOBAL 100M"):
        if manual_input:
            data = manual_input.replace(',', ' ').replace('\n', ' ').upper().split()
            st.session_state.global_history.extend(data)
else:
    up_file = st.file_uploader("Upload Gambar:", type=["png", "jpg", "jpeg"])
    if up_file and st.button("🚀 SCAN FOTO"):
        img = Image.open(up_file)
        results = reader.readtext(np.array(img), detail=0)
        data = [str(x).upper() for x in results if len(x) >= 2]
        st.session_state.global_history.extend(data)

# --- MESIN ANALISA ---
def analyze_v12_2(data):
    col_data = [[], [], [], []]
    for item in data:
        chars = [c for c in item if c.isdigit() or c in ['A', 'B']]
        for i in range(min(4, len(chars))):
            col_data[i].append(chars[i])
    
    final_results = {}
    valid_chars = [str(d) for d in range(10)] + ['A', 'B']
    
    for i in range(4):
        curr = col_data[i]
        if not curr: continue
        last_c = curr[-1]
        trans = Counter(zip(curr, curr[1:]))
        freq = Counter(curr)
        
        scores = {}
        for c in valid_chars:
            s_pola = (trans.get((last_c, c), 0) / (curr.count(last_c) or 1)) * 0.65
            s_freq = (freq.get(c, 0) / len(curr)) * 0.35
            scores[c] = s_pola + s_freq
            
        sorted_all = [x[0] for x in sorted(scores.items(), key=lambda x: x, reverse=True)]
        
        final_results[f"KOLOM {i+1}"] = {
            "akurat": sorted_all[:8],      # Akurat 1-8
            "tengah": sorted_all[2:10],     # Tengah 1-8 (Offset sedikit agar beda)
            "kontra": sorted_all[-10:][::-1] # Kontra 1-10 (Dibalik agar terlemah di atas)
        }
    return final_results

# --- OUTPUT TABEL ---
history = st.session_state.global_history
if history:
    res = analyze_v12_2(history)
    if res:
        def draw_table(title, zone_key, css_class):
            html = f"<h3>{title}</h3><table class='predict-table'><tr><th>POS</th>"
            for k in range(1, 5): html += f"<th>KOL {k}</th>"
            html += "</tr>"
            
            num_rows = 10 if zone_key == "kontra" else 8
            for row in range(num_rows):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{row+1}</td>"
                for col in range(1, 5):
                    k_name = f"KOLOM {col}"
                    val = res[k_name][zone_key][row] if k_name in res and row < len(res[k_name][zone_key]) else "-"
                    html += f"<td class='{css_class}'>{val}</td>"
                html += "</tr>"
            html += "</table>"
            return html

        st.markdown(draw_table("🟢 PREDIKSI AKURAT (1-8)", "akurat", "bg-akurat"), unsafe_allow_html=True)
        st.markdown(draw_table("🟡 PREDIKSI TENGAH (1-8)", "tengah", "bg-mid"), unsafe_allow_html=True)
        st.markdown(draw_table("🔴 KONTRA PREDIKSI (1-10)", "kontra", "bg-kontra"), unsafe_allow_html=True)

        # Share
        st.markdown("---")
        share_btn = f"""<button onclick="navigator.share({{title:'Master Brain V12.2', text:'Hasil Prediksi Multi-Zone Aktif'}})" style="width:100%; background-color:{t['btn']}; color:{t['btn_txt']}; padding:15px; border:none; border-radius:12px; font-size:20px; font-weight:bold; cursor:pointer;">📲 BAGIKAN HASIL TABEL</button>"""
        components.html(share_btn, height=100)
else:
    st.info("💡 Masukkan data untuk memproses tabel 1-8 dan 1-10.")
