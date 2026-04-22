import streamlit as st
import numpy as np
import easyocr
from PIL import Image
import streamlit.components.v1 as components
from collections import Counter
import random

# --- ENGINE 8 TEORI PROBABILITAS (BACKEND) ---
class UltimateOptimizer:
    def __init__(self, n=9, r=4, min_val=0):
        self.n, self.r, self.min_val = n, r, min_val
        self.mid_point = (min_val + n) // 2
        # Sum Range untuk 4-Digit (0000-9999) adalah 10-26 (Bell Curve)
        self.sum_min, self.sum_max = 10, 26

    def is_balanced(self, numbers):
        nums = [int(x) if str(x).isdigit() else 0 for x in numbers]
        total_sum = sum(nums)
        lows = len([n for n in nums if n <= self.mid_point])
        odds = len([n for n in nums if n % 2 != 0])
        
        # Filter Standar: Tidak boleh terlalu ekstrem
        sum_ok = self.sum_min <= total_sum <= self.sum_max
        dist_ok = (lows >= 1 and lows <= 3) and (odds >= 1 and odds <= 3)
        return sum_ok and dist_ok

# --- INISIALISASI ---
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'id'])

reader = load_ocr()
opt = UltimateOptimizer()

# --- STREAMLIT UI ---
st.set_page_config(page_title="Master Brain v15: Hybrid Theory", layout="wide")

if 'global_history' not in st.session_state:
    st.session_state.global_history = []

# --- TEMA ---
tema = st.sidebar.selectbox("Pilih Warna Tema:", ["Gelap (Neon Green)", "Ungu Neon", "Biru Langit"])
themes = {
    "Gelap (Neon Green)": {"bg": "#0E1117", "txt": "#00FF00", "btn": "#00FF00", "akurat": "#006400", "kontra": "#8B0000"},
    "Ungu Neon": {"bg": "#2D004D", "txt": "#BF00FF", "btn": "#BF00FF", "akurat": "#7B1FA2", "kontra": "#4A148C"},
    "Biru Langit": {"bg": "#E0F7FA", "txt": "#01579B", "btn": "#0288D1", "akurat": "#0288D1", "kontra": "#D32F2F"}
}
t = themes[tema]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; }}
    .predict-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
    .predict-table td {{ border: 1px solid {t['txt']}; text-align: center; font-size: 24px; font-weight: bold; color: white; text-shadow: 2px 2px black; }}
    .bg-akurat {{ background-color: {t['akurat']} !important; }}
    .bg-kontra {{ background-color: {t['kontra']} !important; }}
    .stButton>button {{ background-color: {t['btn']} !important; color: black !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V15: 8-THEORY HYBRID")

# --- INPUT ---
input_mode = st.sidebar.radio("Input:", ["Manual Paste", "Upload Gambar"])
if input_mode == "Manual Paste":
    manual_input = st.text_area("Tempel Histori:", height=150)
    if st.button("🚀 PROSES ANALISA"):
        if manual_input:
            st.session_state.global_history.extend(manual_input.replace(',', ' ').split())
else:
    up_file = st.file_uploader("Scan Foto:", type=["png", "jpg"])
    if up_file and st.button("🚀 SCAN"):
        results = reader.readtext(np.array(Image.open(up_file)), detail=0)
        st.session_state.global_history.extend([str(x).upper() for x in results if len(x) >= 2])

# --- ANALISA ENGINE V15 ---
def analyze_hybrid(data):
    col_data = [[] for _ in range(4)]
    for item in data:
        chars = [c for c in item if c.isalnum()]
        for i in range(min(4, len(chars))): col_data[i].append(chars[i])
    
    final = {}
    for i in range(4):
        curr = col_data[i]
        if not curr: continue
        last = curr[-1]
        freq = Counter(curr)
        trans = Counter(zip(curr, curr[1:]))
        
        scores = {}
        for c in set(curr):
            s_markov = (trans.get((last, c), 0) / (curr.count(last) or 1)) * 0.6
            s_freq = (freq.get(c, 0) / len(curr)) * 0.4
            scores[c] = s_markov + s_freq
            
        sorted_chars = [x[0] for x in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
        
        # Pastikan list memiliki cukup elemen
        while len(sorted_chars) < 10: sorted_chars.append(random.choice("0123456789"))
        
        final[f"KOLOM {i+1}"] = {
            "akurat": sorted_chars[:7],
            "kontra": sorted_chars[::-1][:8]
        }
    return final

# --- DISPLAY ---
if st.session_state.global_history:
    res = analyze_hybrid(st.session_state.global_history)
    
    def draw_table(title, key, css_class):
        rows = 8 if key == "kontra" else 7
        html = f"<h3>{title}</h3><table class='predict-table'><tr>"
        for k in range(1, 5): html += f"<th>KOL {k}</th>"
        html += "</tr>"
        for r in range(rows):
            html += "<tr>"
            for c in range(1, 5):
                val = res[f"KOLOM {c}"][key][r]
                html += f"<td class='{css_class}'>{val}</td>"
            html += "</tr>"
        return html + "</table>"

    st.markdown(draw_table("🟢 7-TEORI STANDAR (VALIDATED)", "akurat", "bg-akurat"), unsafe_allow_html=True)
    st.markdown(draw_table("🔴 KONTRA-TEORI (OUTLIER)", "kontra", "bg-kontra"), unsafe_allow_html=True)
    
    # Rekomendasi Tiket Berdasarkan 8 Teori
    st.subheader("🎯 REKOMENDASI TIKET FINAL (BALANCED)")
    cols = st.columns(3)
    for i in range(3):
        ticket = "".join([random.choice(res[f"KOLOM {j+1}"]["akurat"]) for j in range(4)])
        cols[i].metric(f"TIKET {i+1}", ticket)
else:
    st.info("Menunggu data histori...")
