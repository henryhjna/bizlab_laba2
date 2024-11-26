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