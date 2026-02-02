import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="NIH Stroke Scale", page_icon="🧠", layout="centered")

# --- CUSTOM CSS (Artistic Upgrades) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Font and Background */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #ffffff; }

    /* Card Styling for Questions */
    div.row-widget.stRadio {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* Replit-style Yellow Alert Box */
    .coma-alert {
        background-color: #fffbeb;
        color: #92400e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #fde68a;
        margin-bottom: 25px;
    }

    /* Blue Instruction Box */
    .info-box {
        background-color: #eff6ff;
        color: #1e40af;
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #bfdbfe;
        margin-bottom: 10px;
        font-size: 0.9rem;
    }

    /* Hide Streamlit Clutter */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- RESET LOGIC ---
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

def reset_all():
    st.session_state.reset_key += 1

# --- HEADER & SCORE ---
st.title("NIH Stroke Scale")
st.caption("Accurate stroke severity assessment")

# This empty slot allows the score to stay at the top while calculating from below
score_placeholder = st.empty()

st.button("🔄 Reset Calculator", on_click=reset_all, use_container_width=True)
st.divider()

# --- DATA & RULES ---
COMA_RULES = {
    "1b": 2, "1c": 2, "2": 1, "3": 1, "4": 2, "5a": 4, "5b": 4, 
    "6a": 4, "6b": 4, "7": 0, "8": 2, "9": 3, "10": 2, "11": 2
}

NIHSS_ITEMS = [
    {"id": "1a", "name": "1a. Level of Consciousness", "info": "A 3 is scored only if the patient makes no movement (other than reflexive) in response to noxious stimulation.", "options": ["0 - Alert (Keenly responsive)", "1 - Not Alert (Arousable by minor stimulation)", "2 - Not Alert (Requires repeated stimulation)", "3 - Unresponsive (Coma)"]},
    {"id": "1b", "name": "1b. LOC Questions", "options": ["0 - Answers both correctly", "1 - Answers one correctly", "2 - Answers neither correctly"]},
    {"id": "1c", "name": "1c. LOC Commands", "options": ["0 - Performs both correctly", "1 - Performs one correctly", "2 - Performs neither correctly"]},
    {"id": "2", "name": "2. Best Gaze", "options": ["0 - Normal", "1 - Partial gaze palsy", "2 - Forced deviation"]},
    {"id": "3", "name": "3. Visual Fields", "options": ["0 - No visual loss", "1 - Partial hemianopia", "2 - Complete hemianopia", "3 - Bilateral hemianopia"]},
    {"id": "4", "name": "4. Facial Palsy", "options": ["0 - Normal movement", "1 - Minor paralysis", "2 - Partial paralysis", "3 - Complete paralysis"]},
    {"id": "5a", "name": "5a. Left Arm Motor", "options": ["0 - No drift", "1 - Drift", "2 - Some effort against gravity", "3 - No effort against gravity", "4 - No movement", "UN - Untestable"]},
    {"id": "5b", "name": "5b. Right Arm Motor", "options": ["0 - No drift", "1 - Drift", "2 - Some effort against gravity", "3 - No effort against gravity", "4 - No movement", "UN - Untestable"]},
    {"id": "6a", "name": "6a. Left Leg Motor", "options": ["0 - No drift", "1 - Drift", "2 - Some effort against gravity", "3 - No effort against gravity", "4 - No movement", "UN - Untestable"]},
    {"id": "6b", "name": "6b. Right Leg Motor", "options": ["0 - No drift", "1 - Drift", "2 - Some effort against gravity", "3 - No effort against gravity", "4 - No movement", "UN - Untestable"]},
    {"id": "7", "name": "7. Limb Ataxia", "options": ["0 - Absent", "1 - Present in one limb", "2 - Present in two limbs", "UN - Untestable"]},
    {"id": "8", "name": "8. Sensory", "options": ["0 - Normal", "1 - Mild-to-moderate loss", "2 - Severe-to-total loss"]},
    {"id": "9", "name": "9. Best Language", "options": ["0 - No aphasia", "1 - Mild-to-moderate aphasia", "2 - Severe aphasia", "3 - Mute/Global aphasia"]},
    {"id": "10", "name": "10. Dysarthria", "options": ["0 - Normal", "1 - Mild-to-moderate dysarthria", "2 - Severe dysarthria", "UN - Untestable"]},
    {"id": "11", "name": "11. Extinction/Inattention", "options": ["0 - No abnormality", "1 - Partial inattention", "2 - Profound hemi-inattention"]}
]

def get_interpretation(score):
    if score == 0: return "No Stroke Symptoms", "normal"
    elif 1 <= score <= 4: return "Minor Stroke", "normal"
    elif 5 <= score <= 15: return "Moderate Stroke", "inverse"
    elif 16 <= score <= 20: return "Moderate to Severe", "inverse"
    else: return "Severe Stroke", "inverse"

# --- RENDER CALCULATOR ---
current_scores = {}

# 1. Item 1a with Instructions
st.markdown(f"### {NIHSS_ITEMS[0]['name']}")
st.markdown(f'<div class="info-box">ℹ️ {NIHSS_ITEMS[0]["info"]}</div>', unsafe_allow_html=True)
loc_choice = st.radio("LOC", NIHSS_ITEMS[0]["options"], label_visibility="collapsed", key=f"1a_{st.session_state.reset_key}")
loc_score = int(loc_choice[0])
current_scores["1a"] = loc_score
is_coma = (loc_score == 3)

# 2. Replit-style Yellow Coma Notice
if is_coma:
    st.markdown("""
    <div class="coma-alert">
        <strong>⚠️ Coma State Detected (1a = 3)</strong><br>
        Default coma scores have been automatically applied to items 1b, 1c, 8, 9, 10, and 11 per NIHSS guidelines. These locked items are indicated with a border.
    </div>
    """, unsafe_allow_html=True)

# 3. Loop through the rest of the 14 items
for item in NIHSS_ITEMS[1:]:
    st.markdown(f"### {item['name']}")
    item_id = item["id"]
    
    if is_coma and item_id in COMA_RULES:
        auto_val = COMA_RULES[item_id]
        current_scores[item_id] = auto_val
        st.radio(item["name"], item["options"], index=auto_val, disabled=True, label_visibility="collapsed", key=f"{item_id}_{st.session_state.reset_key}")
    else:
        choice = st.radio(item["name"], item["options"], label_visibility="collapsed", key=f"{item_id}_{st.session_state.reset_key}")
        current_scores[item_id] = 0 if "UN" in choice else int(choice[0])

# --- CALCULATE & UPDATE TOP METRIC ---
total_score = sum(current_scores.values())
interpretation, color_mode = get_interpretation(total_score)

with score_placeholder:
    st.metric(label="Patient Total NIHSS Score", value=f"{total_score} / 42", delta=interpretation, delta_color=color_mode)
    st.divider()
