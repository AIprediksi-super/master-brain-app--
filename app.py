import streamlit as st
import numpy as np
from collections import Counter
import re
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v75.0 PRO: Anti-Trash", layout="wide")

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
    
    /* Panel 4 CSS - Terang & Jelas */
    .trash-table { border: 2px solid #ff5722 !important; }
    .trash-table td { 
        background: rgba(255, 87, 34, 0.15) !important; 
        border: 1px solid #ff5722 !important; 
        color: #ffffff !important; 
        text-shadow: 0 0 5px #ff5722;
    }
    
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; }
    .m1-header { color: #ffeb3b; font-weight: bold; }
    .trash-header { color: #ff5722; font-weight: bold; margin-top: 30px; text-shadow: 0 0 10px #ff5722; }
    </style>
    """, unsafe_allow_html=True)

if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    if 'current_res' in st.session_state: del st.session_state.current_res
    if 'pure_res' in st.session_state: del st.session_state.pure_res
    if 'm2_pure' in st.session_state: del st.session_state.m2_pure
    if 'trash_res' in st.session_state: del st.session_state.trash_res
    st.rerun()

# --- 3. MESIN LOGIKA ---
def smart_engine_pure_penta(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_scores = []
    idx_map = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        for idx, val in enumerate(reversed(col[-7:])):
            scores[val] += (280 / ((idx + 1) ** 1.1))
        last_val = col[-1]
        scores[idx_map[last_val]] += 130.0 
        if i > 0: scores[data_np[-1, i-1]] += 65.0
        counts_15 = Counter(col[-15:])
        for n in range(10):
            if n not in counts_15: scores[n] += 155.0
        scores[(last_val + 1) % 10] -= 40.0
        scores[(last_val - 1) % 10] -= 40.0
        final_scores.append(scores)
    return final_scores

def smart_engine_deep(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_scores = []
    total_data = len(rows)
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        freq = Counter(col)
        for idx, val in enumerate(reversed(col[-15:])):
            scores[val] += (220 / ((idx + 1.2) ** 0.8))
        for n in range(10):
            gap = 0
            for val in reversed(col):
                if val == n: break
                gap += 1
            scores[n] += (gap * 8.5) * (1 + (freq[n] / total_data))
        final_scores.append(scores)
    return final_scores

# --- 4. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v75.0 PRO")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

if st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True):
    if input_data:
        m1_s = smart_engine_pure_penta(input_data)
        m2_s = smart_engine_deep(input_data)
        
        # Peringkat Angka Per Kolom (Asli 0-9)
        p1_ranks = [[n for n, s in sorted(m1_s[c].items(), key=lambda x: x[1], reverse=True)] for c in range(4)]
        p2_ranks = [[n for n, s in sorted(m2_s[c].items(), key=lambda x: x[1], reverse=True)] for c in range(4)]
        
        # Simpan Panel 2 & 3 (7 Baris Murni)
        st.session_state.pure_res = p1_ranks
        st.session_state.m2_pure = p2_ranks
        
        # PANEL 1: Saringan 8 Baris M2 disaring M1 menjadi 6 Baris
        m2_top_8_rows = []
        for r in range(8):
            row = [p2_ranks[c][r] for c in range(4)]
            m2_top_8_rows.append(row)
            
        scored_rows = []
        for row in m2_top_8_rows:
            # Hitung skor baris ini di Mesin 1
            row_weight = sum(m1_s[c][row[c]] for c in range(4))
            scored_rows.append((row, row_weight))
        
        # Sortir dan ambil 6 baris terbaik
        st.session_state.current_res = [x[0] for x in sorted(scored_rows, key=lambda x: x[1], reverse=True)[:6]]
        
        # PANEL 4: Angka Sampah (Angka sisa yang tidak masuk Top 7 di M1 atau M2)
        trash_rows = []
        for r in range(5):
            trash_row = []
            for c in range(4):
                used_nums = set(p1_ranks[c][:7] + p2_ranks[c][:7])
                trash_pool = [n for n in range(10) if n not in used_nums]
                if not trash_pool: trash_pool = [n for n in range(10)]
                trash_row.append(random.choice(trash_pool))
            trash_rows.append(trash_row)
        st.session_state.trash_res = trash_rows

if st.button("🗑️ HAPUS DATA", on_click=full_reset, use_container_width=True): pass

# --- 5. DISPLAY ---
if 'current_res' in st.session_state:
    # PANEL 1
    st.markdown("<div class='pure-header'>💎 PANEL 1: HASIL CAMPURAN (6 BARIS)</div>", unsafe_allow_html=True)
    h1 = "<table class='predict-table pure-table'><tr><th>FINAL</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for i in range(6):
        h1 += f"<tr><td class='rank-label' style='background:#004d40 !important;'>BARIS {i+1}</td>" + "".join([f"<td>{st.session_state.current_res[i][c]}</td>" for c in range(4)]) + "</tr>"
    st.markdown(h1 + "</table>", unsafe_allow_html=True)

    # PANEL 2
    st.divider()
    st.markdown("<div class='m1-header'>🏆 PANEL 2: PREDIKSI MURNI MESIN PERTAMA (7 BARIS)</div>", unsafe_allow_html=True)
    h2 = "<table class='predict-table' style='border:2px solid #ffeb3b;'><tr><th>PENTA</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for i in range(7):
        h2 += f"<tr><td class='rank-label' style='background:#fbc02d !important; color:black !important;'>LINE {i+1}</td>" + "".join([f"<td>{st.session_state.pure_res[c][i]}</td>" for c in range(4)]) + "</tr>"
    st.markdown(h2 + "</table>", unsafe_allow_html=True)

    # PANEL 3
    st.divider()
    st.markdown("#### 📊 PANEL 3: PREDIKSI MURNI MESIN KEDUA (7 BARIS)")
    h3 = "<table class='predict-table'><tr><th>M-2</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for i in range(7):
        h3 += f"<tr><td class='rank-label'>BARIS {i+1}</td>" + "".join([f"<td>{st.session_state.m2_pure[c][i]}</td>" for c in range(4)]) + "</tr>"
    st.markdown(h3 + "</table>", unsafe_allow_html=True)

    # PANEL 4
    st.markdown("<div class='trash-header'>🗑️ PANEL 4: KOLEKSI ANGKA SAMPAH (BUANGAN)</div>", unsafe_allow_html=True)
    h4 = "<table class='predict-table trash-table'><tr><th>TRASH</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for i in range(5):
        h4 += f"<tr><td class='rank-label' style='background:#bf360c !important; color:white !important;'>TRASH {i+1}</td>" + "".join([f"<td>{st.session_state.trash_res[i][c]}</td>" for c in range(4)]) + "</tr>"
    st.markdown(h4 + "</table>", unsafe_allow_html=True)
