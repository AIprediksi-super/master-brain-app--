import streamlit as st
import numpy as np
from collections import Counter
import re
import random
import json
import os

# =============================================================================
# --- 1. CONFIG & PREMIUM CSS ---
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
# --- 2. PERSISTENT AI & LOGIC ---
# =============================================================================
DB_FILE = "ai_memory_db.json"

def auto_save_logic(raw_text):
    if not raw_text or len(raw_text) < 10: return
    mem = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: mem = json.load(f)
        except: mem = []
    if raw_text not in mem:
        mem.append(raw_text)
        with open(DB_FILE, "w") as f: json.dump(mem[-100:], f)

def get_k3_recommendation(data_np):
    # Logika K3: Membaca rata-rata dan probabilitas inversi
    k3_data = data_np[:, 2]
    return "0" if np.mean(k3_data) < 5 else "9"

# =============================================================================
# --- 3. UI & STATE CONTROL ---
# =============================================================================
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def handle_reset():
    st.session_state.reset_key += 1
    for key in ['res1','res2','res3','trash','ball_ref','k3_rec']:
        st.session_state.pop(key, None)
    st.rerun()

st.title("🛡️ MASTER BRAIN v125.0 PRO")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2 = st.columns(2)
with c1:
    btn_run = st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True)
with c2:
    st.button("🗑️ HAPUS SEMUA DATA", on_click=handle_reset, use_container_width=True)

if btn_run and input_data:
    auto_save_logic(input_data)
    nums = re.findall(r'\d{4}', input_data)
    if nums:
        data_np = np.array([[int(d) for d in item] for item in nums])
        st.session_state.k3_rec = get_k3_recommendation(data_np)
        
        # Simulasi Oracle & Mesin (Hierarki Berbeda)
        st.session_state.ball_ref = [random.randint(0,9) for _ in range(10)]
        
        def finalize(offset, bonus):
            res = []
            for c in range(4):
                sc = [(n, random.randint(100, 500) + (bonus if n in st.session_state.ball_ref else 0)) for n in range(10)]
                res.append([d for d, s in sorted(sc, key=lambda x: x, reverse=True)])
            return res

        st.session_state.res1 = finalize(0, 3000)
        st.session_state.res2 = finalize(1, 1500)
        st.session_state.res3 = finalize(2, 800)
        st.session_state.trash = [[random.randint(0,9) for _ in range(4)] for _ in range(5)]

# =============================================================================
# --- 4. OUTPUT DASHBOARD ---
# =============================================================================
if 'k3_rec' in st.session_state:
    st.markdown("<div class='pure-header'>🎯 REKOMENDASI TERBAIK K3 (KOLOM 3)</div>", unsafe_allow_html=True)
    st.markdown(f"<table class='decision-table'><tr><td class='decision-box'>{st.session_state.k3_rec}</td></tr></table>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00ffcc;'>[ 0 = KECIL (0-4) | 9 = BESAR (5-9) ]</p>", unsafe_allow_html=True)

    # PANEL 1 (6 BARIS)
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

    # PANEL 2 (7 BARIS)
    st.markdown("<div class='pure-header' style='color:#ffeb3b;'>🏆 PANEL 2: PENTA-SYNC ANALYST</div>", unsafe_allow_html=True)
    h2 = "<table class='predict-table'><tbody>"
    for r in range(7):
        h2 += f"<tr><td class='rank-label' style='background:#fbc02d !important; color:black !important;'>LINE {r+1}</td>"
        for c in range(4):
            v = st.session_state.res2[c][r]
            css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h2 += f"<td {css}>{v}</td>"
        h2 += "</tr>"
    st.markdown(h2 + "</tbody></table>", unsafe_allow_html=True)

    # PANEL 4 (5 BARIS)
    st.markdown("<div class='trash-header'>🗑️ PANEL 4: KOLEKSI ANOMALI</div>", unsafe_allow_html=True)
    h4 = "<table class='predict-table' style='border:2px solid #ff5722;'><tbody>"
    for i, row in enumerate(st.session_state.trash):
        h4 += f"<tr><td class='rank-label' style='background:#bf360c !important;'>TRASH {i+1}</td>"
        for c in range(4):
            v = row[c]
            css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h4 += f"<td {css}>{v}</td>"
        h4 += "</tr>"
    st.markdown(h4 + "</tbody></table>", unsafe_allow_html=True)
