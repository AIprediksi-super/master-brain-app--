import streamlit as st
import numpy as np
from collections import Counter

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v31.0: Single Digit", layout="wide")

# --- 2. CSS CUSTOM (BIRU LAUT MODERN & BERSIH) ---
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
        background: rgba(0, 210, 255, 0.2); border: 1px solid #00d2ff;
        color: white !important; text-shadow: 2px 2px 4px #000;
    }
    .rank-label { font-size: 16px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; }
    .boom-text { font-size: 50px !important; font-weight: 900; display: block; letter-spacing: 10px; }
    .b1 { color: #00ffcc; text-shadow: 0 0 30px #00ffcc; }
    .b2 { color: #f2c94c; text-shadow: 0 0 30px #f2c94c; }
    .b3 { color: #ffffff; text-shadow: 0 0 30px #ffffff; }
    .dead-row { background: rgba(255, 0, 0, 0.5) !important; color: #ffffff !important; border: 2px solid red !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HARD RESET SYSTEM ---
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    if 'current_res' in st.session_state:
        del st.session_state.current_res
    st.rerun()

# --- 4. ENGINE V31.0 (CLEAN SINGLE DIGIT) ---
def single_digit_engine(data):
    if not data: return None
    rows = [[int(d) for d in item if d.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if len(rows) < 5: return "LOW"

    data_np = np.array(rows)
    final_res = []

    for i in range(4):
        col = data_np[:, i]
        scores = {}
        
        freq = Counter(col)
        last_val = col[-1]
        
        # Cari pola angka setelah angka terakhir (Follow-up)
        follow_ups = []
        for idx in range(len(col)-1):
            if col[idx] == last_val:
                follow_ups.append(col[idx+1])
        
        for n in range(10):
            # Skor Gabungan: Frekuensi + Follow-up + Momentum
            s_freq = freq[n] * 10
            s_follow = follow_ups.count(n) * 30
            s_recent = 50 if n in col[-5:] else 0
            
            scores[n] = s_freq + s_follow + s_recent
            
        # Urutkan dan pastikan hanya mengambil angka (0-9)
        sorted_nums = [n for n, s in sorted(scores.items(), key=lambda x: x, reverse=True)]
        final_res.append(sorted_nums)
        
    return final_res

# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v31.0 - CLEAN SINGLE DIGIT")

input_data = st.text_area("Input Data History 4D:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 JALANKAN ANALISA", use_container_width=True):
        if input_data:
            st.session_state.current_res = single_digit_engine(input_data.replace(',', ' ').split())

with c2:
    st.button("🗑️ HAPUS SEMUA DATA", on_click=full_reset, use_container_width=True)

# --- 6. DISPLAY HASIL ---
if 'current_res' in st.session_state and st.session_state.current_res:
    res = st.session_state.current_res
    if res == "LOW":
        st.error("Minimal 5-10 baris data!")
    else:
        # TRIPLE BOOM (Menampilkan 1 angka dari tiap kolom)
        st.markdown("### 💣 TRIPLE BOOM PREDIKSI")
        b1, b2, b3 = st.columns(3)
        with b1:
            val1 = "".join([str(res[i][0]) for i in range(4)])
            st.markdown(f"<div class='main-card'>BOOM #1<br><span class='boom-text b1'>{val1}</span></div>", unsafe_allow_html=True)
        with b2:
            val2 = "".join([str(res[i][1]) for i in range(4)])
            st.markdown(f"<div class='main-card'>BOOM #2<br><span class='boom-text b2'>{val2}</span></div>", unsafe_allow_html=True)
        with b3:
            val3 = "".join([str(res[i][2]) for i in range(4)])
            st.markdown(f"<div class='main-card'>BOOM #3<br><span class='boom-text b3'>{val3}</span></div>", unsafe_allow_html=True)

        # TABEL RANKING R1 - R8 (Angka Tunggal)
        st.markdown("### 📊 DATA TRACKING (R1 - R10)")
        h = "<table class='predict-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
        for r in range(8):
            h += f"<tr><td class='rank-label'>R{r+1}</td>"
            for c in range(4):
                h += f"<td>{res[c][r]}</td>" # Menampilkan 1 angka per kotak
            h += "</tr>"
        for r in range(8, 10):
            h += f"<tr><td class='dead-row'>DEAD</td>"
            for c in range(4):
                h += f"<td class='dead-row'>{res[c][r]}</td>"
            h += "</tr>"
        st.markdown(h + "</table>", unsafe_allow_html=True)
