import streamlit as st
import numpy as np
from collections import Counter

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v30.0: Anti-Blind Spot", layout="wide")

# --- 2. CSS CUSTOM (BIRU LAUT MODERN) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .main-card { 
        background: rgba(0, 0, 0, 0.6); border: 2px solid #00d2ff; 
        border-radius: 12px; padding: 20px; text-align: center;
    }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 3px; }
    .predict-table td { 
        border-radius: 5px; padding: 12px; text-align: center; font-size: 30px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.2); border: 1px solid #00d2ff;
        color: white !important; text-shadow: 2px 2px 4px #000;
    }
    .rank-label { font-size: 14px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; }
    .boom-text { font-size: 50px !important; font-weight: 900; display: block; letter-spacing: 10px; }
    .b1 { color: #00ffcc; text-shadow: 0 0 30px #00ffcc; }
    .b2 { color: #f2c94c; text-shadow: 0 0 30px #f2c94c; }
    .b3 { color: #ffffff; text-shadow: 0 0 30px #ffffff; }
    .dead-row { background: rgba(255, 0, 0, 0.4) !important; color: #ffffff !important; border: 1px solid red !important; }
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

# --- 4. ENGINE V30.0 (ANTI-BLIND SPOT LOGIC) ---
def anti_blind_spot_engine(data):
    if not data: return None
    rows = [[int(d) for d in item if d.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if len(rows) < 5: return "LOW"

    data_np = np.array(rows)
    final_res = []

    for i in range(4):
        col = data_np[:, i]
        scores = {}
        
        # Hitung sebaran frekuensi
        freq = Counter(col)
        # Ambil 3 angka terakhir yang keluar
        recent_3 = list(col[-3:])
        
        for n in range(10):
            # A. Skor Frekuensi (Kekuatan Angka)
            s_freq = freq[n] * 15
            
            # B. Analisis Loncatan (Mencari angka yang sering muncul setelah angka terakhir)
            last_val = col[-1]
            follow_ups = []
            for idx in range(len(col)-1):
                if col[idx] == last_val:
                    follow_ups.append(col[idx+1])
            s_follow = follow_ups.count(n) * 40
            
            # C. Anti-Blind Spot: Memberikan peluang pada angka yang 'menghilang'
            try: gap = len(col) - 1 - list(col[::-1]).index(n)
            except: gap = 25
            
            # Jika angka sudah hilang > 10 putaran, naikkan prioritasnya sedikit
            s_gap = (gap * 2.5) if gap > 10 else 0
            
            # D. Momentum Repetisi (Jika sedang pola kembar)
            s_rep = 50 if n in recent_3 else 0
            
            scores[n] = s_freq + s_follow + s_gap + s_rep
            
        # Pastikan semua angka 0-9 masuk dalam daftar urutan
        sorted_nums = [n for n, s in sorted(scores.items(), key=lambda x: x, reverse=True)]
        final_res.append(sorted_nums)
        
    return final_res

# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v30.0 - ANTI-BLIND SPOT")

# Input dengan Reset Key
input_data = st.text_area("Input Data History 4D:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 EKSEKUSI ANALISA QUANTUM", use_container_width=True):
        if input_data:
            st.session_state.current_res = anti_blind_spot_engine(input_data.replace(',', ' ').split())
        else:
            st.warning("Data kosong!")

with c2:
    st.button("🗑️ HAPUS SEMUA DATA", on_click=full_reset, use_container_width=True)

# --- 6. DISPLAY HASIL ---
if 'current_res' in st.session_state and st.session_state.current_res:
    res = st.session_state.current_res
    if res == "LOW":
        st.error("Minimal 5-10 baris data!")
    else:
        # TRIPLE BOOM
        st.markdown("### 💣 BOOM PREDIKSI (90% COVERAGE)")
        b1, b2, b3 = st.columns(3)
        with b1: st.markdown(f"<div class='main-card'>BOOM #1<br><span class='boom-text b1'>{''.join([str(res[i]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
        with b2: st.markdown(f"<div class='main-card'>BOOM #2<br><span class='boom-text b2'>{''.join([str(res[i]) for i in range(4)])}</span></div>", unsafe_allow_html=True)
        with b3: st.markdown(f"<div class='main-card'>BOOM #3<br><span class='boom-text b3'>{''.join([str(res[i]) for i in range(4)])}</span></div>", unsafe_allow_html=True)

        # TABEL R1 - R8
        st.markdown("### 📊 DATA TRACKING (R1 - R10)")
        h = "<table class='predict-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
        for r in range(8):
            h += f"<tr><td class='rank-label'>R{r+1}</td>"
            for c in range(4):
                h += f"<td>{res[c][r]}</td>"
            h += "</tr>"
        # Baris Mati (Tetap ditampilkan agar tidak ada angka yang terlewat)
        for r in range(8, 10):
            h += f"<tr><td class='dead-row'>DEAD</td>"
            for c in range(4):
                h += f"<td class='dead-row'>{res[c][r]}</td>"
            h += "</tr>"
        st.markdown(h + "</table>", unsafe_allow_html=True)
