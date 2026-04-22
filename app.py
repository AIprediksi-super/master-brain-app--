import streamlit as st
import numpy as np
import easyocr
from PIL import Image
from collections import Counter
import random

# --- ENGINE 8 TEORI (7 STANDAR + 1 KONTRA) ---
class UltimateOptimizer:
    def __init__(self):
        self.mid = 4 # 0-4 Kecil, 5-9 Besar
        self.sum_min, self.sum_max = 10, 26

    def get_column_stats(self, data):
        # Memecah data histori menjadi 4 kolom
        cols = [[] for _ in range(4)]
        for item in data:
            chars = [c for c in item if c.isdigit()]
            for i in range(min(4, len(chars))):
                cols[i].append(int(chars[i]))
        return cols

# --- SETTING UI ---
st.set_page_config(page_title="Master Brain v15: 8-Theory Hybrid", layout="wide")
opt = UltimateOptimizer()

t = {"bg": "#0E1117", "txt": "#00FF00", "akurat": "#006400", "mid": "#8B8000", "kontra": "#8B0000", "btn": "#00FF00"}

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; }}
    .predict-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; background-color: rgba(0,0,0,0.5); }}
    .predict-table th {{ border: 2px solid {t['txt']}; padding: 10px; color: {t['txt']}; text-align: center; }}
    .predict-table td {{ border: 1px solid rgba(255,255,255,0.2); padding: 12px; text-align: center; font-size: 24px; font-weight: bold; color: white; text-shadow: 2px 2px #000; }}
    .bg-seimbang {{ background-color: {t['mid']} !important; }}
    .bg-akurat {{ background-color: {t['akurat']} !important; }}
    .bg-kontra {{ background-color: {t['kontra']} !important; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V15: 8-THEORY OPTIMIZER")

# --- INPUT DATA ---
manual_input = st.sidebar.text_area("Tempel Histori (0000-9999):", height=200)
if st.sidebar.button("🚀 MULAI ANALISA"):
    if manual_input:
        st.session_state.history = manual_input.replace(',', ' ').split()

# --- LOGIKA ANALISA ---
if 'history' in st.session_state:
    cols_data = opt.get_column_stats(st.session_state.history)
    
    def generate_table_data(mode):
        results = []
        for i in range(4):
            data = cols_data[i]
            if not data: 
                results.append(["-"] * 8)
                continue
            
            freq = Counter(data)
            # Ambil angka paling sering (Hot) dan jarang (Cold)
            sorted_chars = [str(x[0]) for x in freq.most_common()]
            while len(sorted_chars) < 10: sorted_chars.append(str(random.randint(0,9)))
            
            if mode == "seimbang":
                # Ambil tengah-tengah frekuensi (Bell Curve)
                results.append(sorted_chars[2:9])
            elif mode == "akurat":
                # Ambil peringkat teratas (Hot Numbers)
                results.append(sorted_chars[:7])
            else: # kontra
                # Ambil peringkat terbawah (Cold Numbers)
                results.append(sorted_chars[::-1][:8])
        return results

    # --- TABEL 1: 7 PREDIKSI PALING SEIMBANG ---
    st.subheader("🟢 TABEL 1: 7 PREDIKSI PALING SEIMBANG (BELL CURVE)")
    data_s = generate_table_data("seimbang")
    html_s = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(7):
        html_s += f"<tr><td style='font-size:14px;'>#{r+1}</td>"
        for c in range(4):
            html_s += f"<td class='bg-seimbang'>{data_s[c][r]}</td>"
        html_s += "</tr>"
    st.markdown(html_s + "</table>", unsafe_allow_html=True)

    # --- TABEL 2: 7 PREDIKSI AKURAT ---
    st.subheader("🔵 TABEL 2: 7 PREDIKSI AKURAT (HOT FREQUENCY)")
    data_a = generate_table_data("akurat")
    html_a = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(7):
        html_a += f"<tr><td style='font-size:14px;'>#{r+1}</td>"
        for c in range(4):
            html_a += f"<td class='bg-akurat'>{data_a[c][r]}</td>"
        html_a += "</tr>"
    st.markdown(html_a + "</table>", unsafe_allow_html=True)

    # --- TABEL 3: 8 KONTRA PREDIKSI ---
    st.subheader("🔴 TABEL 3: 8 KONTRA PREDIKSI (OUTLIER/COLD)")
    data_k = generate_table_data("kontra")
    html_k = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(8):
        html_k += f"<tr><td style='font-size:14px;'>#{r+1}</td>"
        for c in range(4):
            html_k += f"<td class='bg-kontra'>{data_k[c][r]}</td>"
        html_k += "</tr>"
    st.markdown(html_k + "</table>", unsafe_allow_html=True)

else:
    st.info("💡 Silakan masukkan histori data pada sidebar untuk memicu 8-Theory Optimizer.")
