import streamlit as st
import numpy as np
from collections import Counter
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v32.0: Ultimate Logic", layout="wide")

# --- 2. CSS CUSTOM ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 4px; margin-bottom: 20px; }
    .predict-table td { 
        border-radius: 8px; padding: 12px; text-align: center; font-size: 28px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.2); border: 1px solid #00d2ff; color: white !important; 
    }
    .rank-label { font-size: 14px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; width: 90px; }
    .odd-label { color: #ff00ff !important; border: 1px solid #ff00ff !important; }
    .even-label { color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    .small-label { color: #ffff00 !important; border: 1px solid #ffff00 !important; }
    .big-label { color: #ff6600 !important; border: 1px solid #ff6600 !important; }
    .dead-row { background: rgba(255, 0, 0, 0.5) !important; border: 2px solid red !important; }
    h4 { margin-top: 25px; color: #00d2ff; text-transform: uppercase; letter-spacing: 2px; border-left: 5px solid #00d2ff; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    if 'current_res' in st.session_state: del st.session_state.current_res
    st.rerun()

# --- 4. ENGINE V32.0 ---
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
        for idx, val in enumerate(reversed(col)):
            scores[val] += 100 / (idx + 1)
        for n in range(10):
            last_seen = -1
            for idx, val in enumerate(reversed(col)):
                if val == n: last_seen = idx; break
            scores[n] += last_seen * 2 if last_seen != -1 else 50
            scores[n] += np.random.uniform(0, 2)
        final_res.append([n for n, s in sorted(scores.items(), key=lambda x: x[1], reverse=True)])
    return final_res

# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v32.0 - ULTIMATE")
input_data = st.text_area("Tempel Data History Di Sini:", height=150, key=f"inp_{st.session_state.reset_key}")

c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 JALANKAN ANALISA ULTIMATE", use_container_width=True):
        if input_data: st.session_state.current_res = smart_engine(input_data)
with c2:
    st.button("🗑️ HAPUS SEMUA DATA", on_click=full_reset, use_container_width=True)

# --- 6. DISPLAY ---
if 'current_res' in st.session_state and st.session_state.current_res:
    res = st.session_state.current_res
    if res == "LOW":
        st.error("Data kurang! Masukkan minimal 10 baris.")
    else:
        # TABEL UTAMA
        st.markdown("#### 📊 HASIL ANALISA UTAMA")
        h = "<table class='predict-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
        for r in range(8):
            h += f"<tr><td class='rank-label'>R{r+1}</td>" + "".join([f"<td>{res[c][r]}</td>" for c in range(4)]) + "</tr>"
        st.markdown(h + "</table>", unsafe_allow_html=True)

        # BARIS KEDUA: GANJIL & GENAP
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🌸 KHUSUS GANJIL")
            odd_res = [[n for n in col if n % 2 != 0] for col in res]
            hg = "<table class='predict-table'>"
            for r in range(4):
                hg += f"<tr><td class='rank-label odd-label'>ODD-{r+1}</td>" + "".join([f"<td>{odd_res[c][r]}</td>" for c in range(4)]) + "</tr>"
            st.markdown(hg + "</table>", unsafe_allow_html=True)
        with col2:
            st.markdown("#### 🍀 KHUSUS GENAP")
            even_res = [[n for n in col if n % 2 == 0] for col in res]
            he = "<table class='predict-table'>"
            for r in range(4):
                he += f"<tr><td class='rank-label even-label'>EVEN-{r+1}</td>" + "".join([f"<td>{even_res[c][r]}</td>" for c in range(4)]) + "</tr>"
            st.markdown(he + "</table>", unsafe_allow_html=True)

        # BARIS KETIGA: KECIL & BESAR
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### ⚡ KHUSUS KECIL (0-4)")
            small_res = [[n for n in col if n <= 4] for col in res]
            hs = "<table class='predict-table'>"
            for r in range(4):
                hs += f"<tr><td class='rank-label small-label'>SMALL-{r+1}</td>" + "".join([f"<td>{small_res[c][r]}</td>" for c in range(4)]) + "</tr>"
            st.markdown(hs + "</table>", unsafe_allow_html=True)
        with col4:
            st.markdown("#### 🌋 KHUSUS BESAR (5-9)")
            big_res = [[n for n in col if n >= 5] for col in res]
            hb = "<table class='predict-table'>"
            for r in range(4):
                hb += f"<tr><td class='rank-label big-label'>BIG-{r+1}</td>" + "".join([f"<td>{big_res[c][r]}</td>" for c in range(4)]) + "</tr>"
            st.markdown(hb + "</table>", unsafe_allow_html=True)
