import streamlit as st
from collections import Counter
import random
import time

# --- 1. CONFIGURATION (ITEM 1-10) ---
st.set_page_config(
    page_title="Master Brain v18.0: Ultimate Master Engine", 
    layout="wide"
)

# --- 2. INITIAL SESSION STATE (ITEM 11-35) ---
if 'history' not in st.session_state:
    st.session_state.history = []

if 'input_area' not in st.session_state:
    st.session_state.input_area = ""

if 'trigger_run' not in st.session_state:
    st.session_state.trigger_run = False

# --- 3. DAFTAR TEMA APLIKASI (ITEM 36-60) ---
app_themes = {
    "Pelangi & Cosmic 🌈": {
        "bg": "linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d)", 
        "txt": "#FFFFFF"
    },
    "Biru Laut & Nature": {
        "bg": "linear-gradient(to bottom, #000428, #004e92)", 
        "txt": "#E0F7FA"
    },
    "Gelap Neon (Leaf)": {
        "bg": "#0E1117", 
        "txt": "#00FF00"
    },
}

# --- 4. DAFTAR GRADASI TABEL (ITEM 61-80) ---
gradien_options = {
    "Hijau Emerald": "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)", 
    "Biru Cyan": "linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)", 
    "Merah Muda Magma": "linear-gradient(135deg, #f80759 0%, #bc4e9c 100%)", 
    "Emas Mewah": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)"
}

# --- 5. SIDEBAR SELECTION (ITEM 81-90) ---
p_app = st.sidebar.selectbox("Tema Aplikasi:", list(app_themes.keys()))
t_app = app_themes[p_app]

# --- 6. CSS CUSTOM STYLING (DIJABARKAN ITEM 91-150) ---
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

# --- 7. ANIMASI PARTIKEL BINTANG (ITEM 151-165) ---
for i in range(25):
    s_sz = random.randint(2, 5)
    s_lf = random.randint(0, 100)
    s_dr = random.randint(3, 8)
    st.markdown(f'<div class="star" style="width:{s_sz}px; height:{s_sz}px; left:{s_lf}%; animation-duration:{s_dr}s;"></div>', unsafe_allow_html=True)

# --- 8. KONTROL GRADASI UI (ITEM 166-185) ---
col_1, col_2, col_3 = st.columns(3)

with col_1:
    p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)

with col_2:
    p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)

with col_3:
    p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)

g1 = gradien_options[p_t1]
g2 = gradien_options[p_t2]
g3 = gradien_options[p_t3]

# --- 9. INPUT & FILTER AREA (ITEM 186-210) ---
st.markdown("---")

p_filter = st.radio(
    "Saring hasil angka:", 
    ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], 
    horizontal=True
)

manual_input = st.text_area(
    "Tempel Data 4-Digit:", 
    height=150, 
    value=st.session_state.input_area, 
    key="main_box"
)

# --- 10. FUNGSI KONTROL DATA (ITEM 211-235) ---
def reset_paste():
    st.session_state.input_area = ""
    st.rerun()

def reset_all(): 
    st.session_state.history = []
    st.session_state.input_area = ""
    st.rerun()

btn_1, btn_2, btn_3 = st.columns(3)

with btn_1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input:
            st.session_state.history = manual_input.replace(',', ' ').replace('\n', ' ').split()

with btn_2:
    st.button("🗑️ HAPUS TEKS PASTE", on_click=reset_paste)

with btn_3:
    st.button("🔴 RESET SEMUA DATA", on_click=reset_all)

# --- 11. ENGINE ANALISA OTAK UTAMA (ITEM 236-300) ---
def get_predictions(data, f_mode):
    if not data: return {}
    rows = [[int(x) for x in item if x.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if not rows: return {}
    
    lb = max(10, min(25, len(rows)))
    seg = rows[-lb:]
    out = {"t1":[], "t2":[], "t3":[], "t4":[], "t5":[]}
    
    for i in range(4):
        col_f = [r[i] for r in rows]
        col_s = [r[i] for r in seg]
        
        skor_b = sorted([str(x) for x in range(10)], key=lambda x: (col_s.count(int(x))*7 + col_f.count(int(x))*0.5), reverse=True)
        
        tr_g = sum(1 for x in col_s if x % 2 != 0) >= (lb/2)
        tr_b = sum(1 for x in col_s if x >= 5) >= (lb/2)
        
        sink = [a for a in skor_b if ((int(a)%2!=0)==tr_g) and ((int(a)>=5)==tr_b)]
        lwn = [a for a in skor_b if a not in sink]
        
        def filter_engine(l):
            if f_mode == "Ganjil": return [x for x in l if int(x)%2!=0]
            if f_mode == "Genap": return [x for x in l if int(x)%2==0]
            if f_mode == "Kecil (0-4)": return [x for x in l if int(x)<=4]
            if f_mode == "Besar (5-9)": return [x for x in l if int(x)>=5]
            return l

        # Pilar 3 Berbeda Tiap Tabel (Diambil dari masing-masing hasil pilar)
        h_t2 = sink[-2:] if len(sink)>=2 else skor_b[:2]
        h_t1 = sink[:2] if len(sink)>=2 else skor_b[2:4]
        h_t3 = lwn[:2] if len(lwn)>=2 else skor_b[-2:]
        
        out["t2"].append({"m": filter_engine(sink), "p3": h_t2, "back": skor_b})
        out["t1"].append({"m": filter_engine(sink[1:]+sink[:1]), "p3": h_t1, "back": skor_b})
        out["t3"].append({"m": filter_engine(lwn), "p3": h_t3, "back": skor_b})
        
        m_list = sorted(sink if sink else skor_b, key=lambda x: Counter("".join(data[-lb:])).get(x,0), reverse=True)
        h_t4 = m_list[-2:] if len(m_list)>=2 else skor_b[4:6]
        
        out["t4"].append({"m": filter_engine(m_list), "p3": h_t4, "back": skor_b})
        out["t5"].append(filter_engine([x for x in skor_b if x not in m_list[:4]]) + ["-"]*10)
        
    return out

# --- 12. DISPLAY RENDER (ITEM 301-400+) ---
if st.session_state.history:
    res = get_predictions(st.session_state.history, p_filter)
    l_std = 4 if p_filter != "Semua" else 6
    l_ext = 4 if p_filter != "Semua" else 8
    
    def get_sel(d, r, lim):
        # Pilar 3 HANYA muncul di mode "Semua"
        if p_filter == "Semua" and r >= lim - 2:
            return str(d["p3"][r - (lim - 2)])
        m_l = d["m"]
        b_l = d["back"]
        if r < len(m_l): return m_l[r]
        return b_l[r] if r < len(b_l) else "-"

    # TABEL 1, 2, 3
    for tit, key, gr, lim in [("🍀 TABEL SEIMBANG", "t1", g1, l_std), ("🔥 TABEL AKURAT", "t2", g2, l_std), ("❄️ TABEL KONTRA", "t3", g3, l_ext)]:
        st.subheader(tit)
        h = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(lim):
            h += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
            for c in range(4):
                h += f"<td style='background:{gr};'>{get_sel(res[key][c], r, lim)}</td>"
            h += "</tr>"
        st.markdown(h + "</table>", unsafe_allow_html=True)

    # TABEL 4 (MASTER)
    st.subheader("💎 TABEL MASTER")
    hm = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(l_std):
        hm += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
        for c in range(4):
            hm += f"<td style='background:linear-gradient(135deg, #FFD700, #B8860B);'>{get_sel(res['t4'][c], r, l_std)}</td>"
        hm += "</tr>"
    st.markdown(hm + "</table>", unsafe_allow_html=True)

    # TABEL 5 (ELIMINASI)
    st.subheader("💀 TABEL ELIMINASI")
    he = "<table class='predict-table'><tr><th>DEAD</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(8):
        he += "<tr><td style='font-size:12px; background:red;'>DEAD</td>"
        for c in range(4):
            he += f"<td style='background:#232526; color:red;'>{res['t5'][c][r]}</td>"
        he += "</tr>"
    st.markdown(he + "</table>", unsafe_allow_html=True)
