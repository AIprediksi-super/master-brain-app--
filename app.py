import streamlit as st
import numpy as np
from collections import Counter

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v25.0: Absolute Control", layout="wide")

# --- 2. CSS CUSTOM (TETAP BIRU MODERN) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .main-card { 
        background: rgba(0, 0, 0, 0.5); 
        border: 1px solid #00d2ff; 
        border-radius: 12px; padding: 15px; 
        text-align: center;
    }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 3px; }
    .predict-table td { 
        border-radius: 5px; padding: 10px; text-align: center; font-size: 24px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.15); border: 1px solid rgba(0, 210, 255, 0.3);
        color: white !important;
    }
    .rank-label { font-size: 12px !important; background: rgba(0,0,0,0.5) !important; color: #00ffcc !important; }
    .boom-text { font-size: 38px !important; font-weight: 900; display: block; }
    .b1 { color: #00ffcc; text-shadow: 0 0 20px #00ffcc; }
    .b2 { color: #f2c94c; text-shadow: 0 0 20px #f2c94c; }
    .b3 { color: #ffffff; text-shadow: 0 0 20px #ffffff; }
    .dead-row { background: rgba(255, 0, 0, 0.4) !important; color: #ffcccc !important; border: 1px solid red !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE FOR RESET ---
if 'history_data' not in st.session_state:
    st.session_state.history_data = ""

# --- 4. MESIN PREDIKSI V25.0 (HYBRID MOMENTUM) ---
def hybrid_engine(data):
    if not data: return None
    rows = [[int(d) for d in item if d.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if len(rows) < 10: return "LOW_DATA"

    data_np = np.array(rows)
    final_results = []

    for i in range(4):
        col = data_np[:, i]
        scores = {}
        
        # Hitung Frekuensi 10 data terakhir (Momentum Panas)
        recent_10 = list(col[-10:])
        # Hitung Frekuensi Total
        total_freq = list(col)
        
        for n in range(10):
            # 1. Skor Frekuensi Terbaru (Sangat Penting untuk Angka Hidup)
            s_recent = recent_10.count(n) * 40 
            
            # 2. Skor Frekuensi Total
            s_total = total_freq.count(n) * 5
            
            # 3. Analisis Jeda (Gap) - Memberikan peluang pada angka yang baru saja 'istirahat' sebentar
            try: last_seen = len(col) - 1 - list(col[::-1]).index(n)
            except: last_seen = 0
            gap = len(col) - last_seen
            
            # Jika gap 1-3 (baru keluar), beri bonus kecil (pola repetisi)
            # Jika gap > 15 (terlalu lama mati), kurangi skor (angka beku)
            s_gap = 20 if 1 <= gap <= 4 else (5 if gap <= 10 else -10)
            
            scores[n] = s_recent + s_total + s_gap
            
        final_results.append(sorted(scores.items(), key=lambda x: x, reverse=True))
    return final_results

# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v25.0 - ABSOLUTE CONTROL")

# Input area terhubung ke session state agar bisa di-reset
data_input = st.text_area("Input Data History:", value=st.session_state.history_data, height=150, key="input_box")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    btn_run = st.button("⚡ JALANKAN ANALISA", use_container_width=True)
with col_btn2:
    if st.button("🗑️ HAPUS SEMUA DATA", use_container_width=True):
        st.session_state.history_data = ""
        st.rerun()

if btn_run:
    if data_input:
        res = hybrid_engine(data_input.replace(',', ' ').split())
        
        if res == "LOW_DATA":
            st.error("Masukkan minimal 10 baris data!")
        elif res:
            # --- TRIPLE BOOM ---
            st.markdown("### 💣 BOOM PREDIKSI")
            b1, b2, b3 = st.columns(3)
            with b1: st.markdown(f"<div class='main-card'>BOOM #1<br><span class='boom-text b1'>{''.join([str(res[i]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
            with b2: st.markdown(f"<div class='main-card'>BOOM #2<br><span class='boom-text b2'>{''.join([str(res[i]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
            with b3: st.markdown(f"<div class='main-card'>BOOM #3<br><span class='boom-text b3'>{''.join([str(res[i]) for i in range(4)])}</span></div>", unsafe_allow_html=True)

            # --- TABEL PREDIKSI R1 - R8 ---
            st.markdown("### 📊 RANKING POSISI (R1 - R8)")
            h = "<table class='predict-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
            
            for r in range(8):
                h += f"<tr><td class='rank-label'>R{r+1}</td>"
                for c in range(4):
                    h += f"<td>{res[c][r]}</td>"
                h += "</tr>"
                
            for r in range(8, 10):
                h += f"<tr><td class='dead-row'>DEAD</td>"
                for c in range(4):
                    h += f"<td class='dead-row'>{res[c][r]}</td>"
                h += "</tr>"
                
            st.markdown(h + "</table>", unsafe_allow_html=True)
    else:
        st.warning("Silakan isi data terlebih dahulu!")
