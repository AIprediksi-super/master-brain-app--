import streamlit as st
from collections import Counter
import random

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="Master Brain v15.5 Final", layout="wide")
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. THEMES & CSS ---
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

st.markdown(f"""
    <style>
    .stApp {{ background: {t_app['bg']}; color: {t_app['txt']}; }}
    .predict-table {{ width: 100%; border-collapse: separate; border-spacing: 5px; margin-bottom: 25px; }}
    .predict-table td {{ border-radius: 12px; padding: 15px; text-align: center; font-size: 32px; font-weight: 900; color: white !important; -webkit-text-stroke: 1.5px black; text-shadow: 2px 2px 5px #000; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. FILTER & INPUT ---
p_filter = st.radio("Saring hasil angka:", ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], horizontal=True)
manual_input = st.text_area("Tempel Data 4-Digit:", height=150, key="input_area")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input: 
            st.session_state.history = manual_input.replace(',', ' ').replace('\n', ' ').split()
with c2: st.button("🗑️ HAPUS TEKS", on_click=lambda: st.session_state.update({"input_area": ""}))
with c3: st.button("🔴 RESET", on_click=lambda: st.session_state.update({"history": [], "input_area": ""}))

# --- 4. ENGINE OTAK UTAMA ---
def get_predictions(data, f_mode):
    if not data: return {}
    all_rows = [[int(c) for c in item if c.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if not all_rows: return {}

    lb = max(10, min(25, len(all_rows)))
    segmen = all_rows[-lb:]
    res_final = {"t1": [], "t2": [], "t3": [], "t4": [], "t5": []}

    for i in range(4):
        col_full = [r[i] for r in all_rows]
        col_seg = [r[i] for r in segmen]
        scored_all = sorted([str(x) for x in range(10)], key=lambda x: (col_seg.count(int(x))*6 + col_full.count(int(x))*0.5), reverse=True)
        
        is_ganjil = sum(1 for x in col_seg if x % 2 != 0) >= (lb/2)
        is_besar = sum(1 for x in col_seg if x >= 5) >= (lb/2)
        
        sinkron = [a for a in scored_all if ((int(a)%2!=0) == is_ganjil) and ((int(a)>=5) == is_besar)]
        lawan = [a for a in scored_all if a not in sinkron]

        def apply_filter(lst):
            if f_mode == "Ganjil": r = [x for x in lst if int(x)%2!=0]
            elif f_mode == "Genap": r = [x for x in lst if int(x)%2==0]
            elif f_mode == "Kecil (0-4)": r = [x for x in lst if int(x)<=4]
            elif f_mode == "Besar (5-9)": r = [x for x in lst if int(x)>=5]
            else: r = lst
            return r

        # Pilar 3 Hybrid (Ambil dari sinkron dan lawan)
        h1 = sinkron[0] if sinkron else "0"
        h2 = lawan[0] if lawan else "9"

        res_final["t2"].append({"main": apply_filter(sinkron), "hyb": [h1, h2]})
        res_final["t1"].append({"main": apply_filter(sinkron[1:] + sinkron[:1]), "hyb": [h1, h2]})
        res_final["t3"].append({"main": apply_filter(lawan), "hyb": [h1, h2]})
        
        cnt = Counter([str(x) for r in segmen for x in r])
        m_list = sorted(sinkron if sinkron else scored_all, key=lambda x: cnt[x], reverse=True)
        res_final["t4"].append({"main": apply_filter(m_list), "hyb": [h1, h2]})
        res_final["t5"].append([x for x in scored_all if x not in m_list[:4]])

    return res_final

# --- 5. DISPLAY TABEL ---
if st.session_state.history:
    res = get_predictions(st.session_state.history, p_filter)
    if res:
        l_std = 4 if p_filter != "Semua" else 6
        l_ext = 4 if p_filter != "Semua" else 8
        
        def safe_get(lst, idx): return lst[idx] if idx < len(lst) else "-"

        confs = [("🍀 TABEL SEIMBANG", "t1", gradien_options[p_t1], l_std), 
                 ("🔥 TABEL AKURAT", "t2", gradien_options[p_t2], l_std), 
                 ("❄️ TABEL KONTRA", "t3", gradien_options[p_t3], l_ext)]
        
        for title, key, grad, limit in confs:
            st.subheader(title)
            html = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
            for r in range(limit):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
                for c in range(4):
                    d = res[key][c]
                    if r >= limit - 2: # Baris terakhir selalu Hybrid
                        val = d["hyb"][0] if r == limit - 2 else d["hyb"][1]
                    else:
                        val = safe_get(d["main"], r)
                    html += f"<td style='background:{grad};'>{val}</td>"
                html += "</tr>"
            st.markdown(html + "</table>", unsafe_allow_html=True)

        st.subheader("💎 TABEL MASTER")
        html_m = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(l_std):
            html_m += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
            for c in range(4):
                d = res["t4"][c]
                val = d["hyb"][0] if r == l_std - 2 else (d["hyb"][1] if r == l_std - 1 else safe_get(d["main"], r))
                html_m += f"<td style='background:linear-gradient(135deg, #FFD700, #B8860B);'>{val}</td>"
            html_m += "</tr>"
        st.markdown(html_m + "</table>", unsafe_allow_html=True)

        st.subheader("💀 TABEL ELIMINASI")
        html_e = "<table class='predict-table'><tr><th>DEAD</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(8):
            html_e += "<tr><td style='font-size:12px; background:red;'>DEAD</td>"
            for c in range(4):
                val = safe_get(res["t5"][c], r)
                html_e += f"<td style='background:#232526; color:red;'>{val}</td>"
            html_e += "</tr>"
        st.markdown(html_e + "</table>", unsafe_allow_html=True)
