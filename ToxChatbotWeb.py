import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL")
# BOT_AVATAR = os.getenv("BOT_AVATAR")
# USER_AVATAR = os.getenv("USER_AVATAR")
SIDE_BAR_IMG = os.getenv("SIDE_BAR_IMG")

BOT_AVATAR = "🤖"
USER_AVATAR = "🧑"

keywords = [
    "독성", "요약", "물질정보", "영문물질명", "국문물질명", "CAS No", "구조식", "분자식",
    "분자량", "영문유사명", "국문유사명", "색깔 및 성상", "냄새", "끓는점", "어는점", "증기압",
    "밀도/비중", "용해도", "GHS픽토그램", "용도", "독성정보", "인체 영향 정보", "인체영향-증상",
    "인체영향-사례보고", "인체영향-역학연구", "인체영향-기타", "동물 독성시험 정보", "급성 독성",
    "반복투여 독성", "생식발생 독성", "유전독성 및 변이원성", "눈/피부자극성", "면역 독성", "기타",
    "발암성", "발암성 등급 분류", "IARC분류", "NTP분류", "US EPA분류", "US EPA분류2", "US EPA분류3",
    "인체 발암성 정보", "동물 발암성시험 정보", "TD50 및 Acceptable Intake(AI) 정보", "독성동태학 정보",
    "인체 정보", "동물 정보", "흡수", "분포", "대사", "배설", "응급치료정보", "일반적 치료정보",
    "특이적 치료정보", "참고문헌", "URL", "관련DB링크", "국가위험물관리시스템",
    "화학물질정보검색시스템"
]

st.markdown(
    """
    <style>
        .title {
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            color: #00008b;  /* 푸른 계열 색상 */
        }
        .intro {
            font-size: 18px;
            font-weight: bold;
            color: #2E2E2E;
            text-align: center;
            background-color: #F4F8FF;
            padding: 15px;
            border-radius: 10px;
        }
        .highlight {
            font-weight: bold;
            color: #D0021B; /* 빨간색 강조 */
        }
        .example {
            font-size: 16px;
            background-color: #F4F8FF;
            text-align: justify;
            padding: 10px;
            border-left: 5px solid #4A90E2;
            border-radius: 5px;
            margin-top: 10px;
            color: #000000;
        }
    </style>

    <h1 class="title">Tox-Info Chatbot</h1>

    <p class="intro">
        본 페이지는 <span class="highlight">챗봇의 질문-답변 정확성 검증</span>을 위한 <span class="highlight">데모 서버</span>입니다.
        <br>UI 디자인이나 부가적인 기능 구현은 제외되었으며, <br><strong>오로지 질의응답 테스트</strong>만을 목적으로 제공됩니다.
    </p>

    <p class="intro">
        <strong>정확한 답변을 얻기 위해서는</strong> <span class="highlight">'물질명 + 전문보기 항목'</span> 형식으로 입력하시기 바랍니다.
    </p>

    <div class="example">
        <b><질문 예시></b><br>
        - <b><span class="title">에탄올</span></b>의 <span class="highlight">흡수</span> 과정에 대해 알려줘.<br>
        - <b><span class="title">포름알데하이드</span></b>의 <span class="highlight">발암성 등급</span>에 대해서 알려줘.
    </div>

    <p style="text-align: center; margin-top: 15px;">
        📌 위와 같은 방식으로 질문하면 <span class="highlight">더 정확한 답변</span>을 받을 수 있습니다.
    </p>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.image(SIDE_BAR_IMG)

if "conversation" not in st.session_state:
    st.session_state.conversation = []

for message in st.session_state.conversation:
    role, text = message
    avatar = USER_AVATAR if role == "user" else BOT_AVATAR
    with st.chat_message(role, avatar=avatar):
        st.markdown(text.replace("\n", "  \n"), unsafe_allow_html=True)

prompt = st.chat_input("💬 메시지를 입력하세요...")
if prompt:
    st.session_state.conversation.append(("user", prompt))
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt.replace("\n", "  \n"), unsafe_allow_html=True)

    with st.spinner("⏳ 답변 생성하는 중..."):
        try:
            response = requests.post(API_URL, json={"question": prompt}, timeout=10)
            response.raise_for_status()
            data = response.json()
            answer = data.get(
                "processed_output",
                "저는 독성정보 챗봇이에요.🤖🤖\n\n현재 제공된 정보로는 정확한 답변을 드리기 어려워요. 😵‍💫 \n\n"
                "독성정보와 관련된 질문을 해주시거나, 알고 싶은 내용을 더 구체적으로 말씀해 주시면 도움을 드릴 수 있을 것 같아요. \n\n"
                "질문을 작성하실 때, 정확한 물질의 이름과 알고자 하는 정보를 함께 포함해주세요. 예를 들어:\n\n"
                "- **에탄올의 흡수 과정에 대해 알려줘.**\n"
                "- **메틸파라티온의 독성 데이터를 제공해줘.**\n\n"
                "이런 방식으로 질문해 주시면 더 정확하고 자세한 답변을 드릴 수 있을 것 같아요! 😊"
            )
        except requests.exceptions.RequestException as e:
            answer = f"❌ 오류 발생: {str(e)}"
        except ValueError:
            answer = "⚠️ 서버에서 올바른 JSON 응답을 받지 못했어요.\n\n관리자에게 문의해주세요."

    st.session_state.conversation.append(("ai", answer))
    with st.chat_message("ai", avatar=BOT_AVATAR):
        for keyword in keywords:
            text = text.replace(keyword, f'<span style="font-size:20px; font-weight:bold;">{keyword}</span>')

        # st.markdown(text.replace("\n", "  \n"), unsafe_allow_html=True)
        st.markdown(answer.replace("\n", "  \n"), unsafe_allow_html=True)
