import streamlit as st
from collections import Counter
import random

# --- CONFIG UI ---
st.set_page_config(page_title="Master Brain v15: Ultra Hybrid", layout="wide")

# Inisialisasi state agar sistem stabil
if 'history' not in st.session_state:
    st.session_state.history = []
if 'temp_input' not in st.session_state:
    st.session_state.temp_input = ""

# --- DAFTAR TEMA APLIKASI ---
app_themes = {
    "Gelap (Neon Green)": {"bg": "#0E1117", "txt": "#00FF00", "btn": "#00FF00", "btn_txt": "black"},
    "Pelangi 🌈": {"bg": "linear-gradient(to right, #ff9966, #ff5e62, #8e44ad, #3498db)", "txt": "#FFFFFF", "btn": "#FFFFFF", "btn_txt": "black"},
    "Biru Laut": {"bg": "#0077be", "txt": "#E0F7FA", "btn": "#00E5FF", "btn_txt": "black"},
    "Ungu Neon": {"bg": "#2D004D", "txt": "#BF00FF", "btn": "#BF00FF", "btn_txt": "black"},
}

# --- DAFTAR WARNA TABEL ---
table_themes = {
    "Biru Laut": "#0077be",
    "Hijau Daun": "#228B22",
    "Merah Muda Neon": "#FF1493",
    "Hitam Klasik": "#000000"
}

st.title("🧠 MASTER BRAIN V15: ULTRA CUSTOM")

# --- KONTROL WARNA DI LAYAR UTAMA ---
c_tema, c_tabel = st.columns(2)
with c_tema:
    pilihan_app = st.selectbox("🎨 Pilih Tema Aplikasi:", list(app_themes.keys()))
with c_tabel:
    pilihan_tab = st.selectbox("📊 Pilih Warna Tabel Prediksi:", list(table_themes.keys()))

t_app = app_themes[pilihan_app]
t_tab = table_themes[pilihan_tab]

st.markdown(f"""
    <style>
    .stApp {{ background: {t_app['bg']}; color: {t_app['txt']}; transition: all 0.5s ease; }}
    
    /* INPUT TEXT AREA - ANGKA PUTIH TERANG */
    div[data-baseweb="textarea"] {{ 
        border: 2px solid {t_app['txt']} !important; 
        border-radius: 12px !important;
        background-color: #1A1A1A !important;
    }}
    textarea {{ 
        color: #FFFFFF !important; 
        font-weight: bold !important; 
        font-size: 20px !important; 
    }}
    
    .predict-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; background-color: rgba(0,0,0,0.6); }}
    .predict-table th {{ border: 2px solid {t_app['txt']}; padding: 10px; color: {t_app['txt']}; text-align: center; }}
    
    /* TABEL PREDIKSI - PUTIH LES HITAM */
    .predict-table td {{ 
        border: 1px solid rgba(255,255,255,0.2); 
        padding: 12px; 
        text-align: center; 
        font-size: 28px; 
        font-weight: 900; 
        color: white !important;
        -webkit-text-stroke: 1.5px black;
        text-shadow: 2px 2px 4px #000;
    }}
    
    .bg-custom {{ background-color: {t_tab} !important; }}
    
    .stButton>button {{ 
        background-color: {t_app['btn']} !important; 
        color: {t_app['btn_txt']} !important; 
        font-weight: bold; 
        border-radius: 12px; 
        height: 3.5em; 
        width: 100%; 
    }}
    h3 {{ color: {t_app['txt']} !important; text-shadow: 1px 1px 2px black; }}
    </style>
    """, unsafe_allow_html=True)

# --- INPUT UTAMA ---
st.markdown("### 📥 INPUT HISTORI")
manual_input = st.text_area("Tempel Data 4-Digit:", value=st.session_state.temp_input, height=150, placeholder="Contoh: 1234 5678 0912")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input:
            st.session_state.history = manual_input.replace(',', ' ').split()
            st.session_state.temp_input = manual_input 

with c2:
    # TOMBOL HAPUS DATA PASTE (SOLUSI ANTI-ERROR)
    if st.button("🗑️ HAPUS TEKS PASTE"):
        st.session_state.temp_input = "" 
        st.rerun() 

with c3:
    if st.button("🔴 RESET SEMUA DATA"):
        st.session_state.history = []
        st.session_state.temp_input = ""
        st.rerun()

# --- ENGINE ANALISA (8-TEORI) ---
def get_predictions(data, mode):
    cols = [[] for _ in range(4)]
    for item in data:
        chars = [c for c in item if c.isdigit()]
        for i in range(min(4, len(chars))): cols[i].append(chars[i])
    
    results = []
    for i in range(4):
        d = cols[i]
        all_digits = "0123456789"
        freq = Counter(d) if d else {}
        sorted_by_freq = sorted(all_digits, key=lambda x: freq.get(x, 0), reverse=True)
        
        if mode == "seimbang": results.append(sorted_by_freq[1:8])
        elif mode == "akurat": results.append(sorted_by_freq[:7])
        else: results.append(sorted_by_freq[::-1][:8])
    return results

# --- OUTPUT TABEL ---
if st.session_state.history:
    st.markdown("---")
    # Tabel 1
    st.subheader("🟢 TABEL 1: 7 PREDIKSI SEIMBANG")
    data_s = get_predictions(st.session_state.history, "seimbang")
    html_s = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(7):
        html_s += f"<tr><td>#{r+1}</td>"
        for c in range(4): html_s += f"<td class='bg-custom'>{data_s[c][r]}</td>"
        html_s += "</tr>"
    st.markdown(html_s + "</table>", unsafe_allow_html=True)

    # Tabel 2
    st.subheader("🔵 TABEL 2: 7 PREDIKSI AKURAT (HOT)")
    data_a = get_predictions(st.session_state.history, "akurat")
    html_a = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(7):
        html_a += f"<tr><td>#{r+1}</td>"
        for c in range(4): html_a += f"<td class='bg-custom'>{data_a[c][r]}</td>"
        html_a += "</tr>"
    st.markdown(html_a + "</table>", unsafe_allow_html=True)

    # Tabel 3
    st.subheader("🔴 TABEL 3: 8 KONTRA PREDIKSI (COLD)")
    data_k = get_predictions(st.session_state.history, "kontra")
    html_k = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(8):
        html_k += f"<tr><td>#{r+1}</td>"
        for c in range(4): html_k += f"<td class='bg-custom'>{data_k[c][r]}</td>"
        html_k += "</tr>"
    st.markdown(html_k + "</table>", unsafe_allow_html=True)
else:
    st.info("💡 Sistem Siap. Masukkan histori angka di atas untuk memicu kalkulasi.")
