from konlpy.tag import Okt
import streamlit as st

@st.cache_resource
def get_okt():
    return Okt()

def preprocess_text_okt_batch(texts, target_pos):
    okt = get_okt()
    results = []
    for text in texts:
        if isinstance(text, str):
            words = [word for word, pos in okt.pos(text) if pos in target_pos]
            results.append(' '.join(words))
        else:
            results.append("")
    return results
