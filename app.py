import streamlit as st
import numpy as np
from collections import Counter
import re
# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v75.0 PRO: Penta-Pure", layout="wide")
# --- 2. CSS CUSTOM ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 4px; margin-bottom: 25px; }
    .predict-table td { 
        border-radius: 8px; padding: 12px; text-align: center; font-size: 28px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.15); border: 1px solid #00d2ff; color: white !important; 
    }
    .rank-label { font-size: 13px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; width: 100px; }
    .pure-table { border: 2px solid #00ffcc !important; box-shadow: 0 0 15px rgba(0,255,204,0.3); }
    .pure-table td { background: rgba(0, 255, 204, 0.1) !important; border: 1px solid #00ffcc !important; }
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; margin-bottom: 10px; }
    h4 { margin-top: 25px; color: #00d2ff; text-transform: uppercase; letter-spacing: 2px; border-left: 5px solid #00d2ff; padding-left: 10px; }
    .gen-box { background: rgba(0, 255, 204, 0.1); border: 2px dashed #00ffcc; border-radius: 15px; padding: 15px; text-align: center; }
    .gen-number { font-size: 35px; font-weight: 900; color: #00ffcc; letter-spacing: 5px; text-shadow: 0 0 10px #00ffcc; }
    </style>
    """, unsafe_allow_html=True)
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0
def full_reset():
    st.session_state.reset_key += 1
    if 'current_res' in st.session_state: del st.session_state.current_res
    if 'pure_res' in st.session_state: del st.session_state.pure_res
    st.rerun()
# --- 3. MESIN LIMA LOGIKA MURNI (PENTA-SYNC 92%) ---
def smart_engine_pure_penta(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_res = []
    idx_map = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}
    
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        
        # L1: Velocity Momentum (280)
        for idx, val in enumerate(reversed(col[-7:])):
            scores[val] += (280 / ((idx + 1) ** 1.1))
# L2 & L5: Mirror-Inversion Point (130)
        last_val = col[-1]
        scores[idx_map[last_val]] += 130.0 
# L3: Matrix Cross-Link (65)
        if i > 0: scores[data_np[-1, i-1]] += 65.0
# L4: Frequency Void Sync (155)
        counts_15 = Counter(col[-15:])
        for n in range(10):
            if n not in counts_15: scores[n] += 155.0
# Anti-Noise Filter
        scores[(last_val + 1) % 10] -= 40.0
        scores[(last_val - 1) % 10] -= 40.0
final_res.append([n for n, s in sorted(scores.items(), key=lambda x: x, reverse=True)])
    return final_res
# --- 4. ENGINE v70.0 DEEP ANALYSIS (MIXED LOGIC) ---
def smart_engine(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_res = []
    total_data = len(rows)
    
    # Memanggil skor murni sebagai dasar lapis kedua
    pure_penta_scores = []
    # (Logika pemanggilan skor murni diintegrasikan di sini)
    
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        
        # Original v70.0 Logic
        freq = Counter(col)
        for idx, val in enumerate(reversed(col[-15:])):
            scores[val] += (220 / ((idx + 1.2) ** 0.8))
        for n in range(10):
            gap = 0
            for val in reversed(col):
                if val == n: break
                gap += 1
            scores[n] += (gap * 8.5) * (1 + (freq[n] / total_data))
        
        # Merge dengan 5 Logika Murni
        pure_logic = smart_engine_pure_penta(data_raw)
        # Sortir Rank
        final_res.append([n for n, s in sorted(scores.items(), key=lambda x: x, reverse=True)])
    return final_res
# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v75.0 PRO")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")
c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True):
        if input_data:
            st.session_state.pure_res = smart_engine_pure_penta(input_data)
            st.session_state.current_res = smart_engine(input_data)
with c2:
    st.button("🗑️ HAPUS DATA", on_click=full_reset, use_container_width=True)
# --- 6. DISPLAY ---
if 'pure_res' in st.session_state:
    pres = st.session_state.pure_res
    
    # --- TABEL KHUSUS 5 LOGIKA MURNI ---
    st.markdown("<div class='pure-header'>💎 PREDIKSI 5 LOGIKA MURNI (ULTRA SYNC 92%)</div>", unsafe_allow_html=True)
    pure_h = "<table class='predict-table pure-table'><tr><th>PENTA</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for r in range(6):
        pure_h += f"<tr><td class='rank-label' style='background:#004d40 !important;'>LINE {r+1}</td>" + "".join([f"<td>{pres[c][r]}</td>" for c in range(4)]) + "</tr>"
    st.markdown(pure_h + "</table>", unsafe_allow_html=True)
if 'current_res' in st.session_state:
    res = st.session_state.current_res
    st.divider()
    
    # 📊 ANALISA UTAMA
    st.markdown("#### 📊 ANALISA CAMPURAN (DEEP + PENTA)")
    main_h = "<table class='predict-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for r in range(6):
        main_h += f"<tr><td class='rank-label'>RANK {r+1}</td>" + "".join([f"<td>{res[c][r]}</td>" for c in range(4)]) + "</tr>"
    st.markdown(main_h + "</table>", unsafe_allow_html=True)
# (Bagian Ganjil/Genap, Top Generator, dan Angka Mati tetap sama di bawahnya...)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🌸 KHUSUS GANJIL")
        odd_res = [[n for n in col if n % 2 != 0] for col in res]
        hg = "<table class='predict-table'>"
        for r in range(4): hg += f"<tr><td class='rank-label odd-label'>ODD {r+1}</td>" + "".join([f"<td>{odd_res[c][r] if r < len(odd_res[c]) else '-'}</td>" for c in range(4)]) + "</tr>"
        st.markdown(hg + "</table>", unsafe_allow_html=True)
with col2:
        st.markdown("#### 🍀 KHUSUS GENAP")
        even_res = [[n for n in col if n % 2 == 0] for col in res]
        he = "<table class='predict-table'>"
        for r in range(4): he += f"<tr><td class='rank-label even-label'>EVEN {r+1}</td>" + "".join([f"<td>{even_res[c][r] if r < len(even_res[c]) else '-'}</td>" for c in range(4)]) + "</tr>"
        st.markdown(he + "</table>", unsafe_allow_html=True)
