import streamlit as st
import numpy as np
from collections import Counter
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v32.0: Pro Logic", layout="wide")

# --- 2. CSS CUSTOM (Tetap Sama) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .main-card { background: rgba(0, 0, 0, 0.6); border: 2px solid #00d2ff; border-radius: 12px; padding: 20px; text-align: center; }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 4px; }
    .predict-table td { 
        border-radius: 8px; padding: 15px; text-align: center; font-size: 32px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.2); border: 1px solid #00d2ff; color: white !important; 
    }
    .rank-label { font-size: 16px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; }
    .dead-row { background: rgba(255, 0, 0, 0.5) !important; border: 2px solid red !important; }
    </style>
    """, unsafe_allow_html=True)

if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    if 'current_res' in st.session_state: del st.session_state.current_res
    st.rerun()

# --- 4. ENHANCED ENGINE V32.0 ---
def smart_engine(data_raw):
    if not data_raw: return None
    
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    
    if len(rows) < 10: return "LOW"

    data_np = np.array(rows)
    final_res = []

    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        
        # 1. EXPONENTIAL WEIGHTING (Tren Terbaru)
        # Angka paling baru dapet bobot jauh lebih tinggi
        for idx, val in enumerate(reversed(col)):
            weight = 100 / (idx + 1) 
            scores[val] += weight

        # 2. LAPSE TIME ANALYSIS (Interval/Gap)
        # Memberikan bonus poin untuk angka yang sudah "waktunya" keluar
        for n in range(10):
            last_seen = -1
            for idx, val in enumerate(reversed(col)):
                if val == n:
                    last_seen = idx
                    break
            if last_seen == -1: # Belum pernah muncul
                scores[n] += 50
            else:
                scores[n] += last_seen * 2 # Semakin lama tidak muncul, skor naik sedikit

        # 3. KESEIMBANGAN PROBABILITAS (Odd-Even & Big-Small)
        avg_val = np.mean(col)
        for n in range(10):
            # Penyeimbang Besar/Kecil
            if avg_val > 4.5 and n <= 4: scores[n] += 5 
            if avg_val <= 4.5 and n > 4: scores[n] += 5
            
        # 4. RANDOM NOISE (Anti-Stuck)
        for n in range(10):
            scores[n] += np.random.uniform(0, 2)
            
        sorted_nums = [n for n, s in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
        final_res.append(sorted_nums)
        
    return final_res

# --- 5. UI CONTROL (Tetap Sama) ---
st.title("🛡️ MASTER BRAIN v32.0 - PRO LOGIC")

input_data = st.text_area("Tempel Data History Di Sini (Minimal 10 baris):", 
                          height=150, key=f"inp_{st.session_state.reset_key}",
                          placeholder="Contoh format:\n1234\n5678\n9012...")

c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 JALANKAN ANALISA AKURAT", use_container_width=True):
        if input_data:
            st.session_state.current_res = smart_engine(input_data)

with c2:
    st.button("🗑️ HAPUS SEMUA DATA", on_click=full_reset, use_container_width=True)

# --- 6. DISPLAY (Tetap Sama) ---
if 'current_res' in st.session_state and st.session_state.current_res:
    res = st.session_state.current_res
    if res == "LOW":
        st.error("Data kurang! Masukkan minimal 10 baris agar algoritma Lapse Time bekerja.")
    else:
        st.markdown("### 📊 DATA TRACKING (R1 - R10)")
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

