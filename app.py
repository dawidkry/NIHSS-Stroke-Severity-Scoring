import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="NIHSS Calculator", page_icon="🧠", layout="centered")

# Hide the Streamlit "hamburger" menu and footer for an even cleaner look
st.markdown("""
    <style>
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
    {"id": "1a", "name": "1a. Level of Consciousness", "options": ["0: Alert", "1: Not alert; but arousable", "2: Not alert; requires stimulation", "3: Coma"]},
    {"id": "1b", "name": "1b. LOC Questions", "options": ["0: Answers both correctly", "1: Answers one correctly", "2: Answers neither correctly"]},
    {"id": "1c", "name": "1c. LOC Commands", "options": ["0: Performs both correctly", "1: Performs one correctly", "2: Performs neither correctly"]},
    {"id": "2", "name": "2. Best Gaze", "options": ["0: Normal", "1: Partial gaze palsy", "2: Forced deviation"]},
    {"id": "3", "name": "3. Visual Fields", "options": ["0: No visual loss", "1: Partial hemianopia", "2: Complete hemianopia", "3: Bilateral hemianopia"]},
    {"id": "4", "name": "4. Facial Palsy", "options": ["0: Normal movement", "1: Minor paralysis", "2: Partial paralysis", "3: Complete paralysis"]},
    {"id": "5a", "name": "5a. Left Arm Motor", "options": ["0: No drift", "1: Drift", "2: Some effort against gravity", "3: No effort against gravity", "4: No movement", "UN: Untestable"]},
    {"id": "5b", "name": "5b. Right Arm Motor", "options": ["0: No drift", "1: Drift", "2: Some effort against gravity", "3: No effort against gravity", "4: No movement", "UN: Untestable"]},
    {"id": "6a", "name": "6a. Left Leg Motor", "options": ["0: No drift", "1: Drift", "2: Some effort against gravity", "3: No effort against gravity", "4: No movement", "UN: Untestable"]},
    {"id": "6b", "name": "6b. Right Leg Motor", "options": ["0: No drift", "1: Drift", "2: Some effort against gravity", "3: No effort against gravity", "4: No movement", "UN: Untestable"]},
    {"id": "7", "name": "7. Limb Ataxia", "options": ["0: Absent", "1: Present in one limb", "2: Present in two limbs", "UN: Untestable"]},
    {"id": "8", "name": "8. Sensory", "options": ["0: Normal", "1: Mild-to-moderate loss", "2: Severe-to-total loss"]},
    {"id": "9", "name": "9. Best Language", "options": ["0: No aphasia", "1: Mild-to-moderate aphasia", "2: Severe aphasia", "3: Mute/Global aphasia"]},
    {"id": "10", "name": "10. Dysarthria", "options": ["0: Normal", "1: Mild-to-moderate dysarthria", "2: Severe dysarthria", "UN: Untestable"]},
    {"id": "11", "name": "11. Extinction/Inattention", "options": ["0: No abnormality", "1: Visual/tactile/auditory inattention", "2: Profound hemi-inattention"]}
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

# --- UI LAYOUT ---
st.title("NIH Stroke Scale")

# 1. Total Score Metric (Stays at top)
score_placeholder = st.empty()

# 2. Reset Button (Full width)
st.button("🔄 Reset Calculator", on_click=reset_all, use_container_width=True)
st.divider()

# --- INPUT PROCESSING ---
current_scores = {}

# LOC 1a (The trigger)
loc_choice = st.radio(
    NIHSS_ITEMS[0]["name"], 
    NIHSS_ITEMS[0]["options"], 
    horizontal=True, 
    key=f"1a_{st.session_state.reset_key}"
)
loc_score = int(loc_choice[0])
current_scores["1a"] = loc_score
is_coma = (loc_score == 3)

# Clinical Presumption Box (Top Position)
if is_coma:
    st.error("🚨 **CLINICAL PRESUMPTION: SEVERE STROKE**")
    st.info("**Patient in Coma (LOC 1a=3).** Large territory ischemic stroke presumed. Maximum deficit scores auto-applied.")

# All other items
for item in NIHSS_ITEMS[1:]:
    item_id = item["id"]
    
    if is_coma and item_id in COMA_RULES:
        auto_val = COMA_RULES[item_id]
        current_scores[item_id] = auto_val
        st.radio(item["name"], item["options"], index=auto_val, disabled=True, horizontal=True, key=f"{item_id}_{st.session_state.reset_key}")
    else:
        choice = st.radio(item["name"], item["options"], horizontal=True, key=f"{item_id}_{st.session_state.reset_key}")
        current_scores[item_id] = 0 if "UN" in choice else int(choice[0])

# Update the Score Metric at the top
total_score = sum(current_scores.values())
interpretation, delta_color = get_interpretation(total_score)

with score_placeholder:
    st.metric(label="Total NIHSS Score", value=f"{total_score} / 42", delta=interpretation, delta_color=delta_color)
