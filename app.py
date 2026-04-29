import streamlit as st
from collections import Counter
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Master Brain v17.2: Ultimate Engine", 
    layout="wide"
)

# --- 2. INITIAL SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []

if 'input_area' not in st.session_state:
    st.session_state.input_area = ""

if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# --- 3. DAFTAR TEMA APLIKASI ---
app_themes = {
    "Pelangi & Cosmic 🌈": {
        "bg": "linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d)", 
        "txt": "#FFFFFF"
    },
    "Biru Laut & Nature": {
        "bg": "linear-gradient(to bottom, #004e92, #000428)", 
        "txt": "#E0F7FA"
    },
    "Gelap Neon (Leaf)": {
        "bg": "#0E1117", 
        "txt": "#00FF00"
    },
}

# --- 4. DAFTAR GRADASI TABEL ---
gradien_options = {
    "Hijau Emerald": "linear-gradient(135deg, #56ab2f, #a8e063)", 
    "Biru Cyan": "linear-gradient(135deg, #00d2ff, #3a7bd5)", 
    "Merah Muda Magma": "linear-gradient(135deg, #f80759, #bc4e9c)", 
    "Emas Mewah": "linear-gradient(135deg, #f2994a, #f2c94c)"
}

# --- 5. SIDEBAR SELECTION ---
p_app = st.sidebar.selectbox("Tema Aplikasi:", list(app_themes.keys()))
t_app = app_themes[p_app]

# --- 6. CSS CUSTOM STYLING (DIJABARKAN) ---
st.markdown(f"""
    <style>
    .stApp {{ 
        background: {t_app['bg']}; 
        color: {t_app['txt']}; 
        overflow-x: hidden; 
    }}
    .leaf-frame {{ 
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 100%; 
        pointer-events: none; 
        border: 20px solid transparent; 
        z-index: 9999; 
        animation: leafMove 5s infinite alternate ease-in-out; 
    }}
    @keyframes leafMove {{ 
        0% {{ transform: scale(1); filter: hue-rotate(0deg); }} 
        100% {{ transform: scale(1.02); filter: hue-rotate(20deg); }} 
    }}
    .star {{ 
        position: absolute; 
        background: white; 
        border-radius: 50%; 
        opacity: 0.5; 
        animation: fall linear infinite; 
    }}
    @keyframes fall {{ 
        from {{ transform: translateY(-10vh) translateX(0); }} 
        to {{ transform: translateY(110vh) translateX(20vw); }} 
    }}
    .predict-table {{ 
        width: 100%; 
        border-collapse: separate; 
        border-spacing: 5px; 
        margin-bottom: 25px; 
    }}
    .predict-table td {{ 
        border-radius: 12px; 
        padding: 15px; 
        text-align: center; 
        font-size: 32px; 
        font-weight: 900; 
        color: white !important; 
        -webkit-text-stroke: 1.5px black; 
        text-shadow: 0 0 15px rgba(255,255,255,0.7), 3px 3px 5px #000; 
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5); 
    }}
    textarea {{ 
        color: white !important; 
        font-weight: bold !important; 
        font-size: 20px !important; 
        background: rgba(0,0,0,0.4) !important; 
    }}
    </style>
    <div class="leaf-frame"></div>
    """, unsafe_allow_html=True)

# --- 7. PARTIKEL BINTANG JATUH ---
for i in range(25):
    s_sz = random.randint(2, 5)
    s_lf = random.randint(0, 100)
    s_dr = random.randint(3, 8)
    st.markdown(f'<div class="star" style="width:{s_sz}px; height:{s_sz}px; left:{s_lf}%; animation-duration:{s_dr}s;"></div>', unsafe_allow_html=True)

# --- 8. KONTROL GRADASI UI ---
col_t1, col_t2, col_t3 = st.columns(3)

with col_t1:
    p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)

with col_t2:
    p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)

with col_t3:
    p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)

g1 = gradien_options[p_t1]
g2 = gradien_options[p_t2]
g3 = gradien_options[p_t3]

# --- 9. FILTER & INPUT AREA ---
st.markdown("---")

p_filter = st.radio("Saring hasil angka:", ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], horizontal=True)

manual_input = st.text_area("Tempel Data 4-Digit:", height=150, value=st.session_state.input_area, key="main_input")

# --- 10. FUNGSI KONTROL DATA ---
def reset_paste_teks():
    st.session_state.input_area = ""
    st.rerun()

def reset_seluruh_data(): 
    st.session_state.history = []
    st.session_state.input_area = ""
    st.rerun()

c_btn1, c_btn2, c_btn3 = st.columns(3)

with c_btn1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input:
            st.session_state.history = manual_input.replace(',', ' ').replace('\n', ' ').split()

with c_btn2:
    st.button("🗑️ HAPUS TEKS PASTE", on_click=reset_paste_teks)

with c_btn3:
    st.button("🔴 RESET SEMUA DATA", on_click=reset_seluruh_data)

# --- 11. ENGINE ANALISA ADAPTIF ---
def get_predictions(data, f_mode):
    if not data:
        return {}
    
    clean_rows = []
    for item in data:
        chars = [c for c in item if c.isdigit()]
        if len(chars) >= 4:
            clean_rows.append([int(x) for x in chars[:4]])
    
    if not clean_rows:
        return {}
        
    look_back = max(10, min(25, len(clean_rows)))
    segmen_data = clean_rows[-look_back:]
    output_res = {"t1":[], "t2":[], "t3":[], "t4":[], "t5":[]}
    
    for i in range(4):
        kolom_full = [r[i] for r in clean_rows]
        kolom_seg = [r[i] for r in segmen_data]
        
        # Logika Skor Dasar
        skor_list = sorted([str(x) for x in range(10)], key=lambda x: (kolom_seg.count(int(x))*7 + kolom_full.count(int(x))*0.5), reverse=True)
        
        tren_g = sum(1 for x in kolom_seg if x % 2 != 0) >= (look_back/2)
        tren_b = sum(1 for x in kolom_seg if x >= 5) >= (look_back/2)
        
        sinkron_data = [a for a in skor_list if ((int(a)%2!=0)==tren_g) and ((int(a)>=5)==tren_b)]
        lawan_data = [a for a in skor_list if a not in sinkron_data]
        
        def filter_engine(lst):
            if f_mode == "Ganjil": return [x for x in lst if int(x)%2!=0]
            if f_mode == "Genap": return [x for x in lst if int(x)%2==0]
            if f_mode == "Kecil (0-4)": return [x for x in lst if int(x)<=4]
            if f_mode == "Besar (5-9)": return [x for x in lst if int(x)>=5]
            return lst

        # Pilar 3 Berbeda Tiap Tabel
        p3_t2 = sinkron_data[-2:] if len(sinkron_data)>=2 else skor_list[:2]
        p3_t1 = sinkron_data[:2] if len(sinkron_data)>=2 else skor_list[2:4]
        p3_t3 = lawan_data[:2] if len(lawan_data)>=2 else skor_list[-2:]
        
        output_res["t2"].append({"main": filter_engine(sinkron_data), "p3": p3_t2, "back": skor_list})
        output_res["t1"].append({"main": filter_engine(sinkron_data[1:]+sinkron_data[:1]), "p3": p3_t1, "back": skor_list})
        output_res["t3"].append({"main": filter_engine(lawan_data), "p3": p3_t3, "back": skor_list})
        
        master_list = sorted(sinkron_data if sinkron_data else skor_list, key=lambda x: Counter("".join(data[-look_back:])).get(x,0), reverse=True)
        p3_t4 = master_list[-2:] if len(master_list)>=2 else skor_list[4:6]
        
        output_res["t4"].append({"main": filter_engine(master_list), "p3": p3_t4, "back": skor_list})
        output_res["t5"].append(filter_engine([x for x in skor_list if x not in master_list[:4]]) + ["-"]*10)
        
    return output_res

# --- 12. DISPLAY TABEL ---
if st.session_state.history:
    hasil_final = get_predictions(st.session_state.history, p_filter)
    l_std = 4 if p_filter != "Semua" else 6
    l_ext = 4 if p_filter != "Semua" else 8
    
    def ambil_sel_aman(d_dict, r_idx, limit):
        if p_filter == "Semua" and r_idx >= limit - 2:
            return str(d_dict["p3"][r_idx - (limit - 2)])
        m_l = d_dict["main"]
        b_l = d_dict["back"]
        if r_idx < len(m_l): return m_l[r_idx]
        return b_l[r_idx] if r_idx < len(b_l) else "-"

    for t_title, t_key, t_grad, t_lim in [("🍀 TABEL SEIMBANG", "t1", g1, l_std), ("🔥 TABEL AKURAT", "t2", g2, l_std), ("❄️ TABEL KONTRA", "t3", g3, t_lim if 't_lim' in locals() else l_ext)]:
        st.subheader(t_title)
        t_html = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(t_lim if 't_lim' in locals() else l_ext):
            t_html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
            for c in range(4):
                t_html += f"<td style='background:{t_grad};'>{ambil_sel_aman(hasil_final[t_key][c], r, t_lim if 't_lim' in locals() else l_ext)}</td>"
            t_html += "</tr>"
        st.markdown(t_html + "</table>", unsafe_allow_html=True)

    st.subheader("💎 TABEL MASTER")
    m_html = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(l_std):
        m_html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
        for c in range(4):
            m_html += f"<td style='background:linear-gradient(135deg, #FFD700, #B8860B);'>{ambil_sel_aman(hasil_final['t4'][c], r, l_std)}</td>"
        m_html += "</tr>"
    st.markdown(m_html + "</table>", unsafe_allow_html=True)
