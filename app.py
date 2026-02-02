import streamlit as st

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="NIHSS Calculator", page_icon="🧠")

# Custom CSS to make it look professional like your original app
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e9ecef; }
    </style>
    """, unsafe_allow_html=True)

# --- NIHSS DATA ---
# Extracted from your nihss-data.ts and nihss-calculator.tsx files
NIHSS_ITEMS = [
    {"id": "1a", "name": "1a. Level of Consciousness", "options": ["0: Alert", "1: Not alert; but arousable", "2: Not alert; requires stimulation", "3: Coma"]},
    {"id": "1b", "name": "1b. LOC Questions", "options": ["0: Answers both correctly", "1: Answers one correctly", "2: Answers neither correctly"], "coma_default": 2},
    {"id": "1c", "name": "1c. LOC Commands", "options": ["0: Performs both correctly", "1: Performs one correctly", "2: Performs neither correctly"], "coma_default": 2},
    {"id": "2", "name": "2. Best Gaze", "options": ["0: Normal", "1: Partial gaze palsy", "2: Forced deviation"], "coma_default": 1},
    {"id": "3", "name": "3. Visual Fields", "options": ["0: No visual loss", "1: Partial hemianopia", "2: Complete hemianopia", "3: Bilateral hemianopia"], "coma_default": 1},
    {"id": "4", "name": "4. Facial Palsy", "options": ["0: Normal movement", "1: Minor paralysis", "2: Partial paralysis", "3: Complete paralysis"], "coma_default": 2},
    {"id": "5a", "name": "5a. Left Arm Motor", "options": ["0: No drift", "1: Drift", "2: Some effort against gravity", "3: No effort against gravity", "4: No movement", "UN: Untestable"], "coma_default": 4},
    {"id": "5b", "name": "5b. Right Arm Motor", "options": ["0: No drift", "1: Drift", "2: Some effort against gravity", "3: No effort against gravity", "4: No movement", "UN: Untestable"], "coma_default": 4},
    {"id": "6a", "name": "6a. Left Leg Motor", "options": ["0: No drift", "1: Drift", "2: Some effort against gravity", "3: No effort against gravity", "4: No movement", "UN: Untestable"], "coma_default": 4},
    {"id": "6b", "name": "6b. Right Leg Motor", "options": ["0: No drift", "1: Drift", "2: Some effort against gravity", "3: No effort against gravity", "4: No movement", "UN: Untestable"], "coma_default": 4},
    {"id": "7", "name": "7. Limb Ataxia", "options": ["0: Absent", "1: Present in one limb", "2: Present in two limbs", "UN: Untestable"], "coma_default": 0},
    {"id": "8", "name": "8. Sensory", "options": ["0: Normal", "1: Mild-to-moderate loss", "2: Severe-to-total loss"], "coma_default": 2},
    {"id": "9", "name": "9. Best Language", "options": ["0: No aphasia", "1: Mild-to-moderate aphasia", "2: Severe aphasia", "3: Mute/Global aphasia"], "coma_default": 3},
    {"id": "10", "name": "10. Dysarthria", "options": ["0: Normal", "1: Mild-to-moderate dysarthria", "2: Severe dysarthria", "UN: Untestable"], "coma_default": 2},
    {"id": "11", "name": "11. Extinction/Inattention", "options": ["0: No abnormality", "1: Visual/tactile/auditory inattention", "2: Profound hemi-inattention"], "coma_default": 2}
]

def get_severity(score):
    if score == 0: return "No Stroke Symptoms", "normal"
    elif 1 <= score <= 4: return "Minor Stroke", "normal"
    elif 5 <= score <= 15: return "Moderate Stroke", "inverse"
    elif 16 <= score <= 20: return "Moderate to Severe", "inverse"
    else: return "Severe Stroke", "inverse"

# --- APP UI ---
st.title("🧠 NIHSS Score Calculator")
st.caption("Professional Stroke Assessment Tool with Automatic Coma Scoring")

# Initialize scores in session state
if 'scores' not in st.session_state:
    st.session_state.scores = {item['id']: 0 for item in NIHSS_ITEMS}

# Header Section with Reset
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Reset Form"):
        st.session_state.scores = {item['id']: 0 for item in NIHSS_ITEMS}
        st.rerun()

# --- COMA LOGIC CHECK ---
# If 1a is 3 (Coma), trigger guidelines
is_coma = st.session_state.scores.get("1a") == 3

if is_coma:
    st.warning("⚠️ Coma Protocol Active: Guidelines automatically applied to affected items.")

# --- RENDER QUESTIONS ---
for item in NIHSS_ITEMS:
    # Check if item is locked due to coma
    disabled = is_coma and 'coma_default' in item
    
    # Auto-update score if locked
    if disabled:
        st.session_state.scores[item['id']] = item['coma_default']

    # Display Radio buttons
    selected = st.radio(
        label=item['name'],
        options=item['options'],
        index=st.session_state.scores[item['id']] if st.session_state.scores[item['id']] < len(item['options']) else 0,
        key=f"radio_{item['id']}",
        disabled=disabled,
        horizontal=True
    )
    
    # Store numerical value (first char of selection)
    if "UN:" in selected:
        st.session_state.scores[item['id']] = 0
    else:
        st.session_state.scores[item['id']] = int(selected[0])

# --- RESULTS SUMMARY ---
total_score = sum(st.session_state.scores.values())
severity, delta_type = get_severity(total_score)

st.divider()
st.subheader("Assessment Result")
st.metric(label="Total NIHSS Score", value=total_score, delta=severity, delta_color=delta_type)

with st.expander("About NIHSS Scoring Guidelines"):
    st.write("""
    This calculator implements official NIHSS guidelines. When a patient is scored a 3 on item 1a (Coma), 
    the scale dictates that items 1b, 1c, 8, 9, 10, and 11 receive specific default scores because the 
    patient is untestable in those domains.
    """)
