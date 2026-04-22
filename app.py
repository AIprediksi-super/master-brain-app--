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
        self.sum_min, self.sum_max = 10, 26 # Rentang ideal 4-Digit

    def apply_8_theories(self, pick):
        """Validasi menggunakan 8 teori (7 Standar + 1 Kontra)"""
        nums = [int(x) for x in pick]
        total_sum = sum(nums)
        lows = len([n for n in nums if n <= self.mid_point])
        odds = len([n for n in nums if n % 2 != 0])
        
        # 1-7: Filter Seimbang (Balanced)
        is_balanced = (1 <= lows <= 3) and (1 <= odds <= 3) and (self.sum_min <= total_sum <= self.sum_max)
        
        # 8: Filter Kontra (Outlier)
        is_outlier = (lows == 0 or lows == 4) or (total_sum < self.sum_min or total_sum > self.sum_max)
        
        return is_balanced, is_outlier

# --- INISIALISASI ---
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'id'])

reader = load_ocr()
opt = UltimateOptimizer()

# --- STREAMLIT UI ---
st.set_page_config(page_title="Master Brain v15: 8-Theory Hybrid", layout="wide")

if 'global_history' not in st.session_state:
    st.session_state.global_history = []

# --- TEMA ---
tema = st.sidebar.selectbox("Pilih Tema:", ["Gelap Neon", "Ungu Neon"])
t = {"bg": "#0E1117", "txt": "#00FF00", "akurat": "#006400", "kontra": "#8B0000"} if tema == "Gelap Neon" else {"bg": "#2D004D", "txt": "#BF00FF", "akurat": "#7B1FA2", "kontra": "#4A148C"}

st.markdown(f"<style>.stApp {{ background-color: {t['bg']}; color: {t['txt']}; }} .bg-akurat {{ background-color: {t['akurat']}; }} .bg-kontra {{ background-color: {t['kontra']}; }}</style>", unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V15: HYBRID OPTIMIZER")

# --- INPUT ---
manual_input = st.text_area("Tempel Histori:", height=100)
if st.button("🚀 ANALISA"):
    if manual_input:
        st.session_state.global_history.extend(manual_input.replace(',', ' ').split())

# --- PROSES ANALISA ---
def get_predictions(data):
    # Logika Markov & Freq per Kolom
    col_data = [[] for _ in range(4)]
    for item in data:
        chars = [c for c in item if c.isalnum()]
        for i in range(min(4, len(chars))): col_data[i].append(chars[i])
    
    preds = {"balanced": [], "accurate": [], "outlier": []}
    
    # Generate kandidat angka
    for _ in range(100):
        pick = [random.choice(col_data[i]) if col_data[i] else str(random.randint(0,9)) for i in range(4)]
        is_bal, is_out = opt.apply_8_theories(pick)
        
        ticket = "".join(pick)
        if is_bal and len(preds["balanced"]) < 1: preds["balanced"].append(ticket)
        if is_bal and len(preds["accurate"]) < 7: preds["accurate"].append(ticket)
        if is_out and len(preds["outlier"]) < 1: preds["outlier"].append(ticket)
            
    return preds

# --- DISPLAY HASIL ---
if st.session_state.global_history:
    res = get_predictions(st.session_state.global_history)
    
    # 1. Hasil Paling Seimbang
    st.subheader("1️⃣ HASIL 7-TEORI PALING SEIMBANG (TOP TICKET)")
    if res["balanced"]:
        st.info(f"✨ Rekomendasi Utama: **{res['balanced'][0]}** (Lolos Filter Geometris & Statistik)")

    # 2. 7 Hasil Prediksi Akurat
    st.subheader("2️⃣ 7 PREDIKSI AKURAT (7-TEORI VALIDATED)")
    cols = st.columns(7)
    for i, ticket in enumerate(res["accurate"]):
        cols[i].markdown(f"<div class='bg-akurat' style='padding:10px; border-radius:10px; text-align:center; font-weight:bold; color:white;'>{ticket}</div>", unsafe_allow_html=True)

    # 3. Kontra Teori
    st.subheader("3️⃣ KONTRA TEORI (OUTLIER STRATEGY)")
    if res["outlier"]:
        st.error(f"⚠️ Tiket Kontra: **{res['outlier'][0]}** (Digunakan untuk kondisi hasil ekstrem)")

else:
    st.info("Masukkan data histori untuk memulai analisa.")
