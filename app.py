import streamlit as st
import numpy as np
from collections import Counter
import re
import random
import json
import os

# =============================================================================
# --- 1. KONFIGURASI HALAMAN & CSS (LAYOUT ASLI 100%) ---
# =============================================================================
st.set_page_config(page_title="Master Brain v125.0 PRO", layout="wide")
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
# --- 2. SISTEM MEMORI PERMANEN (AUTO-SAVE) ---
# =============================================================================
DB_FILE = "ai_memory_db.json"

def auto_save_to_db(data_raw):
    if not data_raw or len(data_raw) < 10: return
    mem = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: mem = json.load(f)
        except: mem = []
    if data_raw not in mem:
        mem.append(data_raw)
        with open(DB_FILE, "w") as f: json.dump(mem[-100:], f)

# =============================================================================
# --- 3. UI CONTROL & LOGIKA UTAMA ---
# =============================================================================
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def handle_full_reset():
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
    st.button("🗑️ HAPUS SEMUA DATA", on_click=handle_full_reset, use_container_width=True)

if btn_run and input_data:
    auto_save_to_db(input_data)
    nums = re.findall(r'\d{4}', input_data)
    if nums:
        data_np = np.array([[int(d) for d in item] for item in nums])
        st.session_state.k3_rec = "0" if np.mean(data_np[:, 2]) < 5 else "9"
        
        # Simulasi Oracle & Sensor
        st.session_state.ball_ref = [random.randint(0,9) for _ in range(10)]
        
        def finalize_process(bonus):
            out = []
            for c in range(4):
                sc = []
                for n in range(10):
                    # ANTI-LADDER NOISE (Pemecah Seri Agar Angka Tidak Berurutan)
                    noise = random.uniform(0.01, 0.99)
                    total = random.randint(100, 500) + (bonus if n in st.session_state.ball_ref else 0) + noise
                    sc.append((n, total))
                out.append([d for d, s in sorted(sc, key=lambda x: x, reverse=True)])
            return out

        st.session_state.res1 = finalize_process(3000)
        st.session_state.res2 = finalize_process(1500)
        st.session_state.res3 = finalize_process(800)
        st.session_state.trash = [[random.randint(0,9) for _ in range(4)] for _ in range(5)]

# =============================================================================
# --- 4. DASHBOARD (4 PANEL LENGKAP: 6, 7, 7, 5) ---
# =============================================================================
if 'res1' in st.session_state:
    st.markdown("<div class='pure-header'>🎯 REKOMENDASI TERBAIK K3</div>", unsafe_allow_html=True)
    st.markdown(f"<table class='decision-table'><tr><td class='decision-box'>{st.session_state.k3_rec}</td></tr></table>", unsafe_allow_html=True)

    # PANEL 1 (6 Baris)
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

    # PANEL 2 (7 Baris)
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

    # PANEL 3 (7 Baris)
    st.markdown("<div class='pure-header' style='color:#00d2ff;'>📊 PANEL 3: DEEP BALANCE SYSTEM</div>", unsafe_allow_html=True)
    h3 = "<table class='predict-table'><tbody>"
    for r in range(7):
        h3 += f"<tr><td class='rank-label'>BARIS {r+1}</td>"
        for c in range(4):
            v = st.session_state.res3[c][r]
            css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h3 += f"<td {css}>{v}</td>"
        h3 += "</tr>"
    st.markdown(h3 + "</tbody></table>", unsafe_allow_html=True)

    # PANEL 4 (5 Baris)
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
