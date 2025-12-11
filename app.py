"""
Diet Recommendation System - Final Version with Dashboard
=========================================================
Clean Streamlit app with 4 AI agents + Dashboard.
Author: Navya | December 2025
"""

import streamlit as st
import sys
import os
import base64
from datetime import datetime
from fpdf import FPDF
import tempfile
import pandas as pd
import re

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
def process_report(text):
    """Run all agents on medical report."""
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

# ============== CSS ==============
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stSidebar"] {background: linear-gradient(180deg, #2E7D32 0%, #1B5E20 100%);}
.card {background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;}
.section-header {color: #2E7D32; font-size: 1.5rem; font-weight: 600; margin: 2rem 0 1rem 0; border-bottom: 2px solid #E8F5E9; padding-bottom: 0.5rem;}
.profile-card {background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #4CAF50;}
.stat-card {background: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08);}
.stat-number {font-size: 2.5rem; font-weight: 700; color: #2E7D32;}
.stat-label {color: #666; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

# ============== SIDEBAR ==============
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 1rem;">
            <span style="font-size: 3rem;">🥗</span>
            <h2 style="color: white; margin: 0.5rem 0 0 0;">Diet Planner</h2>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">AI-Powered Nutrition</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    pages = [
        ("🏠 Home", "Home"),
        ("📊 Dashboard", "Dashboard"),
        ("👤 My Profile", "Profile"),
        ("🩺 Analyze Health", "Upload"),
        ("💬 Ask Questions", "Ask"),
        ("ℹ️ About", "About")
    ]
    
    for label, key in pages:
        if st.button(label, use_container_width=True, type="primary" if st.session_state.current_page == key else "secondary", key=f"nav_{key}"):
            st.session_state.current_page = key
            st.rerun()
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    
    # Profile status
    profile = get_profile()
    if profile:
        st.markdown(f"""
            <div style="background: rgba(165,214,167,0.2); padding: 10px; border-radius: 8px;">
                <span style="color: #A5D6A7;">👤 {profile.get('name', 'User')}</span><br>
                <span style="color: rgba(255,255,255,0.6); font-size: 12px;">{profile.get('diet_type', '')}</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: rgba(255,183,77,0.2); padding: 10px; border-radius: 8px;"><span style="color: #FFB74D;">⚠ No Profile</span></div>', unsafe_allow_html=True)

# ============== REDIRECT FIRST-TIME USERS ==============
if not has_profile() and st.session_state.current_page not in ["Profile", "About"]:
    st.session_state.current_page = "Profile"

# ============== PAGES ==============

# ---------- DASHBOARD PAGE ----------
if st.session_state.current_page == "Dashboard":
    st.markdown('<h2 style="color: #2E7D32;">📊 Your Nutrition Dashboard</h2>', unsafe_allow_html=True)
    
    profile = get_profile()
    if not profile:
        st.warning("Please complete your profile first.")
        st.stop()
    
    # Load stats
    stats = get_stats()
    reports = load_reports()
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number">{stats["total_reports"]}</div>
                <div class="stat-label">Reports Generated</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number" style="color: #FF6B35;">{len(stats["conditions"])}</div>
                <div class="stat-label">Conditions Tracked</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number" style="color: #2196F3;">{profile.get("diet_type", "N/A")[:3]}</div>
                <div class="stat-label">Diet Type</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        allergies_count = len(profile.get("allergies", []))
        st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number" style="color: #E91E63;">{allergies_count}</div>
                <div class="stat-label">Allergies</div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Conditions Overview (with safe check)
    condition_counts = stats.get("condition_counts", {})
    if condition_counts:
        st.markdown('<p class="section-header">🏥 Health Conditions Detected</p>', unsafe_allow_html=True)
        
        # Create a simple bar chart
        conditions_df = pd.DataFrame([
            {"Condition": k, "Count": v} 
            for k, v in condition_counts.items()
        ])
        
        if not conditions_df.empty:
            st.bar_chart(conditions_df.set_index("Condition"))
    
    # Recent Reports
    st.markdown('<p class="section-header">📄 Your Report History</p>', unsafe_allow_html=True)
    
    if not reports:
        st.info("No reports yet. Upload your first medical report to get started!")
        
        if st.button("📄 Upload Your First Report", type="primary"):
            st.session_state.current_page = "Upload"
            st.rerun()
    else:
        for i, report in enumerate(reports[:10]):  # Show last 10
            date = report.get("date", "Unknown")
            time_str = report.get("time", "")
            conditions = report.get("conditions_found", ["General"])
            report_id = report.get("report_id", 0)
            
            with st.expander(f"📅 {date} {time_str} — {', '.join(conditions[:3])}", expanded=(i == 0)):
                
                tab1, tab2, tab3 = st.tabs(["📋 Summary", "🥗 Diet Plan", "📅 Meal Plan"])
                
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
                            "📥 Download PDF",
                            pdf_data,
                            f"diet_plan_{date}.pdf",
                            "application/pdf",
                            key=f"pdf_{report_id}"
                        )
                    except:
                        pass
                
                with col3:
                    if st.button("🗑️ Delete", key=f"del_{report_id}", type="secondary"):
                        delete_report(report_id)
                        st.rerun()
    
    # Quick Stats
    if reports:
        st.markdown('<p class="section-header">📈 Quick Stats</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'''
                <div class="card">
                    <h4 style="color: #2E7D32;">📅 Timeline</h4>
                    <p><strong>First Report:</strong> {stats.get("first_report_date", "N/A")}</p>
                    <p><strong>Latest Report:</strong> {stats.get("last_report_date", "N/A")}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            most_common = stats.get("most_common_condition", "None")
            st.markdown(f'''
                <div class="card">
                    <h4 style="color: #FF6B35;">🔍 Most Common Condition</h4>
                    <p style="font-size: 1.5rem; font-weight: 600; color: #2E7D32;">{most_common}</p>
                </div>
            ''', unsafe_allow_html=True)

# ---------- PROFILE PAGE ----------
elif st.session_state.current_page == "Profile":
    profile = get_profile()
    is_new = profile is None
    
    if is_new:
        st.markdown('<div style="text-align: center;"><span style="font-size: 4rem;">👋</span><h1 style="color: #2E7D32;">Welcome!</h1><p>Let\'s personalize your diet plan</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color: #2E7D32;">👤 My Profile</h2>', unsafe_allow_html=True)
    
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
        
        if st.form_submit_button("💾 Save Profile", type="primary", use_container_width=True):
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
                st.success("✅ Profile saved!")
                st.balloons()
                import time; time.sleep(1)
                st.session_state.current_page = "Home"
                st.rerun()
    
    if not is_new:
        with st.expander("⚠️ Delete Profile"):
            if st.button("🗑️ Delete"):
                delete_profile()
                st.session_state.user_profile = None
                st.rerun()

# ---------- HOME PAGE ----------
elif st.session_state.current_page == "Home":
    profile = get_profile()
    stats = get_stats()
    
    if profile:
        st.markdown(f'<div class="profile-card"><h2 style="color: #2E7D32; margin: 0;">Welcome back, {profile.get("name", "there")}! 👋</h2></div>', unsafe_allow_html=True)
    
    # Hero
    st.markdown("""
        <div style="background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1610348725531-843dff563e2c?w=1400'); background-size: cover; background-position: center; padding: 4rem 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
            <h1 style="color: white; font-size: 2.5rem; text-shadow: 2px 2px 8px rgba(0,0,0,0.5);">Fuel Your Body, Nourish Your Life</h1>
            <p style="color: white;">AI-powered personalized nutrition</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick stats for returning users
    if stats["total_reports"] > 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{stats["total_reports"]}</div><div class="stat-label">Reports</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#FF6B35;">{len(stats["conditions"])}</div><div class="stat-label">Conditions</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#2196F3;">📊</div><div class="stat-label"><a href="#" onclick="return false;">View Dashboard</a></div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Profile summary
    if profile:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="card" style="text-align:center;"><span style="font-size:2rem;">🥗</span><p style="margin:0;color:#666;">Diet</p><strong>{profile.get("diet_type","")}</strong></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card" style="text-align:center;"><span style="font-size:2rem;">🎯</span><p style="margin:0;color:#666;">Goal</p><strong>{profile.get("weight_goal","")}</strong></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="card" style="text-align:center;"><span style="font-size:2rem;">⏱️</span><p style="margin:0;color:#666;">Cooking</p><strong>{profile.get("cooking_time","")}</strong></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="card" style="text-align:center;"><span style="font-size:2rem;">⚠️</span><p style="margin:0;color:#666;">Allergies</p><strong>{len(profile.get("allergies", []))} items</strong></div>', unsafe_allow_html=True)
    
    # How it works
    st.markdown('<p class="section-header">How It Works</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card" style="text-align:center;"><div style="width:50px;height:50px;background:#FF6B35;border-radius:50%;margin:0 auto 1rem;display:flex;align-items:center;justify-content:center;"><span style="color:white;font-weight:bold;">1</span></div><h4 style="color:#FF6B35;">Upload Report</h4><p style="color:#666;">Upload your medical report</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card" style="text-align:center;"><div style="width:50px;height:50px;background:#4CAF50;border-radius:50%;margin:0 auto 1rem;display:flex;align-items:center;justify-content:center;"><span style="color:white;font-weight:bold;">2</span></div><h4 style="color:#4CAF50;">AI Analysis</h4><p style="color:#666;">4 AI agents analyze your data</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card" style="text-align:center;"><div style="width:50px;height:50px;background:#2196F3;border-radius:50%;margin:0 auto 1rem;display:flex;align-items:center;justify-content:center;"><span style="color:white;font-weight:bold;">3</span></div><h4 style="color:#2196F3;">Get Your Plan</h4><p style="color:#666;">Personalized diet & meal plan</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🩺 Analyze Your Health", type="primary", use_container_width=True):
            st.session_state.current_page = "Upload"
            st.rerun()


# ---------- ANALYZE HEALTH PAGE ----------
elif st.session_state.current_page == "Upload":
    st.markdown('<h2 style="color: #2E7D32;">🩺 Analyze Your Health</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666;">Upload your medical report or enter your health data to get a personalized diet plan.</p>', unsafe_allow_html=True)
    
    profile = get_profile()
    if profile:
        restrictions = []
        if profile.get('diet_type') != 'Non-Vegetarian':
            restrictions.append(profile['diet_type'])
        if profile.get('religious_restrictions') != 'None':
            restrictions.append(profile['religious_restrictions'])
        restrictions.extend(profile.get('allergies', []))
        if restrictions:
            st.markdown(f'<div class="profile-card"><strong>🛡️ Your restrictions:</strong> {", ".join(restrictions[:5])}</div>', unsafe_allow_html=True)
    
    # Clear data option at top
    if st.session_state.medical_text or st.session_state.results:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Clear Data", type="secondary", use_container_width=True):
                st.session_state.medical_text = None
                st.session_state.results = None
                st.rerun()
    
    # Input tabs
    tab1, tab2 = st.tabs(["📁 Upload File", "✍️ Type Text"])
    
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
                if text and not text.startswith("❌"):
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
    if st.button("🚀 Generate Diet Plan", type="primary", use_container_width=True):
        if st.session_state.medical_text and len(st.session_state.medical_text) > 10:
            with st.spinner("Analyzing... (1-2 minutes)"):
                try:
                    st.session_state.results = process_report(st.session_state.medical_text)
                    
                    # Save report to history
                    save_report(
                        medical_text=st.session_state.medical_text,
                        translation=st.session_state.results["translation"],
                        diet_rec=st.session_state.results["diet"],
                        meal_plan=st.session_state.results["meal_plan"]
                    )
                    
                    st.success("✅ Done! Report saved to your dashboard.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter text or upload a file")
    
    # Show results
    if st.session_state.results:
        st.markdown("---")
        
        st.markdown('<p class="section-header">📋 Simple Explanation</p>', unsafe_allow_html=True)
        with st.expander("View", expanded=True):
            st.write(st.session_state.results["translation"])
        
        st.markdown('<p class="section-header">🥗 Foods to Eat & Avoid</p>', unsafe_allow_html=True)
        
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
            st.table(pd.DataFrame({"✅ Eat": eat_items[:10], "❌ Avoid": avoid_items[:10]}))
        
        st.markdown('<p class="section-header">📝 Full Recommendations</p>', unsafe_allow_html=True)
        with st.expander("View"):
            st.write(st.session_state.results["diet"])
        
        st.markdown('<p class="section-header">📅 7-Day Meal Plan</p>', unsafe_allow_html=True)
        with st.expander("View"):
            st.write(st.session_state.results["meal_plan"])
        
        # PDF Download & Preview
        st.markdown('<p class="section-header">📥 Download Report</p>', unsafe_allow_html=True)
        try:
            pdf_bytes = generate_pdf(st.session_state.results, profile)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    "📥 Download Complete Diet Plan (PDF)", 
                    pdf_bytes, 
                    f"diet_plan_{datetime.now().strftime('%Y%m%d')}.pdf", 
                    "application/pdf", 
                    use_container_width=True
                )
            
            # PDF Preview
            with st.expander("👁️ Preview PDF"):
                import base64
                b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"PDF error: {e}")
        
        st.balloons()

# ---------- ASK PAGE ----------
elif st.session_state.current_page == "Ask":
    st.markdown('<h2 style="color: #2E7D32;">💬 Ask Questions</h2>', unsafe_allow_html=True)
    
    profile = get_profile()
    if profile:
        st.markdown(f'<div class="profile-card">Hi {profile.get("name", "there")}! Ask me anything about diet.</div>', unsafe_allow_html=True)
    
    with st.expander("💡 Examples"):
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
    st.markdown('<h2 style="color: #2E7D32;">ℹ️ About This System</h2>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown('''
        <div class="card">
            <h4 style="color: #2E7D32;">🥗 AI-Powered Diet Recommendation System</h4>
            <p style="color: #666; line-height: 1.8;">
                This system uses artificial intelligence to analyze your medical reports and create 
                <strong>personalized diet plans</strong> that respect your dietary preferences, allergies, 
                and cultural restrictions. It's like having a personal nutritionist available 24/7!
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    # How AI Agents Help
    st.markdown('<p class="section-header">🤖 How Our AI Agents Help You</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
            <div class="card">
                <h4 style="color: #2196F3;">🔍 Medical Translator</h4>
                <p style="color: #666;">
                    Converts complex medical jargon into <strong>simple, easy-to-understand language</strong>. 
                    No more confusion about what your blood test results mean!
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
            <div class="card">
                <h4 style="color: #FF6B35;">📅 Meal Planner</h4>
                <p style="color: #666;">
                    Creates a <strong>practical 7-day meal plan</strong> with breakfast, lunch, dinner, 
                    and snacks. Includes quick recipes and a shopping list!
                </p>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
            <div class="card">
                <h4 style="color: #4CAF50;">🥗 Diet Recommender</h4>
                <p style="color: #666;">
                    Analyzes your health conditions and creates <strong>personalized food recommendations</strong>. 
                    Tells you exactly what to eat and what to avoid.
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
            <div class="card">
                <h4 style="color: #E91E63;">💬 Q&A Assistant</h4>
                <p style="color: #666;">
                    Have questions about your diet? Ask anything! The AI will give you 
                    <strong>personalized answers</strong> based on your profile and health conditions.
                </p>
            </div>
        ''', unsafe_allow_html=True)
    
    # Personalization
    st.markdown('<p class="section-header">🛡️ Personalization & Safety</p>', unsafe_allow_html=True)
    
    st.markdown('''
        <div class="card">
            <p style="color: #666; line-height: 1.8;">
                Your profile ensures the AI <strong>never recommends foods you can't eat</strong>:
            </p>
            <ul style="color: #666; line-height: 2;">
                <li>🥬 <strong>Vegetarian/Vegan:</strong> No meat, fish, or animal products</li>
                <li>🙏 <strong>Hindu:</strong> No beef recommendations</li>
                <li>☪️ <strong>Muslim/Halal:</strong> No pork recommendations</li>
                <li>⚠️ <strong>Allergies:</strong> Dangerous foods are completely excluded</li>
                <li>👎 <strong>Dislikes:</strong> Foods you hate won't appear in your plan</li>
                <li>⏱️ <strong>Cooking Time:</strong> Recipes fit your schedule</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)
    
    # Features
    st.markdown('<p class="section-header">✨ Key Features</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
            <div class="card" style="text-align: center;">
                <span style="font-size: 2.5rem;">📊</span>
                <h4 style="color: #2E7D32;">Dashboard</h4>
                <p style="color: #666; font-size: 0.9rem;">Track all your reports and health conditions over time</p>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
            <div class="card" style="text-align: center;">
                <span style="font-size: 2.5rem;">📄</span>
                <h4 style="color: #2E7D32;">PDF Export</h4>
                <p style="color: #666; font-size: 0.9rem;">Download your meal plans to share with family or doctors</p>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
            <div class="card" style="text-align: center;">
                <span style="font-size: 2.5rem;">🔒</span>
                <h4 style="color: #2E7D32;">Privacy</h4>
                <p style="color: #666; font-size: 0.9rem;">Your data stays on your device, not stored on any server</p>
            </div>
        ''', unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown('''
        <div style="background: #FFF3E0; padding: 1.5rem; border-radius: 12px; margin-top: 2rem; border-left: 4px solid #FF6B35;">
            <h4 style="color: #E65100; margin: 0 0 0.5rem 0;">⚠️ Important Disclaimer</h4>
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
    st.markdown('''
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); border-radius: 12px;">
            <p style="color: #666; margin: 0;">Developed with ❤️ by</p>
            <h3 style="color: #2E7D32; margin: 0.5rem 0;">Navya</h3>
            <p style="color: #888; margin: 0;">Data Science & AI Student • December 2025</p>
        </div>
    ''', unsafe_allow_html=True)
