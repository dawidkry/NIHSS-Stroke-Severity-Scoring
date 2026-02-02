import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="NIH Stroke Scale", page_icon="🧠", layout="centered")

# --- CUSTOM CSS (Matching your screenshots) ---
st.markdown("""
    <style>
    /* Clean, modern font stack */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Blue Card for active question */
    div.row-widget.stRadio {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    
    /* Blue border for the currently active/selected question */
    div.row-widget.stRadio:focus-within {
        border: 2px solid #3b82f6;
    }

    /* Yellow Coma Warning Box (Custom CSS to match your photo) */
    .coma-alert {
        background-color: #fffbeb;
        color: #92400e;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #fde68a;
        margin-bottom: 24px;
        font-size: 0.95rem;
    }

    /* Blue "Info" Box for instructions */
    .info-box {
        background-color: #eff6ff;
        color: #1e40af;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #bfdbfe;
        margin-bottom: 15px;
        font-size: 0.85rem;
    }

    /* Styling the Score Box */
    .score-container {
        text-align: center;
        padding: 20px;
        background-color: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }

    /* Remove Streamlit header/footer */
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

# --- HEADER SECTION ---
col_title, col_reset = st.columns([4, 1])
with col_title:
    st.title("NIH Stroke Scale")
    st.caption("Accurate stroke severity assessment")
with col_reset:
    st.button("Reset", on_click=reset_all, use_container_width=True)

# Placeholder for the Score (which calculates later but displays here)
score_placeholder = st.empty()

# --- DATA ---
COMA_RULES = {"1b": 2, "1c": 2, "2": 1, "3": 1, "4": 2, "5a": 4, "5b": 4, "6a": 4, "6b": 4, "7": 0, "8": 2, "9": 3, "10": 2, "11": 2}

# --- CALCULATOR LOGIC ---
current_scores = {}

# 1a. Level of Consciousness
st.markdown("**1a Level of Consciousness**")
# Blue Info Box for 1a instructions
st.markdown('<div class="info-box">The investigator must choose a response if a full evaluation is prevented by obstacles such as endotracheal tube, language barrier, or bandages.</div>', unsafe_allow_html=True)

loc_options = [
    "0 - Alert (Keenly responsive)",
    "1 - Not Alert (Arousable by minor stimulation)",
    "2 - Not Alert (Requires repeated stimulation)",
    "3 - Unresponsive (Coma)"
]

loc_choice = st.radio("Select LOC", loc_options, label_visibility="collapsed", key=f"1a_{st.session_state.reset_key}")
loc_score = int(loc_choice[0])
current_scores["1a"] = loc_score
is_coma = (loc_score == 3)

# 2. Yellow Coma Alert (Triggered by 1a=3)
if is_coma:
    st.markdown(f"""
    <div class="coma-alert">
        <strong>⚠️ Coma State Detected (1a = 3)</strong><br>
        Default coma scores have been automatically applied to items 1b, 1c, 8, 9, 10, and 11 per NIHSS guidelines. These locked items are indicated with a border.
    </div>
    """, unsafe_allow_html=True)

# --- Remaining Items List ---
# (Shortened for brevity, use your full NIHSS_ITEMS list here)
ITEMS = [
    {"id": "1b", "name": "1b LOC Questions", "opts": ["0 - Both correct", "1 - One correct", "2 - Neither correct"]},
    {"id": "1c", "name": "1c LOC Commands", "opts": ["0 - Both correct", "1 - One correct", "2 - Neither correct"]},
    {"id": "2", "name": "2 Best Gaze", "opts": ["0 - Normal", "1 - Partial palsy", "2 - Forced deviation"]},
    # ... add the rest of your items here
]

for item in ITEMS:
    st.markdown(f"**{item['name']}**")
    if is_coma and item['id'] in COMA_RULES:
        auto_val = COMA_RULES[item['id']]
        current_scores[item['id']] = auto_val
        st.radio(item['name'], item['opts'], index=auto_val, disabled=True, label_visibility="collapsed", key=f"{item['id']}_{st.session_state.reset_key}")
    else:
        choice = st.radio(item['name'], item['opts'], label_visibility="collapsed", key=f"{item['id']}_{st.session_state.reset_key}")
        current_scores[item['id']] = int(choice[0])

# --- FINAL SCORE CALCULATION ---
total_score = sum(current_scores.values())

with score_placeholder:
    st.markdown(f"""
    <div class="score-container">
        <div style="font-size: 0.9rem; color: #64748b; font-weight: 600;">Total Score</div>
        <div style="font-size: 3rem; font-weight: 700; color: #1e40af;">{total_score}</div>
        <div style="font-size: 0.9rem; color: #94a3b8;">out of 42</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
