import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(base_folder="data"):
    processed_texts = pd.read_csv(os.path.join(base_folder, 'processed_texts.csv'), encoding='utf-8-sig')
    financial = pd.read_csv(os.path.join(base_folder, 'financial.csv'), encoding='utf-8-sig')
    return processed_texts, financial

def load_stopwords(file_path):
    """텍스트 파일에서 불용어 목록을 읽어와 리스트로 반환"""
    with open(file_path, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f]
    return stopwords
