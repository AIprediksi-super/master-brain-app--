import streamlit as st
import numpy as np
from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(page_title="Master Brain v20.0: Precision Engine", layout="wide")

# --- CYBER STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background: #0b0f19; color: #00e5ff; }
    .main-card { background: #16213e; border: 2px solid #00e5ff; border-radius: 15px; padding: 20px; }
    .predict-table { width: 100%; border-collapse: collapse; background: #1a1a2e; }
    .predict-table td, .predict-table th { 
        padding: 15px; text-align: center; border: 1px solid #0f3460; font-size: 20px;
    }
    .boom-1 { color: #ff0055; font-weight: 900; text-shadow: 0 0 15px #ff0055; font-size: 35px !important; }
    .boom-2 { color: #ffaa00; font-weight: 900; text-shadow: 0 0 15px #ffaa00; font-size: 30px !important; }
    .boom-3 { color: #00ff88; font-weight: 900; text-shadow: 0 0 15px #00ff88; font-size: 25px !important; }
    .dead-row { background: #2d0000 !important; color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE ENGINE V20.0 (PRECISION LOGIC) ---
def advanced_analysis(raw_data):
    if not raw_data: return None
    rows = [[int(d) for d in "".join(filter(str.isdigit, x))[:4]] for x in raw_data if len("".join(filter(str.isdigit, x))) >= 4]
    
    if len(rows) < 10: return "NEED_MORE"
    
    data_np = np.array(rows)
    results = {"cols": []}

    for i in range(4):
        col = data_np[:, i]
        total_n = len(col)
        
        # 1. ANALISIS STATISTIK BERLAPIS
        freq = Counter(col)
        recent_15 = col[-15:] # Fokus 15 data terakhir
        freq_recent = Counter(recent_15)
        
        # 2. LOGIKA GAP (Masa Tunggu)
        gaps = []
        for n in range(10):
            pos = np.where(col == n)[0]
            gap_val = (total_n - pos[-1]) if len(pos) > 0 else total_n
            gaps.append(gap_val)

        # 3. PERHITUNGAN SKOR AKURASI (The Formula)
        # (Bobot Riwayat + (Bobot Tren * 20) + (Gap / 2))
        final_scores = []
        for n in range(10):
            score = (freq[n] * 1.5) + (freq_recent[n] * 20) + (gaps[n] * 0.8)
            final_scores.append((n, score))
        
        # Urutkan: Tertinggi (Top), Terendah (Mati)
        sorted_res = sorted(final_scores, key=lambda x: x[1], reverse=True)
        results["cols"].append(sorted_res)

    return results

# --- UI DISPLAY ---
st.title("🎯 MASTER BRAIN v20.0 - ULTRA PRECISION")

input_txt = st.text_area("Tempel Data 4D:", height=150)

if st.button("⚡ PROSES ANALISA TINGKAT TINGGI"):
    res = advanced_analysis(input_txt.split())
    
    if res == "NEED_MORE":
        st.error("Data terlalu sedikit! Masukkan minimal 10-20 baris data.")
    elif res:
        # --- PREDIKSI UTAMA ---
        st.markdown("### 🔮 TABEL PREDIKSI AKURASI TINGGI")
        h_table = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(5):
            h_table += f"<tr><td>RANK {r+1}</td>"
            for c in range(4):
                h_table += f"<td>{res['cols'][c][r][0]}</td>"
            h_table += "</tr>"
        
        # --- TAMBAHAN 2 BARIS ANGKA MATI ---
        for r in range(8, 10):
            h_table += "<tr class='dead-row'><td>DEAD</td>"
            for c in range(4):
                h_table += f"<td>{res['cols'][c][r][0]}</td>"
            h_table += "</tr>"
        st.markdown(h_table + "</table>", unsafe_allow_html=True)

        st.markdown("---")

        # --- TRIPLE BOOM PREDIKSI ---
        st.markdown("### 💣 BOOM PREDIKSI (KOMBINASI TERKUAT)")
        b1, b2, b3 = st.columns(3)
        
        with b1:
            st.markdown(f"<div class='main-card'><center>BOOM #1<br><span class='boom-1'>{''.join([str(res['cols'][i][0][0]) for i in range(4)])}</span></center></div>", unsafe_allow_html=True)
        with b2:
            st.markdown(f"<div class='main-card'><center>BOOM #2<br><span class='boom-2'>{''.join([str(res['cols'][i][1][0]) for i in range(4)])}</span></center></div>", unsafe_allow_html=True)
        with b3:
            st.markdown(f"<div class='main-card'><center>BOOM #3<br><span class='boom-3'>{''.join([str(res['cols'][i][2][0]) for i in range(4)])}</span></center></div>", unsafe_allow_html=True)

st.sidebar.info("V20.0 menggunakan pembobotan tren 20x lebih kuat untuk menangkap pergeseran angka secara instan.")
