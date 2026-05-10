import streamlit as st
import numpy as np
from collections import Counter
import re
import random

# =============================================================================
# --- 1. KONFIGURASI HALAMAN (LAYOUT WIDE) ---
# =============================================================================
st.set_page_config(page_title="Master Brain v75.0 PRO: Penta-Pure", layout="wide")

# =============================================================================
# --- 2. CSS CUSTOM (GAYA VISUAL DASHBOARD LENGKAP) ---
# =============================================================================
st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(to bottom, #000428, #004e92); 
        color: #E0F7FA; 
    }
    .predict-table { 
        width: 100%; 
        border-collapse: separate; 
        border-spacing: 4px; 
        margin-bottom: 25px; 
    }
    .predict-table td { 
        border-radius: 8px; 
        padding: 12px; 
        text-align: center; 
        font-size: 28px; 
        font-weight: 900; 
        background: rgba(0, 210, 255, 0.15); 
        border: 1px solid #00d2ff; 
        color: white !important; 
    }
    .predict-table th { 
        background: rgba(0, 0, 0, 0.5); 
        color: #00d2ff; 
        padding: 10px; 
    }
    .rank-label { 
        font-size: 13px !important; 
        background: rgba(0,0,0,0.8) !important; 
        color: #00ffcc !important; 
        width: 100px; 
        font-weight: bold;
    }
    /* HIGHLIGHT ANGKA MERAH SIMULATOR */
    .red-ball { 
        color: #ff1744 !important; 
        text-shadow: 0 0 15px rgba(255, 23, 68, 0.9); 
        background: rgba(255, 23, 68, 0.1) !important;
        border: 1px solid #ff1744 !important;
    }
    .pure-table { 
        border: 2px solid #00ffcc !important; 
        box-shadow: 0 0 15px rgba(0,255,204,0.3); 
    }
    .pure-table td { 
        background: rgba(0, 255, 204, 0.1) !important; 
        border: 1px solid #00ffcc !important; 
    }
    .trash-table { 
        border: 2px solid #ff5722 !important; 
    }
    .trash-table td { 
        background: rgba(255, 87, 34, 0.15) !important; 
        border: 1px solid #ff5722 !important; 
    }
    .pure-header { 
        color: #00ffcc; 
        text-shadow: 0 0 10px #00ffcc; 
        font-weight: bold; 
        margin-bottom: 10px; 
    }
    .m1-header { 
        color: #ffeb3b; 
        text-shadow: 0 0 10px #ffeb3b; 
        font-weight: bold; 
        margin-top: 20px; 
    }
    .trash-header { 
        color: #ff5722; 
        font-weight: bold; 
        margin-top: 30px; 
        text-shadow: 0 0 10px #ff5722; 
    }
    h4 { 
        margin-top: 25px; 
        color: #00d2ff; 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        border-left: 5px solid #00d2ff; 
        padding-left: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# --- 3. MANAJEMEN STATE & RESET ---
# =============================================================================
if 'reset_key' not in st.session_state: 
    st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    if 'current_res' in st.session_state: del st.session_state.current_res
    if 'pure_res' in st.session_state: del st.session_state.pure_res
    if 'm2_pure' in st.session_state: del st.session_state.m2_pure
    if 'trash_res' in st.session_state: del st.session_state.trash_res
    if 'ball_ref' in st.session_state: del st.session_state.ball_ref
    st.rerun()

# =============================================================================
# --- 4. MESIN PERTAMA (PENTA-SYNC + L6 INTEGRATED) ---
# =============================================================================
def smart_engine_pure_penta(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_scores_list = []
    
    # Map Indeks (Mirror) & Map Inversi (L6)
    idx_map = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}
    map_inv = {3:8, 0:5, 4:9, 2:7, 7:2, 8:3, 6:1, 5:0, 1:6, 9:4}
    
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        
        # L1: Momentum (280)
        for idx, val in enumerate(reversed(col[-7:])):
            scores[val] += (280 / ((idx + 1) ** 1.1))
            
        # L2: Mirror (130)
        last_val = col[-1]
        scores[idx_map[last_val]] += 130.0 
        
        # L3: Matrix Cross (65)
        if i > 0:
            scores[data_np[-1, i-1]] += 65.0
            
        # L4: Void Sync (155)
        counts_15 = Counter(col[-15:])
        for n in range(10):
            if n not in counts_15:
                scores[n] += 155.0
                
        # --- L6: INVERSI PAKET (95% LOCK) ---
        inv_target = map_inv.get(last_val, last_val)
        scores[inv_target] += 160.0 # Bobot seimbang
        
        # Anti-Noise
        scores[(last_val + 1) % 10] -= 40.0
        scores[(last_val - 1) % 10] -= 40.0
        
        final_scores_list.append(scores)
    return final_scores_list

# =============================================================================
# --- 5. MESIN KEDUA (DEEP ANALYSIS GAP) ---
# =============================================================================
def smart_engine_deep(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_scores_list = []
    total_len = len(rows)
    
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        freq = Counter(col)
        for idx, val in enumerate(reversed(col[-15:])):
            scores[val] += (220 / ((idx + 1.2) ** 0.8))
        for n in range(10):
            gap = 0
            for v in reversed(col):
                if v == n: break
                gap += 1
            scores[n] += (gap * 8.5) * (1 + (freq[n] / total_len))
        final_scores_list.append(scores)
    return final_scores_list

# =============================================================================
# --- 6. ORACLE SIMULATOR (40 BOLA REFERENCE) ---
# =============================================================================
def get_oracle_reference():
    tabung = list(range(10)) * 4
    random.shuffle(tabung)
    bola_ref = []
    for _ in range(10):
        if tabung:
            bola_ref.append(tabung.pop(random.randrange(len(tabung))))
    return bola_ref

# =============================================================================
# --- 7. UI CONTROL & ANALISA ---
# =============================================================================
st.title("🛡️ MASTER BRAIN v75.0 PRO")
input_data = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

c_btn1, c_btn2 = st.columns(2)
with c_btn1:
    if st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True):
        if input_data:
            # Jalankan Mesin
            s1 = smart_engine_pure_penta(input_data)
            s2 = smart_engine_deep(input_data)
            # Jalankan Oracle
            st.session_state.ball_ref = get_oracle_reference()
            
            # Panel 2 Data
            p2_data = []
            for c in range(4):
                sorted_n = [n for n, s in sorted(s1[c].items(), key=lambda x: x[1], reverse=True)]
                p2_data.append(sorted_n)
            st.session_state.pure_res = p2_data
            
            # Panel 3 Data
            p3_data = []
            for c in range(4):
                sorted_n = [n for n, s in sorted(s2[c].items(), key=lambda x: x[1], reverse=True)]
                p3_data.append(sorted_n)
            st.session_state.m2_pure = p3_data
            
            # Panel 1: Saringan 10 ke 6
            k10 = [[p3_data[c][r] for c in range(4)] for r in range(10)]
            b_weighted = []
            for b in k10:
                # Rumus Pengolah Panel 1 (S1 + S2)
                score = sum(s1[c][b[c]] + s2[c][b[c]] for c in range(4))
                b_weighted.append((b, score))
            st.session_state.current_res = [x[0] for x in sorted(b_weighted, key=lambda x: x[1], reverse=True)[:6]]
            
            # Panel 4: Trash
            t_res = []
            for _ in range(5):
                row = []
                for c in range(4):
                    used = set(p2_data[c][:7] + p3_data[c][:7])
                    pool = [n for n in range(10) if n not in used] or list(range(10))
                    row.append(random.choice(pool))
                t_res.append(row)
            st.session_state.trash_res = t_res

with c_btn2:
    st.button("🗑️ HAPUS DATA", on_click=full_reset, use_container_width=True)

# =============================================================================
# --- 8. DISPLAY DASHBOARD (STRUKTUR UTUH 299+ BARIS) ---
# =============================================================================
if 'current_res' in st.session_state:
    # --- DISPLAY PANEL 1 ---
    st.markdown("<div class='pure-header'>💎 PANEL 1: HASIL CAMPURAN (SARINGAN 10➔6)</div>", unsafe_allow_html=True)
    h1 = "<table class='predict-table pure-table'><tr><th>FINAL</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for i in range(6):
        row = st.session_state.current_res[i]
        h1 += f"<tr><td class='rank-label' style='background:#004d40 !important;'>BARIS {i+1}</td>"
        for d in row:
            css = "class='red-ball'" if d in st.session_state.ball_ref else ""
            h1 += f"<td {css}>{d}</td>"
        h1 += "</tr>"
    st.markdown(h1 + "</table>", unsafe_allow_html=True)

    # --- DISPLAY PANEL 2 ---
    st.divider()
    st.markdown("<div class='m1-header'>🏆 PANEL 2: PREDIKSI MURNI MESIN PERTAMA (7 BARIS)</div>", unsafe_allow_html=True)
    h2 = "<table class='predict-table' style='border:2px solid #ffeb3b;'><tr><th>PENTA</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for r in range(7):
        h2 += f"<tr><td class='rank-label' style='background:#fbc02d !important; color:black !important;'>LINE {r+1}</td>"
        for c in range(4):
            val = st.session_state.pure_res[c][r]
            css = "class='red-ball'" if val in st.session_state.ball_ref else ""
            h2 += f"<td {css}>{val}</td>"
        h2 += "</tr>"
    st.markdown(h2 + "</table>", unsafe_allow_html=True)

    # --- DISPLAY PANEL 3 ---
    st.divider()
    st.markdown("#### 📊 PANEL 3: PREDIKSI MURNI MESIN KEDUA (7 BARIS)")
    h3 = "<table class='predict-table'><tr><th>M-2</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for r in range(7):
        h3 += f"<tr><td class='rank-label'>BARIS {r+1}</td>"
        for c in range(4):
            val = st.session_state.m2_pure[c][r]
            css = "class='red-ball'" if val in st.session_state.ball_ref else ""
            h3 += f"<td {css}>{val}</td>"
        h3 += "</tr>"
    st.markdown(h3 + "</table>", unsafe_allow_html=True)

    # --- DISPLAY PANEL 4 ---
    st.divider()
    st.markdown("<div class='trash-header'>🗑️ PANEL 4: KOLEKSI ANGKA SAMPAH (BUANGAN)</div>", unsafe_allow_html=True)
    h4 = "<table class='predict-table trash-table'><tr><th>TRASH</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for i in range(5):
        row = st.session_state.trash_res[i]
        h4 += f"<tr><td class='rank-label' style='background:#bf360c !important; color:white !important;'>TRASH {i+1}</td>"
        for d in row:
            css = "class='red-ball'" if d in st.session_state.ball_ref else ""
            h4 += f"<td {css}>{d}</td>"
        h4 += "</tr>"
    st.markdown(h4 + "</table>", unsafe_allow_html=True)

    st.info("🔴 Angka MERAH: Referensi Oracle Simulator (40 Bola - Tanpa Pengembalian)")
