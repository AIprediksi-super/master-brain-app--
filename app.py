import streamlit as st
from collections import Counter
import random

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="Master Brain v15.5 Final Fix", layout="wide")
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. THEMES & CSS (TETAP) ---
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
    textarea {{ color: white !important; font-weight: bold !important; font-size: 20px !important; background: rgba(0,0,0,0.4) !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. FILTER & INPUT ---
st.markdown("---")
p_filter = st.radio("Saring hasil angka:", ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], horizontal=True)
manual_input = st.text_area("Tempel Data 4-Digit:", height=150, key="input_area")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input.strip(): 
            st.session_state.history = [x for x in manual_input.replace(',', ' ').replace('\n', ' ').split() if len(x) >= 4]
with c2: st.button("🗑️ HAPUS TEKS", on_click=lambda: st.session_state.update({"input_area": ""}))
with c3: st.button("🔴 RESET", on_click=lambda: st.session_state.update({"history": [], "input_area": ""}))

# --- 4. ENGINE OTAK UTAMA ---
def get_predictions(data, f_mode):
    if not data: return None
    all_rows = [[int(c) for c in item if c.isdigit()][:4] for item in data]
    
    lb = max(10, min(25, len(all_rows)))
    segmen = all_rows[-lb:]
    res_final = {"t1": [], "t2": [], "t3": [], "t4": [], "t5": []}

    for i in range(4):
        col_full = [r[i] for r in all_rows]
        col_seg = [r[i] for r in segmen]
        # Skor murni (Tanpa filter) untuk cadangan
        scored_pure = sorted([str(x) for x in range(10)], key=lambda x: (col_seg.count(int(x))*7 + col_full.count(int(x))*0.5), reverse=True)
        
        is_ganjil = sum(1 for x in col_seg if x % 2 != 0) >= (lb/2)
        is_besar = sum(1 for x in col_seg if x >= 5) >= (lb/2)
        
        sinkron = [a for a in scored_pure if ((int(a)%2!=0) == is_ganjil) and ((int(a)>=5) == is_besar)]
        lawan = [a for a in scored_pure if a not in sinkron]

        def get_filtered_list(lst):
            if f_mode == "Ganjil": return [x for x in lst if int(x)%2!=0]
            if f_mode == "Genap": return [x for x in lst if int(x)%2==0]
            if f_mode == "Kecil (0-4)": return [x for x in lst if int(x)<=4]
            if f_mode == "Besar (5-9)": return [x for x in lst if int(x)>=5]
            return lst

        # Pilar 3 Hybrid (Ambil satu unggul, satu lawan)
        h1 = sinkron[0] if sinkron else scored_pure[0]
        h2 = lawan[0] if lawan else scored_pure[-1]

        # Gabungkan: Data Filtered + Hybrid + Sisanya (agar tidak kosong)
        def build_final(primary_list):
            f = get_filtered_list(primary_list)
            # Pastikan pilar 3 juga disaring jika tombol filter aktif
            hyb_f = get_filtered_list([h1, h2]) 
            if not hyb_f: hyb_f = [h1, h2] # Jika pilar 3 kena filter, paksa tampilkan aslinya agar baris bawah terisi
            
            # Gabungkan semuanya dan tambahkan cadangan dari scored_pure agar kolom terisi penuh
            combined = f + hyb_f + get_filtered_list(scored_pure) + ["-"]*10
            return {"main": f, "pilar3": hyb_f, "full": combined}

        res_final["t2"].append(build_final(sinkron))
        res_final["t1"].append(build_final(sinkron[1:] + sinkron[:1]))
        res_final["t3"].append(build_final(lawan))
        
        cnt = Counter([str(x) for r in segmen for x in r])
        m_list = sorted(sinkron if sinkron else scored_pure, key=lambda x: cnt[x], reverse=True)
        res_final["t4"].append(build_final(m_list))
        res_final["t5"].append([x for x in scored_pure if x not in m_list[:4]] + ["-"]*10)

    return res_final

# --- 5. DISPLAY TABEL ---
if st.session_state.history:
    res = get_predictions(st.session_state.history, p_filter)
    if res:
        l_std = 4 if p_filter != "Semua" else 6
        l_ext = 4 if p_filter != "Semua" else 8
        
        confs = [("🍀 TABEL SEIMBANG", "t1", gradien_options[p_t1], l_std), 
                 ("🔥 TABEL AKURAT", "t2", gradien_options[p_t2], l_std), 
                 ("❄️ TABEL KONTRA", "t3", gradien_options[p_t3], l_ext)]
        
        for title, key, grad, limit in confs:
            st.subheader(title)
            html = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
            for r in range(limit):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
                for c in range(4):
                    d = res[key][c]
                    # Logika: 2 Baris Terakhir WAJIB PILAR 3
                    if r >= limit - 2:
                        val = d["pilar3"][r - (limit-2)] if (r - (limit-2)) < len(d["pilar3"]) else "-"
                    else:
                        val = d["full"][r]
                    html += f"<td style='background:{grad};'>{val}</td>"
                html += "</tr>"
            st.markdown(html + "</table>", unsafe_allow_html=True)

        # TABEL MASTER
        st.subheader("💎 TABEL MASTER")
        html_m = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(l_std):
            html_m += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
            for c in range(4):
                d = res["t4"][c]
                val = d["pilar3"][r - (l_std-2)] if r >= l_std - 2 else d["full"][r]
                html_m += f"<td style='background:linear-gradient(135deg, #FFD700, #B8860B);'>{val}</td>"
            html_m += "</tr>"
        st.markdown(html_m + "</table>", unsafe_allow_html=True)

        # TABEL ELIMINASI
        st.subheader("💀 TABEL ELIMINASI")
        html_e = "<table class='predict-table'><tr><th>DEAD</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(8):
            html_e += "<tr><td style='font-size:12px; background:red;'>DEAD</td>"
            for c in range(4):
                val = res["t5"][c][r]
                html_e += f"<td style='background:#232526; color:red;'>{val}</td>"
            html_e += "</tr>"
        st.markdown(html_e + "</table>", unsafe_allow_html=True)
else:
    st.info("👋 Masukkan minimal 10 baris data, lalu klik 'JALANKAN ANALISA'.")
