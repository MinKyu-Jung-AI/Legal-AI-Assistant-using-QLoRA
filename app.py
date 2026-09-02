import streamlit as st
from agent import Agent

st.set_page_config(
    page_title="동서울대학교 법률 챗봇",
    page_icon="⚖️",
    layout="wide"
)

@st.cache_resource
def get_agent():
    """
    Streamlit의 캐시 기능을 사용하여 Agent 객체를 앱 전체에서 한 번만 생성합니다.
    이렇게 하면 페이지를 이동하거나 위젯과 상호작용할 때마다
    무거운 Agent 모델을 다시 로드하는 것을 방지할 수 있습니다.
    """
    with st.spinner("법률 AI 에이전트를 준비하는 중입니다... 잠시만 기다려주세요."):
        agent_instance = Agent()
    return agent_instance

st.sidebar.title("📂 메뉴")
page = st.sidebar.radio(
    "페이지 선택",
    ["홈", "법률 챗봇 데모", "문의하기"]
)

# ===================================================================
# "홈" 페이지
# ===================================================================
if page == "홈":
    st.title("⚖️ 동서울대학교 법률 챗봇 사이트")
    st.subheader("개요")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown(
            """
            본 사이트는 동서울대학교 컴퓨터소프트웨어과 졸업 과제로 제작된 법률 챗봇입니다.  
            특히 개발자들이 자주 마주치는 지식 재산권(저작권, 상표, 오픈 소스 라이선스 등)과
            관련된 법적 부담 여부를 간단히 진단하고 정보를 제공하는 것을 목표로 합니다.
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            ### 🔹 주요 기능
            - **법률 정보 제공:** 저작권, 상표권 등 복잡한 법률 개념을 쉽게 풀어 설명합니다.
            - **사례 기반 진단:** 사용자의 상황을 입력하면, 관련된 법적 쟁점과 주의사항을 안내합니다.
            - **동적 정보 탐색:** 필요시, AI 에이전트가 웹에서 최신 정보를 찾아 답변에 활용합니다.
            """
        )
    with col_right:
        st.image("https://www.du.ac.kr/p/img/sub/logo.png", width=200 )
        st.info("사이드바의 '법률 챗봇 데모' 페이지에서 AI 챗봇을 사용해볼 수 있습니다.")

# ===================================================================
# "법률 챗봇 데모" 페이지
# ===================================================================
elif page == "법률 챗봇 데모":
    st.title("🤖 동서울대학교 법률 챗봇 ")
    st.caption("AI 에이전트에게 지식재산권 관련 질문을 해보세요.")

    agent = get_agent()
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "안녕하세요! 저는 지식재산권 법률 상담을 위해 설계된 AI 에이전트 '깡깡봇'입니다.\n"
                    "저작권, 상표, 오픈 소스 라이선스 등 궁금한 점을 질문해주세요."
                ),
            },
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if prompt := st.chat_input("저작권 관련 질문을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI가 답변을 생성하고 있습니다..."):
                try:
                    answer, meta = agent.answer(prompt)
                    
                    debug_info = (
                        f"초기 판단: `{meta.get('initial_action', 'N/A')}` → "
                        f"최종 액션: `{meta.get('final_action', 'N/A')}` | "
                        f"AI 평가 점수: `{meta.get('reward', 0.0):.2f}`"
                    )
                    
                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "debug": debug_info
                    })

                except Exception as e:
                    error_message = f"죄송합니다, 답변 생성 중 오류가 발생했습니다: {e}"
                    st.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message,
                        "debug": None
                    })

# ===================================================================
# "문의하기" 페이지
# ===================================================================
elif page == "문의하기":
    st.subheader("📨 문의 및 피드백")
    st.write("챗봇의 성능 개선을 위한 소중한 의견을 남겨주세요.")

    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("이름 (선택)")
        email = st.text_input("이메일 (선택)")
        category = st.selectbox(
            "문의 유형",
            ["답변 품질 피드백", "버그 제보", "기능 제안", "기타"]
        )
        message = st.text_area("내용을 입력하세요", height=150, placeholder="예: 'OOO'에 대한 답변이 부정확했어요.")

        submitted = st.form_submit_button("제출하기")

        if submitted:
            if not message:
                st.error("내용을 입력해주세요.")
            else:
                st.success("소중한 의견 감사합니다! 챗봇 개선에 큰 도움이 됩니다.")
