import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="NIHSS Calculator", page_icon="🧠", layout="centered")

# --- CUSTOM CSS (Matching your screenshots) ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Card-like containers for questions */
    div.row-widget.stRadio {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

    /* Total Score Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    
    /* Header styling */
    h1 {
        font-weight: 800 !important;
        color: #0f172a !important;
        letter-spacing: -0.025em;
    }

    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DATA & RULES ---
COMA_RULES = {
    "1b": 2, "1c": 2, "2": 1, "3": 1, "4": 2, "5a": 4, "5b": 4, 
    "6a": 4, "6b": 4, "7": 0, "8": 2, "9": 3, "10": 2, "11": 2
}

NIHSS_ITEMS = [
    {"id": "1a", "name": "1a. Level of Consciousness", "options": ["0: Alert", "1: Not alert; arousable", "2: Not alert; requires stimulation", "3: Coma"]},
    {"id": "1b", "name": "1b. LOC Questions", "options": ["0: Both correct", "1: One correct", "2: Neither correct"]},
    {"id": "1c", "name": "1c. LOC Commands", "options": ["0: Both correct", "1: One correct", "2: Neither correct"]},
    {"id": "2", "name": "2. Best Gaze", "options": ["0: Normal", "1: Partial palsy", "2: Forced deviation"]},
    {"id": "3", "name": "3. Visual Fields", "options": ["0: No loss", "1: Partial", "2: Complete", "3: Bilateral"]},
    {"id": "4", "name": "4. Facial Palsy", "options": ["0: Normal", "1: Minor", "2: Partial", "3: Complete"]},
    {"id": "5a", "name": "5a. Left Arm Motor", "options": ["0: No drift", "1: Drift", "2: Effort vs gravity", "3: No effort vs gravity", "4: No movement", "UN: Untestable"]},
    {"id": "5b", "name": "5b. Right Arm Motor", "options": ["0: No drift", "1: Drift", "2: Effort vs gravity", "3: No effort vs gravity", "4: No movement", "UN: Untestable"]},
    {"id": "6a", "name": "6a. Left Leg Motor", "options": ["0: No drift", "1: Drift", "2: Effort vs gravity", "3: No effort vs gravity", "4: No movement", "UN: Untestable"]},
    {"id": "6b", "name": "6b. Right Leg Motor", "options": ["0: No drift", "1: Drift", "2: Effort vs gravity", "3: No effort against gravity", "4: No movement", "UN: Untestable"]},
    {"id": "7", "name": "7. Limb Ataxia", "options": ["0: Absent", "1: Present in one", "2: Present in two", "UN: Untestable"]},
    {"id": "8", "name": "8. Sensory", "options": ["0: Normal", "1: Mild-moderate loss", "2: Severe-total loss"]},
    {"id": "9", "name": "9. Best Language", "options": ["0: No aphasia", "1: Mild-moderate", "2: Severe", "3: Mute/Global"]},
    {"id": "10", "name": "10. Dysarthria", "options": ["0: Normal", "1: Mild-moderate", "2: Severe", "UN: Untestable"]},
    {"id": "11", "name": "11. Extinction/Inattention", "options": ["0: No abnormality", "1: Partial inattention", "2: Profound inattention"]}
]

def get_interpretation(score):
    if score == 0: return "No Stroke Symptoms", "normal"
    elif 1 <= score <= 4: return "Minor Stroke", "normal"
    elif 5 <= score <= 15: return "Moderate Stroke", "inverse"
    elif 16 <= score <= 20: return "Moderate to Severe", "inverse"
    else: return "Severe Stroke", "inverse"

# --- RESET LOGIC ---
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

def reset_all():
    st.session_state.reset_key += 1

# --- HEADER ---
st.title("NIH Stroke Scale")

# Floating Score Container
with st.container():
    score_box = st.empty()
    st.button("🔄 Reset Calculator", on_click=reset_all, use_container_width=True)

st.write("") # Spacing

# --- INPUT SECTION ---
current_scores = {}

# 1. Trigger Item (LOC 1a)
loc_choice = st.radio(
    NIHSS_ITEMS[0]["name"], 
    NIHSS_ITEMS[0]["options"], 
    horizontal=True, 
    key=f"1a_{st.session_state.reset_key}"
)
loc_score = int(loc_choice[0])
current_scores["1a"] = loc_score
is_coma = (loc_score == 3)

# Clinical Presumption Warning
if is_coma:
    st.error("**CLINICAL PRESUMPTION: SEVERE STROKE**")
    st.info("Coma Protocol (LOC 1a=3). Guidelines require presumed maximum deficit for untestable items.")

# 2. Remaining Items
for item in NIHSS_ITEMS[1:]:
    item_id = item["id"]
    if is_coma and item_id in COMA_RULES:
        auto_val = COMA_RULES[item_id]
        current_scores[item_id] = auto_val
        st.radio(item["name"], item["options"], index=auto_val, disabled=True, horizontal=True, key=f"{item_id}_{st.session_state.reset_key}")
    else:
        choice = st.radio(item["name"], item["options"], horizontal=True, key=f"{item_id}_{st.session_state.reset_key}")
        current_scores[item_id] = 0 if "UN" in choice else int(choice[0])

# --- FINAL CALCULATION ---
total_score = sum(current_scores.values())
interp, color = get_interpretation(total_score)

with score_box:
    # Stylized Result Card
    st.metric(label="NIHSS Total Score", value=f"{total_score} / 42", delta=interp, delta_color=color)
    st.divider()
