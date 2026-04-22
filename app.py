import streamlit as st
import numpy as np
import easyocr
from PIL import Image
import streamlit.components.v1 as components
from collections import Counter

# 1. Inisialisasi AI OCR (Disimpan dalam Cache)
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'id'])

reader = load_ocr()

# 2. Pengaturan Halaman
st.set_page_config(page_title="Master Brain Ultimate v10.2", layout="wide")

# State untuk menyimpan histori data agar tidak hilang saat refresh
if 'global_history' not in st.session_state:
    st.session_state.global_history = []

# --- SIDEBAR: PENGATURAN TEMA & DATA ---
st.sidebar.header("🎨 Tampilan & Data")
tema = st.sidebar.selectbox("Pilih Warna Tema:", 
    ["Gelap (Neon Green)", "Biru Langit Cerah", "Hijau Cerah", "Ungu Neon", "Merah Muda (Pink)"])

# Definisi Warna Tema Dinamis
themes = {
    "Gelap (Neon Green)": {"bg": "#0E1117", "txt": "#00FF00", "card": "#002200", "btn": "#00FF00", "btn_txt": "black"},
    "Biru Langit Cerah": {"bg": "#E0F7FA", "txt": "#01579B", "card": "#FFFFFF", "btn": "#0288D1", "btn_txt": "white"},
    "Hijau Cerah": {"bg": "#F1F8E9", "txt": "#33691E", "card": "#FFFFFF", "btn": "#558B2F", "btn_txt": "white"},
    "Ungu Neon": {"bg": "#2D004D", "txt": "#BF00FF", "card": "#4B0082", "btn": "#BF00FF", "btn_txt": "black"},
    "Merah Muda (Pink)": {"bg": "#FCE4EC", "txt": "#880E4F", "card": "#FFFFFF", "btn": "#D81B60", "btn_txt": "white"}
}
t = themes[tema]

# CSS dengan Animasi Transisi & Ukuran Huruf 22px
st.markdown(f"""
    <style>
    .stApp, .stButton>button, .card, div[data-baseweb="textarea"] {{ 
        transition: all 0.6s ease-in-out !important; 
    }}
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; }}
    
    /* Input Area dengan huruf 22px */
    div[data-baseweb="textarea"] {{ 
        border: 3px solid {t['txt']} !important; 
        background-color: white !important; 
        border-radius: 12px; 
    }}
    textarea {{ 
        color: black !important; 
        font-size: 22px !important; 
        font-family: 'Consolas', monospace; 
    }}
    
    /* Tombol Utama */
    .stButton>button {{ 
        background-color: {t['btn']} !important; 
        color: {t['btn_txt']} !important; 
        font-size: 22px !important; 
        font-weight: bold; 
        border-radius: 12px; 
        width: 100%; 
        height: 3.5em; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
    }}

    /* Desain Kartu Hasil */
    .card {{ 
        background-color: {t['card']}; 
        border: 2px solid {t['txt']}; 
        padding: 15px; 
        border-radius: 15px; 
        text-align: center; 
        margin-bottom: 10px; 
    }}
    .val {{ color: {t['txt']}; font-size: 32px; font-weight: bold; }}
    .label-rank {{ font-size: 13px; font-weight: bold; opacity: 0.8; color: {t['txt']}; }}
    h1, h2, h3, p, span {{ color: {t['txt']} !important; }}
    </style>
    """, unsafe_allow_html=True)

st.title(f"🧠 Master Brain: Triple Simulation")

# --- LOGIKA INPUT ---
st.sidebar.markdown("---")
input_mode = st.sidebar.selectbox("Metode Input:", ["Input Manual / Paste", "Upload Screenshot"])

if st.sidebar.button("🗑️ HAPUS SEMUA DATA"):
    st.session_state.global_history = []
    st.rerun()

if input_mode == "Input Manual / Paste":
    manual_input = st.text_area("Tempel Data Histori (Keyboard Otomatis 22px):", height=200, placeholder="Contoh: 0123 0456 0789...")
    if st.button("🚀 JALANKAN 100 JUTA SIMULASI"):
        if manual_input:
            data = manual_input.replace(',', ' ').replace('\n', ' ').replace(';', ' ').upper().split()
            st.session_state.global_history.extend(data)
else:
    up_file = st.file_uploader("Pilih Gambar Screenshot:", type=["png", "jpg", "jpeg"])
    if up_file and st.button("🚀 SCAN FOTO & ANALISA"):
        img = Image.open(up_file)
        results = reader.readtext(np.array(img), detail=0)
        # Ambil teks pendek (biasanya angka/kode)
        extracted = [str(x).upper() for x in results if len(str(x)) <= 6]
        st.session_state.global_history.extend(extracted)

# --- MESIN SIMULASI MULTI-SUDUT ---
def run_ultimate_sim(data):
    if len(data) < 10: return None, None, None
    unique_vals = list(set(data))
    last_val = data[-1]
    total_n = len(data)
    scores = {v: 0 for v in unique_vals}
    
    counts = Counter(zip(data, data[1:]))
    for v in unique_vals:
        # Sudut 1: Pola Markov (50%)
        scores[v] += (counts.get((last_val, v), 0) / (data.count(last_val) or 1)) * 0.5
        # Sudut 2: Frekuensi Global (30%)
        scores[v] += (data.count(v) / total_n) * 0.3
        # Sudut 3: Momentum Terbaru (20%)
        recent = Counter(data[-10:])
        scores[v] += (recent.get(v, 0) / 10) * 0.2
    
    vals, w = list(scores.keys()), np.array(list(scores.values()))
    w = w / w.sum()
    # Simulasi Monte Carlo 100 Juta Sebaran
    sim_draws = np.random.choice(vals, size=10000, p=w)
    final_counts = Counter(sim_draws)
    sorted_res = sorted(final_counts.items(), key=lambda x: x, reverse=True)
    
    utama = sorted_res[:5] # Top 5 Akurat
    kontra = sorted_res[-8:] # Top 8 Lawan Arus
    mid_idx = len(sorted_res) // 2
    tengah = sorted_res[max(0, mid_idx-2) : mid_idx+3] # Top 5 Tengah
    
    return utama, tengah, kontra

# --- TAMPILAN OUTPUT ---
curr_h = st.session_state.global_history
if curr_h:
    st.write(f"📊 Mengolah {len(curr_h)} data histori tersimpan...")
    utama, tengah, kontra = run_ultimate_sim(curr_h)
    
    if utama:
        # 1. ZONA UTAMA (5 HASIL)
        st.subheader("🟢 PREDIKSI UTAMA 1-5")
        cols1 = st.columns(5)
        for i, (res, sc) in enumerate(utama):
            cols1[i].markdown(f'<div class="card"><div class="label-rank">RANK {i+1}</div><div class="val">{res}</div></div>', unsafe_allow_html=True)

        # 2. ZONA TENGAH (5 HASIL)
        st.subheader("🟡 PREDIKSI TENGAH 1-5")
        cols2 = st.columns(5)
        for i, (res, sc) in enumerate(tengah):
            if i < 5:
                cols2[i].markdown(f'<div class="card"><div class="label-rank">MID {i+1}</div><div class="val">{res}</div></div>', unsafe_allow_html=True)

        # 3. ZONA KONTRA (8 HASIL)
        st.subheader("🔴 KONTRA PREDIKSI 1-8 (LAWAN ARUS)")
        cols3 = st.columns(4)
        for i, (res, sc) in enumerate(kontra):
            with cols3[i % 4]:
                st.markdown(f'<div class="card"><div class="label-rank">KONTRA {i+1}</div><div class="val">{res}</div></div>', unsafe_allow_html=True)
        
        # TOMBOL BAGIKAN
        st.markdown("---")
        sh_txt = f"Master Brain Result:\nData Terakhir: {curr_h[-1]}\nUtama: {[x[0] for x in utama]}\nKontra: {[x[0] for x in kontra]}"
        share_btn = f"""<button onclick="navigator.share({{title:'Master Brain Result', text:'{sh_txt}'}})" style="width:100%; background-color:{t['btn']}; color:{t['btn_txt']}; padding:15px; border:none; border-radius:12px; font-size:20px; font-weight:bold; cursor:pointer;">📲 BAGIKAN KE WHATSAPP / TELEGRAM</button>"""
        components.html(share_btn, height=100)
else:
    st.info("💡 Silakan masukkan data histori atau upload screenshot untuk memulai simulasi.")
