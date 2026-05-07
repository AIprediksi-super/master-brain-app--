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
# --- 2. CSS CUSTOM (GAYA VISUAL DASHBOARD) ---
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
    .rank-label { 
        font-size: 13px !important; 
        background: rgba(0,0,0,0.8) !important; 
        color: #00ffcc !important; 
        width: 100px; 
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
        color: #ffffff !important; 
        text-shadow: 0 0 5px #ff5722;
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

# --- FUNGSI RESET DATA ---
if 'reset_key' not in st.session_state: 
    st.session_state.reset_key = 0

def full_reset():
    st.session_state.reset_key += 1
    if 'current_res' in st.session_state: del st.session_state.current_res
    if 'pure_res' in st.session_state: del st.session_state.pure_res
    if 'm2_pure' in st.session_state: del st.session_state.m2_pure
    if 'trash_res' in st.session_state: del st.session_state.trash_res
    st.rerun()

# =============================================================================
# --- 3. MESIN LIMA LOGIKA MURNI (PENTA-SYNC 92%) ---
# =============================================================================
def smart_engine_pure_penta(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_scores_list = []
    idx_map = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}
    
    # Loop untuk setiap kolom (K1, K2, K3, K4)
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        
        # L1: Velocity Momentum (Bobot 280)
        # Menilai angka berdasarkan kecepatan kemunculan terakhir
        for idx, val in enumerate(reversed(col[-7:])):
            scores[val] += (280 / ((idx + 1) ** 1.1))
            
        # L2 & L5: Mirror-Inversion Point (Bobot 130)
        # Menghitung angka indeks atau kebalikan
        last_val = col[-1]
        mirror_target = idx_map[last_val]
        scores[mirror_target] += 130.0 
        
        # L3: Matrix Cross-Link (Bobot 65)
        # Hubungan angka antar kolom
        if i > 0: 
            cross_val = data_np[-1, i-1]
            scores[cross_val] += 65.0
            
        # L4: Frequency Void Sync (Bobot 155)
        # Mencari angka yang jarang muncul di periode pendek
        counts_15 = Counter(col[-15:])
        for n in range(10):
            if n not in counts_15: 
                scores[n] += 155.0
                
        # Anti-Noise Filter (Pengurang Skor)
        # Mengurangi kemungkinan angka tetangga muncul berturutan
        noise_up = (last_val + 1) % 10
        noise_down = (last_val - 1) % 10
        scores[noise_up] -= 40.0
        scores[noise_down] -= 40.0
        
        final_scores_list.append(scores)
        
    return final_scores_list

# =============================================================================
# --- 4. ENGINE v70.0 DEEP ANALYSIS (MIXED LOGIC) ---
# =============================================================================
def smart_engine_deep(data_raw):
    all_numbers = re.findall(r'\d{4}', data_raw)
    rows = [[int(d) for d in item] for item in all_numbers]
    data_np = np.array(rows)
    final_scores_list = []
    total_data_len = len(rows)
    
    # Loop untuk setiap kolom (K1, K2, K3, K4)
    for i in range(4):
        col = data_np[:, i]
        scores = {n: 0.0 for n in range(10)}
        freq_counter = Counter(col)
        
        # Skor berdasarkan posisi kemunculan terakhir (15 data)
        for idx, val in enumerate(reversed(col[-15:])):
            scores[val] += (220 / ((idx + 1.2) ** 0.8))
            
        # Skor berdasarkan "Gap" atau jarak ketidakmunculan
        for n in range(10):
            gap_count = 0
            for val_in_col in reversed(col):
                if val_in_col == n: 
                    break
                gap_count += 1
            # Rumus Gap dikali frekuensi total
            scores[n] += (gap_count * 8.5) * (1 + (freq_counter[n] / total_data_len))
            
        final_scores_list.append(scores)
        
    return final_scores_list

# =============================================================================
# --- 5. UI CONTROL DAN PROSES ANALISA ---
# =============================================================================
st.title("🛡️ MASTER BRAIN v75.0 PRO")
input_data_raw = st.text_area("Tempel Data History:", height=150, key=f"inp_{st.session_state.reset_key}")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🚀 JALANKAN ANALISA LENGKAP", use_container_width=True):
        if input_data_raw:
            # PROSES PERHITUNGAN SKOR DARI KEDUA MESIN
            scores_mesin_1 = smart_engine_pure_penta(input_data_raw)
            scores_mesin_2 = smart_engine_deep(input_data_raw)
            
            # --- PANEL 2: PREDIKSI MURNI MESIN PERTAMA (7 BARIS) ---
            panel_2_data = []
            for c in range(4):
                # Sortir angka berdasarkan skor tertinggi
                sorted_nums = [n for n, s in sorted(scores_mesin_1[c].items(), key=lambda item: item[1], reverse=True)]
                panel_2_data.append(sorted_nums)
            st.session_state.pure_res = panel_2_data
            
            # --- PANEL 3: PREDIKSI MURNI MESIN KEDUA (7 BARIS) ---
            panel_3_data = []
            for c in range(4):
                # Sortir angka berdasarkan skor tertinggi
                sorted_nums = [n for n, s in sorted(scores_mesin_2[c].items(), key=lambda item: item[1], reverse=True)]
                panel_3_data.append(sorted_nums)
            st.session_state.m2_pure = panel_3_data
            
            # --- PANEL 1: HASIL CAMPURAN (SARINGAN 8➔6) ---
            # Langkah A: Ambil 8 baris teratas dari Mesin Kedua sebagai kandidat
            kandidat_8_baris = []
            for r_idx in range(8):
                baris_kandidat = [panel_3_data[c][r_idx] for c in range(4)]
                kandidat_8_baris.append(baris_kandidat)
            
            # Langkah B: Saring menggunakan skor dari Mesin Pertama
            baris_berbobot = []
            for baris in kandidat_8_baris:
                # Hitung total bobot baris ini di Mesin 1
                total_bobot_m1 = 0
                for c_idx in range(4):
                    angka_di_posisi = baris[c_idx]
                    total_bobot_m1 += scores_mesin_1[c_idx][angka_di_posisi]
                baris_berbobot.append((baris, total_bobot_m1))
            
            # Langkah C: Sortir 8 baris tadi berdasarkan bobot Mesin 1 dan ambil 6 terbaik
            final_6_baris = [b for b, w in sorted(baris_berbobot, key=lambda item: item[1], reverse=True)[:6]]
            st.session_state.current_res = final_6_baris
            
            # --- PANEL 4: KOLEKSI ANGKA SAMPAH (5 BARIS) ---
            # Mencari angka sisa yang tidak masuk dalam Top 7 di Panel 2 & 3
            panel_4_data = []
            for r_trash in range(5):
                baris_sampah = []
                for c_trash in range(4):
                    # Kumpulan angka yang sudah terpakai di Panel 2 dan 3
                    angka_terpakai = set(panel_2_data[c_trash][:7] + panel_3_data[c_trash][:7])
                    pool_sampah = [num for num in range(10) if num not in angka_terpakai]
                    # Jika pool kosong (sangat jarang), ambil dari angka manapun
                    if not pool_sampah: 
                        pool_sampah = [num for num in range(10)]
                    baris_sampah.append(random.choice(pool_sampah))
                panel_4_data.append(baris_sampah)
            st.session_state.trash_res = panel_4_data

with col_btn2:
    st.button("🗑️ HAPUS DATA", on_click=full_reset, use_container_width=True)

# =============================================================================
# --- 6. BAGIAN DISPLAY (MENAMPILKAN TABEL HASIL) ---
# =============================================================================
if 'current_res' in st.session_state:
    
    # --- DISPLAY PANEL 1 ---
    st.markdown("<div class='pure-header'>💎 PANEL 1: HASIL CAMPURAN (SARINGAN 8➔6)</div>", unsafe_allow_html=True)
    html_p1 = "<table class='predict-table pure-table'><tr><th>FINAL</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for idx_row in range(6):
        data_row = st.session_state.current_res[idx_row]
        html_p1 += f"<tr><td class='rank-label' style='background:#004d40 !important;'>BARIS {idx_row+1}</td>"
        html_p1 += "".join([f"<td>{data_row[col_idx]}</td>" for col_idx in range(4)])
        html_p1 += "</tr>"
    st.markdown(html_p1 + "</table>", unsafe_allow_html=True)

    # --- DISPLAY PANEL 2 ---
    st.divider()
    st.markdown("<div class='m1-header'>🏆 PANEL 2: PREDIKSI MURNI MESIN PERTAMA (7 BARIS)</div>", unsafe_allow_html=True)
    html_p2 = "<table class='predict-table' style='border:2px solid #ffeb3b;'><tr><th>PENTA</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for idx_row in range(7):
        html_p2 += f"<tr><td class='rank-label' style='background:#fbc02d !important; color:black !important;'>LINE {idx_row+1}</td>"
        html_p2 += "".join([f"<td>{st.session_state.pure_res[col_idx][idx_row]}</td>" for col_idx in range(4)])
        html_p2 += "</tr>"
    st.markdown(html_p2 + "</table>", unsafe_allow_html=True)

    # --- DISPLAY PANEL 3 ---
    st.divider()
    st.markdown("#### 📊 PANEL 3: PREDIKSI MURNI MESIN KEDUA (7 BARIS)")
    html_p3 = "<table class='predict-table'><tr><th>M-2</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for idx_row in range(7):
        html_p3 += f"<tr><td class='rank-label'>BARIS {idx_row+1}</td>"
        html_p3 += "".join([f"<td>{st.session_state.m2_pure[col_idx][idx_row]}</td>" for col_idx in range(4)])
        html_p3 += "</tr>"
    st.markdown(html_p3 + "</table>", unsafe_allow_html=True)

    # --- DISPLAY PANEL 4 ---
    st.markdown("<div class='trash-header'>🗑️ PANEL 4: KOLEKSI ANGKA SAMPAH (BUANGAN)</div>", unsafe_allow_html=True)
    html_p4 = "<table class='predict-table trash-table'><tr><th>TRASH</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
    for idx_row in range(5):
        data_trash = st.session_state.trash_res[idx_row]
        html_p4 += f"<tr><td class='rank-label' style='background:#bf360c !important; color:white !important;'>TRASH {idx_row+1}</td>"
        html_p4 += "".join([f"<td>{data_trash[col_idx]}</td>" for col_idx in range(4)])
        html_p4 += "</tr>"
    st.markdown(html_p4 + "</table>", unsafe_allow_html=True)
