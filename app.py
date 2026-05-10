import streamlit as st
import numpy as np
from collections import Counter
import re
import random

# =============================================================================
# --- 1. KONFIGURASI HALAMAN (LAYOUT WIDE) ---
# =============================================================================
st.set_page_config(page_title="Master Brain v110.0 PRO", layout="wide")

# =============================================================================
# --- 2. CSS CUSTOM (STRUKTUR VISUAL ASLI 100%) ---
# =============================================================================
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 4px; margin-bottom: 25px; }
    .predict-table td { border-radius: 8px; padding: 12px; text-align: center; font-size: 28px; font-weight: 900; background: rgba(0, 210, 255, 0.15); border: 1px solid #00d2ff; color: white !important; }
    .predict-table th { background: rgba(0, 0, 0, 0.5); color: #00d2ff; padding: 10px; font-size: 16px;}
    .rank-label { font-size: 13px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; width: 100px; font-weight: bold;}
    .red-ball { color: #ff1744 !important; text-shadow: 0 0 15px rgba(255, 23, 68, 0.9); background: rgba(255, 23, 68, 0.1) !important; border: 1px solid #ff1744 !important; }
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; margin-top: 25px; }
    .trash-header { color: #ff5722; font-weight: bold; margin-top: 30px; text-shadow: 0 0 10px #ff5722; }
    .trash-table { border: 2px solid #ff5722 !important; }
    .trash-table td { background: rgba(255, 87, 34, 0.15) !important; border: 1px solid #ff5722 !important; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# --- 3. MANAJEMEN STATE & RESET ---
# =============================================================================
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    for key in ['res1','res2','res3','trash','ball_ref']:
        if key in st.session_state: st.session_state.pop(key, None)
    st.rerun()

# =============================================================================
# --- 4. ENGINE LEVEL TERTINGGI (AUTONOMOUS META-HEURISTIC) ---
# =============================================================================
def executive_engine_core(data_np):
    all_s = {"p1": [], "p2": [], "p3": []}
    for i in range(4):
        col = data_np[:, i]
        # P1: LOGIKA EVOLUSI MARKOV (Membaca Kebiasaan Transisi)
        s1 = {n: 0.0 for n in range(10)}
        last_v = col[-1]
        for j in range(len(col)-1):
            if col[j] == last_v: s1[col[j+1]] += 300
        
        # P2: LOGIKA PENTA-SYNC (Membaca Pola Kedekatan & Tren)
        s2 = {n: Counter(col)[n] * 50 for n in range(10)}
        for idx, v in enumerate(reversed(col[-10:])): s2[v] += (400 / (idx + 1))
        
        # P3: LOGIKA DEEP BALANCE (Membaca Gravitasi & Gap)
        avg = np.mean(col)
        s3 = {n: (10 - abs(n - avg)) * 50 for n in range(10)}
        for n in range(10):
            gap = 0
            for v in reversed(col):
                if v == n: break
                gap += 1
            s3[n] += (gap * 20)
            
        all_s["p1"].append(s1); all_s["p2"].append(s2); all_s["p3"].append(s3)
    return all_s

# =============================================================================
# --- 5. UI CONTROL & DISPLAY (SINKRONISASI BARIS 6, 7, 7, 5) ---
# =============================================================================
st.title("🛡️ MASTER BRAIN v110.0: EXECUTIVE ARCHITECT")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2 = st.columns(2)
with c1:
    btn_run = st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True)
with c2:
    st.button("🗑️ HAPUS SEMUA DATA", on_click=full_reset, use_container_width=True)

if btn_run:
    nums = re.findall(r'\d{4}', input_data)
    if nums:
        data_np = np.array([[int(d) for d in item] for item in nums])
        engines = executive_engine_core(data_np)
        
        # Simulator 40 Bola Referensi
        pool = []
        for i in range(4):
            top = sorted(engines["p1"][i].items(), key=lambda x: x[1], reverse=True)[:2]
            for n, s in top: pool.extend([n] * 15)
        while len(pool) < 40: pool.append(random.randint(0, 9))
        random.shuffle(pool)
        st.session_state.ball_ref = pool[:10]
        
        def process(scores, bonus):
            final = []
            for c in range(4):
                sc = [(n, scores[c][n] + (bonus if n in st.session_state.ball_ref else 0)) for n in range(10)]
                final.append([d for d, s in sorted(sc, key=lambda x: x[1], reverse=True)])
            return final

        # Eksekusi dengan Bobot Berbeda agar Angka Tidak Sama Persis
        st.session_state.res1 = process(engines["p1"], 2500)
        st.session_state.res2 = process(engines["p2"], 1500)
        st.session_state.res3 = process(engines["p3"], 800)
        
        # Panel 4: Trash (5 Baris)
        t_res = []
        for _ in range(5):
            row = []
            for c in range(4):
                used = set(st.session_state.res1[c][:3])
                pool = [n for n in range(10) if n not in used] or [random.randint(0,9)]
                row.append(random.choice(pool))
            t_res.append(row)
        st.session_state.trash = t_res

if 'res1' in st.session_state:
    # PANEL 1 (6 BARIS)
    st.markdown("<div class='pure-header'>💎 PANEL 1: EXECUTIVE PECAH KOLOM (6 BARIS)</div>", unsafe_allow_html=True)
    h1 = "<table class='predict-table'><tbody>"
    for r in range(6):
        h1 += f"<tr><td class='rank-label'>BARIS {r+1}</td>"
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
    st.markdown("<div class='pure-header' style='color:#00d2ff;'>📊 PANEL 3: DEEP STATISTICAL BRAIN (7 BARIS)</div>", unsafe_allow_html=True)
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
    h4 = "<table class='predict-table trash-table'><tbody>"
    for i, row in enumerate(st.session_state.trash):
        h4 += f"<tr><td class='rank-label' style='background:#bf360c !important;'>TRASH {i+1}</td>"
        for c in range(4):
            v = row[c]
            css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            h4 += f"<td {css}>{v}</td>"
        h4 += "</tr>"
    st.markdown(h4 + "</tbody></table>", unsafe_allow_html=True)
