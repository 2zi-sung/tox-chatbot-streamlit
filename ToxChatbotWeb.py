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

st.markdown(
    """
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #4A90E2;  /* 푸른 계열 색상 */
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
            background-color: #00008b;
            padding: 10px;
            border-left: 5px solid #4A90E2;
            border-radius: 5px;
            margin-top: 10px;
        }
    </style>

    <h1 class="title">Tox-Info Chatbot</h1>

    <p class="intro">
        본 페이지는 챗봇의 질문-답변 정확성 검증을 위한 <span class="highlight">데모 서버</span>입니다.
        UI 디자인이나 부가적인 기능 구현은 제외되었으며, 오로지 질의응답 테스트만을 목적으로 제공됩니다.
        
        정확한 답변을 얻기 위해서는 '물질명 + 전문보기 항목' 형식으로 입력하시기 바랍니다.
    </p>

    <div class="example">
        <b><질문 예시></b><br>
        - <b>에탄올</b>의 흡수 과정에 대해 알려줘.<br>
        - <b>메틸파라티온</b>의 독성 데이터를 제공해줘.
    </div>

    <p style="text-align: center; margin-top: 15px;">
        📌 위와 같은 방식으로 질문하면 <span class="highlight">더 정확한 답변</span>을 받을 수 있어요! 😊
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
        st.markdown(answer.replace("\n", "  \n"), unsafe_allow_html=True)
