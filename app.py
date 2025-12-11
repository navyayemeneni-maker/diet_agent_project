"""
Diet Recommendation System - Clean Single File App
Author: Navya | December 2025
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
from fpdf import FPDF
import base64
import tempfile
import pandas as pd
import re

# Setup paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
load_dotenv()

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Diet Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== SESSION STATE ==============
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'agents_initialized' not in st.session_state:
    st.session_state.agents_initialized = False
if 'results' not in st.session_state:
    st.session_state.results = None

# ============== HELPER FUNCTIONS ==============
def initialize_agents():
    """Initialize all AI agents"""
    try:
        from file_reader import FileReader
        from agent1_translator import MedicalTranslatorAgent
        from agent2_recommender import DietRecommenderAgent
        from agent3_meal_planner import MealPlanBuilderAgent
        from agent4_qa import QASupportAgent
        
        st.session_state.file_reader = FileReader()
        st.session_state.translator = MedicalTranslatorAgent()
        st.session_state.recommender = DietRecommenderAgent()
        st.session_state.meal_planner = MealPlanBuilderAgent()
        st.session_state.qa_bot = QASupportAgent()
        st.session_state.agents_initialized = True
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def process_report(text):
    """Process medical report through agents"""
    translation = st.session_state.translator.translate_medical_report(text)
    diet_rec = st.session_state.recommender.recommend_diet(text)
    meal_plan = st.session_state.meal_planner.create_meal_plan(diet_rec)
    
    # Set context for Q&A agent so it can answer questions about this report
    st.session_state.qa_bot.set_context(
        diet_plan=diet_rec,
        meal_plan=meal_plan,
        health_condition=translation
    )
    
    return {"translation": translation, "diet": diet_rec, "meal_plan": meal_plan}

def clean_text(text):
    """Clean text for PDF - remove markdown and convert to ASCII-safe text"""
    if not text:
        return ""
    
    # Remove markdown formatting
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)  # Remove headers
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)  # Remove bold+italic
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Remove bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)  # Remove italic
    text = re.sub(r'__(.+?)__', r'\1', text)  # Remove bold
    text = re.sub(r'_(.+?)_', r'\1', text)  # Remove italic
    text = re.sub(r'^\*\*\*$', '', text, flags=re.MULTILINE)  # Remove horizontal rules
    text = re.sub(r'^---$', '', text, flags=re.MULTILINE)  # Remove horizontal rules
    text = re.sub(r'`(.+?)`', r'\1', text)  # Remove inline code
    text = re.sub(r'^\s*[-*+]\s+', '- ', text, flags=re.MULTILINE)  # Convert list markers
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)  # Clean numbered lists
    
    # Replace ALL special Unicode characters with ASCII equivalents
    replacements = {
        # Dashes
        "–": "-", "—": "-", "‑": "-", "−": "-",
        # Quotes
        """: '"', """: '"', "„": '"', "‟": '"',
        "'": "'", "'": "'", "‚": "'", "‛": "'",
        "`": "'", "´": "'",
        # Bullets and symbols
        "•": "-", "·": "-", "●": "-", "○": "-",
        "►": ">", "◄": "<", "▪": "-", "▫": "-",
        # Spaces
        "\u00a0": " ", "\u2003": " ", "\u2002": " ", "\u2009": " ",
        # Other
        "…": "...", "™": "(TM)", "®": "(R)", "©": "(C)",
        "°": " degrees", "±": "+/-", "×": "x", "÷": "/",
        "≤": "<=", "≥": ">=", "≠": "!=", "≈": "~",
        "→": "->", "←": "<-", "↑": "^", "↓": "v",
        "µ": "u", "α": "alpha", "β": "beta", "γ": "gamma",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    
    # Remove any remaining non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Remove multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

# ============== CUSTOM CSS ==============
st.markdown("""
<style>
/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2E7D32 0%, #1B5E20 100%);
    padding-top: 0;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0;
}

/* Main area */
.main .block-container {
    padding: 2rem 3rem;
    max-width: 1100px;
}

/* Navigation buttons */
.nav-btn {
    display: block;
    width: 100%;
    padding: 12px 20px;
    margin: 5px 0;
    background: rgba(255,255,255,0.1);
    border: none;
    border-radius: 8px;
    color: white;
    text-align: left;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.2s;
}

.nav-btn:hover {
    background: rgba(255,255,255,0.2);
}

.nav-btn.active {
    background: rgba(255,255,255,0.25);
    border-left: 3px solid #A5D6A7;
}

/* Cards */
.card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}

/* Hero section */
.hero {
    background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
    padding: 3rem 2rem;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 2rem;
}

.hero h1 {
    color: white;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.hero p {
    color: rgba(255,255,255,0.9);
    font-size: 1.2rem;
}

/* Section headers */
.section-header {
    color: #2E7D32;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #E8F5E9;
}

/* Status badge */
.status-ready {
    background: #E8F5E9;
    color: #2E7D32;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
}

.status-not-ready {
    background: #FFF3E0;
    color: #E65100;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ============== SIDEBAR ==============
with st.sidebar:
    # Logo/Title
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 1rem;">
            <span style="font-size: 3rem;">🥗</span>
            <h2 style="color: white; margin: 0.5rem 0 0 0; font-size: 1.4rem;">Diet Planner</h2>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin: 0;">AI-Powered Nutrition</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("<p style='color: rgba(255,255,255,0.6); font-size: 12px; margin-bottom: 8px; padding-left: 5px;'>MENU</p>", unsafe_allow_html=True)
    
    if st.button("🏠  Home", use_container_width=True, type="secondary" if st.session_state.current_page != "Home" else "primary"):
        st.session_state.current_page = "Home"
        st.rerun()
    
    if st.button("📄  Upload Report", use_container_width=True, type="secondary" if st.session_state.current_page != "Upload" else "primary"):
        st.session_state.current_page = "Upload"
        st.rerun()
    
    if st.button("💬  Ask Questions", use_container_width=True, type="secondary" if st.session_state.current_page != "Ask" else "primary"):
        st.session_state.current_page = "Ask"
        st.rerun()
    
    if st.button("ℹ️  About", use_container_width=True, type="secondary" if st.session_state.current_page != "About" else "primary"):
        st.session_state.current_page = "About"
        st.rerun()
    
    # Divider
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # System Status
    st.markdown("<p style='color: rgba(255,255,255,0.6); font-size: 12px; margin-bottom: 8px; padding-left: 5px;'>SYSTEM STATUS</p>", unsafe_allow_html=True)
    
    if st.session_state.agents_initialized:
        st.markdown("""
            <div style="background: rgba(165,214,167,0.2); padding: 10px 15px; border-radius: 8px; margin-bottom: 10px;">
                <span style="color: #A5D6A7;">✓ Agents Ready</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: rgba(255,183,77,0.2); padding: 10px 15px; border-radius: 8px; margin-bottom: 10px;">
                <span style="color: #FFB74D;">⚠ Not Initialized</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Initialize Agents", use_container_width=True):
            with st.spinner("Starting agents..."):
                if initialize_agents():
                    st.success("Ready!")
                    st.rerun()

# ============== MAIN CONTENT ==============

# ---------- HOME PAGE ----------
if st.session_state.current_page == "Home":
    # Hero with beautiful image
    st.markdown("""
        <div style="background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4)), 
                    url('https://images.unsplash.com/photo-1610348725531-843dff563e2c?w=1400&q=80');
                    background-size: cover;
                    background-position: center;
                    padding: 5rem 2rem;
                    border-radius: 20px;
                    text-align: center;
                    margin-bottom: 2rem;
                    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);">
            <h1 style="color: white; 
                       font-size: 3rem; 
                       margin-bottom: 1rem;
                       font-weight: 800;
                       text-shadow: 3px 3px 10px rgba(0,0,0,0.6);">
                Fuel Your Body, Nourish Your Life
            </h1>
            <p style="color: white; 
                      font-size: 1.3rem;
                      font-weight: 300;
                      text-shadow: 2px 2px 6px rgba(0,0,0,0.5);">
                AI-powered personalized nutrition guidance
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Promise section
    st.markdown("""
        <div style="text-align: center; margin: 2.5rem 0 2rem 0;">
            <h2 style="color: #7FD957; font-weight: 300; font-size: 1.6rem; font-style: italic;">
                My promise to <span style="color: #FF6B35;">you</span>...
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature cards - 3 columns for better readability
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🍎</div>
                <h4 style="color: #FF6B35; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.8rem;">
                    Nourishment Without Restriction
                </h4>
                <p style="color: #666; font-size: 0.95rem; line-height: 1.6;">
                    Fuel your body without feeling deprived
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🥬</div>
                <h4 style="color: #7FD957; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.8rem;">
                    Simple & Sustainable
                </h4>
                <p style="color: #666; font-size: 0.95rem; line-height: 1.6;">
                    Make healthy eating effortless every day
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🫑</div>
                <h4 style="color: #4CAF50; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.8rem;">
                    Personalized for You
                </h4>
                <p style="color: #666; font-size: 0.95rem; line-height: 1.6;">
                    A plan that works for your unique needs
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # How it works - 3 steps
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0 1.5rem 0;">
            <h2 style="color: #7FD957; font-weight: 700; font-size: 1.8rem;">How It Works</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 2rem;">
                <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1.2rem auto; box-shadow: 0 8px 20px rgba(255, 107, 53, 0.3);">
                    <span style="color: white; font-size: 1.8rem; font-weight: bold;">1</span>
                </div>
                <h4 style="color: #FF6B35; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.8rem;">Upload Report</h4>
                <p style="color: #666; font-size: 0.95rem;">Upload your medical report (PDF, Word) or type your health information</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 2rem;">
                <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #7FD957 0%, #A8E063 100%); border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1.2rem auto; box-shadow: 0 8px 20px rgba(127, 217, 87, 0.3);">
                    <span style="color: white; font-size: 1.8rem; font-weight: bold;">2</span>
                </div>
                <h4 style="color: #7FD957; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.8rem;">AI Analysis</h4>
                <p style="color: #666; font-size: 0.95rem;">Our 4 AI agents analyze your data and create personalized recommendations</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 2rem;">
                <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #2196F3 0%, #42A5F5 100%); border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1.2rem auto; box-shadow: 0 8px 20px rgba(33, 150, 243, 0.3);">
                    <span style="color: white; font-size: 1.8rem; font-weight: bold;">3</span>
                </div>
                <h4 style="color: #2196F3; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.8rem;">Get Your Plan</h4>
                <p style="color: #666; font-size: 0.95rem;">Receive diet recommendations, 7-day meal plan, and ask follow-up questions</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #7FD957 0%, #4CAF50 100%); 
                        padding: 2rem; border-radius: 15px; text-align: center; margin-top: 1rem;
                        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);">
                <h3 style="color: white; margin-bottom: 0.5rem;">Ready to Start?</h3>
                <p style="color: rgba(255,255,255,0.9); font-size: 0.95rem;">Get your personalized diet plan in minutes</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Upload Your Report", type="primary", use_container_width=True):
            st.session_state.current_page = "Upload"
            st.rerun()

# ---------- UPLOAD PAGE ----------
elif st.session_state.current_page == "Upload":
    st.markdown('<h2 style="color: #2E7D32;">📄 Upload Medical Report</h2>', unsafe_allow_html=True)
    
    if not st.session_state.agents_initialized:
        st.warning("⚠️ Please initialize agents first using the sidebar button")
        st.stop()
    
    # Initialize medical_text in session state
    if 'medical_text' not in st.session_state:
        st.session_state.medical_text = None
    
    # Input options
    tab1, tab2 = st.tabs(["📁 Upload File", "✍️ Type Text"])
    
    with tab1:
        st.info("Supported: PDF, Word (.docx), Text (.txt)")
        uploaded = st.file_uploader("Choose file", type=["pdf", "docx", "txt"])
        
        if uploaded:
            ext = uploaded.name.split(".")[-1]
            temp_file = f"temp_upload.{ext}"
            with open(temp_file, "wb") as f:
                f.write(uploaded.getbuffer())
            
            extracted_text = st.session_state.file_reader.read_file(temp_file)
            if extracted_text and not extracted_text.startswith("❌"):
                st.session_state.medical_text = extracted_text
                st.success(f"✓ Loaded: {uploaded.name}")
                with st.expander("Preview extracted text", expanded=True):
                    st.text(extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text)
            else:
                st.error("Could not read file")
                st.session_state.medical_text = None
    
    with tab2:
        typed_text = st.text_area(
            "Enter your medical information:",
            height=200,
            placeholder="Example: Fasting blood glucose 186 mg/dL, HbA1c 8.2%...",
            key="typed_medical_text"
        )
        if typed_text:
            st.session_state.medical_text = typed_text
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate button
    if st.button("🚀 Generate Diet Plan", type="primary", use_container_width=True):
        medical_text = st.session_state.get('medical_text', None)
        if medical_text and len(medical_text.strip()) > 10:
            with st.spinner("Analyzing... (this takes 1-2 minutes)"):
                st.session_state.results = process_report(medical_text)
            st.success("✅ Done!")
            st.rerun()
        else:
            st.warning("Please enter at least 10 characters or upload a file first")
    
    # Show results
    if st.session_state.results:
        st.markdown("---")
        
        # Translation
        st.markdown('<p class="section-header">📋 Simple Explanation</p>', unsafe_allow_html=True)
        with st.expander("View explanation", expanded=True):
            st.write(st.session_state.results["translation"])
        
        # Foods to Eat / Avoid Table
        st.markdown('<p class="section-header">🥗 Foods to Eat & Avoid</p>', unsafe_allow_html=True)
        
        # Parse diet recommendations to extract foods
        eat_items = []
        avoid_items = []
        avoid_section = False
        diet_text = st.session_state.results["diet"]
        
        for line in diet_text.split("\n"):
            line = line.strip()
            lower_line = line.lower()
            
            # Detect section headers
            if "avoid" in lower_line or "limit" in lower_line:
                if not line.startswith(("-", "•", "*")):
                    avoid_section = True
                    continue
            elif "include" in lower_line or "eat more" in lower_line or "recommended" in lower_line:
                if not line.startswith(("-", "•", "*")):
                    avoid_section = False
                    continue
            
            # Process bullet points
            if not line.startswith(("-", "•", "*")):
                continue
            
            # Clean the food name
            food = re.sub(r'^[-•*]\s*', '', line)
            food = re.sub(r'\s*[:(].*$', '', food)
            food = food.strip()
            
            if not food or len(food) > 50 or len(food) < 3:
                continue
            
            if avoid_section:
                avoid_items.append(food)
            else:
                eat_items.append(food)
        
        # Build table
        max_len = max(len(eat_items), len(avoid_items)) if (eat_items or avoid_items) else 0
        
        if max_len == 0:
            st.info("Food list will appear in the recommendations below")
        else:
            while len(eat_items) < max_len:
                eat_items.append("")
            while len(avoid_items) < max_len:
                avoid_items.append("")
            
            diet_df = pd.DataFrame({
                "✅ Foods to Eat": eat_items[:10],  # Limit to 10 items
                "❌ Foods to Avoid": avoid_items[:10]
            })
            st.table(diet_df)
        
        # Full diet recommendations
        st.markdown('<p class="section-header">📝 Full Diet Recommendations</p>', unsafe_allow_html=True)
        with st.expander("View full recommendations"):
            st.write(st.session_state.results["diet"])
        
        # Meal plan
        st.markdown('<p class="section-header">📅 7-Day Meal Plan</p>', unsafe_allow_html=True)
        with st.expander("View meal plan"):
            st.write(st.session_state.results["meal_plan"])
        
        # PDF Download
        st.markdown('<p class="section-header">📥 Download Report</p>', unsafe_allow_html=True)
        
        # Generate PDF using file-based approach (more reliable)
        def generate_pdf():
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_margins(left=15, top=15, right=15)
            
            # Page 1: Title and Medical Summary
            pdf.add_page()
            pdf.set_font("Times", "B", 18)
            pdf.cell(0, 12, "AI Diet Recommendation Report", ln=True, align="C")
            pdf.set_font("Times", "I", 11)
            pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
            pdf.ln(10)
            
            # Medical Summary
            pdf.set_font("Times", "B", 14)
            pdf.set_fill_color(230, 247, 230)
            pdf.cell(0, 10, "Medical Summary (Simple Explanation)", ln=True, fill=True)
            pdf.ln(3)
            pdf.set_font("Times", "", 11)
            summary = clean_text(st.session_state.results["translation"])
            pdf.multi_cell(0, 6, summary)
            pdf.ln(8)
            
            # Page 2: Foods Table
            pdf.add_page()
            pdf.set_font("Times", "B", 14)
            pdf.set_fill_color(230, 247, 230)
            pdf.cell(0, 10, "Foods to Eat & Avoid", ln=True, fill=True)
            pdf.ln(5)
            
            # Table header
            col_w = 90
            pdf.set_font("Times", "B", 11)
            pdf.set_fill_color(76, 175, 80)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(col_w, 9, "Foods to Eat", border=1, fill=True, align="C")
            pdf.set_fill_color(244, 67, 54)
            pdf.cell(col_w, 9, "Foods to Avoid", border=1, fill=True, align="C", ln=True)
            
            # Table rows
            pdf.set_font("Times", "", 10)
            pdf.set_text_color(0, 0, 0)
            for i in range(min(12, max(len(eat_items), len(avoid_items), 1))):
                eat = clean_text(eat_items[i]) if i < len(eat_items) else ""
                avoid = clean_text(avoid_items[i]) if i < len(avoid_items) else ""
                pdf.cell(col_w, 7, eat[:42], border=1, align="L")
                pdf.cell(col_w, 7, avoid[:42], border=1, align="L", ln=True)
            pdf.ln(8)
            
            # Page 3: Diet Recommendations
            pdf.add_page()
            pdf.set_font("Times", "B", 14)
            pdf.set_fill_color(230, 247, 230)
            pdf.cell(0, 10, "Complete Diet Recommendations", ln=True, fill=True)
            pdf.ln(3)
            pdf.set_font("Times", "", 11)
            diet = clean_text(st.session_state.results["diet"])
            pdf.multi_cell(0, 6, diet)
            
            # Page 4: Meal Plan
            pdf.add_page()
            pdf.set_font("Times", "B", 14)
            pdf.set_fill_color(230, 247, 230)
            pdf.cell(0, 10, "7-Day Meal Plan", ln=True, fill=True)
            pdf.ln(3)
            pdf.set_font("Times", "", 11)
            meal = clean_text(st.session_state.results["meal_plan"])
            pdf.multi_cell(0, 6, meal)
            
            # Footer on last page
            pdf.ln(15)
            pdf.set_font("Times", "I", 9)
            pdf.set_text_color(128, 128, 128)
            pdf.cell(0, 8, "Generated by AI Diet Recommendation System | Developed by Navya", ln=True, align="C")
            pdf.cell(0, 6, "Disclaimer: This is not medical advice. Consult a healthcare professional.", ln=True, align="C")
            
            # Save to temp file and read bytes
            temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
            pdf.output(temp_path)
            with open(temp_path, "rb") as f:
                pdf_bytes = f.read()
            os.remove(temp_path)
            return pdf_bytes
        
        try:
            pdf_bytes = generate_pdf()
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Download Complete Diet Plan (PDF)",
                    data=pdf_bytes,
                    file_name=f"diet_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            # Show PDF preview
            with st.expander("Preview PDF"):
                b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
        
        st.balloons()

# ---------- ASK QUESTIONS PAGE ----------
elif st.session_state.current_page == "Ask":
    st.markdown('<h2 style="color: #2E7D32;">💬 Ask Questions</h2>', unsafe_allow_html=True)
    
    if not st.session_state.agents_initialized:
        st.warning("⚠️ Please initialize agents first using the sidebar button")
        st.stop()
    
    st.markdown("""
        <div class="card">
            <p style="color: #666;">Ask any questions about diet, nutrition, or your health conditions. Our AI will provide helpful answers.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Example questions
    with st.expander("💡 Example questions"):
        st.markdown("""
        - Can I eat rice if I have diabetes?
        - What foods help lower cholesterol?
        - How much water should I drink daily?
        - What are good protein sources for vegetarians?
        """)
    
    question = st.text_area("Your question:", height=100, placeholder="Type your question here...")
    
    if st.button("Get Answer", type="primary"):
        if question and len(question) > 5:
            with st.spinner("Thinking..."):
                answer = st.session_state.qa_bot.answer_question(question)
            
            st.markdown('<p class="section-header">Answer</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="card">{answer}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a question")

# ---------- ABOUT PAGE ----------
elif st.session_state.current_page == "About":
    st.markdown('<h2 style="color: #2E7D32;">ℹ️ About This System</h2>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
            <h4 style="color: #2E7D32;">AI-Powered Diet Recommendation System</h4>
            <p style="color: #666;">This system uses 4 specialized AI agents to analyze your medical reports and create personalized diet plans.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Agents
    st.markdown('<p class="section-header">The 4 AI Agents</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="card">
                <h4 style="color: #2196F3;">🔍 Agent 1: Medical Translator</h4>
                <p style="color: #666;">Translates complex medical terms into simple language</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="card">
                <h4 style="color: #FF6B35;">📅 Agent 3: Meal Planner</h4>
                <p style="color: #666;">Creates 7-day meal plans with recipes</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card">
                <h4 style="color: #4CAF50;">🥗 Agent 2: Diet Recommender</h4>
                <p style="color: #666;">Recommends foods to eat and avoid</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="card">
                <h4 style="color: #9C27B0;">💬 Agent 4: Q&A Bot</h4>
                <p style="color: #666;">Answers your nutrition questions</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Tech stack
    st.markdown('<p class="section-header">Technology</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="card">
            <ul style="color: #666;">
                <li><strong>AI Model:</strong> Google Gemini</li>
                <li><strong>Framework:</strong> Streamlit</li>
                <li><strong>Language:</strong> Python 3.x</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Developer
    st.markdown('<p class="section-header">Developer</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="card" style="text-align: center;">
            <h4 style="color: #FF6B35;">Navya</h4>
            <p style="color: #666;">Data Science & AI Student</p>
            <p style="color: #999; font-size: 0.9rem;">December 2025</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
        <div style="background: #FFF3E0; padding: 1rem; border-radius: 8px; margin-top: 2rem; border-left: 4px solid #FF6B35;">
            <p style="color: #E65100; margin: 0; font-size: 0.9rem;">
                <strong>⚠️ Disclaimer:</strong> This is not medical advice. Always consult a healthcare professional before making dietary changes.
            </p>
        </div>
    """, unsafe_allow_html=True)
