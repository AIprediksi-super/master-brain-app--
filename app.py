import streamlit as st
import numpy as np
from collections import Counter

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v26.0: Clean Precision", layout="wide")

# --- 2. CSS CUSTOM (BIRU LAUT MODERN & BERSIH) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .main-card { 
        background: rgba(0, 0, 0, 0.5); 
        border: 1px solid #00d2ff; 
        border-radius: 12px; padding: 15px; text-align: center;
    }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 3px; }
    .predict-table td { 
        border-radius: 5px; padding: 12px; text-align: center; font-size: 28px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.2); border: 1px solid rgba(0, 210, 255, 0.4);
        color: white !important; text-shadow: 2px 2px 4px #000;
    }
    .rank-label { font-size: 14px !important; background: rgba(0,0,0,0.6) !important; color: #00ffcc !important; font-weight: bold; }
    .boom-text { font-size: 45px !important; font-weight: 900; display: block; letter-spacing: 5px; }
    .b1 { color: #00ffcc; text-shadow: 0 0 25px #00ffcc; }
    .b2 { color: #f2c94c; text-shadow: 0 0 25px #f2c94c; }
    .b3 { color: #ffffff; text-shadow: 0 0 25px #ffffff; }
    .dead-row { background: rgba(255, 0, 0, 0.4) !important; color: #ffcccc !important; border: 1px solid red !important; font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'input_box' not in st.session_state:
    st.session_state.input_box = ""

# --- 4. ENGINE ANALISA (MENGHASILKAN ANGKA BERSIH) ---
def clean_engine(data):
    if not data: return None
    rows = [[int(d) for d in item if d.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if len(rows) < 10: return "LOW_DATA"

    data_np = np.array(rows)
    final_results = []

    for i in range(4):
        col = data_np[:, i]
        scores = {}
        recent_12 = list(col[-12:]) # Fokus tren terbaru
        
        for n in range(10):
            # Hitung Jarak (Gap)
            try: last_seen = len(col) - 1 - list(col[::-1]).index(n)
            except: last_seen = 0
            gap = len(col) - last_seen
            
            # Logika Skor: Fokus pada angka aktif & siklus menengah
            score = (recent_12.count(n) * 50) + (list(col).count(n) * 2) + (gap * 1.5)
            # Proteksi: Kurangi sedikit skor jika angka baru saja keluar tepat di putaran terakhir
            if n == col[-1]: score -= 30
            
            scores[n] = score
        
        # Hanya ambil angkanya saja setelah diurutkan berdasarkan skor
        sorted_nums = [item[0] for item in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
        final_results.append(sorted_nums)
        
    return final_results

# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v26.0 - CLEAN PRECISION")

# Input area
input_val = st.text_area("Input Data History 4D:", value=st.session_state.input_box, height=150)

col_run, col_reset = st.columns(2)
with col_run:
    run_trigger = st.button("⚡ JALANKAN ANALISA", use_container_width=True)
with col_reset:
    if st.button("🗑️ HAPUS SEMUA DATA", use_container_width=True):
        st.session_state.input_box = ""
        st.rerun()

if run_trigger:
    if input_val:
        res = clean_engine(input_val.replace(',', ' ').split())
        
        if res == "LOW_DATA":
            st.error("Masukkan minimal 10 baris data untuk analisa!")
        elif res:
            # --- TRIPLE BOOM (ANGKA BERSIH) ---
            st.markdown("### 💣 BOOM PREDIKSI TERKUAT")
            b1, b2, b3 = st.columns(3)
            with b1: st.markdown(f"<div class='main-card'>BOOM #1<br><span class='boom-text b1'>{''.join([str(res[i][0]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
            with b2: st.markdown(f"<div class='main-card'>BOOM #2<br><span class='boom-text b2'>{''.join([str(res[i][1]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
            with b3: st.markdown(f"<div class='main-card'>BOOM #3<br><span class='boom-text b3'>{''.join([str(res[i][2]) for i in range(4)])}</span></div>", unsafe_allow_html=True)

            # --- TABEL RANKING R1 - R8 (ANGKA BERSIH TANPA SKOR) ---
            st.markdown("### 📊 RANKING POSISI (R1 - R8)")
            h = "<table class='predict-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
            
            for r in range(8):
                h += f"<tr><td class='rank-label'>R{r+1}</td>"
                for c in range(4):
                    h += f"<td>{res[c][r]}</td>"
                h += "</tr>"
                
            # Zona Mati (Rank 9 & 10)
            for r in range(8, 10):
                h += f"<tr><td class='dead-row'>DEAD</td>"
                for c in range(4):
                    h += f"<td class='dead-row'>{res[c][r]}</td>"
                h += "</tr>"
                
            st.markdown(h + "</table>", unsafe_allow_html=True)
