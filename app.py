import streamlit as st
import numpy as np
from collections import Counter
import re
import random
import json
import os

# =============================================================================
# --- 1. CONFIG & STYLES (LAYOUT ASLI 100%) ---
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
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; margin-top: 25px; text-align: center; }
    .trash-header { color: #ff5722; font-weight: bold; margin-top: 30px; text-shadow: 0 0 10px #ff5722; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# --- 2. PERSISTENT AI & SENSOR ENGINES ---
# =============================================================================
DB_FILE = "ai_memory_db.json"

def auto_save(data_raw):
    if not data_raw or len(data_raw) < 10: return
    mem = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: mem = json.load(f)
        except: mem = []
    if data_raw not in mem:
        mem.append(data_raw)
        with open(DB_FILE, "w") as f: json.dump(mem[-100:], f)

def get_engine_scores(data_np):
    all_s = {"p1": [], "p2": [], "p3": []}
    for i in range(4):
        col = data_np[:, i]
        # P1: Neural (Markov)
        s1 = {n: 0.0 for n in range(10)}
        for j in range(len(col)-1):
            if col[j] == col[-1]: s1[col[j+1]] += 500.0
        # P2: Penta Sync
        s2 = {n: Counter(col)[n] * 60.0 for n in range(10)}
        for idx, v in enumerate(reversed(col[-10:])): s2[v] += (450.0 / (idx + 1))
        # P3: Deep Balance
        s3 = {n: (10.0 - abs(n - np.mean(col))) * 55.0 for n in range(10)}
        all_s["p1"].append(s1); all_s["p2"].append(s2); all_s["p3"].append(s3)
    return all_s

# =============================================================================
# --- 3. UI & STATE CONTROL ---
# =============================================================================
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def handle_reset():
    st.session_state.reset_key += 1
    for key in ['res1', 'res2', 'res3', 'trash', 'ball_ref', 'k3_rec']:
        st.session_state.pop(key, None)
    st.rerun()

st.title("🛡️ MASTER BRAIN v125.0: FINAL SOP")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2 = st.columns(2)
with c1:
    btn_run = st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True)
with c2:
    st.button("🗑️ HAPUS SEMUA DATA", on_click=handle_reset, use_container_width=True)

if btn_run and input_data:
    auto_save(input_data)
    nums = re.findall(r'\d{4}', input_data)
    if nums:
        data_np = np.array([[int(d) for d in item] for item in nums])
        engines = get_engine_scores(data_np)
        
        # Oracle Simulator Cerdas
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
                    # KUNCI UTAMA: Gabungkan skor asli mesin + bonus simulator + micro noise
                    m_noise = random.uniform(0.01, 0.99)
                    total = scores[c][n] + (bonus if n in st.session_state.ball_ref else 0) + m_noise
                    scored.append((n, total))
                # Sortir berdasarkan skor mesin (Anti-Ladder)
                out.append([d for d, s in sorted(scored, key=lambda x: x[1], reverse=True)])
            return out

        st.session_state.res1 = process_final(engines["p1"], 3000)
        st.session_state.res2 = process_final(engines["p2"], 1500)
        st.session_state.res3 = process_final(engines["p3"], 800)
        st.session_state.trash = [[random.choice([n for n in range(10) if n not in st.session_state.res1[c][:3]]) for c in range(4)] for _ in range(5)]

# =============================================================================
# --- 4. DASHBOARD (SINKRONISASI BARIS 6, 7, 7, 5) ---
# =============================================================================
if 'res1' in st.session_state:
    st.markdown("<div class='pure-header'>🎯 REKOMENDASI TERBAIK K3</div>", unsafe_allow_html=True)
    st.markdown(f"<table class='decision-table'><tr><td class='decision-box'>{st.session_state.k3_rec}</td></tr></table>", unsafe_allow_html=True)

    config = [
        ("💎 PANEL 1: AI EXECUTIVE DECISION", st.session_state.res1, 6, "OTAK", "#00ffcc"),
        ("🏆 PANEL 2: PENTA-SYNC ANALYST", st.session_state.res2, 7, "OTOT", "#ffeb3b"),
        ("📊 PANEL 3: DEEP BALANCE SYSTEM", st.session_state.res3, 7, "JIWA", "#00d2ff")
    ]
    
    for title, p_data, rows, label, color in config:
        st.markdown(f"<div class='pure-header' style='color:{color};'>{title}</div>", unsafe_allow_html=True)
        html = "<table class='predict-table'><tbody>"
        for r in range(rows):
            html += f"<tr><td class='rank-label'>{label} {r+1}</td>"
            for c in range(4):
                v = p_data[c][r]
                css = "class='red-ball'" if v in st.session_state.ball_ref else ""
                html += f"<td {css}>{v}</td>"
            html += "</tr>"
        st.markdown(html + "</tbody></table>", unsafe_allow_html=True)

    # PANEL 4 (5 BARIS)
    st.markdown("<div class='trash-header'>🗑️ PANEL 4: KOLEKSI ANOMALI</div>", unsafe_allow_html=True)
    h4 = "<table class='predict-table' style='border:2px solid #ff5722;'><tbody>"
    for i, row in enumerate(st.session_state.trash):
        h4 += f"<tr><td class='rank-label' style='background:#bf360c !important;'>TRASH {i+1}</td>"
        for c in range(4):
            v = row[c]; css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h4 += f"<td {css}>{v}</td>"
        h4 += "</tr>"
    st.markdown(h4 + "</tbody></table>", unsafe_allow_html=True)
