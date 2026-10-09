"""
Ledger — design system.

Visual language: a private underwriting desk, not a consumer fintech app.
Deep ink-teal background (not literal black), bone/parchment text (not
pure white or cream), aged-brass accent evoking ledger hardware and old
financial print. Serif for headlines and numerals (ledger typography),
clean sans for UI and form fields. Horizontal-rule structure over
boxed cards; right-aligned figures in the financial-statement tradition.
"""

# --- Palette ---
INK = "#0F1B1E"            # primary background — deep ink-teal, not pure black
PANEL = "#16262A"          # slightly raised surface (sidebar, panels)
PANEL_ALT = "#1C2E33"      # secondary surface (tables, inputs)
BONE = "#E8E4D9"           # primary text — warm bone, not pure white
BONE_DIM = "#9BA6A3"       # secondary / muted text
BRASS = "#B08D57"          # primary accent — aged brass, ledger hardware
BRASS_BRIGHT = "#C9A86A"   # brass hover/active state
SAGE = "#6FA98D"           # positive / approved
BRICK = "#B2584F"          # negative / rejected
RULE = "#2A3C40"           # hairline divider color

FONT_SERIF = "'Source Serif 4', 'Georgia', serif"
FONT_SANS = "'IBM Plex Sans', 'Inter', sans-serif"


def inject_css(st):
    """Call once at the top of app.py to apply the Ledger visual identity."""
    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: {FONT_SANS};
        }}

        .stApp {{
            background-color: {INK};
            color: {BONE};
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {PANEL};
            border-right: 1px solid {RULE};
        }}
        section[data-testid="stSidebar"] * {{
            color: {BONE} !important;
        }}

        /* Headings use the serif */
        .stApp h1, .stApp h2, .stApp h3,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            font-family: {FONT_SERIF} !important;
            color: {BONE} !important;
            font-weight: 500 !important;
            letter-spacing: 0.01em;
        }}

        .stApp h1 {{
            font-size: 2.6rem !important;
            border-bottom: 1px solid {RULE};
            padding-bottom: 0.7rem;
            margin-bottom: 0.4rem !important;
        }}

        .stApp h3 {{
            font-size: 1.35rem !important;
            margin-top: 2rem !important;
        }}

        /* Body text */
        p, label, span, div {{
            color: {BONE};
        }}

        /* Muted captions */
        .ledger-caption {{
            color: {BONE_DIM};
            font-size: 0.92rem;
            font-family: {FONT_SANS};
        }}

        /* Number & text inputs */
        .stNumberInput input, .stTextInput input {{
            background-color: {PANEL_ALT} !important;
            color: {BONE} !important;
            border: 1px solid {RULE} !important;
            border-radius: 2px !important;
        }}

        /* Number input +/- step buttons */
        .stNumberInput button {{
            background-color: {PANEL_ALT} !important;
            color: {BONE} !important;
            border: 1px solid {RULE} !important;
        }}

        /* Selectbox — this Streamlit version renders a React Aria ComboBox:
           a plain <input type="text"> showing the selected value, plus a
           listbox popover rendered in a portal at the document root. */
        .stSelectbox [role="group"],
        .stSelectbox input[role="combobox"] {{
            background-color: {PANEL_ALT} !important;
            color: {BONE} !important;
            border: 1px solid {RULE} !important;
            border-radius: 2px !important;
        }}

        .stSelectbox input[role="combobox"] {{
            caret-color: {BONE};
        }}

        .stSelectbox input[role="combobox"]::placeholder {{
            color: {BONE_DIM} !important;
            opacity: 1 !important;
        }}

        /* The open/chevron button sits inside the same bordered group;
           keep it transparent so only the group's single border shows */
        .stSelectbox [role="group"] button {{
            background-color: transparent !important;
            border: none !important;
        }}

        .stSelectbox svg {{
            fill: {BONE_DIM} !important;
        }}

        /* Popover listbox is portaled to <body>, outside .stSelectbox,
           so it needs its own top-level selectors */
        div[role="listbox"],
        [id*="react-aria"][role="listbox"] {{
            background-color: {PANEL_ALT} !important;
            border: 1px solid {RULE} !important;
        }}

        [role="option"] {{
            background-color: {PANEL_ALT} !important;
            color: {BONE} !important;
        }}
        [role="option"]:hover,
        [role="option"][aria-selected="true"],
        [role="option"][data-focused="true"] {{
            background-color: {RULE} !important;
            color: {BRASS_BRIGHT} !important;
        }}

        .stSlider [data-baseweb="slider"] {{
            color: {BRASS} !important;
        }}
        .stSlider [role="slider"] {{
            background-color: {BRASS} !important;
            border-color: {BRASS} !important;
        }}

        /* Input field labels */
        .stNumberInput label, .stTextInput label, .stSelectbox label {{
            color: {BONE_DIM} !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
        }}

        /* Primary button — brass accent, sharp corners, no shadow soup */
        .stButton > button {{
            background-color: {BRASS} !important;
            color: {INK} !important;
            border: none !important;
            border-radius: 2px !important;
            font-family: {FONT_SANS} !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em;
            padding: 0.6rem 1.6rem !important;
            transition: background-color 0.15s ease;
        }}
        .stButton > button:hover {{
            background-color: {BRASS_BRIGHT} !important;
        }}
        .stButton > button p {{
            color: {INK} !important;
            font-weight: 600 !important;
        }}

        /* Horizontal rule divider, used instead of boxed cards */
        .ledger-rule {{
            border: none;
            border-top: 1px solid {RULE};
            margin: 1.6rem 0;
        }}

        /* Result panel */
        .ledger-result {{
            background-color: {PANEL};
            border-left: 3px solid var(--result-color, {BRASS});
            padding: 1.4rem 1.8rem;
            margin: 1rem 0;
        }}

        .ledger-result-label {{
            font-family: {FONT_SANS};
            color: {BONE_DIM};
            font-size: 0.85rem;
            text-transform: none;
            margin-bottom: 0.3rem;
        }}

        .ledger-result-value {{
            font-family: {FONT_SERIF};
            font-size: 2.6rem;
            font-weight: 500;
            line-height: 1.1;
        }}

        .ledger-approved {{ color: {SAGE}; }}
        .ledger-rejected {{ color: {BRICK}; }}

        /* Dataframe / table styling */
        .stDataFrame, .stTable {{
            background-color: {PANEL_ALT} !important;
        }}

        /* Remove default streamlit top padding bloat */
        .block-container {{
            padding-top: 2.5rem;
            max-width: 920px;
        }}

        /* Metric widget restyle to match ledger numerals */
        [data-testid="stMetricValue"] {{
            font-family: {FONT_SERIF} !important;
            color: {BONE} !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {BONE_DIM} !important;
            font-family: {FONT_SANS} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def result_panel_html(label: str, value_text: str, is_approved: bool) -> str:
    """Returns HTML for the main prediction result panel."""
    color_class = "ledger-approved" if is_approved else "ledger-rejected"
    accent = SAGE if is_approved else BRICK
    return f"""
    <div class="ledger-result" style="--result-color: {accent};">
        <div class="ledger-result-label">{label}</div>
        <div class="ledger-result-value {color_class}">{value_text}</div>
    </div>
    """


def rule_html() -> str:
    return '<hr class="ledger-rule" />'

def result_animation_html(is_approved: bool) -> str:
    """Returns a small CSS-animated flourish shown alongside the result panel."""
    if is_approved:
        color = SAGE
        return f"""
        <div class="ledger-anim-wrap">
            <svg class="ledger-anim-approve" width="64" height="64" viewBox="0 0 64 64">
                <circle cx="32" cy="32" r="28" fill="none" stroke="{color}" stroke-width="3"
                        stroke-dasharray="176" stroke-dashoffset="176" class="ledger-circle"/>
                <path d="M20 33 L28 41 L45 23" fill="none" stroke="{color}" stroke-width="4"
                      stroke-linecap="round" stroke-linejoin="round"
                      stroke-dasharray="40" stroke-dashoffset="40" class="ledger-check"/>
            </svg>
        </div>
        <style>
            .ledger-anim-wrap {{ display: flex; justify-content: center; margin: 0.5rem 0 1rem 0; }}
            .ledger-circle {{ animation: draw-circle 0.6s ease-out forwards; }}
            .ledger-check {{ animation: draw-check 0.4s ease-out 0.5s forwards; }}
            @keyframes draw-circle {{ to {{ stroke-dashoffset: 0; }} }}
            @keyframes draw-check {{ to {{ stroke-dashoffset: 0; }} }}
        </style>
        """
    else:
        color = BRICK
        return f"""
        <div class="ledger-anim-wrap">
            <svg class="ledger-anim-reject" width="64" height="64" viewBox="0 0 64 64">
                <circle cx="32" cy="32" r="28" fill="none" stroke="{color}" stroke-width="3"
                        stroke-dasharray="176" stroke-dashoffset="176" class="ledger-circle"/>
                <line x1="23" y1="23" x2="41" y2="41" stroke="{color}" stroke-width="4"
                      stroke-linecap="round" stroke-dasharray="26" stroke-dashoffset="26" class="ledger-x1"/>
                <line x1="41" y1="23" x2="23" y2="41" stroke="{color}" stroke-width="4"
                      stroke-linecap="round" stroke-dasharray="26" stroke-dashoffset="26" class="ledger-x2"/>
            </svg>
        </div>
        <style>
            .ledger-anim-wrap {{ display: flex; justify-content: center; margin: 0.5rem 0 1rem 0; opacity: 0; animation: fade-in 0.4s ease-out forwards; }}
            .ledger-circle {{ animation: draw-circle 0.6s ease-out forwards; }}
            .ledger-x1 {{ animation: draw-x 0.3s ease-out 0.5s forwards; }}
            .ledger-x2 {{ animation: draw-x 0.3s ease-out 0.65s forwards; }}
            @keyframes draw-circle {{ to {{ stroke-dashoffset: 0; }} }}
            @keyframes draw-x {{ to {{ stroke-dashoffset: 0; }} }}
            @keyframes fade-in {{ to {{ opacity: 1; }} }}
        </style>
        """
