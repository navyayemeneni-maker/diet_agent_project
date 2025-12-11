"""
Diet Recommendation System - Final Version with Dashboard
=========================================================
Clean Streamlit app with 4 AI agents + Dashboard.
Author: Navya | December 2025
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
import os
import base64
from datetime import datetime
from fpdf import FPDF
import tempfile
import pandas as pd
import re

# Streamlit Extras for enhanced UI
try:
    from streamlit_extras.colored_header import colored_header
    from streamlit_extras.metric_cards import style_metric_cards
    from streamlit_extras.add_vertical_space import add_vertical_space
    EXTRAS_AVAILABLE = True
except ImportError:
    EXTRAS_AVAILABLE = False

# ============== SVG ICONS (Lucide) ==============
ICONS = {
    "home": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "dashboard": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>',
    "user": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "health": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
    "chat": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "info": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
    "salad": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 21h10"/><path d="M12 21a9 9 0 0 0 9-9H3a9 9 0 0 0 9 9Z"/><path d="M11.38 12a2.4 2.4 0 0 1-.4-4.77 2.4 2.4 0 0 1 3.2-2.77 2.4 2.4 0 0 1 3.47-.63 2.4 2.4 0 0 1 3.37 3.37 2.4 2.4 0 0 1-1.1 3.7 2.51 2.51 0 0 1 .03 1.1"/><path d="m13 12 4-4"/><path d="M10.9 7.25A2.4 2.4 0 0 0 5 8.8c0 .15.02.3.04.45"/></svg>',
    "target": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "clock": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "alert": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    "upload": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>',
    "download": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>',
    "file": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>',
    "calendar": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>',
    "chart": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>',
    "hospital": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6v4"/><path d="M14 14h-4"/><path d="M14 18h-4"/><path d="M14 8h-4"/><path d="M18 12h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2"/><path d="M18 22V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v18"/></svg>',
    "bot": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>',
    "sparkles": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    "x": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>',
    "trash": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>',
}

def icon(name, size=20, color="currentColor"):
    """Return SVG icon with custom size and color."""
    svg = ICONS.get(name, ICONS["info"])
    svg = svg.replace('width="20"', f'width="{size}"')
    svg = svg.replace('height="20"', f'height="{size}"')
    if color != "currentColor":
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    return svg

# Setup path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Page config (MUST be first)
st.set_page_config(
    page_title="Diet Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== IMPORTS ==============
from profile_manager import get_profile, save_profile, delete_profile, has_profile
from report_manager import save_report, load_reports, get_stats, delete_report

# ============== SESSION STATE ==============
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = get_profile()
if 'results' not in st.session_state:
    st.session_state.results = None
if 'medical_text' not in st.session_state:
    st.session_state.medical_text = None

# ============== HELPER FUNCTIONS ==============
@st.cache_data(ttl=300, show_spinner=False)
def process_report(text):
    """Run all agents on medical report. Cached for 5 minutes."""
    from agent1_translator import run_agent1
    from agent2_recommender import run_agent2
    from agent3_meal_planner import run_agent3
    
    translation = run_agent1(text)
    diet_rec = run_agent2(translation)
    meal_plan = run_agent3(diet_rec)
    
    return {
        "translation": translation,
        "diet": diet_rec,
        "meal_plan": meal_plan
    }

def clean_text(text):
    """Clean text for PDF."""
    if not text:
        return ""
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    for bad, good in {"–": "-", "—": "-", """: '"', """: '"', "'": "'", "'": "'", "•": "-"}.items():
        text = text.replace(bad, good)
    return text.encode('ascii', 'ignore').decode('ascii').strip()

class StyledPDF(FPDF):
    """Custom PDF with borders and page numbers on ALL pages."""
    
    def __init__(self, profile=None):
        super().__init__()
        self.profile = profile
    
    def header(self):
        # Draw border on EVERY page (including auto-generated overflow pages)
        self.set_draw_color(46, 125, 50)  # Green border
        self.set_line_width(0.5)
        self.rect(10, 10, 190, 277)  # Full page border
        
        # Green header bar
        self.set_fill_color(46, 125, 50)  # Green
        self.rect(10, 10, 190, 12, 'F')
        
        # Header text
        self.set_font("Times", "B", 10)
        self.set_text_color(255, 255, 255)
        self.set_xy(15, 12)
        self.cell(0, 8, "AI Diet Recommendation Report", align="L")
        
        # Date on right
        self.set_xy(150, 12)
        self.cell(0, 8, datetime.now().strftime('%B %d, %Y'), align="L")
        
        self.set_text_color(0, 0, 0)
        self.ln(20)
    
    def footer(self):
        # Position at 15mm from bottom
        self.set_y(-20)
        
        # Green footer bar
        self.set_fill_color(46, 125, 50)
        self.rect(10, self.get_y() + 5, 190, 10, 'F')
        
        # Page number
        self.set_font("Times", "I", 9)
        self.set_text_color(255, 255, 255)
        self.set_y(-14)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
        
        self.set_text_color(0, 0, 0)
    
    def section_title(self, title):
        """Add a styled section title."""
        self.set_font("Times", "B", 14)
        self.set_fill_color(232, 245, 233)  # Light green
        self.set_text_color(46, 125, 50)
        self.cell(0, 10, title, ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)
    
    def body_text(self, text):
        """Add body text."""
        self.set_font("Times", "", 10)
        self.multi_cell(0, 5, text)
        self.ln(5)


def generate_pdf(results, profile=None):
    """Generate styled PDF with borders and page numbers on ALL pages."""
    pdf = StyledPDF(profile)
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.set_margins(15, 25, 15)
    
    # Page 1: Title & Medical Summary
    pdf.add_page()
    
    # Title
    pdf.set_font("Times", "B", 20)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 15, "Your Personalized Diet Plan", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    
    # User info
    if profile:
        pdf.set_font("Times", "I", 12)
        pdf.cell(0, 8, f"Prepared for: {profile.get('name', 'User')}", ln=True, align="C")
        pdf.set_font("Times", "", 10)
        pdf.cell(0, 6, f"Diet Type: {profile.get('diet_type', 'N/A')} | Goal: {profile.get('weight_goal', 'N/A')}", ln=True, align="C")
        
        allergies = profile.get('allergies', [])
        if allergies:
            pdf.cell(0, 6, f"Allergies: {', '.join(allergies)}", ln=True, align="C")
    
    pdf.ln(10)
    
    # Medical Summary
    pdf.section_title("Medical Summary")
    pdf.body_text(clean_text(results["translation"]))
    
    # Page 2: Diet Recommendations
    pdf.add_page()
    pdf.section_title("Diet Recommendations")
    pdf.body_text(clean_text(results["diet"]))
    
    # Page 3: Meal Plan
    pdf.add_page()
    pdf.section_title("7-Day Meal Plan")
    pdf.body_text(clean_text(results["meal_plan"]))
    
    # Final page: Disclaimer
    pdf.ln(10)
    pdf.set_font("Times", "I", 9)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 5, "Disclaimer: This report is generated by AI and is not medical advice. Always consult a healthcare professional before making dietary changes.")
    pdf.ln(5)
    pdf.cell(0, 5, "Generated by AI Diet Recommendation System | Developed by Navya", align="C")
    
    # Output
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(temp_path)
    with open(temp_path, "rb") as f:
        pdf_bytes = f.read()
    os.remove(temp_path)
    
    return pdf_bytes

# ============== PROFESSIONAL CSS ==============
st.markdown("""
<style>
/* ===== GLOBAL RESET & TYPOGRAPHY ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

#MainMenu, footer, header {visibility: hidden;}

.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ===== SIDEBAR STYLING ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2E7D32 0%, #1B5E20 100%);
}

/* Desktop: Fixed sidebar, hide collapse button */
@media (min-width: 769px) {
    [data-testid="stSidebar"] {
        min-width: 280px !important;
        width: 280px !important;
        transform: none !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] {
        transform: none !important;
        width: 280px !important;
        min-width: 280px !important;
        margin-left: 0 !important;
    }
    
    /* Hide collapse button on desktop */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    button[data-testid="baseButton-header"],
    [data-testid="stSidebarNavCollapseIcon"],
    .st-emotion-cache-1gwvy71 {
        display: none !important;
    }
}

/* Mobile: Allow sidebar to collapse, show toggle button */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        min-width: 260px !important;
        width: 260px !important;
    }
    
    /* Style the mobile toggle button */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    button[data-testid="baseButton-header"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: #2E7D32 !important;
        border-radius: 8px !important;
        padding: 8px !important;
        border: none !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2) !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] svg,
    button[data-testid="baseButton-header"] svg {
        color: white !important;
        stroke: white !important;
    }
    
    /* Sidebar content adjustments for mobile */
    [data-testid="stSidebar"] h2 {
        font-size: 1.25rem !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        padding: 0.6rem 0.8rem !important;
        font-size: 0.9rem !important;
    }
}

[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-weight: 500;
    transition: all 0.3s ease;
    margin-bottom: 0.5rem;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.2);
    border-color: rgba(255,255,255,0.4);
    transform: translateX(5px);
}

[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(255,255,255,0.25);
    border-color: rgba(255,255,255,0.5);
}

/* ===== MAIN CONTENT BUTTONS ===== */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s ease;
    border: none;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
    color: white;
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
}

.stButton > button[kind="secondary"] {
    background: white;
    color: #2E7D32;
    border: 2px solid #2E7D32;
}

.stButton > button[kind="secondary"]:hover {
    background: #E8F5E9;
}

/* ===== CARDS ===== */
.card {
    background: white;
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    border: 1px solid rgba(0,0,0,0.05);
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

/* ===== STAT CARDS ===== */
.stat-card {
    background: white;
    padding: 1.75rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    border: 1px solid rgba(0,0,0,0.05);
}

.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.stat-number {
    font-size: 2.75rem;
    font-weight: 700;
    color: #2E7D32;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.stat-label {
    color: #666;
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ===== SECTION HEADERS ===== */
.section-header {
    color: #2E7D32;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 2.5rem 0 1.25rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 3px solid #E8F5E9;
    position: relative;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, #2E7D32, #4CAF50);
    border-radius: 2px;
}

/* ===== PROFILE CARD ===== */
.profile-card {
    background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
    padding: 1.25rem 1.75rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    border-left: 5px solid #4CAF50;
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.15);
}

/* ===== FORM INPUTS ===== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    border-radius: 10px;
    border: 2px solid #E0E0E0;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #4CAF50;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader {
    background: #F5F5F5;
    border-radius: 10px;
    font-weight: 600;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: #E8F5E9;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] {
    border: 2px dashed #C8E6C9;
    border-radius: 16px;
    padding: 1rem;
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #4CAF50;
    background: #F1F8E9;
}

/* ===== ALERTS ===== */
.stAlert {
    border-radius: 12px;
}

/* ===== SPINNER ===== */
.stSpinner > div {
    border-color: #4CAF50 transparent transparent transparent;
}

/* ===== HERO SECTION ===== */
.hero-section {
    background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                url('https://images.unsplash.com/photo-1610348725531-843dff563e2c?w=1400');
    background-size: cover;
    background-position: center;
    padding: 4rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
}

/* Force white text in hero - override Streamlit theme */
.hero-section h1,
.hero-section p,
.hero-section * {
    color: #FFFFFF !important;
}

.hero-section h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.5) !important;
}

.hero-section p {
    font-size: 1.1rem !important;
    font-weight: 400 !important;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.3) !important;
}

/* ===== STEP CARDS ===== */
.step-card {
    background: white;
    padding: 2rem 1.5rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    border: 1px solid rgba(0,0,0,0.05);
    height: 100%;
}

.step-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.step-number {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    margin: 0 auto 1.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.25rem;
    color: white;
}

.step-title {
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.step-desc {
    color: #666;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* ===== ANIMATIONS ===== */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-in {
    animation: fadeInUp 0.5s ease-out;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #F5F5F5;
}

::-webkit-scrollbar-thumb {
    background: #C8E6C9;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #A5D6A7;
}

/* ===== MOBILE RESPONSIVE ===== */
@media (max-width: 768px) {
    /* Hero section */
    .hero-section {
        padding: 2.5rem 1.5rem !important;
        border-radius: 16px !important;
    }
    
    .hero-section h1 {
        font-size: 1.75rem !important;
    }
    
    .hero-section p {
        font-size: 1rem !important;
    }
    
    /* Stat cards */
    .stat-card {
        padding: 1rem !important;
    }
    
    .stat-number {
        font-size: 2rem !important;
    }
    
    /* Step cards */
    .step-card {
        padding: 1.5rem 1rem !important;
        margin-bottom: 1rem;
    }
    
    .step-number {
        width: 48px !important;
        height: 48px !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.2rem !important;
    }
    
    /* Cards */
    .card {
        padding: 1rem !important;
    }
    
    /* Profile card */
    .profile-card {
        padding: 1rem !important;
    }
}

/* Extra small screens */
@media (max-width: 480px) {
    .hero-section h1 {
        font-size: 1.5rem !important;
    }
    
    .stat-number {
        font-size: 1.75rem !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ============== SIDEBAR ==============
with st.sidebar:
    st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 1rem;">
            <div style="color: white;">{icon("salad", 48, "white")}</div>
            <h2 style="color: white; margin: 0.5rem 0 0 0;">Diet Planner</h2>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">AI-Powered Nutrition</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation with SVG icons
    nav_items = [
        ("home", "Home", "Home"),
        ("dashboard", "Dashboard", "Dashboard"),
        ("user", "My Profile", "Profile"),
        ("health", "Analyze Health", "Upload"),
        ("chat", "Ask Questions", "Ask"),
        ("info", "About", "About")
    ]
    
    for icon_name, label, key in nav_items:
        is_active = st.session_state.current_page == key
        btn_style = "background: rgba(255,255,255,0.25);" if is_active else "background: rgba(255,255,255,0.1);"
        
        st.markdown(f'''
            <style>
                div[data-testid="stButton"] button[kind="secondary"]:has(+ #{key}_marker) {{
                    {btn_style}
                }}
            </style>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f'<div style="color: white; padding-top: 8px;">{icon(icon_name, 18, "white")}</div>', unsafe_allow_html=True)
        with col2:
            if st.button(label, use_container_width=True, type="primary" if is_active else "secondary", key=f"nav_{key}"):
                st.session_state.current_page = key
                st.rerun()
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    
    # Profile status with SVG icon
    profile = get_profile()
    if profile:
        st.markdown(f'''
            <div style="background: rgba(165,214,167,0.2); padding: 12px; border-radius: 10px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #A5D6A7;">{icon("user", 16, "#A5D6A7")}</span>
                    <span style="color: #A5D6A7; font-weight: 500;">{profile.get('name', 'User')}</span>
                </div>
                <span style="color: rgba(255,255,255,0.6); font-size: 12px; margin-left: 24px;">{profile.get('diet_type', '')}</span>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div style="background: rgba(255,183,77,0.2); padding: 12px; border-radius: 10px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #FFB74D;">{icon("alert", 16, "#FFB74D")}</span>
                    <span style="color: #FFB74D;">No Profile</span>
                </div>
            </div>
        ''', unsafe_allow_html=True)

# ============== REDIRECT FIRST-TIME USERS ==============
if not has_profile() and st.session_state.current_page not in ["Profile", "About"]:
    st.session_state.current_page = "Profile"

# ============== PAGES ==============

# ---------- DASHBOARD PAGE ----------
if st.session_state.current_page == "Dashboard":
    if EXTRAS_AVAILABLE:
        colored_header(
            label="Your Nutrition Dashboard",
            description="Track your health journey and view past reports",
            color_name="green-70"
        )
    else:
        st.markdown(f'<h2 style="color: #2E7D32; font-weight: 700; display: flex; align-items: center; gap: 10px;">{icon("dashboard", 28, "#2E7D32")} Your Nutrition Dashboard</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; margin-top: -0.5rem;">Track your health journey and view past reports</p>', unsafe_allow_html=True)
    
    profile = get_profile()
    if not profile:
        st.warning("Please complete your profile first.")
        st.stop()
    
    # Load stats
    stats = get_stats()
    reports = load_reports()
    
    # Summary Cards with Streamlit Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Reports Generated",
            value=stats["total_reports"],
            delta=f"+1" if stats["total_reports"] > 0 else None
        )
    
    with col2:
        st.metric(
            label="Conditions Tracked",
            value=len(stats["conditions"]),
            delta=None
        )
    
    with col3:
        st.metric(
            label="Diet Type",
            value=profile.get("diet_type", "N/A"),
            delta=None
        )
    
    with col4:
        allergies_count = len(profile.get("allergies", []))
        st.metric(
            label="Allergies",
            value=allergies_count,
            delta=None
        )
    
    # Style the metric cards if streamlit-extras is available
    if EXTRAS_AVAILABLE:
        style_metric_cards(
            background_color="#FFFFFF",
            border_left_color="#2E7D32",
            border_color="#E8F5E9",
            box_shadow="0 4px 20px rgba(0,0,0,0.08)"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Conditions Overview (with safe check)
    condition_counts = stats.get("condition_counts", {})
    if condition_counts:
        st.markdown(f'<p class="section-header">{icon("hospital", 20, "#2E7D32")} Health Conditions Detected</p>', unsafe_allow_html=True)
        
        # Create a simple bar chart
        conditions_df = pd.DataFrame([
            {"Condition": k, "Count": v} 
            for k, v in condition_counts.items()
        ])
        
        if not conditions_df.empty:
            st.bar_chart(conditions_df.set_index("Condition"))
    
    # Recent Reports
    st.markdown(f'<p class="section-header">{icon("file", 20, "#2E7D32")} Your Report History</p>', unsafe_allow_html=True)
    
    if not reports:
        # Beautiful empty state
        st.markdown(f'''
            <div style="text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, #F5F5F5, #EEEEEE); border-radius: 20px; margin: 1rem 0;">
                <div style="margin-bottom: 1rem;">{icon("file", 64, "#2E7D32")}</div>
                <h3 style="color: #2E7D32; margin: 0 0 0.5rem 0;">No Reports Yet</h3>
                <p style="color: #666; margin: 0 0 1.5rem 0;">Upload your first medical report to get personalized diet recommendations</p>
            </div>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Analyze Your First Report", type="primary", use_container_width=True):
                st.session_state.current_page = "Upload"
                st.rerun()
    else:
        for i, report in enumerate(reports[:10]):  # Show last 10
            date = report.get("date", "Unknown")
            time_str = report.get("time", "")
            conditions = report.get("conditions_found", ["General"])
            report_id = report.get("report_id", 0)
            
            with st.expander(f"{date} {time_str} — {', '.join(conditions[:3])}", expanded=(i == 0)):
                
                tab1, tab2, tab3 = st.tabs(["Summary", "Diet Plan", "Meal Plan"])
                
                with tab1:
                    st.markdown("**Simple Explanation:**")
                    st.write(report.get("simple_explanation", "N/A"))
                
                with tab2:
                    st.markdown("**Diet Recommendations:**")
                    st.write(report.get("diet_recommendations", "N/A"))
                
                with tab3:
                    st.markdown("**7-Day Meal Plan:**")
                    st.write(report.get("meal_plan", "N/A"))
                
                # Actions
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    # Regenerate PDF
                    try:
                        pdf_data = generate_pdf({
                            "translation": report.get("simple_explanation", ""),
                            "diet": report.get("diet_recommendations", ""),
                            "meal_plan": report.get("meal_plan", "")
                        }, profile)
                        
                        st.download_button(
                            "Download PDF",
                            pdf_data,
                            f"diet_plan_{date}.pdf",
                            "application/pdf",
                            key=f"pdf_{report_id}"
                        )
                    except:
                        pass
                
                with col3:
                    if st.button("Delete", key=f"del_{report_id}", type="secondary"):
                        delete_report(report_id)
                        st.rerun()
    
    # Quick Stats
    if reports:
        st.markdown(f'<p class="section-header">{icon("chart", 20, "#2E7D32")} Quick Stats</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'''
                <div class="card">
                    <h4 style="color: #2E7D32;">{icon("calendar", 18, "#2E7D32")} Timeline</h4>
                    <p><strong>First Report:</strong> {stats.get("first_report_date", "N/A")}</p>
                    <p><strong>Latest Report:</strong> {stats.get("last_report_date", "N/A")}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            most_common = stats.get("most_common_condition", "None")
            st.markdown(f'''
                <div class="card">
                    <h4 style="color: #FF6B35;">{icon("target", 18, "#FF6B35")} Most Common Condition</h4>
                    <p style="font-size: 1.5rem; font-weight: 600; color: #2E7D32;">{most_common}</p>
                </div>
            ''', unsafe_allow_html=True)

# ---------- PROFILE PAGE ----------
elif st.session_state.current_page == "Profile":
    profile = get_profile()
    is_new = profile is None
    
    if is_new:
        st.markdown(f'''
            <div style="text-align: center; padding: 2rem 0;" class="animate-in">
                <div>{icon("user", 80, "#2E7D32")}</div>
                <h1 style="color: #2E7D32; font-weight: 700; margin: 1rem 0 0.5rem 0;">Welcome!</h1>
                <p style="color: #666; font-size: 1.1rem;">Let's personalize your diet plan in just a few steps</p>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'<h2 style="color: #2E7D32; font-weight: 700; display: flex; align-items: center; gap: 10px;">{icon("user", 28, "#2E7D32")} My Profile</h2>', unsafe_allow_html=True)
    
    with st.form("profile_form"):
        st.markdown("### Basic Info")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name *", value=profile.get('name', '') if profile else '')
        with col2:
            diet_options = ["Vegetarian", "Vegan", "Eggetarian", "Pescatarian", "Non-Vegetarian"]
            diet_type = st.selectbox("Diet Type *", diet_options, index=diet_options.index(profile.get('diet_type', 'Non-Vegetarian')) if profile else 4)
        
        st.markdown("### Restrictions")
        col1, col2 = st.columns(2)
        
        with col1:
            religion_options = ["None", "Hindu (No beef)", "Muslim/Halal (No pork)", "Jewish/Kosher", "Jain", "Other"]
            religious = st.selectbox("Religious Restrictions", religion_options, index=religion_options.index(profile.get('religious_restrictions', 'None')) if profile else 0)
        with col2:
            allergy_options = ["Peanuts", "Tree Nuts", "Dairy", "Eggs", "Gluten", "Soy", "Fish", "Shellfish"]
            allergies = st.multiselect("Allergies", allergy_options, default=profile.get('allergies', []) if profile else [])
        
        dislikes = st.text_input("Foods you dislike (comma separated)", value=', '.join(profile.get('disliked_foods', [])) if profile else '')
        
        st.markdown("### Preferences")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            time_options = ["Under 15 minutes", "15-30 minutes", "30-60 minutes", "No limit"]
            cooking_time = st.selectbox("Cooking Time", time_options, index=time_options.index(profile.get('cooking_time', '15-30 minutes')) if profile else 1)
        with col2:
            activity_options = ["Sedentary", "Light", "Moderate", "Active"]
            activity = st.selectbox("Activity Level", activity_options, index=activity_options.index(profile.get('activity_level', 'Moderate')) if profile else 2)
        with col3:
            goal_options = ["Lose weight", "Maintain", "Gain muscle"]
            weight_goal = st.selectbox("Weight Goal", goal_options, index=goal_options.index(profile.get('weight_goal', 'Maintain')) if profile else 1)
        
        budget_options = ["Budget-friendly", "Moderate", "No limit"]
        budget = st.selectbox("Budget", budget_options, index=budget_options.index(profile.get('budget', 'Moderate')) if profile else 1)
        
        if st.form_submit_button("Save Profile", type="primary", use_container_width=True):
            if not name.strip():
                st.error("Please enter your name")
            else:
                new_profile = {
                    "name": name.strip(),
                    "diet_type": diet_type,
                    "religious_restrictions": religious,
                    "allergies": allergies,
                    "disliked_foods": [d.strip() for d in dislikes.split(',') if d.strip()],
                    "cooking_time": cooking_time,
                    "activity_level": activity,
                    "weight_goal": weight_goal,
                    "budget": budget
                }
                save_profile(new_profile)
                st.success("Profile saved!")
                st.balloons()
                import time; time.sleep(1)
                st.session_state.current_page = "Home"
                st.rerun()
    
    if not is_new:
        with st.expander("Delete Profile"):
            if st.button("Delete Profile"):
                delete_profile()
                st.session_state.user_profile = None
                st.rerun()

# ---------- HOME PAGE ----------
elif st.session_state.current_page == "Home":
    profile = get_profile()
    stats = get_stats()
    
    # Hero Section
    st.markdown("""
        <div class="hero-section animate-in">
            <h1 style="color: white !important; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; text-shadow: 2px 2px 8px rgba(0,0,0,0.5);">Fuel Your Body, Nourish Your Life</h1>
            <p style="color: white !important; font-size: 1.1rem; text-shadow: 1px 1px 4px rgba(0,0,0,0.3);">AI-powered personalized nutrition tailored just for you</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome message for returning users
    if profile:
        st.markdown(f'''
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 1.5rem 2rem; border-radius: 16px; margin-bottom: 2rem; border-left: 4px solid #2E7D32;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="color: #2E7D32;">{icon("user", 32, "#2E7D32")}</div>
                    <div>
                        <h3 style="color: #2E7D32; margin: 0; font-weight: 600;">Welcome back, {profile.get("name", "there")}!</h3>
                        <p style="color: #666; margin: 0.25rem 0 0 0; font-size: 0.95rem;">Ready to optimize your nutrition today?</p>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    

    
    # Stats for returning users
    if stats["total_reports"] > 0:
        st.markdown(f'<p class="section-header">{icon("chart", 20, "#2E7D32")} Your Progress</p>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'''
                <div class="stat-card">
                    <div style="color:#2E7D32;">{icon("file", 36, "#2E7D32")}</div>
                    <div class="stat-number">{stats["total_reports"]}</div>
                    <div class="stat-label">Reports</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
                <div class="stat-card">
                    <div style="color:#FF6B35;">{icon("hospital", 36, "#FF6B35")}</div>
                    <div class="stat-number" style="color:#FF6B35;">{len(stats["conditions"])}</div>
                    <div class="stat-label">Conditions</div>
                </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
                <div class="stat-card">
                    <div style="color:#2196F3;">{icon("salad", 36, "#2196F3")}</div>
                    <div class="stat-number" style="color:#2196F3; font-size: 1.5rem;">{profile.get("diet_type", "N/A") if profile else "N/A"}</div>
                    <div class="stat-label">Diet Type</div>
                </div>
            ''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''
                <div class="stat-card">
                    <div style="color:#9C27B0;">{icon("target", 36, "#9C27B0")}</div>
                    <div class="stat-number" style="color:#9C27B0; font-size: 1.5rem;">{profile.get("weight_goal", "N/A") if profile else "N/A"}</div>
                    <div class="stat-label">Goal</div>
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # How it works
    st.markdown(f'<p class="section-header">{icon("sparkles", 20, "#2E7D32")} How It Works</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
            <div class="step-card">
                <div class="step-number" style="background: linear-gradient(135deg, #FF6B35, #FF8A65);">{icon("upload", 24, "white")}</div>
                <h4 class="step-title" style="color: #FF6B35;">Upload Report</h4>
                <p class="step-desc">Upload your medical report or enter health data</p>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="step-card">
                <div class="step-number" style="background: linear-gradient(135deg, #4CAF50, #81C784);">{icon("bot", 24, "white")}</div>
                <h4 class="step-title" style="color: #4CAF50;">AI Analysis</h4>
                <p class="step-desc">4 specialized AI agents analyze your health data</p>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
            <div class="step-card">
                <div class="step-number" style="background: linear-gradient(135deg, #2196F3, #64B5F6);">{icon("calendar", 24, "white")}</div>
                <h4 class="step-title" style="color: #2196F3;">Get Your Plan</h4>
                <p class="step-desc">Receive personalized diet & 7-day meal plan</p>
            </div>
        ''', unsafe_allow_html=True)
    


# ---------- ANALYZE HEALTH PAGE ----------
elif st.session_state.current_page == "Upload":
    if EXTRAS_AVAILABLE:
        colored_header(
            label="Analyze Your Health",
            description="Upload your medical report or enter your health data to get a personalized diet plan",
            color_name="green-70"
        )
    else:
        st.markdown(f'<h2 style="color: #2E7D32; font-weight: 700; display: flex; align-items: center; gap: 10px;">{icon("health", 28, "#2E7D32")} Analyze Your Health</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; font-size: 1.05rem;">Upload your medical report or enter your health data to get a personalized diet plan.</p>', unsafe_allow_html=True)
    
    profile = get_profile()
    if profile:
        restrictions = []
        if profile.get('diet_type') != 'Non-Vegetarian':
            restrictions.append(profile['diet_type'])
        if profile.get('religious_restrictions') != 'None':
            restrictions.append(profile['religious_restrictions'])
        restrictions.extend(profile.get('allergies', []))
        if restrictions:
            st.markdown(f'<div class="profile-card"><strong>{icon("check", 16, "#4CAF50")} Your restrictions:</strong> {", ".join(restrictions[:5])}</div>', unsafe_allow_html=True)
    
    # Clear data option at top
    if st.session_state.medical_text or st.session_state.results:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Clear Data", type="secondary", use_container_width=True):
                st.session_state.medical_text = None
                st.session_state.results = None
                st.rerun()
    
    # Input tabs
    tab1, tab2 = st.tabs(["Upload File", "Type Text"])
    
    with tab1:
        st.info("Supported: PDF, Word, Text")
        uploaded = st.file_uploader("Choose file", type=["pdf", "docx", "txt"])
        
        if uploaded:
            try:
                from file_reader import FileReader
                reader = FileReader()
                ext = uploaded.name.split(".")[-1]
                temp_file = f"temp_upload.{ext}"
                with open(temp_file, "wb") as f:
                    f.write(uploaded.getbuffer())
                text = reader.read_file(temp_file)
                if text and not text.startswith("Error"):
                    st.session_state.medical_text = text
                    st.success(f"✓ Loaded: {uploaded.name}")
                    with st.expander("Preview"):
                        st.text(text[:1000])
            except Exception as e:
                st.error(f"Error: {e}")
    
    with tab2:
        typed = st.text_area("Enter medical info:", height=200, placeholder="Example: Fasting glucose 186 mg/dL, HbA1c 8.2%...")
        if typed:
            st.session_state.medical_text = typed
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate button
    if st.button("Generate Diet Plan", type="primary", use_container_width=True):
        if st.session_state.medical_text and len(st.session_state.medical_text) > 10:
            # Progress indicator
            progress_container = st.empty()
            progress_container.markdown(f'''
                <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 2rem; border-radius: 16px; text-align: center;">
                    <div style="margin-bottom: 1rem;">{icon("bot", 48, "#2E7D32")}</div>
                    <h3 style="color: #2E7D32; margin: 0;">AI is analyzing your health data...</h3>
                    <p style="color: #666; margin: 0.5rem 0 0 0;">This takes about 1-2 minutes</p>
                </div>
            ''', unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Translation
                status_text.text("Step 1/3: Translating medical terms...")
                progress_bar.progress(10)
                from agent1_translator import run_agent1
                translation = run_agent1(st.session_state.medical_text)
                progress_bar.progress(35)
                
                # Step 2: Diet recommendations
                status_text.text("Step 2/3: Creating diet recommendations...")
                from agent2_recommender import run_agent2
                diet_rec = run_agent2(translation)
                progress_bar.progress(65)
                
                # Step 3: Meal plan
                status_text.text("Step 3/3: Generating 7-day meal plan...")
                from agent3_meal_planner import run_agent3
                meal_plan = run_agent3(diet_rec)
                progress_bar.progress(90)
                
                # Save results
                st.session_state.results = {
                    "translation": translation,
                    "diet": diet_rec,
                    "meal_plan": meal_plan
                }
                
                # Save report to history
                save_report(
                    medical_text=st.session_state.medical_text,
                    translation=translation,
                    diet_rec=diet_rec,
                    meal_plan=meal_plan
                )
                
                progress_bar.progress(100)
                status_text.text("Complete!")
                progress_container.empty()
                
                st.success("Done! Report saved to your dashboard.")
                st.rerun()
            except Exception as e:
                progress_container.empty()
                progress_bar.empty()
                status_text.empty()
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter text or upload a file")
    
    # Show results
    if st.session_state.results:
        st.markdown("---")
        
        st.markdown(f'<p class="section-header">{icon("file", 20, "#2E7D32")} Simple Explanation</p>', unsafe_allow_html=True)
        with st.expander("View", expanded=True):
            st.write(st.session_state.results["translation"])
        
        st.markdown(f'<p class="section-header">{icon("salad", 20, "#2E7D32")} Foods to Eat & Avoid</p>', unsafe_allow_html=True)
        
        # Parse foods
        eat_items, avoid_items = [], []
        avoid_section = False
        for line in st.session_state.results["diet"].split("\n"):
            line = line.strip()
            if "avoid" in line.lower() and not line.startswith(("-", "•")):
                avoid_section = True
                continue
            if "include" in line.lower() and not line.startswith(("-", "•")):
                avoid_section = False
                continue
            if line.startswith(("-", "•", "*")):
                food = re.sub(r'^[-•*]\s*', '', line)
                food = re.sub(r'\s*[:(].*', '', food).strip()
                if 3 < len(food) < 50:
                    (avoid_items if avoid_section else eat_items).append(food)
        
        if eat_items or avoid_items:
            max_len = max(len(eat_items), len(avoid_items))
            eat_items.extend([""] * (max_len - len(eat_items)))
            avoid_items.extend([""] * (max_len - len(avoid_items)))
            st.table(pd.DataFrame({"Eat": eat_items[:10], "Avoid": avoid_items[:10]}))
        
        st.markdown(f'<p class="section-header">{icon("file", 20, "#2E7D32")} Full Recommendations</p>', unsafe_allow_html=True)
        with st.expander("View"):
            st.write(st.session_state.results["diet"])
        
        st.markdown(f'<p class="section-header">{icon("calendar", 20, "#2E7D32")} 7-Day Meal Plan</p>', unsafe_allow_html=True)
        with st.expander("View"):
            st.write(st.session_state.results["meal_plan"])
        
        # PDF Download
        st.markdown(f'<p class="section-header">{icon("download", 20, "#2E7D32")} Download Report</p>', unsafe_allow_html=True)
        try:
            pdf_bytes = generate_pdf(st.session_state.results, profile)
            
            st.markdown('''
                <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 1.5rem; border-radius: 16px; text-align: center; margin-bottom: 1rem;">
                    <p style="color: #2E7D32; margin: 0 0 0.5rem 0; font-size: 1.1rem; font-weight: 600;">Your personalized diet plan is ready!</p>
                    <p style="color: #558B2F; margin: 0; font-size: 0.9rem;">Download the PDF to view your complete meal plan, recommendations, and health summary.</p>
                </div>
            ''', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    "Download Complete Diet Plan (PDF)",
                    pdf_bytes, 
                    f"diet_plan_{datetime.now().strftime('%Y%m%d')}.pdf", 
                    "application/pdf", 
                    use_container_width=True,
                    type="primary"
                )
            
            # PDF Preview using components.html (works on Streamlit Cloud)
            with st.expander("Preview PDF"):
                b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                
                # Create iframe HTML with sandbox attributes
                pdf_iframe = f'''
                    <iframe 
                        src="data:application/pdf;base64,{b64_pdf}" 
                        width="100%" 
                        height="600" 
                        type="application/pdf"
                        sandbox="allow-same-origin allow-scripts"
                        style="border: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <p>Your browser does not support PDFs. 
                        <a href="data:application/pdf;base64,{b64_pdf}" download="diet_plan.pdf">Download the PDF</a> instead.</p>
                    </iframe>
                '''
                
                components.html(pdf_iframe, height=620, scrolling=True)
                
        except Exception as e:
            st.error(f"PDF error: {e}")
        
        st.balloons()

# ---------- ASK PAGE ----------
elif st.session_state.current_page == "Ask":
    if EXTRAS_AVAILABLE:
        colored_header(
            label="Ask Questions",
            description="Get personalized answers about your diet and nutrition",
            color_name="green-70"
        )
    else:
        st.markdown(f'<h2 style="color: #2E7D32; font-weight: 700; display: flex; align-items: center; gap: 10px;">{icon("chat", 28, "#2E7D32")} Ask Questions</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666;">Get personalized answers about your diet and nutrition</p>', unsafe_allow_html=True)
    
    profile = get_profile()
    if profile:
        st.markdown(f'''
            <div class="profile-card">
                <span>{icon("bot", 24, "#4CAF50")}</span>
                <span style="margin-left: 0.5rem;">Hi <strong>{profile.get("name", "there")}</strong>! Ask me anything about your diet.</span>
            </div>
        ''', unsafe_allow_html=True)
    
    with st.expander("Examples"):
        st.markdown("- Can I eat rice with diabetes?\n- What are good protein sources?\n- How much water should I drink?")
    
    question = st.text_area("Your question:", height=100)
    
    if st.button("Get Answer", type="primary"):
        if question and len(question) > 5:
            with st.spinner("Thinking..."):
                try:
                    from agent4_qa import run_agent4
                    diet_context = st.session_state.results.get("diet", "") if st.session_state.results else ""
                    answer = run_agent4(question, diet_context)
                    st.markdown('<p class="section-header">Answer</p>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card">{answer}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question")

# ---------- ABOUT PAGE ----------
elif st.session_state.current_page == "About":
    if EXTRAS_AVAILABLE:
        colored_header(
            label="About This System",
            description="Learn how our AI-powered system creates personalized nutrition plans",
            color_name="green-70"
        )
    else:
        st.markdown(f'<h2 style="color: #2E7D32; font-weight: 700; display: flex; align-items: center; gap: 10px;">{icon("info", 28, "#2E7D32")} About This System</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666;">Learn how our AI-powered system creates personalized nutrition plans</p>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown(f'''
        <div class="card">
            <h4 style="color: #2E7D32; display: flex; align-items: center; gap: 8px;">{icon("salad", 24, "#2E7D32")} AI-Powered Diet Recommendation System</h4>
            <p style="color: #666; line-height: 1.8;">
                This system uses artificial intelligence to analyze your medical reports and create 
                <strong>personalized diet plans</strong> that respect your dietary preferences, allergies, 
                and cultural restrictions. It's like having a personal nutritionist available 24/7!
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    # How AI Agents Help
    st.markdown(f'<p class="section-header">{icon("bot", 20, "#2E7D32")} How Our AI Agents Help You</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
            <div class="card">
                <h4 style="color: #2196F3; display: flex; align-items: center; gap: 8px;">{icon("health", 20, "#2196F3")} Medical Translator</h4>
                <p style="color: #666;">
                    Converts complex medical jargon into <strong>simple, easy-to-understand language</strong>. 
                    No more confusion about what your blood test results mean!
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'''
            <div class="card">
                <h4 style="color: #FF6B35; display: flex; align-items: center; gap: 8px;">{icon("calendar", 20, "#FF6B35")} Meal Planner</h4>
                <p style="color: #666;">
                    Creates a <strong>practical 7-day meal plan</strong> with breakfast, lunch, dinner, 
                    and snacks. Includes quick recipes and a shopping list!
                </p>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
            <div class="card">
                <h4 style="color: #4CAF50; display: flex; align-items: center; gap: 8px;">{icon("salad", 20, "#4CAF50")} Diet Recommender</h4>
                <p style="color: #666;">
                    Analyzes your health conditions and creates <strong>personalized food recommendations</strong>. 
                    Tells you exactly what to eat and what to avoid.
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'''
            <div class="card">
                <h4 style="color: #E91E63; display: flex; align-items: center; gap: 8px;">{icon("chat", 20, "#E91E63")} Q&A Assistant</h4>
                <p style="color: #666;">
                    Have questions about your diet? Ask anything! The AI will give you 
                    <strong>personalized answers</strong> based on your profile and health conditions.
                </p>
            </div>
        ''', unsafe_allow_html=True)
    
    # Personalization
    st.markdown(f'<p class="section-header">{icon("check", 20, "#2E7D32")} Personalization & Safety</p>', unsafe_allow_html=True)
    
    st.markdown(f'''
        <div class="card">
            <p style="color: #666; line-height: 1.8;">
                Your profile ensures the AI <strong>never recommends foods you can't eat</strong>:
            </p>
            <ul style="color: #666; line-height: 2;">
                <li>{icon("salad", 16, "#4CAF50")} <strong>Vegetarian/Vegan:</strong> No meat, fish, or animal products</li>
                <li>{icon("check", 16, "#4CAF50")} <strong>Hindu:</strong> No beef recommendations</li>
                <li>{icon("check", 16, "#4CAF50")} <strong>Muslim/Halal:</strong> No pork recommendations</li>
                <li>{icon("alert", 16, "#E91E63")} <strong>Allergies:</strong> Dangerous foods are completely excluded</li>
                <li>{icon("x", 16, "#FF6B35")} <strong>Dislikes:</strong> Foods you hate won't appear in your plan</li>
                <li>{icon("clock", 16, "#2196F3")} <strong>Cooking Time:</strong> Recipes fit your schedule</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)
    
    # Features
    st.markdown(f'<p class="section-header">{icon("sparkles", 20, "#2E7D32")} Key Features</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
            <div class="card" style="text-align: center;">
                <div style="color: #2E7D32;">{icon("dashboard", 40, "#2E7D32")}</div>
                <h4 style="color: #2E7D32;">Dashboard</h4>
                <p style="color: #666; font-size: 0.9rem;">Track all your reports and health conditions over time</p>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
            <div class="card" style="text-align: center;">
                <div style="color: #2E7D32;">{icon("file", 40, "#2E7D32")}</div>
                <h4 style="color: #2E7D32;">PDF Export</h4>
                <p style="color: #666; font-size: 0.9rem;">Download your meal plans to share with family or doctors</p>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
            <div class="card" style="text-align: center;">
                <div style="color: #2E7D32;">{icon("check", 40, "#2E7D32")}</div>
                <h4 style="color: #2E7D32;">Privacy</h4>
                <p style="color: #666; font-size: 0.9rem;">Your data stays on your device, not stored on any server</p>
            </div>
        ''', unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown(f'''
        <div style="background: #FFF3E0; padding: 1.5rem; border-radius: 12px; margin-top: 2rem; border-left: 4px solid #FF6B35;">
            <h4 style="color: #E65100; margin: 0 0 0.5rem 0; display: flex; align-items: center; gap: 8px;">{icon("alert", 20, "#E65100")} Important Disclaimer</h4>
            <p style="color: #E65100; margin: 0; font-size: 0.95rem;">
                This system provides <strong>general dietary guidance</strong> based on AI analysis. 
                It is <strong>not a substitute for professional medical advice</strong>. 
                Always consult a qualified healthcare professional or registered dietitian 
                before making significant changes to your diet, especially if you have 
                existing health conditions.
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Developer
    st.markdown(f'''
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); border-radius: 12px;">
            <p style="color: #666; margin: 0;">Developed by</p>
            <h3 style="color: #2E7D32; margin: 0.5rem 0;">Navya</h3>
            <p style="color: #888; margin: 0;">Data Science & AI Student | December 2025</p>
        </div>
    ''', unsafe_allow_html=True)
