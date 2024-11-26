# html_templates.py

import streamlit as st

# HTML 템플릿 렌더링 함수
def render_html_template():
    html_content = """
    <!DOCTYPE html>
    <meta http-equiv="Content-Language" content="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="상대가치 평가 자동화 툴 (한양대학교 LABA2기 - 나현종 교수)">
        <meta name="author" content="나현종">
        <meta name="keywords" content="가치평가, 기업가치평가, 상대가치평가 자동화, 자동화, 상대가치, PER, PBR, EV/EBITDA, LABA">
        <title>기업가치 평가</title>
        <style>
        .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a {
            display: none;  /* 앵커 링크(사슬 아이콘) 숨기기 */
        }
        </style>
    </head>
    </html>
    """
    st.markdown(html_content, unsafe_allow_html=True)

# 로고와 제목 표시 함수
def display_logo_and_title():
    st.markdown(
        """
        <div style="position: absolute; top: 10px; right: 10px; display: flex; align-items: center; gap: 10px; font-family: Arial, sans-serif;">
            <img src="https://lh4.googleusercontent.com/proxy/ZNxI8np7zCKwnobg5G4-fBouL-6TIHB8AlsrUCdU7iEbhjZ72O3v39qjCa6OeDKAItStcHIHtvWKQnmwXoWsXFJffSd6cJuF4GwVj8MzBKU8D5W0Fw741y7o0rwx3j17clU" alt="로고" style="width: 50px; height: 50px; object-fit: contain;">
            <div style="color: #005BAC; font-size: 24px; font-weight: bold;">
                상대가치 평가 자동화
            </div>
            <div style="color: #005BAC; font-size: 16px;">
                LABA2기 (김예찬, 서진영, 이연지, 이채연 (ㄱㄴㄷ순)) <br>
                지도교수 나현종
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
