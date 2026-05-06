import streamlit as st
import numpy as np
from collections import Counter
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v50.0: Ultra-Precision", layout="wide")

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
    .dead-table { border: 2px solid #ff4b4b !important; }
    .dead-table td { background: rgba(255, 0, 0, 0.2) !important; border: 1px solid #ff4b4b !important; color: #ffcccc !important; }
    .dead-title-label { background: #660000 !important; color: #ff9999 !important; border: 1px solid #ff4b4b !important; }
    .odd-label { color: #ff00ff !important; border: 1px solid #ff00ff !important; }
    .even-label { color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    .small-label { color: #ffff00 !important; border: 1px solid #ffff00 !important; }
    .big-label { color: #ff6600 !important; border: 1px solid #ff6600 !important; }
    h4 { margin-top: 25px; color: #00d2ff; text-transform: uppercase; letter-spacing: 2px; border-left: 5px solid #00d2ff; padding-left: 10px; }
    .gen-box { background: rgba(0, 255, 204, 0.1); border: 2px dashed #00ffcc; border-radius: 15px; padding: 15px; text-align: center; margin-top: 10px; }
    .gen-number { font-size: 35px; font-weight: 900; color: #00ffcc; letter-spacing: 5px; text-shadow: 0 0 10px #00ffcc; display: block; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    if 'current_res' in st.session_state: del st.session_state.current_res
    st.rerun()

# --- 4. ENGINE v50.0 ULTRA-PRECISION ---
def smart_engine(data_raw):
    if not data_raw: return None
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    if len(rows) < 10: return "LOW"
    
    data_np = np.array(rows)
    final_res = []
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        recent = col[-5:]
        for idx, val in enumerate(reversed(recent)): scores[val] += (100 / (idx + 1)) 
        if len(col) >= 3:
            diff1 = col[-1] - col[-2]
            diff2 = col[-2] - col[-3]
            pred_delta = (col[-1] + ((diff1 + diff2) // 2)) % 10
            scores[pred_delta] += 45
        for n in range(10):
            gap = 0
            for val in reversed(col):
                if val == n: break
                gap += 1
            scores[n] += gap * 4.5
        freq = Counter(col)
        for n, count in freq.items(): scores[n] += count * 2.0
        scores[np.random.randint(0,10)] += np.random.uniform(5, 25)
        final_res.append([n for n, s in sorted(scores.items(), key=lambda x: x, reverse=True)])
    return final_res

# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v50.0 - ULTRA PRECISION")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    if st.button("🚀 JALANKAN ANALISA PRESISI", use_container_width=True):
        if input_data: st.session_state.current_res = smart_engine(input_data)
with c2:
    if 'current_res' in st.session_state:
        res = st.session_state.current_res
        if res != "LOW":
            # Menyiapkan teks untuk copy
            copy_text = f"PREDIKSI MASTER BRAIN\nMain: {''.join([str(res[c][0]) for c in range(4)])}\nRank 2: {''.join([str(res[c][1]) for c in range(4)])}\nMati: {''.join([str(res[c][-1]) for c in range(4)])}"
            st.copy_to_clipboard(copy_text)
            st.button("📋 COPY RINGKASAN", use_container_width=True)
with c3:
    st.button("🗑️ HAPUS DATA", on_click=full_reset, use_container_width=True)

# --- 6. DISPLAY ---
if 'current_res' in st.session_state and st.session_state.current_res:
    res = st.session_state.current_res
    if res == "LOW":
        st.error("Data kurang! Gunakan minimal 15-20 baris.")
    else:
        st.markdown("#### 📊 ANALISA UTAMA")
        main_h = "<table class='predict-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
        for r in range(6):
            main_h += f"<tr><td class='rank-label'>RANK {r+1}</td>" + "".join([f"<td>{res[c][r]}</td>" for c in range(4)]) + "</tr>"
        st.markdown(main_h + "</table>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🌸 KHUSUS GANJIL")
            odd_res = [[n for n in col if n % 2 != 0] for col in res]
            hg = "<table class='predict-table'>"
            for r in range(4): hg += f"<tr><td class='rank-label odd-label'>ODD {r+1}</td>" + "".join([f"<td>{odd_res[c][r] if r < len(odd_res[c]) else '-'}</td>" for c in range(4)]) + "</tr>"
            st.markdown(hg + "</table>", unsafe_allow_html=True)
            st.markdown("#### ⚡ KHUSUS KECIL (0-4)")
            s_res = [[n for n in col if n <= 4] for col in res]
            hs = "<table class='predict-table'>"
            for r in range(4): hs += f"<tr><td class='rank-label small-label'>SMALL {r+1}</td>" + "".join([f"<td>{s_res[c][r] if r < len(s_res[c]) else '-'}</td>" for c in range(4)]) + "</tr>"
            st.markdown(hs + "</table>", unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🍀 KHUSUS GENAP")
            even_res = [[n for n in col if n % 2 == 0] for col in res]
            he = "<table class='predict-table'>"
            for r in range(4): he += f"<tr><td class='rank-label even-label'>EVEN {r+1}</td>" + "".join([f"<td>{even_res[c][r] if r < len(even_res[c]) else '-'}</td>" for c in range(4)]) + "</tr>"
            st.markdown(he + "</table>", unsafe_allow_html=True)
            st.markdown("#### 🌋 KHUSUS BESAR (5-9)")
            b_res = [[n for n in col if n >= 5] for col in res]
            hb = "<table class='predict-table'>"
            for r in range(4): hb += f"<tr><td class='rank-label big-label'>BIG {r+1}</td>" + "".join([f"<td>{b_res[c][r] if r < len(b_res[c]) else '-'}</td>" for c in range(4)]) + "</tr>"
            st.markdown(hb + "</table>", unsafe_allow_html=True)

        st.markdown("#### 🎯 GENERATOR 4D")
        g1, g2, g3, g4 = st.columns(4)
        def get_v(l, c): return str(l[c][0]) if l[c] else "?"
        
        with g1:
            num = "".join([str(res[c][0]) for c in range(4)])
            st.markdown(f"<div class='gen-box'>Main Mix<br><span class='gen-number'>{num}</span></div>", unsafe_allow_html=True)
            if st.button("Salin Main", key="c1"): st.copy_to_clipboard(num)
        with g2:
            num = "".join([str(odd_res[c][0]) if odd_res[c] else "?" for c in range(4)])
            st.markdown(f"<div class='gen-box'>Odd Power<br><span class='gen-number'>{num}</span></div>", unsafe_allow_html=True)
            if st.button("Salin Ganjil", key="c2"): st.copy_to_clipboard(num)
        with g3:
            num = "".join([str(even_res[c][0]) if even_res[c] else "?" for c in range(4)])
            st.markdown(f"<div class='gen-box'>Even Power<br><span class='gen-number'>{num}</span></div>", unsafe_allow_html=True)
            if st.button("Salin Genap", key="c3"): st.copy_to_clipboard(num)
        with g4:
            num = f"{s_res[0][0]}{b_res[1][0]}{s_res[2][0]}{b_res[3][0]}"
            st.markdown(f"<div class='gen-box'>Mix S/B<br><span class='gen-number'>{num}</span></div>", unsafe_allow_html=True)
            if st.button("Salin Mix", key="c4"): st.copy_to_clipboard(num)

        st.divider()
        st.markdown("<h4 class='dead-header'>🚫 TABEL ANGKA MATI</h4>", unsafe_allow_html=True)
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.markdown("##### 💀 MATI TOTAL")
            hd = "<table class='predict-table dead-table'>"
            for r in range(1, 3): hd += f"<tr><td class='rank-label dead-title-label'>DEAD {r}</td>" + "".join([f"<td>{res[c][-r]}</td>" for c in range(4)]) + "</tr>"
            st.markdown(hd + "</table>", unsafe_allow_html=True)
        with d_col2:
            st.markdown("##### 💀 MATI KOMBINASI")
            hdgg = "<table class='predict-table dead-table'>"
            hdgg += f"<tr><td class='rank-label dead-title-label'>D-ODD</td>" + "".join([f"<td>{odd_res[c][-1] if odd_res[c] else '-'}</td>" for c in range(4)]) + "</tr>"
            hdgg += f"<tr><td class='rank-label dead-title-label'>D-EVEN</td>" + "".join([f"<td>{even_res[c][-1] if even_res[c] else '-'}</td>" for c in range(4)]) + "</tr>"
            st.markdown(hdgg + "</table>", unsafe_allow_html=True)
