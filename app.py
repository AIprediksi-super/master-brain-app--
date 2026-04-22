import streamlit as st
import numpy as np
import easyocr
from PIL import Image
from collections import Counter

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])
reader = load_ocr()

st.set_page_config(page_title="Master Brain Ultra-Sim", layout="wide")
st.title("🧠 Master Brain: Ultra-Simulation Mode")

if 'history' not in st.session_state:
    st.session_state.history = []

st.sidebar.header("Data Entry")
input_mode = st.sidebar.selectbox("Pilih Input:", ["Upload Screenshot", "Input Manual"])

final_data = []
if input_mode == "Upload Screenshot":
    up_file = st.file_uploader("Upload Gambar:", type=["png", "jpg", "jpeg"])
    if up_file:
        img = Image.open(up_file)
        results = reader.readtext(np.array(img), detail=0)
        final_data = [str(x).upper() for x in results if len(str(x)) <= 5]
else:
    manual = st.text_input("Ketik data (pisahkan spasi):").upper()
    final_data = manual.split()

def get_top_5_analysis(data):
    if len(data) < 3: return []
    last_val = data[-1]
    weights = np.linspace(0.5, 1.0, len(data)-1)
    trans = {}
    for i in range(len(data)-1):
        if data[i] == last_val:
            nxt = data[i+1]
            trans[nxt] = trans.get(nxt, 0) + weights[i]
    return sorted(trans.items(), key=lambda x: x, reverse=True)[:5]

if final_data:
    top_5 = get_top_5_analysis(final_data)
    st.subheader("🏆 5 Prediksi Terbaik")
    if top_5:
        cols = st.columns(5)
        for i, (res, weight) in enumerate(top_5):
            cols[i].metric(f"Rank {i+1}", res)
else:
    st.info("Masukkan data atau upload screenshot untuk mulai.")
