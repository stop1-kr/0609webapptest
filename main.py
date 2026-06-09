import streamlit as st
import time

# 🎈 페이지 기본 설정 (가장 상단에 위치해야 함)
st.set_page_config(
    page_title="✨MBTI 진로 탐험대✨",
    page_icon="🚀",
    layout="centered"
)

# 🎨 커스텀 CSS (화려하고 예쁜 디자인 적용)
st.markdown("""
<style>
    /* 배경 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }
    
    /* 메인 타이틀 스타일 */
    .main-title {
        font-size: 3rem !important;
        font-weight: 900;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #ff9a9e, #fecfef, #a1c4fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 서브 타이틀 스타일 */
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 30px;
    }
    
    /* 결과 카드 스타일 */
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        text-align: center;
        border: 3px dashed #a1c4fd;
        margin-top: 20px;
    }
    
    .job-title {
        font-size: 2rem;
        color: #ff6b6b;
        font-weight: bold;
        margin: 15px 0;
    }
    
    .job-desc {
        font-size: 1.1rem;
        color: #4a4a4a;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# 📊 MBTI 별 직업 데이터베이스 (딕셔너리 활용)
mbti_jobs = {
    "ISTJ": {"name": "세상의 소금형 🧂", "jobs": "👮 경찰관, 📊 회계사, 🏛️ 공무원", "desc": "꼼꼼하고 책임감이 강하며, 정해진 규칙을 잘 따르는 당신! 체계적인 환경에서 빛을 발해요. ✨"},
    "ISFJ": {"name": "임금 뒷편의 권력형 🛡️", "jobs": "🏥 간호사, 📚 사서, 🧑‍🏫 교사", "desc": "따뜻한 마음으로 타인을 돕는 일에 보람을 느끼는 당신! 헌신적이고 세심한 배려가 돋보여요. 💖"},
    "INFJ": {"name": "예언자형 🔮", "jobs": "✍️ 작가, 🛋️ 심리상담사, 🎨 디자이너", "desc": "깊은 통찰력과 영감을 가진 당신! 사람들의 마음을 치유하고 창의적인 아이디어를 내는 일에 어울려요. 🌟"},
    "INTJ": {"name": "과학자형 🔬", "jobs": "💻 소프트웨어 개발자, 🔬 과학자, 📈 경영 컨설턴트", "desc": "전략적이고 분석적인 사고의 달인! 복잡한 문제를 해결하고 미래를 설계하는 일에 최고입니다. 🧠"},
    "ISTP": {"name": "백과사전형 📖", "jobs": "🔧 기계공학자, ✈️ 조종사, 🕵️ 탐정", "desc": "뛰어난 관찰력과 손재주를 가진 당신! 논리적이고 실용적으로 문제를 척척 해결해냅니다. 🛠️"},
    "ISFP": {"name": "성인군자형 🕊️", "jobs": "🖌️ 일러스트레이터, 🎵 음악가, 🌿 셰프", "desc": "아름다움을 사랑하고 감수성이 풍부한 당신! 예술적인 감각을 자유롭게 표현하는 직업이 딱이에요. 🎨"},
    "INFP": {"name": "잔다르크형 ⚔️", "jobs": "📖 시인, 🎬 영상 편집자, 🤝 사회복지사", "desc": "풍부한 상상력과 따뜻한 이상주의자! 자신의 가치관을 실현하고 세상을 아름답게 만드는 일에 끌려요. 🌈"},
    "INTP": {"name": "아이디어 뱅크형 💡", "jobs": "🧪 연구원, 🕹️ 게임 개발자, 📐 건축가", "desc": "지적 호기심이 넘치고 논리적인 당신! 끊임없이 탐구하고 새로운 것을 만들어내는 천재성이 있어요. 🧩"},
    "ESTP": {"name": "수완좋은 활동가형 🏃", "jobs": "🚀 창업가, 🚒 소방관, 💼 영업 매니저", "desc": "에너지가 넘치고 스릴을 즐기는 당신! 위기 상황에서도 빠른 판단력으로 활약하는 실전파입니다. 🔥"},
    "ESFP": {"name": "사교적인 유형 🎉", "jobs": "🎤 엔터테이너, 👗 패션 디자이너, 🏖️ 파티 플래너", "desc": "어디서나 분위기 메이커! 사람들과 어울리며 즐거움을 선사하는 활동적인 일이 제격이에요. 🥳"},
    "ENFP": {"name": "스파크형 ✨", "jobs": "💡 기획 마케터, 🎤 크리에이터, 🌍 여행 가이드", "desc": "열정적이고 통통 튀는 상상력의 소유자! 새로운 것에 도전하고 사람들에게 영감을 주는 일을 사랑해요. 🎈"},
    "ENTP": {"name": "발명가형 ⚙️", "jobs": "⚖️ 변호사, 💡 발명가, 🎬 기획자", "desc": "독창적이고 토론을 즐기는 당신! 뛰어난 언변과 기발한 아이디어로 세상을 놀라게 할 거예요. 🗣️"},
    "ESTJ": {"name": "사업가형 💼", "jobs": "🏢 경영자, 🏦 은행장, ⚖️ 판사", "desc": "체계적이고 리더십이 강한 당신! 조직을 이끌고 목표를 달성하는 데 타고난 재능이 있습니다. 🏆"},
    "ESFJ": {"name": "친선도모형 🤝", "jobs": "🏫 교장선생님, 🏨 호텔 지배인, 💖 인사 담당자", "desc": "친절하고 조화로움을 중시하는 당신! 사람들을 챙기고 공동체에 기여하는 일에서 큰 행복을 느껴요. 🌻"},
    "ENFJ": {"name": "언변능숙형 🗣️", "jobs": "👨‍🏫 강사, 🤝 PR 전문가, 🧑‍💼 정치인", "desc": "타인의 성장을 돕는 카리스마 리더! 뛰어난 공감 능력과 설득력으로 세상을 긍정적으로 변화시킵니다. 🌱"},
    "ENTJ": {"name": "지도자형 👑", "jobs": "🚀 CEO, 📈 투자 은행가, ⚖️ 경영 전략가", "desc": "대담하고 결단력 있는 당신! 거대한 비전을 세우고 진취적으로 밀어붙이는 타고난 리더입니다. 🦅"}
}

# 🚀 헤더 영역
st.markdown('<div class="main-title">✨ 나의 MBTI 진로 탐험대 🚀</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">당신의 성격 유형을 완성하고 <b>찰떡궁합 직업</b>을 알아보세요! 🌈</div>', unsafe_allow_html=True)

st.write("---")

# 🎛️ MBTI 선택 영역 (4가지 지표)
st.subheader("👇 당신의 성향을 선택해주세요 👇")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### ⚡ 에너지 방향")
    ie = st.radio("E / I", ["E (외향: 🗣️사람들과 함께)", "I (내향: 🤫혼자만의 시간)"])
with col2:
    st.markdown("### 🔍 인식 방식")
    sn = st.radio("S / N", ["S (감각: 👀현실과 경험)", "N (직관: 💡이상과 미래)"])
with col3:
    st.markdown("### 🧠 판단 방식")
    tf = st.radio("T / F", ["T (사고: ⚖️논리와 사실)", "F (감정: ❤️사람과 관계)"])
with col4:
    st.markdown("### 🗓️ 생활 양식")
    jp = st.radio("J / P", ["J (판단: 📝계획과 체계)", "P (인식: 🌊자율과 융통)"])

# 선택한 MBTI 조합하기
user_mbti = ie[0] + sn[0] + tf[0] + jp[0]

st.write("---")

# 🎁 결과 보기 버튼
if st.button("✨ 내 진로 결과 확인하기! 🎯", use_container_width=True):
    with st.spinner('🔮 당신의 미래를 탐색 중입니다...'):
        time.sleep(1.5) # 로딩 효과
        
    st.balloons() # 🎈 풍선 애니메이션
    
    result = mbti_jobs[user_mbti]
    
    # 결과 화면 출력 (HTML 적용)
    result_html = f"""
    <div class="result-card">
        <h3>🎉 당신의 MBTI는 <span style="color:#a1c4fd; font-size: 2.5rem;">{user_mbti}</span> 입니다! 🎉</h3>
        <p style="font-size: 1.2rem; color: #888;">{result['name']}</p>
        <hr style="border: 1px dashed #eee;">
        <p style="font-size: 1.2rem; margin-top: 15px;">🌟 <b>추천 직업 Top 3</b> 🌟</p>
        <div class="job-title">{result['jobs']}</div>
        <p class="job-desc">{result['desc']}</p>
    </div>
    """
    st.markdown(result_html, unsafe_allow_html=True)
    
    st.success("진로 탐색 완료! 이 직업들이 당신의 훌륭한 성향과 아주 잘 맞을 거예요! 💪😊")
