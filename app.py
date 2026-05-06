import streamlit as st
import numpy as np
from collections import Counter

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v23.0: Zero Logic", layout="wide")

# --- 2. CSS CUSTOM (BIRU LAUT MODERN) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .main-card { 
        background: rgba(0, 0, 0, 0.4); 
        border: 1px solid #00d2ff; 
        border-radius: 15px; padding: 20px; 
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.3);
    }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 5px; }
    .predict-table td { 
        border-radius: 8px; padding: 12px; text-align: center; font-size: 26px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.2); border: 1px solid #00d2ff;
        color: white !important; text-shadow: 2px 2px 4px #000;
    }
    .boom-text { font-size: 42px !important; font-weight: 900; display: block; }
    .b1 { color: #00ffcc; text-shadow: 0 0 25px #00ffcc; }
    .b2 { color: #f2c94c; text-shadow: 0 0 25px #f2c94c; }
    .b3 { color: #ffffff; text-shadow: 0 0 25px #ffffff; }
    .dead-row { background: rgba(255, 0, 0, 0.3) !important; color: #ff9999 !important; border: 1px solid red !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MESIN PREDIKSI V23.0 (ZERO-LOGIC ENGINE) ---
def zero_logic_engine(data):
    if not data: return None
    rows = [[int(d) for d in item if d.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if len(rows) < 10: return "LOW_DATA"

    data_np = np.array(rows)
    final_results = []

    for i in range(4):
        col = data_np[:, i]
        scores = {}
        
        # ANALISA 1: DETEKSI ANGKA MENGENDAP (GAP TERLAMA)
        # Angka yang paling lama tidak keluar punya skor 'hutang' tinggi
        gaps = []
        for n in range(10):
            try:
                last_idx = len(col) - 1 - list(col[::-1]).index(n)
                gap = len(col) - last_seen
            except:
                gap = len(col)
            gaps.append(gap)

        # ANALISA 2: FREKUENSI PULSE (5 DATA TERAKHIR)
        recent_5 = col[-5:]
        
        for n in range(10):
            # Rumus Baru: Prioritaskan angka yang absennya sedang (5-10 putaran) 
            # dan kurangi skor angka yang baru keluar (1-2 putaran lalu)
            current_gap = 0
            try: current_gap = len(col) - 1 - list(col[::-1]).index(n)
            except: current_gap = 99
            
            # Skor Utama: Semakin besar gap (sampai batas tertentu), semakin kuat
            # Tapi jika gap terlalu besar (angka beku), skor dikurangi sedikit
            dist_score = (current_gap * 2.5) 
            
            # Bonus jika angka tersebut sering muncul secara total (Kekuatan angka)
            freq_bonus = list(col).count(n) * 1.2
            
            # Penalti Keras: Jika angka muncul di 3 putaran terakhir, buang dari Rank Atas
            penalty = 0
            if n in col[-3:]: penalty = 100
            
            scores[n] = dist_score + freq_bonus - penalty
            
        final_results.append(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    return final_results

# --- 4. UI INTERFACE ---
st.title("🛡️ MASTER BRAIN v23.0 - ZERO LOGIC")

manual_input = st.text_area("Input Data (History):", height=150)

if st.button("🔥 JALANKAN EKSEKUSI DATA", use_container_width=True):
    res = zero_logic_engine(manual_input.replace(',', ' ').split())
    
    if res == "LOW_DATA":
        st.error("Data tidak cukup untuk dianalisa!")
    elif res:
        # --- TRIPLE BOOM ---
        st.markdown("### 💣 BOOM PREDIKSI (95% PROBABILITY)")
        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f"<div class='main-card'>BOOM #1<br><span class='boom-text b1'>{''.join([str(res[i][0][0]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
        with b2:
            st.markdown(f"<div class='main-card'>BOOM #2<br><span class='boom-text b2'>{''.join([str(res[i][1][0]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
        with b3:
            st.markdown(f"<div class='main-card'>BOOM #3<br><span class='boom-text b3'>{''.join([str(res[i][2][0]) for i in range(4)])}</span></div>", unsafe_allow_html=True)

        # --- TABEL PREDIKSI ---
        st.markdown("### 📊 TRACKING RANKING POSISI")
        h = "<table class='predict-table'><tr><th>LVL</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
        
        for r in range(5):
            h += f"<tr><td>R{r+1}</td>"
            for c in range(4):
                h += f"<td>{res[c][r][0]}</td>"
            h += "</tr>"
            
        for r in range(8, 10):
            h += f"<tr><td class='dead-row'>DEAD</td>"
            for c in range(4):
                h += f"<td class='dead-row'>{res[c][r][0]}</td>"
            h += "</tr>"
            
        st.markdown(h + "</table>", unsafe_allow_html=True)
