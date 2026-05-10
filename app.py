import streamlit as st
import numpy as np
from collections import Counter
import re
import random

# =============================================================================
# --- 1. KONFIGURASI HALAMAN ---
# =============================================================================
st.set_page_config(page_title="Master Brain v75.0 PRO: Penta-Pure", layout="wide")

# =============================================================================
# --- 2. CSS CUSTOM (VISUAL DASHBOARD) ---
# =============================================================================
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 4px; margin-bottom: 25px; }
    .predict-table td, .predict-table th { 
        border-radius: 8px; padding: 12px; text-align: center; font-size: 28px; 
        font-weight: 900; background: rgba(0, 210, 255, 0.15); border: 1px solid #00d2ff; color: white !important; 
    }
    .rank-label { font-size: 13px !important; background: rgba(0,0,0,0.8) !important; color: #00ffcc !important; width: 100px; }
    .pure-table { border: 2px solid #00ffcc !important; box-shadow: 0 0 15px rgba(0,255,204,0.3); }
    .trash-table { border: 2px solid #ff5722 !important; }
    .trash-table td { background: rgba(255, 87, 34, 0.15) !important; border: 1px solid #ff5722 !important; }
    .pure-header { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-weight: bold; margin-bottom: 10px; }
    .m1-header { color: #ffeb3b; text-shadow: 0 0 10px #ffeb3b; font-weight: bold; margin-top: 20px; }
    .trash-header { color: #ff5722; font-weight: bold; margin-top: 30px; text-shadow: 0 0 10px #ff5722; }
    h4 { margin-top: 25px; color: #00d2ff; text-transform: uppercase; letter-spacing: 2px; border-left: 5px solid #00d2ff; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'reset_key' not in st.session_state: st.session_state.reset_key = 0
def full_reset():
    st.session_state.reset_key += 1
    for key in ['current_res', 'pure_res', 'm2_pure', 'trash_res']:
        if key in st.session_state: del st.session_state[key]
    st.rerun()

# =============================================================================
# --- 3. MESIN PERTAMA: PENTA-SYNC (SEKARANG DENGAN L6) ---
# =============================================================================
def smart_engine_pure_penta(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_scores_list = []
    
    # Map Indeks (L2/L5) & Map Inversi (L6)
    idx_map = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}
    map_inv = {3:8, 0:5, 4:9, 2:7, 7:2, 8:3, 6:1, 5:0, 1:6, 9:4}
    
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        
        # L1: Velocity Momentum (280)
        for idx, val in enumerate(reversed(col[-7:])):
            scores[val] += (280 / ((idx + 1) ** 1.1))
            
        # L2 & L5: Mirror (130)
        last_val = col[-1]
        scores[idx_map[last_val]] += 130.0 
        
        # L3: Matrix Cross (65)
        if i > 0: scores[data_np[-1, i-1]] += 65.0
            
        # L4: Frequency Void (155)
        counts_15 = Counter(col[-15:])
        for n in range(10):
            if n not in counts_15: scores[n] += 155.0
            
        # --- L6: INVERSI PAKET SEIMBANG (160) ---
        inv_target = map_inv.get(last_val, last_val)
        scores[inv_target] += 160.0
        
        # Anti-Noise Filter (-40)
        scores[(last_val + 1) % 10] -= 40.0
        scores[(last_val - 1) % 10] -= 40.0
        
        final_scores_list.append(scores)
    return final_scores_list

# =============================================================================
# --- 4. MESIN KEDUA: DEEP ANALYSIS (GAP LOGIC) ---
# =============================================================================
def smart_engine_deep(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_scores_list = []
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        freq_counter = Counter(col)
        for idx, val in enumerate(reversed(col[-15:])):
            scores[val] += (220 / ((idx + 1.2) ** 0.8))
        for n in range(10):
            gap = 0
            for v in reversed(col):
                if v == n: break
                gap += 1
            scores[n] += (gap * 8.5) * (1 + (freq_counter[n] / len(rows)))
        final_scores_list.append(scores)
    return final_scores_list

# =============================================================================
# --- 5. PROSES ANALISA & UI ---
# =============================================================================
st.title("🛡️ MASTER BRAIN v75.0 PRO")
input_data_raw = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True):
        if input_data_raw:
            s1 = smart_engine_pure_penta(input_data_raw)
            s2 = smart_engine_deep(input_data_raw)
            
            # Data Panel 2 (Murni Mesin 1)
            p2 = [[n for n, s in sorted(s1[c].items(), key=lambda x: x[1], reverse=True)] for c in range(4)]
            st.session_state.pure_res = p2
            
            # Data Panel 3 (Murni Mesin 2)
            p3 = [[n for n, s in sorted(s2[c].items(), key=lambda x: x[1], reverse=True)] for c in range(4)]
            st.session_state.m2_pure = p3
            
            # Panel 1: Hasil Campuran (Gabungan Skor S1 + S2)
            k10 = [[p3[c][r] for c in range(4)] for r in range(10)]
            b_final = sorted([(b, sum(s1[c][b[c]] + s2[c][b[c]] for c in range(4))) for b in k10], key=lambda x: x[1], reverse=True)
            st.session_state.current_res = [x[0] for x in b_final[:6]]
            
            # Panel 4: Trash Zone
            t_res = []
            for _ in range(5):
                row = []
                for c in range(4):
                    used = set(p2[c][:7] + p3[c][:7])
                    pool = [n for n in range(10) if n not in used] or list(range(10))
                    row.append(random.choice(pool))
                t_res.append(row)
            st.session_state.trash_res = t_res

with col_btn2: st.button("🗑️ HAPUS DATA", on_click=full_reset, use_container_width=True)

# =============================================================================
# --- 6. DISPLAY DASHBOARD ---
# =============================================================================
if 'current_res' in st.session_state:
    st.markdown("<div class='pure-header'>💎 PANEL 1: HASIL CAMPURAN (SARINGAN 10➔6)</div>", unsafe_allow_html=True)
    h1 = "<table class='predict-table pure-table'><tr><th>FINAL</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for i, row in enumerate(st.session_state.current_res):
        h1 += f"<tr><td class='rank-label' style='background:#004d40 !important;'>BARIS {i+1}</td>" + "".join(f"<td>{d}</td>" for d in row) + "</tr>"
    st.markdown(h1 + "</table>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div class='m1-header'>🏆 PANEL 2: PREDIKSI MURNI MESIN PERTAMA (7 BARIS)</div>", unsafe_allow_html=True)
    h2 = "<table class='predict-table' style='border:2px solid #ffeb3b;'><tr><th>PENTA</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for r in range(7):
        h2 += f"<tr><td class='rank-label' style='background:#fbc02d !important; color:black !important;'>LINE {r+1}</td>" + "".join(f"<td>{st.session_state.pure_res[c][r]}</td>" for c in range(4)) + "</tr>"
    st.markdown(h2 + "</table>", unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 📊 PANEL 3: PREDIKSI MURNI MESIN KEDUA (7 BARIS)")
    h3 = "<table class='predict-table'><tr><th>M-2</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for r in range(7):
        h3 += f"<tr><td class='rank-label'>BARIS {r+1}</td>" + "".join(f"<td>{st.session_state.m2_pure[c][r]}</td>" for c in range(4)) + "</tr>"
    st.markdown(h3 + "</table>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div class='trash-header'>🗑️ PANEL 4: KOLEKSI ANGKA SAMPAH (BUANGAN)</div>", unsafe_allow_html=True)
    h4 = "<table class='predict-table trash-table'><tr><th>TRASH</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for i, row in enumerate(st.session_state.trash_res):
        h4 += f"<tr><td class='rank-label' style='background:#bf360c !important;'>TRASH {i+1}</td>" + "".join(f"<td>{d}</td>" for d in row) + "</tr>"
    st.markdown(h4 + "</table>", unsafe_allow_html=True)

    st.caption("⚙️ Status: Penta-Sync L6 Terintegrasi | Prioritas Mundur K4 ➔ K1")
