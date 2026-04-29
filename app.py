import streamlit as st
from collections import Counter
import random
import time

# --- 1. CONFIG & INITIAL STATE (ITEM 1-15) ---
st.set_page_config(page_title="Master Brain v16.1: Ultimate Triple Engine", layout="wide")
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_area' not in st.session_state:
    st.session_state.input_area = ""
if 'trigger_run' not in st.session_state:
    st.session_state.trigger_run = False
if 'active_theme' not in st.session_state:
    st.session_state.active_theme = "Pelangi & Cosmic 🌈"

# --- 2. DAFTAR TEMA & GRADASI (ITEM 16-45) ---
app_themes = {
    "Pelangi & Cosmic 🌈": {"bg": "linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d)", "txt": "#FFFFFF"},
    "Biru Laut & Nature": {"bg": "linear-gradient(to bottom, #000428, #004e92)", "txt": "#E0F7FA"},
    "Gelap Neon (Leaf)": {"bg": "#0E1117", "txt": "#00FF00"},
}
gradien_options = {
    "Hijau Emerald": "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)", 
    "Biru Cyan": "linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)", 
    "Merah Muda Magma": "linear-gradient(135deg, #f80759 0%, #bc4e9c 100%)", 
    "Emas Mewah": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)"
}
p_app = st.sidebar.selectbox("Tema Aplikasi:", list(app_themes.keys()))
t_app = app_themes[p_app]

# --- 3. CSS & ANIMASI UTUH (ITEM 46-100) ---
st.markdown(f"""
    <style>
    .stApp {{ background: {t_app['bg']}; color: {t_app['txt']}; overflow-x: hidden; }}
    .leaf-frame {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; border: 20px solid transparent; z-index: 9999; animation: leafMove 5s infinite alternate ease-in-out; }}
    @keyframes leafMove {{ 
        0% {{ transform: scale(1); filter: hue-rotate(0deg); }} 
        100% {{ transform: scale(1.02); filter: hue-rotate(20deg); }} 
    }}
    .star {{ position: absolute; background: white; border-radius: 50%; opacity: 0.5; animation: fall linear infinite; }}
    @keyframes fall {{ 
        from {{ transform: translateY(-10vh) translateX(0); }} 
        to {{ transform: translateY(110vh) translateX(20vw); }} 
    }}
    .predict-table {{ width: 100%; border-collapse: separate; border-spacing: 5px; margin-bottom: 25px; transition: all 0.3s ease; }}
    .predict-table td {{ 
        border-radius: 12px; padding: 15px; text-align: center; 
        font-size: 32px; font-weight: 900; color: white !important; 
        -webkit-text-stroke: 1.5px black; text-shadow: 0 0 15px rgba(255,255,255,0.7), 3px 3px 5px #000; 
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5); 
    }}
    textarea {{ color: white !important; font-weight: bold !important; font-size: 20px !important; background: rgba(0,0,0,0.4) !important; }}
    .stButton>button {{ width: 100%; border-radius: 8px; font-weight: bold; height: 45px; }}
    </style>
    <div class="leaf-frame"></div>
    """, unsafe_allow_html=True)

# LOOP ANIMASI PARTIKEL (ITEM 101-115)
for i in range(25):
    sz = random.randint(2, 5)
    lf = random.randint(0, 100)
    dr = random.randint(3, 8)
    st.markdown(f'<div class="star" style="width:{sz}px; height:{sz}px; left:{lf}%; animation-duration:{dr}s;"></div>', unsafe_allow_html=True)

# --- 4. KONTROL GRADASI (ITEM 116-125) ---
c_t1, c_t2, c_t3 = st.columns(3)
with c_t1:
    p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)
with c_t2:
    p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)
with c_t3:
    p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)
g1 = gradien_options[p_t1]
g2 = gradien_options[p_t2]
g3 = gradien_options[p_t3]

# --- 5. FILTER & INPUT (ITEM 126-155) ---
st.markdown("---")
p_filter = st.radio("Saring hasil angka:", ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], horizontal=True)
manual_input = st.text_area("Tempel Data 4-Digit:", height=150, value=st.session_state.input_area, key="input_field")

def handle_reset_paste():
    st.session_state.input_area = ""
    st.rerun()

def handle_reset_all(): 
    st.session_state.history = []
    st.session_state.input_area = ""
    st.session_state.trigger_run = False
    st.rerun()

btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input: 
            st.session_state.history = manual_input.replace(',', ' ').replace('\n', ' ').split()
            st.session_state.trigger_run = True
with btn_col2:
    st.button("🗑️ HAPUS TEKS PASTE", on_click=handle_reset_paste)
with btn_col3:
    st.button("🔴 RESET SEMUA DATA", on_click=handle_reset_all)

# --- 6. ENGINE ANALISA (OTAK UTAMA) (ITEM 156-185) ---
def get_predictions(data, f_mode):
    if not data: 
        return {}
    rows = [[int(c) for c in item if c.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if not rows: 
        return {}
    lb = max(10, min(25, len(rows)))
    seg = rows[-lb:]
    res_final = {"t1":[], "t2":[], "t3":[], "t4":[], "t5":[]}
    for i in range(4):
        col_f = [r[i] for r in rows]
        col_s = [r[i] for r in seg]
        scored = sorted([str(x) for x in range(10)], key=lambda x: (col_s.count(int(x))*7 + col_f.count(int(x))*0.5), reverse=True)
        is_g = sum(1 for x in col_s if x % 2 != 0) >= (lb/2)
        is_b = sum(1 for x in col_s if x >= 5) >= (lb/2)
        sink = [a for a in scored if ((int(a)%2!=0)==is_g) and ((int(a)>=5)==is_b)]
        lawan = [a for a in scored if a not in sink]
        def apply_f(lst_in):
            if f_mode == "Ganjil": 
                return [x for x in lst_in if int(x)%2!=0]
            if f_mode == "Genap": 
                return [x for x in lst_in if int(x)%2==0]
            if f_mode == "Kecil (0-4)": 
                return [x for x in lst_in if int(x)<=4]
            if f_mode == "Besar (5-9)": 
                return [x for x in lst_in if int(x)>=5]
            return lst_in
        h_val = [sink if sink else scored, lawan if lawan else scored]
        res_final["t2"].append({"m": apply_f(sink), "h": h_val, "c": scored})
        res_final["t1"].append({"m": apply_f(sink[1:]+sink[:1]), "h": h_val, "c": scored})
        res_final["t3"].append({"m": apply_f(lawan), "h": h_val, "c": scored})
        m_list = sorted(sink if sink else scored, key=lambda x: Counter("".join(data[-lb:])).get(x,0), reverse=True)
        res_final["t4"].append({"m": apply_f(m_list), "h": h_val, "c": scored})
        res_final["t5"].append([x for x in scored if x not in m_list[:4]] + scored)
    return res_final

# --- 7. DISPLAY TABEL (ITEM 186-215+) ---
if st.session_state.history:
    res = get_predictions(st.session_state.history, p_filter)
    if res:
        l_std = 4 if p_filter != "Semua" else 6
        l_ext = 4 if p_filter != "Semua" else 8
        def ambil_aman(d_dict, r_idx, limit, is_t5=False):
            if is_t5: 
                return d_dict[r_idx] if r_idx < len(d_dict) else "-"
            if r_idx >= limit - 2: 
                return str(d_dict["h"][r_idx - (limit - 2)])
            m_l = d_dict["m"]
            c_l = d_dict["c"]
            if r_idx < len(m_l): 
                return m_l[r_idx]
            return c_l[r_idx] if r_idx < len(c_l) else "-"

        t_confs = [("🍀 TABEL SEIMBANG", "t1", g1, l_std), ("🔥 TABEL AKURAT", "t2", g2, l_std), ("❄️ TABEL KONTRA", "t3", g3, l_ext)]
        for title, key, grad, limit in t_confs:
            st.subheader(title)
            html = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
            for r in range(limit):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
                for c in range(4):
                    d = res[key][c]
                    val = ambil_aman(d, r, limit)
                    html += f"<td style='background:{grad};'>{val}</td>"
                html += "</tr>"
            st.markdown(html + "</table>", unsafe_allow_html=True)

        st.subheader("💎 TABEL MASTER")
        m_html = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(l_std):
            m_html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
            for c in range(4):
                d = res["t4"][c]
                val = ambil_aman(d, r, l_std)
                m_html += f"<td style='background:{gradien_options['Emas Mewah']};'>{val}</td>"
            m_html += "</tr>"
        st.markdown(m_html + "</table>", unsafe_allow_html=True)

        st.subheader("💀 TABEL ELIMINASI")
        e_html = "<table class='predict-table'><tr><th>DEAD</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(8):
            e_html += f"<tr><td style='font-size:12px; background:red;'>DEAD</td>"
            for c in range(4):
                val = res["t5"][c][r]
                e_html += f"<td style='background:#232526; color:red;'>{val}</td>"
            e_html += "</tr>"
        st.markdown(e_html + "</table>", unsafe_allow_html=True)
