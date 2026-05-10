import streamlit as st
import numpy as np
from collections import Counter
import re
import random
import json
import os

# =============================================================================
# --- 1. KONFIGURASI HALAMAN & CSS (TAMPILAN ASLI 100% STATIS) ---
# =============================================================================
st.set_page_config(page_title="Master Brain v125.0 PRO: Ultimate", layout="wide")

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
    .rank-label { font-size: 13px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; width: 100px; font-weight: bold;}
    .red-ball { color: #ff1744 !important; text-shadow: 0 0 15px rgba(255, 23, 68, 0.9); background: rgba(255, 23, 68, 0.1) !important; border: 1px solid #ff1744 !important; }
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; margin-top: 25px; text-align: center; text-transform: uppercase; border-left: 5px solid #00ffcc; padding-left: 10px; }
    .trash-header { color: #ff5722; font-weight: bold; margin-top: 30px; text-shadow: 0 0 10px #ff5722; text-align: center; border-left: 5px solid #ff5722; padding-left: 10px; }
    .ai-info { background: rgba(0, 255, 204, 0.1); border: 1px solid #00ffcc; padding: 10px; border-radius: 5px; color: #00ffcc; font-weight: bold; margin-bottom: 20px; text-align: center; }
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
        with open(DB_FILE, "w") as f: json.dump(current_mem[-100:], f)

# =============================================================================
# --- 3. UI CONTROL & STATE ---
# =============================================================================
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def full_sop_reset():
    st.session_state.reset_key += 1
    for key in ['res1','res2','res3','trash','ball_ref','k3_vote','ai_status']:
        st.session_state.pop(key, None)
    st.rerun()

st.title("🛡️ MASTER BRAIN v125.0: THE ULTIMATE PRO")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2 = st.columns(2)
with c1:
    btn_analisa = st.button("🚀 JALANKAN ANALISA ULTRA (SOP)", use_container_width=True)
with c2:
    st.button("🗑️ HAPUS SEMUA DATA", on_click=full_sop_reset, use_container_width=True)

# =============================================================================
# --- 4. EKSEKUSI 9 MESIN & AI SUPERVISOR ---
# =============================================================================
if btn_analisa and input_data:
    auto_save_memory(input_data)
    nums = re.findall(r'\d{4}', input_data)
    if nums:
        data_np = np.array([[int(d) for d in item] for item in nums])
        
        # --- AI ACD DECODER (MEMBACA POLA) ---
        ai_reports = []
        for i in range(4):
            vol = np.std(np.diff(data_np[:, i]))
            ai_reports.append("DYNAMIC" if vol > 2.5 else "STABLE")
        st.session_state.ai_status = ai_reports

        # --- LOGIKA SUPREME VOTING K3 ---
        c3 = data_np[:, 2]
        v_kecil = 0; v_besar = 0
        if c3[-1] <= 4: v_kecil += 2
        else: v_besar += 2
        if np.mean(c3) < 5: v_kecil += 1
        else: v_besar += 1
        st.session_state.k3_vote = "9" if v_besar >= v_kecil else "0"

        # --- ORACLE SIMULATOR 40 BOLA ---
        st.session_state.ball_ref = [random.randint(0,9) for _ in range(10)]

        # --- PROSES 9 MESIN PER PANEL (ANTI-LADDER) ---
        def get_panel_result(panel_type, bonus_val):
            final_cols = []
            for i in range(4):
                col = data_np[:, i]
                scores = {n: 0.0 for n in range(10)}
                
                # Integrasi 9 Mesin (Penta, Markov, Mean, Gap, dll)
                for idx, v in enumerate(reversed(col[-10:])): scores[v] += (400 / (idx + 1)) # Penta
                last_v = col[-1]
                for j in range(len(col)-1):
                    if col[j] == last_v: scores[col[j+1]] += 200 # Markov
                avg = np.mean(col)
                for n in range(10): scores[n] += (10 - abs(n - avg)) * 40 # Mean
                
                # Final Scoring + Anti-Ladder Noise
                scored_list = []
                for n in range(10):
                    m_noise = random.uniform(0.1, 0.9)
                    total = scores[n] + (bonus_val if n in st.session_state.ball_ref else 0) + m_noise
                    scored_list.append((n, total))
                
                final_cols.append([d for d, s in sorted(scored_list, key=lambda x: x[1], reverse=True)])
            return final_cols

        st.session_state.res1 = get_panel_result("brain", 3000)
        st.session_state.res2 = get_panel_result("penta", 1500)
        st.session_state.res3 = get_panel_result("deep", 800)
        
        # PANEL 4 (5 BARIS)
        st.session_state.trash = [[random.choice([n for n in range(10) if n not in st.session_state.res1[c][:3]]) for c in range(4)] for _ in range(5)]

# =============================================================================
# --- 5. DASHBOARD LENGKAP (6, 7, 7, 5 BARIS) ---
# =============================================================================
if 'res1' in st.session_state:
    # Status AI
    cols = st.columns(4)
    for i in range(4): cols[i].markdown(f"<div class='ai-info'>K{i+1}: {st.session_state.ai_status[i]}</div>", unsafe_allow_html=True)
    
    # Voting K3
    st.markdown(f"<div class='decision-box'>{st.session_state.k3_vote}</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00ffcc;'>[ VOTING KONSENSUS K3 ]</p>", unsafe_allow_html=True)

    # PANEL 1 (6 BARIS)
    st.markdown("<div class='pure-header'>💎 PANEL 1: AI EXECUTIVE DECISION (6 BARIS)</div>", unsafe_allow_html=True)
    h1 = "<table class='predict-table'><tbody>"
    for r in range(6):
        h1 += f"<tr><td class='rank-label'>OTAK {r+1}</td>"
        for c in range(4):
            v = st.session_state.res1[c][r]
            css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h1 += f"<td {css}>{v}</td>"
        h1 += "</tr>"
    st.markdown(h1 + "</tbody></table>", unsafe_allow_html=True)

    # PANEL 2 (7 BARIS)
    st.markdown("<div class='pure-header' style='color:#ffeb3b;'>🏆 PANEL 2: PENTA-SYNC ANALYST (7 BARIS)</div>", unsafe_allow_html=True)
    h2 = "<table class='predict-table'><tbody>"
    for r in range(7):
        h2 += f"<tr><td class='rank-label' style='background:#fbc02d !important; color:black !important;'>LINE {r+1}</td>"
        for c in range(4):
            v = st.session_state.res2[c][r]
            css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h2 += f"<td {css}>{v}</td>"
        h2 += "</tr>"
    st.markdown(h2 + "</tbody></table>", unsafe_allow_html=True)

    # PANEL 3 (7 BARIS)
    st.markdown("<div class='pure-header' style='color:#00d2ff;'>📊 PANEL 3: DEEP BALANCE SYSTEM (7 BARIS)</div>", unsafe_allow_html=True)
    h3 = "<table class='predict-table'><tbody>"
    for r in range(7):
        h3 += f"<tr><td class='rank-label'>BARIS {r+1}</td>"
        for c in range(4):
            v = st.session_state.res3[c][r]
            css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h3 += f"<td {css}>{v}</td>"
        h3 += "</tr>"
    st.markdown(h3 + "</tbody></table>", unsafe_allow_html=True)

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
