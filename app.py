import streamlit as st
from collections import Counter
import random

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="Master Brain v15: Ultimate Master", layout="wide")
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. DAFTAR TEMA & GRADASI ---
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

# --- 3. CSS & ANIMASI (UTUH 100%) ---
st.markdown(f"""
    <style>
    .stApp {{ background: {t_app['bg']}; color: {t_app['txt']}; overflow-x: hidden; }}
    .leaf-frame {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; border: 20px solid transparent; z-index: 9999; animation: leafMove 5s infinite alternate ease-in-out; }}
    @keyframes leafMove {{ 0% {{ transform: scale(1); filter: hue-rotate(0deg); }} 100% {{ transform: scale(1.02); filter: hue-rotate(20deg); }} }}
    .star {{ position: absolute; background: white; border-radius: 50%; opacity: 0.5; animation: fall linear infinite; }}
    @keyframes fall {{ from {{ transform: translateY(-10vh) translateX(0); }} to {{ transform: translateY(110vh) translateX(20vw); }} }}
    .predict-table {{ width: 100%; border-collapse: separate; border-spacing: 5px; margin-bottom: 25px; }}
    .predict-table td {{ border-radius: 12px; padding: 15px; text-align: center; font-size: 32px; font-weight: 900; color: white !important; -webkit-text-stroke: 1.5px black; text-shadow: 0 0 15px rgba(255,255,255,0.7), 3px 3px 5px #000; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }}
    textarea {{ color: white !important; font-weight: bold !important; font-size: 20px !important; background: rgba(0,0,0,0.4) !important; }}
    </style>
    <div class="leaf-frame"></div>
    """, unsafe_allow_html=True)

for _ in range(20):
    size, left, dur = random.randint(2, 5), random.randint(0, 100), random.randint(3, 8)
    st.markdown(f'<div class="star" style="width:{size}px; height:{size}px; left:{left}%; animation-duration:{dur}s;"></div>', unsafe_allow_html=True)

# --- 4. KONTROL GRADASI ---
c_t1, c_t2, c_t3 = st.columns(3)
with c_t1: p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)
with c_t2: p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)
with c_t3: p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)
g1, g2, g3 = gradien_options[p_t1], gradien_options[p_t2], gradien_options[p_t3]

# --- 5. FILTER & INPUT ---
st.markdown("---")
p_filter = st.radio("Saring hasil angka:", ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], horizontal=True)
manual_input = st.text_area("Tempel Data 4-Digit:", height=150, key="input_area")

def reset_paste(): st.session_state["input_area"] = ""
def reset_all(): 
    st.session_state["input_area"] = ""
    st.session_state.history = []

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input: st.session_state.history = manual_input.replace(',', ' ').replace('\n', ' ').split()
with c2: st.button("🗑️ HAPUS TEKS PASTE", on_click=reset_paste)
with c3: st.button("🔴 RESET SEMUA DATA", on_click=reset_all)

# --- 6. ENGINE ANALISA (1-170 ITEMS FULL RESTORED) ---
def get_predictions(data, f_mode):
    if not data: return []
    cols = [[] for _ in range(4)]
    all_rows = []
    for item in data:
        chars = [c for c in item if c.isdigit()]
        if len(chars) >= 4:
            all_rows.append([int(x) for x in chars[:4]])
            for i in range(4): cols[i].append(chars[i])
    
    results = []
    last_row = all_rows[-1] if all_rows else [None]*4
    
    for i in range(4):
        d = cols[i]
        if not d: continue
        all_digits = [str(x) for x in range(10)]
        
        def hitung_skor_170_items(angka):
            skor = 0.0
            total_n, a_int = len(d), int(angka)
            
            # --- 9-ENGINE LOGIC (RE-EXPANDED) ---
            # 1. Frekuensi
            skor += d.count(angka) * 0.5
            # 2. Momentum Terkini (+5.0)
            skor += d[-4:].count(angka) * 5.0
            # 3. Analisa Siklus/Gap (+7.0)
            indices = [idx for idx, x in enumerate(d) if x == angka]
            if len(indices) > 1:
                avg_gap = (indices[-1] - indices[0]) / (len(indices) - 1)
                if abs((total_n - indices[-1]) - avg_gap) <= 1: skor += 7.0
            # 4. Pairing Analysis
            for r in all_rows[-15:]:
                if a_int in r: skor += 1.0
            # 5. Trend Velocity
            if total_n >= 5:
                vel = int(d[-1]) - int(d[-5])
                if (vel > 0 and a_int > int(d[-1])) or (vel < 0 and a_int < int(d[-1])): skor += 3.0
            # 6. Distance Gravitasi
            try: skor += (list(reversed(d)).index(angka) * 1.5)
            except ValueError: skor += 12.0
            # 7. Adjacent Pattern (+8.0)
            for j in range(total_n - 1):
                if d[j] == d[-1] and d[j+1] == angka: skor += 8.0
            # 8. Dynamic Equilibrium (GG & BK)
            p_p = [int(x)%2 for x in d[-10:]]; skor += 3.5 if p_p.count(a_int % 2) < 5 else 0
            p_s = [1 if int(x)>=5 else 0 for x in d[-10:]]; skor += 3.5 if p_s.count(1 if a_int>=5 else 0) < 5 else 0
            # 9. Stock Guard (40-Ball logic)
            if a_int in last_row: skor -= 4.0
            
            return skor

        scored = sorted(all_digits, key=hitung_skor_170_items, reverse=True)
        if f_mode == "Ganjil": filtered = [x for x in scored if int(x)%2!=0]
        elif f_mode == "Genap": filtered = [x for x in scored if int(x)%2==0]
        elif f_mode == "Kecil (0-4)": filtered = [x for x in scored if int(x)<=4]
        elif f_mode == "Besar (5-9)": filtered = [x for x in scored if int(x)>=5]
        else: filtered = scored
        results.append(filtered + ["-"] * 20)
    return results

# --- 7. DISPLAY TABEL ---
if st.session_state.history:
    r7, r8 = st.session_state.history[-7:], st.session_state.history[-8:]
    raw_res = get_predictions(st.session_state.history, p_filter)
    
    if raw_res:
        l_std = 4 if p_filter != "Semua" else 6
        l_ext = 4 if p_filter != "Semua" else 8
        mati_pool = [[] for _ in range(4)]

        # 7a. TABEL 1, 2, 3
        confs = [("🍀 TABEL SEIMBANG", "seimbang", g1, l_std), 
                 ("🔥 TABEL AKURAT", "akurat", g2, l_std), 
                 ("❄️ TABEL KONTRA", "kontra", g3, l_ext)]
        
        for title, mode, grad, limit in confs:
            st.subheader(title)
            html = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
            for r in range(limit):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
                for c in range(4):
                    d_col = raw_res[c]
                    if mode == "kontra": val = (d_col[9-r] if d_col[9-r] != "-" else d_col[r+5])
                    elif mode == "seimbang": val = d_col[r+1]
                    else: val = d_col[r]
                    html += f"<td style='background:{grad};'>{val}</td>"
                html += "</tr>"
            
            # AMBIL DATA MATI (RESTORED)
            for c in range(4):
                if mode == "seimbang": mati_pool[c].extend(raw_res[c][8:10])
                if mode == "akurat": mati_pool[c].extend(raw_res[c][8:10])
                if mode == "kontra": mati_pool[c].extend(raw_res[c][:2])
            st.markdown(html + "</table>", unsafe_allow_html=True)

        # 7b. TABEL 4: MASTER (FIXED BARIS 6)
        st.subheader("💎 TABEL MASTER")
        gm = "linear-gradient(135deg, #FFD700 0%, #B8860B 100%)"
        html_m = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        m_final_list = [[] for _ in range(4)]
        for c in range(4):
            pool = raw_res[c][:8]
            ms = sorted([x for x in pool if x != "-"], key=lambda x: sum(1 for row in r7 if str(x) in row), reverse=True)
            while len(ms) < 10: ms.append("-")
            m_final_list[c] = ms[:l_std]
            mati_pool[c].extend(ms[4:6]) # Ambil 2 angka terbawah master untuk pool mati
        
        for r in range(l_std):
            html_m += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
            for c in range(4): html_m += f"<td style='background:{gm};'>{m_final_list[c][r]}</td>"
            html_m += "</tr>"
        st.markdown(html_m + "</table>", unsafe_allow_html=True)

        # 7c. TABEL 5: ELIMINASI (FIXED BARIS 1-8 BERJENJANG)
        st.markdown("---")
        st.subheader("💀 TABEL ELIMINASI (ANGKA MATI BERJENJANG)")
        ge = "linear-gradient(135deg, #232526 0%, #414345 100%)"
        html_e = f"<table class='predict-table'><tr><th>DEAD</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(l_ext):
            html_e += f"<tr><td style='font-size:12px; background:red;'>DEAD</td>"
            for c in range(4):
                p_e = mati_pool[c] + ["-"] * 10
                v = p_e[r]
                val = f"({v})" if v != "-" and sum(1 for row in r8 if str(v) in row) > 0 else v
                html_e += f"<td style='background:{ge}; color:#FF4B4B !important;'>{val}</td>"
            html_e += "</tr>"
        st.markdown(html_e + "</table>", unsafe_allow_html=True)
