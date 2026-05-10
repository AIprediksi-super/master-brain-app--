import streamlit as st
import numpy as np
from collections import Counter
import re
import random

# =============================================================================
# --- 1. KONFIGURASI HALAMAN ---
# =============================================================================
st.set_page_config(page_title="Master Brain v99.0 Final Architect", layout="wide")

# CSS ASLI (Sesuai Struktur Anda)
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
# --- 2. SEMBILAN MESIN ANALISA (DISTRIBUSI PANEL) ---
# =============================================================================
def run_full_matrix(data_np):
    results = {"p1": [], "p2": [], "p3": []}
    for i in range(4):
        col = data_np[:, i]
        
        # LOGIKA PANEL 1: OTAK (Markov + Entropy + Mean)
        s1 = {n: (10 - abs(n - np.mean(col))) * 25 for n in range(10)}
        last_v = col[-1]
        for j in range(len(col)-1):
            if col[j] == last_v: s1[col[j+1]] += 150
            
        # LOGIKA PANEL 2: OTOT (Penta + Modus + Regresi)
        s2 = {n: Counter(col)[n] * 45 for n in range(10)}
        for idx, v in enumerate(reversed(col[-7:])): s2[v] += (280 / (idx + 1))
        
        # LOGIKA PANEL 3: JIWA (Gap + Fibonacci + Golden Ratio)
        s3 = {n: 0.0 for n in range(10)}
        for n in range(10):
            gap = 0
            for v in reversed(col):
                if v == n: break
                gap += 1
            s3[n] += (gap * 18)
        fib = [1, 2, 3, 5, 8]
        for f in fib: s3[(col[-1] + f) % 10] += 120
        
        results["p1"].append(s1); results["p2"].append(s2); results["p3"].append(s3)
    return results

# =============================================================================
# --- 3. DYNAMIC SIMULATOR (ADAPTIF 40 BOLA) ---
# =============================================================================
def smart_simulator(engines):
    pool = []
    for i in range(4):
        top_2 = sorted(engines["p1"][i].items(), key=lambda x: x[1], reverse=True)[:2]
        for n, s in top_2: pool.extend([n] * 5)
    while len(pool) < 40: pool.append(random.randint(0, 9))
    random.shuffle(pool)
    return pool[:10]

# =============================================================================
# --- 4. UI & PROSES EKSEKUSI ---
# =============================================================================
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

st.title("🛡️ MASTER BRAIN v99.0 FINAL ARCHITECT")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

if st.button("🚀 EKSEKUSI ANALISA TOTAL (9 MESIN)", use_container_width=True):
    nums = re.findall(r'\d{4}', input_data)
    if nums:
        data_np = np.array([[int(d) for d in item] for item in nums])
        engines = run_full_matrix(data_np)
        st.session_state.ball_ref = smart_simulator(engines)
        
        def process(scores, bonus):
            final = []
            for c in range(4):
                scored = [(n, scores[c][n] + (bonus if n in st.session_state.ball_ref else 0)) for n in range(10)]
                final.append([d for d, s in sorted(scored, key=lambda x: x[1], reverse=True)])
            return final

        st.session_state.res1 = process(engines["p1"], 800)
        st.session_state.res2 = process(engines["p2"], 500)
        st.session_state.res3 = process(engines["p3"], 300)
        
        # PANEL 4: ADVANCED TRASH (Mencari sisa yang diabaikan mesin utama)
        t_res = []
        for r in range(5):
            row = []
            for c in range(4):
                used = set(st.session_state.res1[c][:3] + st.session_state.res2[c][:3])
                pool = [n for n in range(10) if n not in used] or [random.randint(0,9)]
                row.append(random.choice(pool))
            t_res.append(row)
        st.session_state.trash = t_res

# =============================================================================
# --- 5. DASHBOARD PANEL ---
# =============================================================================
if 'res1' in st.session_state:
    panels = [
        ("PANEL 1: OTAK (NEURAL LOGIC)", st.session_state.res1, "#00ffcc", "OTAK"),
        ("PANEL 2: OTOT (TREND & MOMENTUM)", st.session_state.res2, "#ffeb3b", "OTOT"),
        ("PANEL 3: JIWA (STATISTICAL BALANCE)", st.session_state.res3, "#00d2ff", "JIWA")
    ]
    
    for title, p_data, color, label in panels:
        st.markdown(f"<div class='pure-header' style='color:{color};'>{title}</div>", unsafe_allow_html=True)
        html = "<table class='predict-table'><tbody>"
        for r in range(6):
            html += f"<tr><td class='rank-label'>{label} {r+1}</td>"
            for c in range(4):
                v = p_data[c][r]
                css = "class='red-ball'" if v in st.session_state.ball_ref else ""
                html += f"<td {css}>{v}</td>"
            html += "</tr>"
        st.markdown(html + "</tbody></table>", unsafe_allow_html=True)

    # PANEL 4 (STAY BETTER)
    st.markdown("<div class='trash-header'>🗑️ PANEL 4: KOLEKSI ANOMALI (ZONA UNPREDICTED)</div>", unsafe_allow_html=True)
    html4 = "<table class='predict-table trash-table'><tbody>"
    for i, row in enumerate(st.session_state.trash):
        html4 += f"<tr><td class='rank-label' style='background:#bf360c !important;'>TRASH {i+1}</td>"
        for c in range(4):
            v = row[c]
            css = "class='red-ball'" if v in st.session_state.ball_ref else ""
            html4 += f"<td {css}>{v}</td>"
        html4 += "</tr>"
    st.markdown(html4 + "</tbody></table>", unsafe_allow_html=True)
    st.info("🔴 Angka Merah: Sinkronisasi Dynamic Simulator 40 Bola.")
