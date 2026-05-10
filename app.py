import streamlit as st
import numpy as np
from collections import Counter
import re
import random
import json
import os

# =============================================================================
# --- 1. CONFIG & STYLES ---
# =============================================================================
st.set_page_config(page_title="Master Brain v125.0: SOP Verified", layout="wide")
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .decision-table { width: 140px; margin: 0 auto; border-collapse: separate; border-spacing: 0; margin-bottom: 20px;}
    .decision-box { 
        border-radius: 20px; padding: 15px; text-align: center; 
        font-size: 85px; font-weight: 900; 
        background: radial-gradient(circle, #00ffcc, #004d40); 
        color: white !important; border: 4px solid #ffffff;
        box-shadow: 0 0 40px rgba(0, 255, 204, 0.9);
    }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 4px; margin-bottom: 25px; }
    .predict-table td { border-radius: 8px; padding: 12px; text-align: center; font-size: 28px; font-weight: 900; background: rgba(0, 210, 255, 0.15); border: 1px solid #00d2ff; color: white !important; }
    .rank-label { font-size: 13px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; width: 100px; font-weight: bold;}
    .red-ball { color: #ff1744 !important; text-shadow: 0 0 15px rgba(255, 23, 68, 0.9); background: rgba(255, 23, 68, 0.1) !important; border: 1px solid #ff1744 !important; }
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; margin-top: 25px; text-align: center; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# --- 2. ENGINE LOGIC ---
# =============================================================================
def get_advanced_logic(data_np):
    res = {"p1": [], "p2": [], "p3": []}
    for i in range(4):
        col = data_np[:, i]
        # P1: Brain (Markov)
        s1 = {n: 0.0 for n in range(10)}
        for j in range(len(col)-1):
            if col[j] == col[-1]: s1[col[j+1]] += 400.0
        # P2: Penta Sync
        s2 = {n: Counter(col)[n] * 65.0 for n in range(10)}
        for idx, v in enumerate(reversed(col[-10:])): s2[v] += (450.0 / (idx + 1))
        # P3: Deep Balance
        avg = np.mean(col)
        s3 = {n: (10.0 - abs(n - avg)) * 60.0 for n in range(10)}
        res["p1"].append(s1); res["p2"].append(s2); res["p3"].append(s3)
    return res

# =============================================================================
# --- 3. UI & EXECUTION ---
# =============================================================================
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

st.title("🛡️ MASTER BRAIN v125.0: SOP STABLE")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2 = st.columns(2)
with c1:
    btn_run = st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True)
with c2:
    st.button("🗑️ HAPUS SEMUA DATA", on_click=lambda: st.session_state.update(reset_key=st.session_state.reset_key+1), use_container_width=True)

if btn_run and input_data:
    nums = re.findall(r'\d{4}', input_data)
    if nums:
        data_np = np.array([[int(d) for d in item] for item in nums])
        engines = get_advanced_logic(data_np)
        
        # Oracle Simulator
        pool = []
        for i in range(4):
            top = sorted(engines["p1"][i].items(), key=lambda x: x[1], reverse=True)[:2]
            for n, s in top: pool.extend([n] * 20)
        while len(pool) < 40: pool.append(random.randint(0, 9))
        random.shuffle(pool)
        st.session_state.ball_ref = pool[:10]
        st.session_state.k3_rec = "0" if np.mean(data_np[:, 2]) < 5 else "9"

        def process_final(scores, bonus):
            out = []
            for c in range(4):
                scored = []
                for n in range(10):
                    # ANTI-LADDER NOISE
                    noise = random.uniform(0.001, 0.999)
                    total = scores[c][n] + (bonus if n in st.session_state.ball_ref else 0) + noise
                    scored.append((n, total))
                out.append([d for d, s in sorted(scored, key=lambda x: x[1], reverse=True)])
            return out

        st.session_state.res1 = process_final(engines["p1"], 3000)
        st.session_state.res2 = process_final(engines["p2"], 1500)
        st.session_state.res3 = process_final(engines["p3"], 800)

# =============================================================================
# --- 4. DISPLAY DASHBOARD ---
# =============================================================================
if 'res1' in st.session_state:
    st.markdown("<div class='pure-header'>🎯 REKOMENDASI TERBAIK K3</div>", unsafe_allow_html=True)
    st.markdown(f"<table class='decision-table'><tr><td class='decision-box'>{st.session_state.k3_rec}</td></tr></table>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00ffcc;'>[ 0 = KECIL | 9 = BESAR ]</p>", unsafe_allow_html=True)

    # Panel 1 (6 Baris)
    st.markdown("<div class='pure-header'>💎 PANEL 1: AI EXECUTIVE DECISION</div>", unsafe_allow_html=True)
    h1 = "<table class='predict-table'><tbody>"
    for r in range(6):
        h1 += f"<tr><td class='rank-label'>OTAK {r+1}</td>"
        for c in range(4):
            v = st.session_state.res1[c][r]
            css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h1 += f"<td {css}>{v}</td>"
        h1 += "</tr>"
    st.markdown(h1 + "</tbody></table>", unsafe_allow_html=True)
