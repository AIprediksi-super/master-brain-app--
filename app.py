import streamlit as st
import numpy as np
from collections import Counter
import re
import random
import json
import os

# =============================================================================
# --- 1. KONFIGURASI HALAMAN & CSS (LAYOUT ASLI 100% STATIS) ---
# =============================================================================
st.set_page_config(page_title="Master Brain v125.0 PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .decision-box { 
        border-radius: 20px; padding: 15px; text-align: center; 
        font-size: 85px; font-weight: 900; 
        background: radial-gradient(circle, #00ffcc, #004d40); 
        color: white !important; border: 4px solid #ffffff;
        box-shadow: 0 0 40px rgba(0, 255, 204, 0.9); margin: 0 auto; width: 140px;
    }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 4px; margin-bottom: 25px; }
    .predict-table td { border-radius: 8px; padding: 12px; text-align: center; font-size: 28px; font-weight: 900; background: rgba(0, 210, 255, 0.15); border: 1px solid #00d2ff; color: white !important; }
    .rank-label { font-size: 13px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; width: 100px; font-weight: bold; text-transform: uppercase;}
    .red-ball { color: #ff1744 !important; text-shadow: 0 0 15px rgba(255, 23, 68, 0.9); background: rgba(255, 23, 68, 0.1) !important; border: 1px solid #ff1744 !important; }
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; margin-top: 25px; text-align: center; text-transform: uppercase; }
    .trash-header { color: #ff5722; font-weight: bold; margin-top: 30px; text-shadow: 0 0 10px #ff5722; text-align: center; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# --- 2. SISTEM MEMORI PERMANEN (AUTO-SAVE) ---
# =============================================================================
DB_FILE = "ai_memory_db.json"

def auto_save_memory(raw_data):
    if not raw_data or len(raw_data) < 10: return
    current_mem = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: current_mem = json.load(f)
        except: current_mem = []
    if raw_data not in current_mem:
        current_mem.append(raw_data)
        with open(DB_FILE, "w") as f: json.dump(current_mem[-50:], f)

# =============================================================================
# --- 3. UI CONTROL & STATE ---
# =============================================================================
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def full_sop_reset():
    st.session_state.reset_key += 1
    for key in ['res1','res2','res3','trash','ball_ref','k3_vote']:
        if key in st.session_state: del st.session_state[key]
    st.rerun()

st.title("🛡️ MASTER BRAIN v125.0 PRO")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

c_bt1, c_btn2 = st.columns(2)
with c_bt1:
    btn_analisa = st.button("🚀 ANALISA + SIMPAN MEMORI AI", use_container_width=True)
with c_btn2:
    st.button("🗑️ HAPUS & RESET SEMUA DATA", on_click=full_sop_reset, use_container_width=True)

# =============================================================================
# --- 4. ENGINE EKSEKUSI (SOP VERIFIED) ---
# =============================================================================
if btn_analisa and input_data:
    auto_save_memory(input_data)
    nums = re.findall(r'\d{4}', input_data)
    if nums:
        data_np = np.array([[int(d) for d in item] for item in nums])
        
        # LOGIKA REKOMENDASI K3 (VOTING DINAMIS)
        c3_data = data_np[:, 2]
        st.session_state.k3_vote = "9" if (np.mean(c3_data[-5:]) > 4.6 or np.mean(c3_data) > 5) else "0"
        
        # SIMULATOR ORACLE (BOBOT 3500)
        st.session_state.ball_ref = [random.randint(0,9) for _ in range(10)]

        # LOGIKA PER PANEL (ANTI-TWIN)
        def finalize_sop(engine_type, bonus):
            output_cols = []
            for c in range(4):
                col = data_np[:, c]
                if engine_type == 1: # OTAK: MARKOV AI
                    scores = {n: 0.0 for n in range(10)}
                    for j in range(len(col)-1):
                        if col[j] == col[-1]: scores[col[j+1]] += 600
                elif engine_type == 2: # OTOT: PENTA L6
                    scores = {n: Counter(col)[n]*15 for n in range(10)}
                    for idx, v in enumerate(reversed(col[-8:])): scores[v] += (500/(idx+1))
                else: # JIWA: DEEP STATS
                    avg = np.mean(col)
                    scores = {n: (10-abs(n-avg))*80 for n in range(10)}

                # GABUNGKAN SKOR + NOISE (ANTI-LADDER)
                scored = []
                for n in range(10):
                    total = scores[n] + (bonus if n in st.session_state.ball_ref else 0) + random.uniform(0.1, 0.9)
                    scored.append((n, total))
                output_cols.append([d for d, s in sorted(scored, key=lambda x: x, reverse=True)])
            return output_cols

        st.session_state.res1 = finalize_sop(1, 3500)
        st.session_state.res2 = finalize_sop(2, 1800)
        st.session_state.res3 = finalize_sop(3, 1000)
        st.session_state.trash = [[random.choice([n for n in range(10) if n not in st.session_state.res1[c][:3]]) for c in range(4)] for _ in range(5)]

# =============================================================================
# --- 5. DASHBOARD DISPLAY (6, 7, 7, 5 BARIS) ---
# =============================================================================
if 'res1' in st.session_state:
    st.markdown(f"<div class='decision-box'>{st.session_state.k3_vote}</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00ffcc; font-weight:bold;'>[ VOTING REKOMENDASI TERBAIK K3 ]</p>", unsafe_allow_html=True)

    configs = [
        ("💎 PANEL 1: AI EXECUTIVE (6 BARIS)", st.session_state.res1, 6, "OTAK", "#00ffcc"),
        ("🏆 PANEL 2: PENTA-SYNC (7 BARIS)", st.session_state.res2, 7, "OTOT", "#ffeb3b"),
        ("📊 PANEL 3: DEEP STATS (7 BARIS)", st.session_state.res3, 7, "JIWA", "#00d2ff")
    ]
    
    for title, data, row_count, label, color in configs:
        st.markdown(f"<div class='pure-header' style='color:{color};'>{title}</div>", unsafe_allow_html=True)
        html = "<table class='predict-table'><tbody>"
        for r in range(row_count):
            html += f"<tr><td class='rank-label'>{label} {r+1}</td>"
            for c in range(4):
                v = data[c][r]
                css = "class='red-ball'" if v in st.session_state.ball_ref else ""
                html += f"<td {css}>{v}</td>"
            html += "</tr>"
        st.markdown(html + "</tbody></table>", unsafe_allow_html=True)

    # PANEL 4 (5 BARIS)
    st.markdown("<div class='trash-header'>🗑️ PANEL 4: KOLEKSI ANOMALI (5 BARIS)</div>", unsafe_allow_html=True)
    h4 = "<table class='predict-table' style='border:2px solid #ff5722;'><tbody>"
    for i, row in enumerate(st.session_state.trash):
        h4 += f"<tr><td class='rank-label' style='background:#bf360c !important;'>TRASH {i+1}</td>"
        for c in range(4):
            v = row[c]; css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h4 += f"<td {css}>{v}</td>"
        h4 += "</tr>"
    st.markdown(h4 + "</tbody></table>", unsafe_allow_html=True)
