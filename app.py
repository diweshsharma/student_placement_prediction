import streamlit as st
import requests

st.set_page_config(
    page_title="Placement Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #080818; }
.block-container { padding: 2rem 4rem; max-width: 1200px; }

.header-wrap { text-align: center; padding: 2rem 0 2.5rem 0; }
.main-title { font-size: 30px; font-weight: 600; color: #F0F0FF; margin-bottom: 10px; letter-spacing: -0.5px; }
.main-sub { font-size: 14px; color: #5A5A7A; }

.section-card { background: #0F0F24; border: 1px solid #1C1C3A; border-radius: 14px; padding: 1.5rem 1.75rem; margin-bottom: 1.25rem; }
.section-label { font-size: 11px; font-weight: 600; color: #5B52D6; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 8px; }
.section-label::after { content: ''; flex: 1; height: 1px; background: #1C1C3A; }

.placed-card { background: linear-gradient(135deg, #071A07 0%, #0A2A0A 100%); border: 1px solid #1A4A1A; border-radius: 14px; padding: 1.75rem; }
.placed-status { font-size: 12px; color: #4CAF50; font-weight: 500; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
.placed-salary { font-size: 36px; font-weight: 600; color: #69BB6C; line-height: 1; letter-spacing: -1px; }
.placed-unit { font-size: 13px; color: #2E7D32; margin-top: 6px; }

.notplaced-card { background: linear-gradient(135deg, #1A0707 0%, #2A0A0A 100%); border: 1px solid #4A1A1A; border-radius: 14px; padding: 1.75rem; }
.notplaced-title { font-size: 16px; font-weight: 600; color: #EF9A9A; margin-bottom: 4px; }
.notplaced-sub { font-size: 12px; color: #9E3A3A; margin-bottom: 1.25rem; }
.weak-label { font-size: 10px; font-weight: 600; color: #CF6679; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
.tag-wrap { display: flex; flex-wrap: wrap; gap: 6px; }
.tag { background: #2D0F0F; color: #F48FB1; font-size: 11px; padding: 5px 13px; border-radius: 20px; font-weight: 500; border: 1px solid #5C1A1A; }

.empty-card { background: #0F0F24; border: 1px solid #1C1C3A; border-radius: 14px; padding: 3rem 2rem; text-align: center; }
.empty-icon { font-size: 36px; margin-bottom: 14px; }
.empty-text { font-size: 13px; color: #4A4A6A; line-height: 1.7; }

.ai-card { background: #0A0A1F; border: 1px solid #2A2A50; border-radius: 14px; padding: 1.5rem 1.75rem; margin-top: 1.25rem; }
.ai-label { font-size: 10px; font-weight: 600; color: #7B72F0; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px; }
.ai-text { font-size: 13px; color: #9A9ABB; line-height: 1.8; }

div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #5B52D6, #4A3FC4);
    color: #F0F0FF;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 14px;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    margin-top: 0.5rem;
    letter-spacing: 0.01em;
}
div[data-testid="stButton"] > button:hover { background: linear-gradient(135deg, #4A42C4, #3A30B0); }

div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label { font-size: 12px; color: #6A6A8A !important; font-family: 'Inter', sans-serif; }

section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-wrap">
    <div class="main-title">Student Placement Predictor</div>
    <div class="main-sub">Enter your academic and skill profile to predict your placement outcome</div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Academic Profile</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        branch = st.selectbox('Branch', ["CSE", "ECE", "EE", "IT", "ME", "CE", "Chemical"])
    with c2:
        college_tier = st.selectbox('College Tier', ['Tier-1', 'Tier-2', 'Tier-3'])

    c3, c4 = st.columns(2)
    with c3:
        cgpa = st.slider('CGPA', min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    with c4:
        backlogs = st.slider('Backlogs', min_value=0, max_value=10, value=0)

    c5, c6 = st.columns(2)
    with c5:
        internships = st.slider('Internships', min_value=0, max_value=5, value=0)
    with c6:
        projects_count = st.slider('Projects', min_value=0, max_value=20, value=3)

    c7, c8 = st.columns(2)
    with c7:
        certifications = st.slider('Certifications', min_value=0, max_value=20, value=2)
    with c8:
        hackathons = st.slider('Hackathons', min_value=0, max_value=20, value=1)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Technical & Soft Skills</div>', unsafe_allow_html=True)

    c9, c10 = st.columns(2)
    with c9:
        coding_skills = st.slider('Coding Skills', min_value=1, max_value=10, value=5)
        ml_knowledge = st.slider('ML Knowledge', min_value=0.0, max_value=10.0, value=5.0)
        communication_skills = st.slider('Communication', min_value=0.0, max_value=10.0, value=5.0)
    with c10:
        dsa_score = st.slider('DSA Score', min_value=0.0, max_value=10.0, value=5.0)
        system_design = st.slider('System Design', min_value=0.0, max_value=10.0, value=5.0)
        aptitude_score = st.slider('Aptitude Score', min_value=0.0, max_value=100.0, value=50.0)

    c11, c12 = st.columns(2)
    with c11:
        open_source_contributions = st.slider('Open Source', min_value=0, max_value=20, value=1)
    with c12:
        extracurriculars = st.selectbox('Extracurriculars', [0, 1, 2, 3],
                                         format_func=lambda x: ['None', 'Low', 'Medium', 'High'][x])

    predict_btn = st.button('Predict My Placement')
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    if predict_btn:
        payload = {
            "branch": branch, "college_tier": college_tier, "cgpa": cgpa,
            "backlogs": backlogs, "coding_skills": coding_skills, "dsa_score": dsa_score,
            "aptitude_score": aptitude_score, "communication_skills": communication_skills,
            "ml_knowledge": ml_knowledge, "system_design": system_design,
            "internships": internships, "projects_count": projects_count,
            "certifications": certifications, "hackathons": hackathons,
            "open_source_contributions": open_source_contributions,
            "extracurriculars": extracurriculars
        }
        with st.spinner("Analyzing your profile..."):
            try:
                response = requests.post("http://127.0.0.1:8000/predict", json=payload)
                st.session_state['result'] = response.json()
                st.session_state['suggestions'] = None
            except Exception as e:
                st.error(f"Could not connect to API. Make sure FastAPI is running.\n\n{e}")

    if 'result' in st.session_state and st.session_state['result']:
        result = st.session_state['result']

        if result['status'] == 'Placed':
            st.markdown(f"""
            <div class="placed-card">
                <div class="placed-status">✓ Placement predicted</div>
                <div class="placed-salary">{result['salary']}</div>
                <div class="placed-unit">Expected salary package</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            tags_html = "".join([
                f'<span class="tag">↑ {area.replace("_", " ").title()}</span>'
                for area in result['weak_areas']
            ])
            st.markdown(f"""
            <div class="notplaced-card">
                <div class="notplaced-title">Low placement probability</div>
                <div class="notplaced-sub">Focus on these areas to improve your chances</div>
                <div class="weak-label">Weak areas identified</div>
                <div class="tag-wrap">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("✦ Get AI Improvement Suggestions"):
                with st.spinner("Generating suggestions..."):
                    try:
                        ai_response = requests.post(
                            "http://127.0.0.1:8000/suggestions",
                            json={"weak_areas": result['weak_areas']}
                        )
                        st.session_state['suggestions'] = ai_response.json()['suggestions']
                    except:
                        st.session_state['suggestions'] = "AI suggestions unavailable."

    else:
        st.markdown("""
        <div class="empty-card">
            <div class="empty-icon">🎓</div>
            <div class="empty-text">Fill in your profile on the left<br>and click <strong style="color:#7B72F0;">Predict My Placement</strong></div>
        </div>
        """, unsafe_allow_html=True)

if st.session_state.get('suggestions'):
    suggestions_html = st.session_state['suggestions'].replace('\n', '<br>')
    st.markdown(f"""
    <div class="ai-card">
        <div class="ai-label">✦ AI Improvement Suggestions</div>
        <div class="ai-text">{suggestions_html}</div>
    </div>
    """, unsafe_allow_html=True)
