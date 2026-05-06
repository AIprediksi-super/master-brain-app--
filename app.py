import streamlit as st
import numpy as np
from collections import Counter

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v24.0: Deep Precision", layout="wide")

# --- 2. CSS CUSTOM (TETAP BIRU MODERN) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .main-card { 
        background: rgba(0, 0, 0, 0.5); 
        border: 1px solid #00d2ff; 
        border-radius: 12px; padding: 15px; 
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
    }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 3px; }
    .predict-table td { 
        border-radius: 5px; padding: 10px; text-align: center; font-size: 24px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.15); border: 1px solid rgba(0, 210, 255, 0.3);
        color: white !important; text-shadow: 1px 1px 2px #000;
    }
    .rank-label { font-size: 12px !important; background: rgba(0,0,0,0.4) !important; color: #00ffcc !important; }
    .boom-text { font-size: 38px !important; font-weight: 900; display: block; }
    .b1 { color: #00ffcc; text-shadow: 0 0 20px #00ffcc; }
    .b2 { color: #f2c94c; text-shadow: 0 0 20px #f2c94c; }
    .b3 { color: #ffffff; text-shadow: 0 0 20px #ffffff; }
    .dead-row { background: rgba(255, 0, 0, 0.25) !important; color: #ff9999 !important; border: 1px solid red !important; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MESIN PREDIKSI V24.0 (DEEP GAP & FREQUENCY PULSE) ---
def deep_precision_engine(data):
    if not data: return None
    rows = [[int(d) for d in item if d.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if len(rows) < 15: return "LOW_DATA"

    data_np = np.array(rows)
    final_results = []

    for i in range(4):
        col = data_np[:, i]
        scores = {}
        
        # Analisis Jarak (Gap) yang lebih dalam
        for n in range(10):
            # Temukan semua posisi angka n
            indices = np.where(col == n)[0]
            if len(indices) > 0:
                current_gap = len(col) - 1 - indices[-1]
                # Hitung rata-rata jarak kemunculan (Average Cycle)
                if len(indices) > 1:
                    avg_cycle = np.mean(np.diff(indices))
                else:
                    avg_cycle = len(col)
            else:
                current_gap = len(col)
                avg_cycle = 20 # Standar siklus

            # LOGIKA AKURASI: Angka yang current_gap-nya mendekati avg_cycle adalah angka "Hot"
            # Ini mendeteksi kapan sebuah angka SEHARUSNYA keluar berdasarkan siklusnya sendiri
            cycle_diff = abs(current_gap - avg_cycle)
            proximity_score = 100 / (cycle_diff + 1)
            
            # Tambahkan bobot frekuensi murni 15 data terakhir
            recent_weight = list(col[-15:]).count(n) * 15
            
            # Penalti untuk angka yang terlalu sering muncul beruntun (Over-saturation)
            penalty = 0
            if n == col[-1]: penalty = 80 # Sangat jarang angka yang sama muncul 2x di posisi sama
            
            scores[n] = proximity_score + recent_weight - penalty
            
        final_results.append(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    return final_results

# --- 4. UI INTERFACE ---
st.title("🚀 MASTER BRAIN v24.0 - DEEP PRECISION")

input_data = st.text_area("Input Data History (Minimal 15 baris):", height=150)

if st.button("⚡ JALANKAN ANALISA SIKLUS", use_container_width=True):
    res = deep_precision_engine(input_data.replace(',', ' ').split())
    
    if res == "LOW_DATA":
        st.error("Masukkan minimal 15 baris data untuk mengaktifkan Deep Gap Analysis!")
    elif res:
        # --- TRIPLE BOOM ---
        st.markdown("### 💣 BOOM PREDIKSI (SIKLUS TERKUAT)")
        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f"<div class='main-card'>BOOM #1<br><span class='boom-text b1'>{''.join([str(res[i][0][0]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
        with b2:
            st.markdown(f"<div class='main-card'>BOOM #2<br><span class='boom-text b2'>{''.join([str(res[i][1][0]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
        with b3:
            st.markdown(f"<div class='main-card'>BOOM #3<br><span class='boom-text b3'>{''.join([str(res[i][2][0]) for i in range(4)])}</span></div>", unsafe_allow_html=True)

        # --- TABEL PREDIKSI R1 - R8 ---
        st.markdown("### 📊 DATA TRACKING (RANK R1 - R8)")
        h = "<table class='predict-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
        
        # Tampilkan Rank 1 sampai 8 (Sesuai Permintaan)
        for r in range(8):
            h += f"<tr><td class='rank-label'>R{r+1}</td>"
            for c in range(4):
                # Ambil angka dari hasil sorted (index 0 adalah angka, index 1 adalah skor)
                h += f"<td>{res[c][r][0]}</td>"
            h += "</tr>"
            
        # Angka Mati (2 Baris Sisa: Rank 9 & 10)
        for r in range(8, 10):
            h += f"<tr><td class='dead-row'>DEAD</td>"
            for c in range(4):
                h += f"<td class='dead-row'>{res[c][r][0]}</td>"
            h += "</tr>"
            
        st.markdown(h + "</table>", unsafe_allow_html=True)

st.sidebar.info("v24.0: Ditambahkan Rank R1-R8. Menggunakan Siklus Rata-rata (Average Cycle) untuk meningkatkan akurasi.")
