import streamlit as st
from modules.data_loader import load_data, load_stopwords
from modules.gpt_api import gptai, load_api_key
from modules.preprocessing import preprocess_text_okt_batch
from modules.valuation import preprocess_and_find_similar_companies
import pandas as pd

st.set_page_config(page_title="기업가치 평가", layout="wide")

# 불용어 로드
korean_stopwords = load_stopwords("resources/korean_stopwords.txt")
domain_stopwords = load_stopwords("resources/domain_stopwords.txt")

# 데이터 로드
processed_texts, financial = load_data()

# OpenAI API 키 로드
api_key = load_api_key()
use_model = "gpt-4"
system_message = "유저가 회사명을 입력하면 인터넷을 검색해서 해당 회사의 사업 개요(사업의 내용)를 서술하라. 마케팅 전략이나, 고객경험, 디자인, 사회공헌 활동, 재무성과 같은 것들은 언급하지 마시오."

# CSS 스타일 추가
st.markdown(
    """
    <style>
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a {
        display: none;  /* 앵커 링크(사슬 아이콘) 숨기기 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
def display_logo_and_title():
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://lh4.googleusercontent.com/proxy/ZNxI8np7zCKwnobg5G4-fBouL-6TIHB8AlsrUCdU7iEbhjZ72O3v39qjCa6OeDKAItStcHIHtvWKQnmwXoWsXFJffSd6cJuF4GwVj8MzBKU8D5W0Fw741y7o0rwx3j17clU" alt="로고" style="width: 300px; margin-bottom: 10px;">
            <h1 style="color: #005BAC; font-size: 32px;">상대가치 평가 자동화</h1>
            <h2 style="color: #005BAC; font-size: 24px;">LABA 2기</h2>
            <h3 style="color: #000000; font-size: 15px;">김예찬, 서진영, 이연지, 이채연 (ㄱㄴㄷ순)</h3>
            <h2 style="color: #005BAC; font-size: 24px;">지도교수</h2>
            <h3 style="color: #000000; font-size: 15px;">나현종</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# 호출
display_logo_and_title()

st.sidebar.title("기업가치 평가")
st.sidebar.markdown("---")

target_coname = st.sidebar.text_input("대상 회사명", "", placeholder="회사명을 입력하세요")

if target_coname.strip():  # 회사명이 입력되었을 경우
    dart_url = (
        f"https://dart.fss.or.kr/dsab007/detailSearch.ax?"
        f"currentPage=1&maxResults=15&textCrpNm={target_coname.strip()}&"
        f"publicType=A001&publicType=F001&publicType=F002&publicType=F004&"
        f"startDate=20201126&endDate=20241126"
    )
else:  # 회사명이 입력되지 않았을 경우 기본 URL
    dart_url = "https://dart.fss.or.kr/"

st.sidebar.markdown("---")  # 구분선 추가
st.sidebar.markdown(
    f"""
    #### 재무 지표를 모른다면?  
    [검색해보세요]({dart_url})
    """,
    unsafe_allow_html=True  # HTML 허용
)

st.sidebar.markdown("---")  
ni_target = st.sidebar.number_input("당기순이익 (억원)", value=0, placeholder="회사의 당기순이익을 입력하세요") * 1e8
teq_target = st.sidebar.number_input("자본총계 (억원)", value=0, placeholder="회사의 자본총계를 입력하세요") * 1e8
ebitda_target = st.sidebar.number_input("EBITDA (억원)", value=0, placeholder="회사의 EBITDA를 입력하세요") * 1e8

mktcap_options = {"평균 연간 시가총액": "avg_annual_mktcap", "현재 시가총액 (아직 안됌ㅠ)": "current_mktcap"}
mktcap_to_use = st.sidebar.selectbox("시가총액 기간", list(mktcap_options.keys()), index=0)
selected_mktcap = mktcap_options[mktcap_to_use]

st.sidebar.markdown("---")

if st.sidebar.button("결과 보기"):
    with st.spinner("분석 중입니다. 잠시만 기다려 주세요. 보통 1~2분 가량 소요됩니다."):
        response = gptai(use_model, 300, system_message, target_coname, api_key)
        if "error" in response:
            st.error(f"GPT 호출 오류: {response['message']} (상태 코드: {response['error']})")
        else:
            gpt_answer = response["choices"][0]["message"]["content"]
            gpt_answer_cleaned = preprocess_text_okt_batch([gpt_answer], target_pos=['Noun'])[0]
            # 함수 호출 부분
            result = preprocess_and_find_similar_companies(
                processed_texts,
                gpt_answer_cleaned,
                korean_stopwords + domain_stopwords,
                financial,
                selected_mktcap,  # 수정된 변수명
                ni_target,
                teq_target,
                ebitda_target
            )

            # 결과 처리 코드
            if result:
                (filtered_top_5, per_based_value, pbr_based_value, ev_ebitda_based_value,
                average_value, excluded_per_count, excluded_ev_ebitda_count,
                average_per, average_pbr, average_ev_ebitda) = result

                # 회사 소개 출력
                st.markdown(f"""
                <div style="background-color:#f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
                    <h3 style="color:#333; text-align:center;">[{target_coname} 회사소개]</h3>
                    <p style="line-height:1.6; color:#555; text-align:justify;">{gpt_answer}</p>
                </div>
                """, unsafe_allow_html=True)

                # 유사한 회사 목록 테이블 출력
                if not filtered_top_5.empty:
                    # 열 이름 변경: coname -> 회사명, similarity -> 유사도
                    renamed_top_5  = filtered_top_5.rename(columns={'coname': '회사명', 'similarity': '유사도'})
                    renamed_top_5['유사도'] = renamed_top_5['유사도'] * 100
                                        
                    st.markdown("### [가장 유사한 회사 목록]")
                    st.write(renamed_top_5 [['회사명', '유사도', 'PER', 'PBR', 'EV_EBITDA']].style
                            .set_table_styles([
                                {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f0f0')]},
                                {'selector': 'td', 'props': [('text-align', 'center')]},
                            ])
                            .format({
                                '유사도': '{:.1f}%',   # 유사도는 퍼센트 형식
                                'PER': '{:.2f}',      # PER은 소수점 둘째 자리
                                'PBR': '{:.2f}',      # PBR도 동일
                                'EV_EBITDA': '{:.2f}' # EV/EBITDA도 동일
                            })
                            .bar(subset=['유사도'], color='#ffddcc', vmin=0, vmax=100))  # 유사도에 따른 색상 강조

                # 가치평가 Multiples 출력
                st.markdown("### [가치평가 Multiples]")

                # 평균값 처리
                average_per_display = f"{average_per:,.2f}" if average_per is not None else "데이터 없음"
                average_pbr_display = f"{average_pbr:,.2f}" if average_pbr is not None else "데이터 없음"
                average_ev_ebitda_display = f"{average_ev_ebitda:,.2f}" if average_ev_ebitda is not None else "데이터 없음"

                st.markdown(f"""
                <ul>
                    <li>평균 PER: {average_per_display}</li>
                    <li>평균 PBR: {average_pbr_display}</li>
                    <li>평균 EV/EBITDA: {average_ev_ebitda_display}</li>
                </ul>
                """, unsafe_allow_html=True)

                # Multiple을 사용한 기업가치 계산 결과
                st.markdown("### [Multiple을 사용한 기업가치]")

                per_based_display = f"{per_based_value:,.2f}억 원" if per_based_value is not None else "계산 불가"
                pbr_based_display = f"{pbr_based_value:,.2f}억 원" if pbr_based_value is not None else "계산 불가"
                ev_ebitda_based_display = f"{ev_ebitda_based_value:,.2f}억 원" if ev_ebitda_based_value is not None else "계산 불가"
                average_value_display = f"{average_value:,.2f}억 원" if average_value is not None else "계산 불가"

                st.markdown(f"""
                <ul>
                    <li>PER을 사용한 기업가치: {per_based_display}</li>
                    <li>PBR을 사용한 기업가치: {pbr_based_display}</li>
                    <li>EV/EBITDA를 사용한 기업가치: {ev_ebitda_based_display}</li>
                    <li>평균 기업가치: {average_value_display}</li>
                </ul>
                """, unsafe_allow_html=True)

                # 제외된 회사 개수 출력
                st.markdown("### [계산시 특이사항]")
                st.markdown(f"""
                <p>PER 계산에서 제외된 회사: {excluded_per_count}개</p>
                <p>EV/EBITDA 계산에서 제외된 회사: {excluded_ev_ebitda_count}개</p>
                """, unsafe_allow_html=True)

            else:
                st.warning("유사한 회사를 찾을 수 없습니다.")
