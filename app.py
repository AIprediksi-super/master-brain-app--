import streamlit as st
import numpy as np
from collections import Counter
import random

# --- CONFIG UI & THEMES ---
st.set_page_config(page_title="Master Brain v15: 8-Theory Hybrid", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []

# PENGATUR WARNA TEMA (DI LAYAR UTAMA)
themes = {
    "Gelap (Neon Green)": {"bg": "#0E1117", "txt": "#00FF00", "akurat": "#006400", "mid": "#8B8000", "kontra": "#8B0000", "btn": "#00FF00", "btn_txt": "black"},
    "Ungu Neon": {"bg": "#2D004D", "txt": "#BF00FF", "akurat": "#7B1FA2", "mid": "#9C27B0", "kontra": "#4A148C", "btn": "#BF00FF", "btn_txt": "black"},
    "Biru Langit": {"bg": "#E0F7FA", "txt": "#01579B", "akurat": "#0288D1", "mid": "#FBC02D", "kontra": "#D32F2F", "btn": "#0288D1", "btn_txt": "white"},
    "Merah Muda (Pink)": {"bg": "#FCE4EC", "txt": "#880E4F", "akurat": "#C2185B", "mid": "#FBC02D", "kontra": "#AD1457", "btn": "#D81B60", "btn_txt": "white"}
}

st.title("🧠 MASTER BRAIN V15: 4-DIGIT OPTIMIZER")

# Tampilan Pengatur Warna di Layar Utama
col_tema, col_empty = st.columns([1, 2])
with col_tema:
    pilihan_tema = st.selectbox("🎨 Pilih Tema Warna:", list(themes.keys()))
t = themes[pilihan_tema]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; transition: all 0.5s ease; }}
    .predict-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; background-color: rgba(0,0,0,0.5); }}
    .predict-table th {{ border: 2px solid {t['txt']}; padding: 10px; color: {t['txt']}; text-align: center; }}
    .predict-table td {{ border: 1px solid rgba(255,255,255,0.2); padding: 12px; text-align: center; font-size: 26px; font-weight: bold; color: white; text-shadow: 2px 2px #000; }}
    .bg-seimbang {{ background-color: {t['mid']} !important; }}
    .bg-akurat {{ background-color: {t['akurat']} !important; }}
    .bg-kontra {{ background-color: {t['kontra']} !important; }}
    .stButton>button {{ background-color: {t['btn']} !important; color: {t['btn_txt']} !important; font-weight: bold; border-radius: 8px; }}
    textarea {{ color: black !important; font-weight: bold !important; font-size: 18px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- INPUT UTAMA ---
st.markdown("### 📥 MASUKKAN HISTORI DATA")
manual_input = st.text_area("Tempel Data (0000-9999):", height=150, placeholder="Contoh: 1234 5678 0912 ...")

c1, c2 = st.columns([1, 5])
with c1:
    btn_analisa = st.button("🚀 ANALISA")
with c2:
    if st.button("🗑️ RESET DATA"):
        st.session_state.history = []
        st.rerun()

if btn_analisa and manual_input:
    st.session_state.history = manual_input.replace(',', ' ').split()

# --- LOGIKA ANALISA ---
def get_column_stats(data):
    cols = [[] for _ in range(4)]
    for item in data:
        chars = [c for c in item if c.isdigit()]
        for i in range(min(4, len(chars))):
            cols[i].append(chars[i])
    return cols

if st.session_state.history:
    cols_data = get_column_stats(st.session_state.history)
    
    def get_predictions(mode):
        results = []
        for i in range(4):
            data = cols_data[i]
            all_digits = "0123456789"
            if not data:
                results.append([str(random.randint(0,9)) for _ in range(8)])
                continue
            
            freq = Counter(data)
            sorted_by_freq = sorted(all_digits, key=lambda x: freq[x], reverse=True)
            
            if mode == "seimbang":
                results.append(sorted_by_freq[1:8])
            elif mode == "akurat":
                results.append(sorted_by_freq[:7])
            else: # kontra
                results.append(sorted_by_freq[::-1][:8])
        return results

    # --- OUTPUT TABEL ---
    st.markdown("---")
    
    # Tabel 1
    st.subheader("🟢 TABEL 1: 7 PREDIKSI PALING SEIMBANG")
    data_s = get_predictions("seimbang")
    html_s = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(7):
        html_s += f"<tr><td>#{r+1}</td>"
        for c in range(4): html_s += f"<td class='bg-seimbang'>{data_s[c][r]}</td>"
        html_s += "</tr>"
    st.markdown(html_s + "</table>", unsafe_allow_html=True)

    # Tabel 2
    st.subheader("🔵 TABEL 2: 7 PREDIKSI AKURAT (HOT)")
    data_a = get_predictions("akurat")
    html_a = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(7):
        html_a += f"<tr><td>#{r+1}</td>"
        for c in range(4): html_a += f"<td class='bg-akurat'>{data_a[c][r]}</td>"
        html_a += "</tr>"
    st.markdown(html_a + "</table>", unsafe_allow_html=True)

    # Tabel 3
    st.subheader("🔴 TABEL 3: 8 KONTRA PREDIKSI (COLD)")
    data_k = get_predictions("kontra")
    html_k = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(8):
        html_k += f"<tr><td>#{r+1}</td>"
        for c in range(4): html_k += f"<td class='bg-kontra'>{data_k[c][r]}</td>"
        html_k += "</tr>"
    st.markdown(html_k + "</table>", unsafe_allow_html=True)

else:
    st.info("💡 Masukkan histori angka untuk melihat hasil optimasi 8-teori.")
