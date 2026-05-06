import streamlit as st
import numpy as np
from collections import Counter

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v32.0: Logic Fix", layout="wide")

# --- 2. CSS CUSTOM ---
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

# --- 3. HARD RESET ---
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    if 'current_res' in st.session_state: del st.session_state.current_res
    st.rerun()

# --- 4. ENGINE V32.0 (STRICT DATA READER) ---
def smart_engine(data_raw):
    if not data_raw: return None
    
    # Membersihkan data: hanya ambil blok yang benar-benar 4 digit angka
    rows = []
    import re
    all_numbers = re.findall(r'\d{4}', data_raw)
    for item in all_numbers:
        rows.append([int(d) for d in item])
    
    if len(rows) < 5: return "LOW"

    data_np = np.array(rows)
    final_res = []

    for i in range(4):
        col = data_np[:, i]
        # Algoritma Scoring: Frekuensi (60%) + Momentum Terbaru (40%)
        freq = Counter(col)
        recent = col[-5:]
        
        scores = {}
        for n in range(10):
            # Skor Frekuensi murni
            s_freq = freq.get(n, 0) * 10
            # Skor Momentum (angka yang sedang panas/sering muncul belakangan)
            s_recent = list(recent).count(n) * 50
            # Skor Acak Kecil (agar hasil tidak selalu berurutan jika skor sama)
            s_rand = np.random.uniform(0, 1)
            
            scores[n] = s_freq + s_recent + s_rand
            
        sorted_nums = [n for n, s in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
        final_res.append(sorted_nums)
    return final_res

# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v32.0 - ANTI-ERROR")

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

# --- 6. DISPLAY ---
if 'current_res' in st.session_state and st.session_state.current_res:
    res = st.session_state.current_res
    if res == "LOW":
        st.error("Data tidak valid atau kurang banyak! Masukkan minimal 10 baris angka 4D.")
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
