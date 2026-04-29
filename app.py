import streamlit as st
from collections import Counter
import random

# --- 1. CONFIG & STATE (ITEM 1-10) ---
st.set_page_config(page_title="Master Brain v15.6: Ultimate Master Engine", layout="wide")
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_area' not in st.session_state:
    st.session_state.input_area = ""

# --- 2. DAFTAR TEMA & GRADASI (ITEM 11-25) ---
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

# --- 3. CSS & ANIMASI UTUH (ITEM 26-60) ---
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
    </style>
    <div class="leaf-frame"></div>
    """, unsafe_allow_html=True)

# LOOP PARTIKEL BINTANG (ITEM 61-68)
for _ in range(20):
    s_size = random.randint(2, 5)
    s_left = random.randint(0, 100)
    s_dur = random.randint(3, 8)
    st.markdown(f'<div class="star" style="width:{s_size}px; height:{s_size}px; left:{s_left}%; animation-duration:{s_dur}s;"></div>', unsafe_allow_html=True)

# --- 4. KONTROL GRADASI (ITEM 69-78) ---
col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)
with col_g2:
    p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)
with col_g3:
    p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)
g1, g2, g3 = gradien_options[p_t1], gradien_options[p_t2], gradien_options[p_t3]

# --- 5. FILTER & INPUT (ITEM 79-110) ---
st.markdown("---")
p_filter = st.radio("Saring hasil angka:", ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], horizontal=True)
manual_input = st.text_area("Tempel Data 4-Digit:", height=150, key="input_area")

def clear_input_only():
    st.session_state.input_area = ""

def full_system_reset():
    st.session_state.history = []
    st.session_state.input_area = ""

btn_c1, btn_c2, btn_c3 = st.columns(3)
with btn_c1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input:
            st.session_state.history = manual_input.replace(',', ' ').replace('\n', ' ').split()
with btn_c2:
    st.button("🗑️ HAPUS TEKS PASTE", on_click=clear_input_only)
with btn_c3:
    st.button("🔴 RESET SEMUA DATA", on_click=full_system_reset)

# --- 6. ENGINE ANALISA (OTAK UTAMA 3 PILAR) (ITEM 111-140) ---
def get_predictions(data, f_mode):
    if not data: return {}
    rows = [[int(c) for c in item if c.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if not rows: return {}
    lb = max(10, min(25, len(rows)))
    seg = rows[-lb:]
    res_data = {"t1":[], "t2":[], "t3":[], "t4":[], "t5":[]}
    
    for i in range(4):
        col_full = [r[i] for r in rows]
        col_seg = [r[i] for r in seg]
        
        # LOGIKA SKORING DETAIL
        score_panas = lambda x: col_seg.count(int(x)) * 7.5
        score_statis = lambda x: col_full.count(int(x)) * 0.5
        scored = sorted([str(x) for x in range(10)], key=lambda x: score_panas(x) + score_statis(x), reverse=True)
        
        # CROSS-CHECK TREN 10-25 BARIS
        is_g = sum(1 for x in col_seg if x % 2 != 0) >= (lb/2)
        is_b = sum(1 for x in col_seg if x >= 5) >= (lb/2)
        
        sinkron = [a for a in scored if ((int(a)%2!=0)==is_g) and ((int(a)>=5)==is_b)]
        lawan = [a for a in scored if a not in sinkron]
        
        def apply_f(l_data):
            if f_mode == "Ganjil": return [x for x in l_data if int(x)%2!=0]
            if f_mode == "Genap": return [x for x in l_data if int(x)%2==0]
            if f_mode == "Kecil (0-4)": return [x for x in l_data if int(x)<=4]
            if f_mode == "Besar (5-9)": return [x for x in l_data if int(x)>=5]
            return l_data

        # PILAR 3: HYBRID (ITEM 130-135)
        h_val = [sinkron[0] if sinkron else "0", lawan[0] if lawan else "9"]
        
        res_data["t2"].append({"m": apply_f(sinkron), "h": h_val})
        res_data["t1"].append({"m": apply_f(sinkron[1:]+sinkron[:1]), "h": h_val})
        res_data["t3"].append({"m": apply_f(lawan), "h": h_val})
        
        # MASTER ANALYSER
        m_list = sorted(sinkron if sinkron else scored, key=lambda x: Counter("".join(data[-lb:])).get(x,0), reverse=True)
        res_data["t4"].append({"m": apply_f(m_list), "h": h_val})
        res_data["t5"].append([x for x in scored if x not in m_list[:4]] + ["-"]*10)
        
    return res_data

# --- 7. DISPLAY TABEL (ITEM 141-160+) ---
if st.session_state.history:
    final_res = get_predictions(st.session_state.history, p_filter)
    if final_res:
        l_std = 4 if p_filter != "Semua" else 6
        l_ext = 4 if p_filter != "Semua" else 8
        
        def render_val(lst, r_idx, limit_val, hyb_data):
            if r_idx >= limit_val - 2: 
                return hyb_data[r_idx - (limit_val - 2)]
            return lst[r_idx] if r_idx < len(lst) else "-"
        
        t_confs = [("🍀 TABEL SEIMBANG", "t1", g1, l_std), ("🔥 TABEL AKURAT", "t2", g2, l_std), ("❄️ TABEL KONTRA", "t3", g3, l_ext)]
        for title, k, gr, lim in t_confs:
            st.subheader(title)
            t_html = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
            for r in range(lim):
                t_html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
                for c in range(4):
                    col_d = final_res[k][c]
                    t_html += f"<td style='background:{gr};'>{render_val(col_d['m'], r, lim, col_d['h'])}</td>"
                t_html += "</tr>"
            st.markdown(t_html + "</table>", unsafe_allow_html=True)

        st.subheader("💎 TABEL MASTER")
        m_html = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(l_std):
            m_html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
            for c in range(4):
                m_d = final_res["t4"][c]
                m_html += f"<td style='background:{gradien_options['Emas Mewah']};'>{render_val(m_d['m'], r, l_std, m_d['h'])}</td>"
            m_html += "</tr>"
        st.markdown(m_html + "</table>", unsafe_allow_html=True)

        st.subheader("💀 TABEL ELIMINASI")
        e_html = "<table class='predict-table'><tr><th>DEAD</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(8):
            e_html += f"<tr><td style='font-size:12px; background:red;'>DEAD</td>"
            for c in range(4):
                e_html += f"<td style='background:#232526; color:red;'>{final_res['t5'][c][r]}</td>"
            e_html += "</tr>"
        st.markdown(e_html + "</table>", unsafe_allow_html=True)
