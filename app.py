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
    .kontra-table { border: 2px solid #ff4b4b !important; }
    .kontra-table td { background: rgba(255, 75, 75, 0.1) !important; border: 1px solid #ff4b4b !important; }
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; margin-bottom: 10px; }
    .kontra-header { color: #ff4b4b; text-shadow: 0 0 10px #ff4b4b; font-weight: bold; margin-bottom: 10px; margin-top: 30px; }
    h4 { margin-top: 25px; color: #00d2ff; text-transform: uppercase; letter-spacing: 2px; border-left: 5px solid #00d2ff; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    for key in ['current_res', 'pure_res', 'kontra_res']:
        if key in st.session_state: del st.session_state[key]
    st.rerun()

# --- 3. ENGINE LOGIC ---
def engine_processor(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    if not all_numbers: return None, None
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    
    final_rank = []
    kontra_rank = []
    
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        freq = Counter(col)
        
        # Logika Gabungan (Momentum + Gap + Freq)
        for idx, val in enumerate(reversed(col[-15:])):
            scores[val] += (250 / ((idx + 1.1) ** 0.9))
        for n in range(10):
            gap = 0
            for val in reversed(col):
                if val == n: break
                gap += 1
            scores[n] += (gap * 8.0) * (1 + (freq[n] / len(rows)))
        
        # Urutan Terkuat (Prediksi Utama)
        sorted_top = [n for n, s in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
        # Urutan Terlemah (Kontra Prediksi)
        sorted_bottom = [n for n, s in sorted(scores.items(), key=lambda x: x[1], reverse=False)]
        
        final_rank.append(sorted_top)
        kontra_rank.append(sorted_bottom)
        
    return final_rank, kontra_rank

# --- 4. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v75.0 PRO")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True):
        if input_data:
            res, kontra = engine_processor(input_data)
            st.session_state.current_res = res
            st.session_state.kontra_res = kontra
with c2:
    st.button("🗑️ HAPUS DATA", on_click=full_reset, use_container_width=True)

# --- 5. DISPLAY ---
if 'current_res' in st.session_state and st.session_state.current_res:
    res = st.session_state.current_res
    
    # TABEL PREDIKSI UTAMA
    st.markdown("<div class='pure-header'>💎 PREDIKSI UTAMA (TOP RANK)</div>", unsafe_allow_html=True)
    main_h = "<table class='predict-table pure-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for r in range(6):
        main_h += f"<tr><td class='rank-label' style='background:#004d40 !important;'>RANK {r+1}</td>" + "".join([f"<td>{res[c][r]}</td>" for c in range(4)]) + "</tr>"
    st.markdown(main_h + "</table>", unsafe_allow_html=True)

if 'kontra_res' in st.session_state and st.session_state.kontra_res:
    kontra = st.session_state.kontra_res
    
    # TABEL KONTRA PREDIKSI
    st.markdown("<div class='kontra-header'>⚠️ KONTRA PREDIKSI (ANTI-MAIN / TERLEMAH)</div>", unsafe_allow_html=True)
    kontra_h = "<table class='predict-table kontra-table'><tr><th>KONTRA</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for r in range(5):
        # Mengambil 5 terbawah
        kontra_h += f"<tr><td class='rank-label' style='background:#4a1414 !important;'>#{r+1}</td>" + "".join([f"<td>{kontra[c][r]}</td>" for c in range(4)]) + "</tr>"
    st.markdown(kontra_h + "</table>", unsafe_allow_html=True)
