import streamlit as st
import numpy as np

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v27.0: Absolute Reset", layout="wide")

# --- 2. CSS CUSTOM (BIRU MODERN & BERSIH) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000428, #004e92); color: #E0F7FA; }
    .main-card { 
        background: rgba(0, 0, 0, 0.6); 
        border: 2px solid #00d2ff; 
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.4);
    }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 4px; }
    .predict-table td { 
        border-radius: 8px; padding: 15px; text-align: center; font-size: 30px; font-weight: 900; 
        background: rgba(0, 210, 255, 0.25); border: 1px solid #00d2ff;
        color: white !important; text-shadow: 2px 2px 5px #000;
    }
    .rank-label { font-size: 16px !important; background: rgba(0,0,0,0.7) !important; color: #00ffcc !important; }
    .boom-text { font-size: 48px !important; font-weight: 900; display: block; letter-spacing: 8px; }
    .b1 { color: #00ffcc; text-shadow: 0 0 30px #00ffcc; }
    .b2 { color: #f2c94c; text-shadow: 0 0 30px #f2c94c; }
    .b3 { color: #ffffff; text-shadow: 0 0 30px #ffffff; }
    .dead-row { background: rgba(255, 0, 0, 0.5) !important; color: #ffffff !important; border: 2px solid #ff0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HARD RESET SYSTEM ---
if 'data_key' not in st.session_state:
    st.session_state.data_key = 0

def clear_everything():
    st.session_state.data_key += 1  # Mengganti key widget akan memaksa reset total
    st.session_state.run_analysis = False
    st.rerun()

# --- 4. ADAPTIVE MOMENTUM ENGINE (AKURASI TINGGI) ---
def adaptive_engine(data):
    if not data: return None
    rows = [[int(d) for d in item if d.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if len(rows) < 10: return "LOW"

    data_np = np.array(rows)
    final_res = []

    for i in range(4):
        col = data_np[:, i]
        scores = {}
        
        # Fokus hanya pada momentum sangat pendek (8 data terakhir)
        # Ini untuk menangkap angka yang sedang 'menggila' atau sering muncul
        recent_pulse = list(col[-8:])
        
        for n in range(10):
            # 1. Skor Momentum (Jika baru keluar di 8 putaran terakhir, skor naik drastis)
            s_pulse = recent_pulse.count(n) * 60
            
            # 2. Skor Repetisi (Jika baru keluar tepat di posisi terakhir, beri peluang muncul lagi)
            s_repeat = 40 if n == col[-1] else 0
            
            # 3. Skor Frekuensi Total (Stabilitas angka)
            s_total = list(col).count(n) * 3
            
            # 4. Filter Angka Beku (Jika tidak keluar > 20 putaran, buang ke Dead)
            try: last_seen = len(col) - 1 - list(col[::-1]).index(n)
            except: last_seen = 0
            gap = len(col) - last_seen
            s_gap = -50 if gap > 20 else (gap * 1.2)

            scores[n] = s_pulse + s_repeat + s_total + s_gap
        
        # Sortir dan ambil angkanya saja
        sorted_nums = [n for n, s in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
        final_res.append(sorted_nums)
        
    return final_res

# --- 5. UI CONTROL ---
st.title("🛡️ MASTER BRAIN v27.0 - ULTIMATE MOMENTUM")

# Input dengan Key Dinamis untuk Hard Reset
input_data = st.text_area("Input Data History 4D:", height=150, key=f"input_{st.session_state.data_key}")

c_run, c_del = st.columns(2)
with c_run:
    analyze_btn = st.button("🚀 JALANKAN ANALISA MOMENTUM", use_container_width=True)
with c_del:
    st.button("🗑️ RESET TOTAL APLIKASI", on_click=clear_everything, use_container_width=True)

if analyze_btn:
    if input_data:
        res = adaptive_engine(input_data.replace(',', ' ').split())
        
        if res == "LOW":
            st.error("Data terlalu sedikit (Minimal 10 baris)!")
        elif res:
            # --- TRIPLE BOOM ---
            st.markdown("### 💣 TRIPLE BOOM (ARUS PANAS)")
            b1, b2, b3 = st.columns(3)
            with b1: st.markdown(f"<div class='main-card'>BOOM #1<br><span class='boom-text b1'>{res[0][0]}{res[1][0]}{res[2][0]}{res[3][0]}</span></div>", unsafe_allow_html=True)
            with b2: st.markdown(f"<div class='main-card'>BOOM #2<br><span class='boom-text b2'>{res[0][1]}{res[1][1]}{res[2][1]}{res[3][1]}</span></div>", unsafe_allow_html=True)
            with b3: st.markdown(f"<div class='main-card'>BOOM #3<br><span class='boom-text b3'>{res[0][2]}{res[1][2]}{res[2][2]}{res[3][2]}</span></div>", unsafe_allow_html=True)

            # --- TABEL RANKING R1 - R8 ---
            st.markdown("### 📊 TRACKING POSISI (R1 - R8)")
            h = "<table class='predict-table'><tr><th>RANK</th><th>K1</th><th>K2</th><th>K3</th><th>K4</th></tr>"
            for r in range(8):
                h += f"<tr><td class='rank-label'>R{r+1}</td>"
                for c in range(4):
                    h += f"<td>{res[c][r]}</td>"
                h += "</tr>"
            
            # DEAD ZONE (2 Baris Sisa)
            for r in range(8, 10):
                h += f"<tr><td class='dead-row'>DEAD</td>"
                for c in range(4):
                    h += f"<td class='dead-row'>{res[c][r]}</td>"
                h += "</tr>"
            st.markdown(h + "</table>", unsafe_allow_html=True)
