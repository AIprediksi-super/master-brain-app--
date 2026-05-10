import streamlit as st
import numpy as np
from collections import Counter
import re
import random
import json
import os

# =============================================================================
# --- 1. KONFIGURASI HALAMAN & CSS (SOP VISUAL TOTAL) ---
# =============================================================================
st.set_page_config(page_title="Master Brain v125.0 PRO: Ultimate SOP", layout="wide")

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
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; margin-top: 25px; text-align: center; text-transform: uppercase; border-left: 5px solid #00ffcc; padding-left: 10px; }
    .trash-header { color: #ff5722; font-weight: bold; margin-top: 30px; text-shadow: 0 0 10px #ff5722; text-align: center; text-transform: uppercase; border-left: 5px solid #ff5722; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# --- 2. SISTEM MEMORI PERMANEN (SOP AUTO-SAVE) ---
# =============================================================================
DB_FILE = "ai_memory_db.json"

def auto_save_memory(raw_text):
    if not raw_text or len(raw_text) < 10: return
    current_mem = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: current_mem = json.load(f)
        except: current_mem = []
    if raw_text not in current_mem:
        current_mem.append(raw_text)
        with open(DB_FILE, "w") as f: json.dump(current_mem[-50:], f)

# =============================================================================
# --- 3. UI CONTROL & RESET (LAYOUT SINKRON) ---
# =============================================================================
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def handle_sop_reset():
    st.session_state.reset_key += 1
    for k in ['p1','p2','p3','trash','ball_ref','k3_vote']:
        if k in st.session_state: st.session_state.pop(k, None)
    st.rerun()

st.title("🛡️ MASTER BRAIN v125.0: SUPREME SOP")
input_data = st.text_area("Tempel Data History (4 Digit):", height=150, key=f"inp_{st.session_state.reset_key}")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    btn_analisa = st.button("🚀 JALANKAN ANALISA + SIMPAN AI", use_container_width=True)
with col_btn2:
    st.button("🗑️ HAPUS & RESET SEMUA DATA", on_click=handle_sop_reset, use_container_width=True)

# =============================================================================
# --- 4. LOGIKA MESIN (JALUR TERPISAH & EXECUTIVE CLASH) ---
# =============================================================================
if btn_analisa and input_data:
    auto_save_memory(input_data)
    nums = re.findall(r'\d{4}', input_data)
    if nums:
        data_np = np.array([[int(d) for d in item] for item in nums])
        st.session_state.ball_ref = [random.randint(0,9) for _ in range(10)]

        # --- A. PANEL 2 & 3: SENSOR DASAR ---
        p2_scores_matrix = [] # Penta Inversi
        p3_scores_matrix = [] # Deep Balance
        for i in range(4):
            col = data_np[:, i]
            # Skor P2
            s2 = {n: Counter(col)[n]*40 for n in range(10)}
            for idx, v in enumerate(reversed(col[-8:])): s2[v] += (500/(idx+1)) # Recency
            p2_scores_matrix.append(s2)
            # Skor P3
            avg = np.mean(col)
            p3_scores_matrix.append({n: (10-abs(n-avg))*70 for n in range(10)}) # Mean Gravity

        # --- B. PANEL 1: EXECUTIVE CLASH (ADU DATA P2 + P3 + MARKOV) ---
        p1_final = []
        for i in range(4):
            col = data_np[:, i]
            # Markov AI (Veto Skor)
            s_markov = {n: 0.0 for n in range(10)}
            for j in range(len(col)-1):
                if col[j] == col[-1]: s_markov[col[j+1]] += 800
            
            scored = []
            for n in range(10):
                # Penggabungan 3 Sumber: P2 + P3 + Markov + Simulator + Micro Noise
                total = p2_scores_matrix[i][n] + p3_scores_matrix[i][n] + s_markov[n]
                total += (4000 if n in st.session_state.ball_ref else 0) + random.uniform(0.1, 0.9)
                scored.append((n, total))
            # Sortir Berdasarkan Skor (ANTI-LADDER)
            p1_final.append([d for d, s in sorted(scored, key=lambda x: x[1], reverse=True)])
        st.session_state.p1 = p1_final

        # --- C. FINALISASI PANEL 2 & 3 (UNIK & TERISOLASI) ---
        def finalize_single(scores_matrix, bonus_val, noise_seed):
            out = []
            for i in range(4):
                scored = []
                for n in range(10):
                    total = scores_matrix[i][n] + (bonus_val if n in st.session_state.ball_ref else 0) + random.uniform(noise_seed, noise_seed+1)
                    scored.append((n, total))
                out.append([d for d, s in sorted(scored, key=lambda x: x[1], reverse=True)])
            return out

        st.session_state.p2 = finalize_single(p2_scores_matrix, 2000, 10.0)
        st.session_state.p3 = finalize_single(p3_scores_matrix, 1000, 20.0)

        # --- D. VOTING K3 DECISION ---
        c3 = data_np[:, 2]
        st.session_state.k3_vote = "9" if (np.mean(c3[-5:]) > 4.5 or np.mean(c3) > 5) else "0"
        
        # --- E. PANEL 4: ANOMALI ---
        st.session_state.trash = [[random.choice([n for n in range(10) if n not in st.session_state.p1[c][:3]]) for c in range(4)] for _ in range(5)]

# =============================================================================
# --- 5. DASHBOARD DISPLAY (SOP SINKRONISASI BARIS 6, 7, 7, 5) ---
# =============================================================================
if 'p1' in st.session_state:
    # REKOMENDASI TERBAIK K3
    st.markdown(f"<div class='decision-box'>{st.session_state.k3_vote}</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00ffcc; font-weight:bold;'>[ VOTING REKOMENDASI TERBAIK K3 ]</p>", unsafe_allow_html=True)

    config = [
        ("💎 PANEL 1: AI EXECUTIVE CLASH (6 BARIS)", st.session_state.p1, 6, "OTAK", "#00ffcc"),
        ("🏆 PANEL 2: PENTA-SYNC ANALYST (7 BARIS)", st.session_state.p2, 7, "OTOT", "#ffeb3b"),
        ("📊 PANEL 3: DEEP BALANCE SYSTEM (7 BARIS)", st.session_state.p3, 7, "JIWA", "#00d2ff")
    ]
    
    for title, data, rows, label, color in config:
        st.markdown(f"<div class='pure-header' style='color:{color};'>{title}</div>", unsafe_allow_html=True)
        html = "<table class='predict-table'><tbody>"
        for r in range(rows):
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
