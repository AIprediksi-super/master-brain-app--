import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Master Brain v19.0: Cyber Engine", layout="wide")

# --- CUSTOM CSS (CYBERPUNK STYLE) ---
st.markdown("""
    <style>
    .stApp { background: #050a10; color: #00ffc8; }
    .main-card {
        background: rgba(0, 255, 200, 0.05);
        border: 1px solid #00ffc8;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 255, 200, 0.2);
    }
    .stat-box {
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
    }
    .predict-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .predict-table td, .predict-table th {
        padding: 12px;
        text-align: center;
        border: 1px solid rgba(0, 255, 200, 0.2);
    }
    .highlight { color: #fff; font-weight: bold; text-shadow: 0 0 10px #00ffc8; font-size: 24px; }
    .dead-zone { color: #ff4b4b; text-shadow: 0 0 10px #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- BRAIN ENGINE V19.0 (THE LOGIC) ---
def analyze_data(raw_data):
    if not raw_data: return None
    
    # 1. Cleaning & Formatting
    rows = []
    for item in raw_data:
        clean = "".join(filter(str.isdigit, item))
        if len(clean) >= 4: rows.append([int(d) for d in clean[:4]])
    
    if len(rows) < 5: return "NEED_MORE_DATA"

    # 2. Advanced Statistical Processing
    data_np = np.array(rows)
    total_len = len(rows)
    results = {"cols": [], "master_4d": []}

    for i in range(4): # Loop tiap kolom (As, Kop, Kepala, Ekor)
        col_data = data_np[:, i]
        
        # A. Frequency Scoring (Weighted)
        # 10 data terakhir bobotnya 10x lebih besar
        recent_data = col_data[-10:]
        freq = Counter(col_data)
        recent_freq = Counter(recent_data)
        
        # B. Gap Analysis (Sudah berapa lama tidak muncul)
        gaps = {}
        for num in range(10):
            last_seen = np.where(col_data == num)[0]
            gaps[num] = (total_len - last_seen[-1]) if len(last_seen) > 0 else total_len

        # C. Combined Scoring Algorithm
        # Rumus: (Frekuensi Total * 1) + (Frekuensi Baru * 15) + (Gap * 0.5)
        scores = {}
        for num in range(10):
            scores[num] = (freq[num] * 1) + (recent_freq[num] * 15) + (gaps[num] * 0.5)
        
        sorted_nums = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results["cols"].append({
            "top": [n[0] for n in sorted_nums[:5]],
            "cold": [n[0] for n in sorted_nums[-3:]],
            "scores": scores
        })

    return results

# --- UI INTERFACE ---
st.title("⚡ MASTER BRAIN v19.0")
st.subheader("Ultimate Cybernetic Prediction Engine")

col_in, col_out = st.columns([1, 2])

with col_in:
    st.markdown("### 📥 Input Historis")
    data_input = st.text_area("Tempel angka 4D di sini:", height=300, placeholder="Contoh:\n1234\n5678\n9012...")
    
    if st.button("🚀 ANALISA SEKARANG", use_container_width=True):
        if data_input:
            st.session_state.processed = analyze_data(data_input.split())
        else:
            st.error("Data kosong!")

with col_out:
    if 'processed' in st.session_state:
        res = st.session_state.processed
        
        if res == "NEED_MORE_DATA":
            st.warning("Masukkan minimal 5 baris data untuk analisa akurat.")
        elif res:
            st.markdown("### 🔮 HASIL PREDIKSI TERAKURAT")
            
            # --- TABEL UTAMA ---
            html_table = "<table class='predict-table'><tr><th>RANK</th><th>AS</th><th>KOP</th><th>KEPALA</th><th>EKOR</th></tr>"
            for r in range(5):
                html_table += f"<tr><td>#{r+1}</td>"
                for c in range(4):
                    num = res["cols"][c]["top"][r]
                    html_table += f"<td class='highlight'>{num}</td>"
                html_table += "</tr>"
            html_table += "</table>"
            st.markdown(html_table, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # --- TABEL ELIMINASI & COLD ---
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### 💀 ANGKA MATI (ZONA MERAH)")
                dead_nums = " - ".join([str(res["cols"][i]["cold"][0]) for i in range(4)])
                st.markdown(f"<h1 class='dead-zone'>{dead_nums}</h1>", unsafe_allow_html=True)
                st.caption("Angka dengan probabilitas terendah saat ini.")
            
            with c2:
                st.markdown("### 💎 TOP BOOM 4D")
                boom = "".join([str(res["cols"][i]["top"][0]) for i in range(4)])
                st.markdown(f"<h1 style='color:#f2c94c;'>{boom}</h1>", unsafe_allow_html=True)
                st.caption("Kombinasi terkuat berdasarkan skor algoritma.")

# --- FOOTER ---
st.markdown("---")
st.caption("Master Brain v19.0 - Menggunakan Logika Gap Analysis & Weighted Frequency")
