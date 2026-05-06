import streamlit as st
import numpy as np
from collections import Counter

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v28.0: Inverse Matrix", layout="wide")

# --- 2. CSS CUSTOM (BIRU LAUT MODERN) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .main-card { 
        background: rgba(0, 0, 0, 0.6); border: 2px solid #00d2ff; 
        border-radius: 12px; padding: 20px; text-align: center;
    }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 4px; }
    .predict-table td { 
        border-radius: 8px; padding: 15px; text-align: center; font-size: 32px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.25); border: 1px solid #00d2ff;
        color: white !important; text-shadow: 2px 2px 5px #000;
    }
    .rank-label { font-size: 16px !important; background: rgba(0,0,0,0.7) !important; color: #00ffcc !important; }
    .boom-text { font-size: 50px !important; font-weight: 900; display: block; letter-spacing: 10px; }
    .b1 { color: #00ffcc; text-shadow: 0 0 30px #00ffcc; }
    .b2 { color: #f2c94c; text-shadow: 0 0 30px #f2c94c; }
    .b3 { color: #ffffff; text-shadow: 0 0 30px #ffffff; }
    .dead-row { background: rgba(255, 0, 0, 0.5) !important; color: #ffffff !important; border: 2px solid #ff0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HARD RESET SYSTEM ---
if 'data_key' not in st.session_state:
    st.session_state.data_key = 0

def hard_reset():
    st.session_state.data_key += 1
    st.rerun()

# --- 4. INVERSE MATRIX ENGINE (MENDONGKRAK AKURASI) ---
def inverse_matrix_engine(data):
    if not data: return None
    rows = [[int(d) for d in item if d.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if len(rows) < 10: return "LOW"

    data_np = np.array(rows)
    final_res = []

    for i in range(4):
        col = data_np[:, i]
        scores = {}
        
        # Analisis 1: Frekuensi Murni (Angka Hidup)
        freq = Counter(col)
        
        # Analisis 2: Gap Analysis (Angka Mati/Lama)
        gaps = {}
        for n in range(10):
            try:
                last_seen = len(col) - 1 - list(col[::-1]).index(n)
                gaps[n] = len(col) - last_seen
            except:
                gaps[n] = len(col) + 10

        # RUMUS BARU (INVERSE BIAS):
        # Kita mencari angka yang "Frekuensi Tinggi" tapi "Sedang Absen" 3-7 putaran.
        # Ini adalah titik manis (sweet spot) akurasi.
        for n in range(10):
            f_score = freq[n] * 10
            g_score = gaps[n]
            
            # Jika angka baru keluar (gap 1-2), beri penalti agar tidak meleset
            # Jika angka terlalu lama mati (gap > 20), beri penalti
            if g_score <= 2: bias = -50
            elif g_score > 20: bias = -30
            else: bias = g_score * 5
            
            scores[n] = f_score + bias
            
        sorted_nums = [n for n, s in sorted(scores.items(), key=lambda x: x, reverse=True)]
        final_res.append(sorted_nums)
        
    return final_res

# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v28.0 - INVERSE MATRIX")

# Widget input dengan key dinamis untuk reset total
input_data = st.text_area("Input Data History 4D:", height=150, key=f"input_{st.session_state.data_key}")

c_run, c_del = st.columns(2)
with c_run:
    analyze_btn = st.button("🚀 JALANKAN ANALISA INVERSE", use_container_width=True)
with c_del:
    st.button("🗑️ RESET TOTAL DATA", on_click=hard_reset, use_container_width=True)

if analyze_btn:
    if input_data:
        res = inverse_matrix_engine(input_data.replace(',', ' ').split())
        
        if res == "LOW":
            st.error("Data minimal 10 baris!")
        elif res:
            # --- TRIPLE BOOM ---
            st.markdown("### 💣 TRIPLE BOOM PREDIKSI")
            b1, b2, b3 = st.columns(3)
            with b1: st.markdown(f"<div class='main-card'>BOOM #1<br><span class='boom-text b1'>{res[0][0]}{res[1][0]}{res[2][0]}{res[3][0]}</span></div>", unsafe_allow_html=True)
            with b2: st.markdown(f"<div class='main-card'>BOOM #2<br><span class='boom-text b2'>{res[0][1]}{res[1][1]}{res[2][1]}{res[3][1]}</span></div>", unsafe_allow_html=True)
            with b3: st.markdown(f"<div class='main-card'>BOOM #3<br><span class='boom-text b3'>{res[0][2]}{res[1][2]}{res[2][2]}{res[3][2]}</span></div>", unsafe_allow_html=True)

            # --- TABEL RANKING R1 - R8 ---
            st.markdown("### 📊 DATA TRACKING (R1 - R8)")
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
