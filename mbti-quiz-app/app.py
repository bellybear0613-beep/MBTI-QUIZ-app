import streamlit as st
import json
import os

st.set_page_config(page_title="MBTI_QUIZ_APP", layout="centered")

st.sidebar.title("MBTI_QUIZ_APP")
st.sidebar.info("학번: 2024404008") 
st.sidebar.info("이름: 김규리") 

@st.cache_data
def load_quiz_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'answers' not in st.session_state:
    st.session_state['answers'] = {}

def login_screen():
    st.header("🔑 테스트를 위해 로그인해주세요")
    st.write("제시된 아이디와 비밀번호로 로그인하세요.")
    
    with st.form("login_form"):
        user_id = st.text_input("아이디 (학번)", placeholder="2024404008")
        user_pw = st.text_input("비밀번호", type="password", placeholder="040122")
        submit_button = st.form_submit_button("로그인")
        
        if submit_button:
            if user_id == "2024404008" and user_pw == "040122": 
                st.session_state['logged_in'] = True
                st.success("로그인 성공! 테스트를 시작합니다.")
                st.rerun()
            else:
                st.error("학번 또는 비밀번호가 틀렸습니다.")

def quiz_screen():
    quiz_data = load_quiz_data("users.json")
    
    if not quiz_data:
        st.error("데이터 파일(users.json)을 찾을 수 없습니다.")
        return

    st.header("📊 나만의 MBTI 성향 테스트")
    st.caption("모든 질문에 답한 뒤 최하단의 결과 확인 버튼을 눌러주세요.")
    st.divider()

    for q in quiz_data:
        st.subheader(f"Q{q['id']}. {q['text']}")
        options_labels = [opt['label'] for opt in q['options']]
        
        choice = st.radio(
            f"선택지_{q['id']}",
            options_labels,
            index=None,
            key=f"q_{q['id']}",
            label_visibility="collapsed"
        )
        
        if choice:
            selected_score = next(opt['score'] for opt in q['options'] if opt['label'] == choice)
            st.session_state['answers'][q['id']] = selected_score
        st.write("")

    st.divider()

    if st.button("✨ 결과 확인하기", use_container_width=True):
        if len(st.session_state['answers']) < len(quiz_data):
            st.warning("아직 답변하지 않은 문항이 있습니다!")
        else:
            show_result()

def show_result():
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for ans_score in st.session_state['answers'].values():
        scores[ans_score] += 1
    
    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"
    
    st.balloons()
    st.success(f"당신의 성향 분석 결과는 **[{mbti}]** 입니다!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**에너지 방향:** {'외향(E)' if mbti[0]=='E' else '내향(I)'}")
        st.write(f"**인식 방식:** {'감각(S)' if mbti[1]=='S' else '직관(N)'}")
    with col2:
        st.write(f"**판단 근거:** {'사고(T)' if mbti[2]=='T' else '감정(F)'}")
        st.write(f"**생활 양식:** {'판단(J)' if mbti[3]=='J' else '인식(P)'}")

    if st.button("다시 테스트하기"):
        st.session_state['answers'] = {}
        st.rerun()

if not st.session_state['logged_in']:
    login_screen()
else:
    if st.sidebar.button("로그아웃"):
        st.session_state['logged_in'] = False
        st.session_state['answers'] = {}
        st.rerun()
    
    quiz_screen()