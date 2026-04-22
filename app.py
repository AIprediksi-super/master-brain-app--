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
st.set_page_config(page_title="Master Brain v11.2: Triple-Zone Per Digit", layout="wide")

if 'global_history' not in st.session_state:
    st.session_state.global_history = []

# --- SIDEBAR TEMA ---
st.sidebar.header("🎨 Tampilan & Data")
tema = st.sidebar.selectbox("Pilih Warna Tema:", 
    ["Gelap (Neon Green)", "Biru Langit Cerah", "Hijau Cerah", "Ungu Neon", "Merah Muda (Pink)"])

themes = {
    "Gelap (Neon Green)": {"bg": "#0E1117", "txt": "#00FF00", "card_akurat": "#002200", "card_mid": "#222200", "card_kontra": "#220000", "btn": "#00FF00", "btn_txt": "black"},
    "Biru Langit Cerah": {"bg": "#E0F7FA", "txt": "#01579B", "card_akurat": "#E1F5FE", "card_mid": "#FFF9C4", "card_kontra": "#FFEBEE", "btn": "#0288D1", "btn_txt": "white"},
    "Hijau Cerah": {"bg": "#F1F8E9", "txt": "#33691E", "card_akurat": "#DCEDC8", "card_mid": "#FFF9C4", "card_kontra": "#FFCCBC", "btn": "#558B2F", "btn_txt": "white"},
    "Ungu Neon": {"bg": "#2D004D", "txt": "#BF00FF", "card_akurat": "#4B0082", "card_mid": "#5D4037", "card_kontra": "#311B92", "btn": "#BF00FF", "btn_txt": "black"},
    "Merah Muda (Pink)": {"bg": "#FCE4EC", "txt": "#880E4F", "card_akurat": "#F8BBD0", "card_mid": "#FFF9C4", "card_kontra": "#FFCCBC", "btn": "#D81B60", "btn_txt": "white"}
}
t = themes[tema]

# CSS Dinamis dengan Animasi
st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; transition: all 0.6s ease-in-out; }}
    div[data-baseweb="textarea"] {{ border: 3px solid {t['txt']} !important; background-color: white !important; border-radius: 12px; }}
    textarea {{ color: black !important; font-size: 22px !important; font-family: 'Consolas', monospace; }}
    .stButton>button {{ background-color: {t['btn']} !important; color: {t['btn_txt']} !important; font-size: 20px !important; font-weight: bold; border-radius: 12px; width: 100%; height: 3.5em; }}
    
    .box {{ padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid {t['txt']}; }}
    .akurat {{ background-color: {t['card_akurat']}; }}
    .mid {{ background-color: {t['card_mid']}; }}
    .kontra {{ background-color: {t['card_kontra']}; }}
    
    .val-digit {{ color: {t['txt']}; font-size: 26px; font-weight: bold; }}
    .col-header {{ font-size: 20px; font-weight: bold; text-align: center; margin-bottom: 15px; text-decoration: underline; }}
    .zone-title {{ font-size: 14px; font-weight: bold; margin-top: 10px; margin-bottom: 5px; opacity: 0.8; }}
    h1, h2, h3, p, span {{ color: {t['txt']} !important; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Master Brain v11.2: Triple Zone Per Digit")

# --- PANEL INPUT ---
st.sidebar.markdown("---")
input_mode = st.sidebar.selectbox("Metode Input:", ["Input Manual / Paste", "Upload Screenshot"])
if st.sidebar.button("🗑️ HAPUS DATA"):
    st.session_state.global_history = []
    st.rerun()

if input_mode == "Input Manual / Paste":
    manual_input = st.text_area("Tempel Data Histori (22px):", height=200, placeholder="Contoh: 2469 1357 0912...")
    if st.button("🚀 ANALISA TRIPLE ZONE"):
        if manual_input:
            data = manual_input.replace(',', ' ').replace('\n', ' ').upper().split()
            st.session_state.global_history.extend(data)
else:
    up_file = st.file_uploader("Upload Foto:", type=["png", "jpg", "jpeg"])
    if up_file and st.button("🚀 SCAN & ANALISA"):
        img = Image.open(up_file)
        results = reader.readtext(np.array(img), detail=0)
        data = [str(x).upper() for x in results if any(c.isdigit() for c in x)]
        st.session_state.global_history.extend(data)

# --- MESIN ANALISA TRIPLE ZONE PER DIGIT ---
def analyze_triple_zone(data):
    col_data = [[], [], [], []]
    for item in data:
        digits = [d for d in item if d.isdigit()]
        for i in range(min(4, len(digits))):
            col_data[i].append(digits[i])
    
    final_results = {}
    for i in range(4):
        curr = col_data[i]
        if not curr: continue
        
        last_d = curr[-1]
        unique_d = [str(d) for d in range(10)]
        
        # Hitung Skor: Pola Markov + Frekuensi
        trans = Counter(zip(curr, curr[1:]))
        freq = Counter(curr)
        
        scores = {}
        for d in unique_d:
            s_pola = (trans.get((last_d, d), 0) / (curr.count(last_d) or 1)) * 0.6
            s_freq = (freq.get(d, 0) / len(curr)) * 0.4
            scores[d] = s_pola + s_freq
            
        sorted_all = sorted(scores.items(), key=lambda x: x, reverse=True)
        
        # Bagi menjadi 3 Zona (Akurat, Tengah, Kontra)
        akurat = sorted_all[:5]
        kontra = sorted_all[-5:]
        mid_idx = len(sorted_all) // 2
        tengah = sorted_all[max(0, mid_idx-2) : mid_idx+3]
        
        final_results[f"DIGIT {i+1}"] = {"akurat": akurat, "tengah": tengah, "kontra": kontra}
        
    return final_results

# --- TAMPILAN OUTPUT ---
history = st.session_state.global_history
if history:
    res_zones = analyze_triple_zone(history)
    
    if res_zones:
        st.write(f"📊 Analisa Global 100 Juta pada {len(history)} data (Terakhir: {history[-1]})")
        
        # Layout 4 Kolom (Digit 1 - Digit 4)
        cols = st.columns(4)
        for i in range(4):
            key = f"DIGIT {i+1}"
            if key in res_zones:
                with cols[i]:
                    st.markdown(f'<div class="col-header">{key}</div>', unsafe_allow_html=True)
                    
                    # Sub-Zona Akurat
                    st.markdown('<div class="zone-title">🟢 AKURAT (TOP 5)</div>', unsafe_allow_html=True)
                    for d, sc in res_zones[key]["akurat"]:
                        st.markdown(f'<div class="box akurat"><div class="val-digit">{d}</div></div>', unsafe_allow_html=True)
                        
                    # Sub-Zona Tengah
                    st.markdown('<div class="zone-title">🟡 TENGAH (TOP 5)</div>', unsafe_allow_html=True)
                    for d, sc in res_zones[key]["tengah"]:
                        st.markdown(f'<div class="box mid"><div class="val-digit">{d}</div></div>', unsafe_allow_html=True)
                        
                    # Sub-Zona Kontra
                    st.markdown('<div class="zone-title">🔴 KONTRA (TOP 5)</div>', unsafe_allow_html=True)
                    for d, sc in res_zones[key]["kontra"]:
                        st.markdown(f'<div class="box kontra"><div class="val-digit">{d}</div></div>', unsafe_allow_html=True)

        # Tombol Share
        st.markdown("---")
        sh_txt = f"Master Brain v11.2 Result Per Digit:\nLast: {history[-1]}"
        share_btn = f"""<button onclick="navigator.share({{title:'Result MB', text:'{sh_txt}'}})" style="width:100%; background-color:{t['btn']}; color:{t['btn_txt']}; padding:15px; border:none; border-radius:12px; font-size:20px; font-weight:bold; cursor:pointer;">📲 BAGIKAN HASIL DIGIT</button>"""
        components.html(share_btn, height=100)
else:
    st.info("💡 Masukkan data histori untuk memunculkan Triple Zone per kolom.")
