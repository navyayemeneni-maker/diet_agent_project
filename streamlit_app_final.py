"""
Diet Recommendation System - Web Interface
Beautiful Green Leafy Theme

Author: Navya
Date: December 2025
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

def clean_for_pdf(text: str) -> str:
    """
    Replace characters that FPDF 'latin-1' cannot handle.
    Keeps it simple: replace long dashes and smart quotes with basic ASCII.
    """
    if not text:
        return ""
    replacements = {
        "–": "-",
        "—": "-",
        "‑": "-",  # non-breaking hyphen
        "“": '"',
        "”": '"',
        "’": "'",
        "•": "-",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

# Add agents folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Import modules
from file_reader import FileReader
from agent1_translator import MedicalTranslatorAgent
from agent2_recommender import DietRecommenderAgent
from agent3_meal_planner import MealPlanBuilderAgent
from agent4_qa import QASupportAgent

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Diet Recommendation System",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state
if 'agents_initialized' not in st.session_state:
    st.session_state.agents_initialized = False
if 'medical_text' not in st.session_state:
    st.session_state.medical_text = None
if 'translation' not in st.session_state:
    st.session_state.translation = None
if 'diet_recommendation' not in st.session_state:
    st.session_state.diet_recommendation = None
if 'meal_plan' not in st.session_state:
    st.session_state.meal_plan = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize agents
def initialize_agents():
    try:
        with st.spinner("Initializing AI agents..."):
            st.session_state.file_reader = FileReader()
            st.session_state.translator = MedicalTranslatorAgent()
            st.session_state.recommender = DietRecommenderAgent()
            st.session_state.meal_planner = MealPlanBuilderAgent()
            st.session_state.qa_bot = QASupportAgent()
            st.session_state.agents_initialized = True
        st.success("All agents ready!")
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False
# PDF Generation Function
def generate_pdf(translation, diet_recommendation, meal_plan):
    """Generate PDF report with meal plan"""
    
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Diet Recommendation Report", ln=True, align="C")
    pdf.ln(5)
    
    # Date
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
    pdf.ln(10)
    
    # Medical Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Medical Summary (Simple Explanation)", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.ln(3)
    
    # Clean and add translation
    translation_clean = translation.replace('**', '').replace('*', '').replace('#', '')
    pdf.multi_cell(0, 6, translation_clean[:500])  # First 500 chars
    pdf.ln(5)
    
    # Diet Recommendations
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Diet Recommendations", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.ln(3)
    
    diet_clean = diet_recommendation.replace('**', '').replace('*', '').replace('#', '')
    pdf.multi_cell(0, 6, diet_clean[:800])  # First 800 chars
    pdf.ln(5)
    
    # Add new page for meal plan
    pdf.add_page()
    
    # Meal Plan
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "7-Day Meal Plan", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.ln(3)
    
    meal_plan_clean = meal_plan.replace('**', '').replace('*', '').replace('#', '')
    pdf.multi_cell(0, 5, meal_plan_clean[:2000])  # First 2000 chars
    
    # Footer
    pdf.ln(10)
    pdf.set_font("Arial", "I", 9)
    pdf.cell(0, 10, "AI-Powered Diet Recommendation System | Developed by Navya", ln=True, align="C")
    
    # Save to bytes
    pdf_output = pdf.output(dest='S').encode('latin-1')
    return pdf_output

# Process report
def process_medical_report(text):
    # 1. Translate the medical report into simple language
    translation = st.session_state.translator.translate_medical_report(text)
    st.session_state.translation = translation

    # 2. Get diet recommendations (method expects only 'text')
    diet_rec = st.session_state.recommender.recommend_diet(text)

    # 3. Get a 7‑day meal plan from the meal planner agent
    meal_plan = st.session_state.meal_planner.create_meal_plan(diet_rec)

    return {
        "translation": translation,
        "diet_recommendation": diet_rec,
        "meal_plan": meal_plan,
    }

# Green Leafy Vegetable Theme - Professional CSS
st.markdown("""
<style>
/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #90EE90 0%, #228B22 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Main content area */
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* Headers */
h1, h2, h3 {
    color: #2C5F2D;
}

/* Buttons */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1rem;
}

.stButton>button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>🥗 Navigation</h2>", unsafe_allow_html=True)
    
    page = st.selectbox(
        "",
        ["Home", "Upload Report", "Ask Questions", "About"],
        key="nav_selectbox"
    )
    
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>System Status</h3>", unsafe_allow_html=True)
    
    if st.session_state.agents_initialized:
        st.success("✅ Agents Initialized")
    else:
        st.warning("Agents Not Ready")
        if st.button("INITIALIZE AGENTS"):
            initialize_agents()

# HOME PAGE
if page == "Home":
    
    # Hero Section with Beautiful Fruit Image
    st.markdown("""
        <div style="background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4)), 
                    url('https://images.unsplash.com/photo-1610348725531-843dff563e2c?w=1400&q=80');
                    background-size: cover;
                    background-position: center;
                    padding: 5rem 2rem;
                    border-radius: 25px;
                    text-align: center;
                    margin-bottom: 3rem;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);">
            <h1 style="color: white; 
                       font-size: 3.5rem; 
                       margin-bottom: 1.5rem;
                       font-weight: 800;
                       text-shadow: 3px 3px 10px rgba(0,0,0,0.6);">
                Fuel Your Body, Nourish Your Life
            </h1>
            <p style="color: white; 
                      font-size: 1.4rem;
                      font-weight: 300;
                      text-shadow: 2px 2px 6px rgba(0,0,0,0.5);">
                AI-powered personalized nutrition guidance
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # My Promise Section
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2.5rem 0;">
            <h2 style="color: #7FD957; 
                       font-weight: 300; 
                       font-size: 1.8rem;
                       font-style: italic;">
                My promise to <span style="font-style: italic; color: #FF6B35;">you</span>...
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
            <div style="background: white; padding: 2rem 1rem; border-radius: 20px; text-align: center; height: 240px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🍎</div>
                <h4 style="color: #FF6B35; font-weight: 600; margin-bottom: 0.8rem; font-size: 1rem;">
                    Nourishment Without Restriction
                </h4>
                <p style="color: #666; font-size: 0.85rem; line-height: 1.6;">
                    Learn to fuel your body without feeling like you quit
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: white; padding: 2rem 1rem; border-radius: 20px; text-align: center; height: 240px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🥬</div>
                <h4 style="color: #7FD957; font-weight: 600; margin-bottom: 0.8rem; font-size: 1rem;">
                    Simple & Sustainable
                </h4>
                <p style="color: #666; font-size: 0.85rem; line-height: 1.6;">
                    Nutrition shouldn't be complicated, let's make healthy eating effortless
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: white; padding: 2rem 1rem; border-radius: 20px; text-align: center; height: 240px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🥒</div>
                <h4 style="color: #4CAF50; font-weight: 600; margin-bottom: 0.8rem; font-size: 1rem;">
                    Mindful & Enjoyable
                </h4>
                <p style="color: #666; font-size: 0.85rem; line-height: 1.6;">
                    Shift your mindset and reconnect with the joy of food
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div style="background: white; padding: 2rem 1rem; border-radius: 20px; text-align: center; height: 240px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🫑</div>
                <h4 style="color: #FF6B6B; font-weight: 600; margin-bottom: 0.8rem; font-size: 1rem;">
                    Personalized for You
                </h4>
                <p style="color: #666; font-size: 0.85rem; line-height: 1.6;">
                    No one-size-fits-all approach - just a plan that works for you
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
            <div style="background: white; padding: 2rem 1rem; border-radius: 20px; text-align: center; height: 240px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🫛</div>
                <h4 style="color: #2196F3; font-weight: 600; margin-bottom: 0.8rem; font-size: 1rem;">
                    Affordable & Accessible
                </h4>
                <p style="color: #666; font-size: 0.85rem; line-height: 1.6;">
                    Eating well doesn't have to break the bank
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("""
        <div style="text-align: center; margin: 4rem 0 2.5rem 0;">
            <h2 style="color: #7FD957; 
                       font-weight: 700; 
                       font-size: 2rem;">
                How It Works
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Simple 4-step layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style="background: white; padding: 2.5rem 1.5rem; border-radius: 20px; text-align: center; height: 280px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);">
                <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto; box-shadow: 0 8px 20px rgba(255, 107, 53, 0.3);">
                    <span style="color: white; font-size: 2rem; font-weight: bold;">1</span>
                </div>
                <h4 style="color: #FF6B35; font-weight: 700; margin-bottom: 1rem; font-size: 1.1rem;">Upload Report</h4>
                <p style="color: #666; font-size: 0.9rem; line-height: 1.6;">Upload your medical report or type your health concerns</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: white; padding: 2.5rem 1.5rem; border-radius: 20px; text-align: center; height: 280px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);">
                <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #7FD957 0%, #A8E063 100%); border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto; box-shadow: 0 8px 20px rgba(127, 217, 87, 0.3);">
                    <span style="color: white; font-size: 2rem; font-weight: bold;">2</span>
                </div>
                <h4 style="color: #7FD957; font-weight: 700; margin-bottom: 1rem; font-size: 1.1rem;">AI Analysis</h4>
                <p style="color: #666; font-size: 0.9rem; line-height: 1.6;">Our AI analyzes your health data in 2-3 minutes</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: white; padding: 2.5rem 1.5rem; border-radius: 20px; text-align: center; height: 280px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);">
                <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #F4A261 0%, #E9C46A 100%); border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto; box-shadow: 0 8px 20px rgba(244, 162, 97, 0.3);">
                    <span style="color: white; font-size: 2rem; font-weight: bold;">3</span>
                </div>
                <h4 style="color: #F4A261; font-weight: 700; margin-bottom: 1rem; font-size: 1.1rem;">Get Your Plan</h4>
                <p style="color: #666; font-size: 0.9rem; line-height: 1.6;">Receive personalized diet recommendations and meal plans</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div style="background: white; padding: 2.5rem 1.5rem; border-radius: 20px; text-align: center; height: 280px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);">
                <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #2196F3 0%, #42A5F5 100%); border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto; box-shadow: 0 8px 20px rgba(33, 150, 243, 0.3);">
                    <span style="color: white; font-size: 2rem; font-weight: bold;">4</span>
                </div>
                <h4 style="color: #2196F3; font-weight: 700; margin-bottom: 1rem; font-size: 1.1rem;">Ask Questions</h4>
                <p style="color: #666; font-size: 0.9rem; line-height: 1.6;">Get instant answers to your nutrition questions</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Demo Section
    st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF8E7 0%, #FFE5CC 100%); padding: 3rem; border-radius: 25px; margin-top: 3rem; 
                    box-shadow: 0 15px 40px rgba(244, 162, 97, 0.2); border: 2px solid #FFD89B;">
            <h3 style="color: #FF6B35; text-align: center; font-size: 2rem; margin-bottom: 1rem; font-weight: 700;">
                Try a Quick Demo
            </h3>
            <p style="text-align: center; color: #666; margin-bottom: 2rem; font-size: 1.05rem;">
                See how our AI creates personalized diet plans
            </p>
    """, unsafe_allow_html=True)
    
    demo_option = st.selectbox(
        "Choose a health condition:",
        ["Select a demo case...", "Diabetes Management", "Low Iron / Anemia", "High Blood Pressure"]
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        demo_button = st.button("START DEMO", type="primary", use_container_width=True)
    
    if demo_button:
        if demo_option != "Select a demo case...":
            if not st.session_state.agents_initialized:
                initialize_agents()
            
            if demo_option == "Diabetes Management":
                demo_text = "Patient with fasting blood glucose 186 mg/dL and HbA1c 8.2%. Exhibits polydipsia and polyuria."
            elif demo_option == "Low Iron / Anemia":
                demo_text = "Iron levels at 59 µg/dL (normal: 60-180). Patient reports fatigue and weakness."
            else:
                demo_text = "Blood pressure 164/98 mmHg. Stage 2 hypertension diagnosed."
            
            st.info(f"**Processing:** {demo_text}")
            results = process_medical_report(demo_text)
            st.success("✅ Demo completed!")
            
            with st.expander("📄 Simple Explanation", expanded=True):
                st.write(results['translation'])
            with st.expander("🥗 Diet Recommendations"):
                st.write(results['diet_recommendation'])
            with st.expander("📅 Meal Plan"):
                st.write(results['meal_plan'])
        else:
            st.warning("Please select a demo case first!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# UPLOAD REPORT PAGE
elif page == "Upload Report":
    st.header("Upload Your Medical Report")
    if not st.session_state.get("agents_initialized", False):
        st.warning("Please initialize agents first!")
        st.info("Click the button in the sidebar to initialize agents")
    else:
        input_method = st.selectbox(
            "Choose input method:",
            ("Upload File", "Type/Paste Text"),
            key="input_method_select_final",
        )
        medical_text = None

        if input_method == "Upload File":
            st.info("📄 Supported formats: PDF, Word (.docx), Text (.txt)")
            uploaded_file = st.file_uploader(
                "Upload file",
                type=["pdf", "docx", "txt"],
                key="file_uploader_main_final",
            )
            if uploaded_file:
                file_extension = uploaded_file.name.split(".")[-1]
                temp_filename = f"temp_upload.{file_extension}"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                if hasattr(st.session_state, "file_reader"):
                    medical_text = st.session_state.file_reader.read_file(temp_filename)
                    if medical_text and not medical_text.startswith("❌"):
                        st.text_area(
                            "Extracted Text",
                            medical_text,
                            height=150,
                            key="extracted_text_area_final",
                        )
                    else:
                        st.error(
                            medical_text if medical_text else "Could not read file"
                        )
                        medical_text = None
                else:
                    st.error("File reader not initialized")
                    medical_text = None
        else:
            medical_text = st.text_area(
                "Enter your medical information:",
                height=200,
                placeholder=(
                    "Example: Fasting blood glucose 186 mg/dL, "
                    "HbA1c 8.2%, Cholesterol 250 mg/dL..."
                ),
                key="medical_text_input_final",
            )

        if st.button("Generate Diet Plan", type="primary", key="generate_button_final"):
            if medical_text and len(medical_text.strip()) > 10:
                results = process_medical_report(medical_text)

                st.success("✅ Analysis Complete!")
                st.markdown("---")

                # 1) Simple explanation
                with st.expander("📋 Simple Explanation", expanded=True):
                    st.write(results["translation"])

                # Foods table - Section-aware parsing
                st.subheader("🥗 What to Eat and Avoid (Summary)")
                
                import re
                
                eat_items = []
                avoid_items = []
                diet_text = results["diet_recommendation"]
                avoid_section = False
                
                for line in diet_text.split("\n"):
                    line = line.strip()
                    
                    # Detect section headers
                    lower_line = line.lower()
                    if "avoid" in lower_line or "limit" in lower_line:
                        if not line.startswith(("-", "•", "*")):
                            avoid_section = True
                            continue
                    elif "include" in lower_line or "eat more" in lower_line:
                        if not line.startswith(("-", "•", "*")):
                            avoid_section = False
                            continue
                    
                    # Process bullets only
                    if not line.startswith(("-", "•", "*")):
                        continue
                    
                    # Clean the food name
                    food = re.sub(r'^[-•*]\s*', '', line)
                    food = re.sub(r'\s*[:(].*$', '', food)
                    food = re.sub(r'(avoid|limit|eat|include)', '', food, flags=re.IGNORECASE)
                    food = food.strip()
                    
                    if not food or len(food) > 60 or len(food) < 3:
                        continue
                    
                    if avoid_section:
                        avoid_items.append(food)
                    else:
                        eat_items.append(food)
                
                # Build table
                max_len = max(len(eat_items), len(avoid_items)) if (eat_items or avoid_items) else 0
                
                if max_len == 0:
                    st.warning("No food items detected. Try regenerating.")
                    diet_df = pd.DataFrame({"Foods to Eat": ["N/A"], "Foods to Avoid": ["N/A"]})
                else:
                    while len(eat_items) < max_len:
                        eat_items.append("")
                    while len(avoid_items) < max_len:
                        avoid_items.append("")
                    
                    diet_df = pd.DataFrame({"Foods to Eat": eat_items, "Foods to Avoid": avoid_items})
                
                st.table(diet_df)

                st.table(diet_df)
                # 3) 7-day meal plan (collapsible)
                with st.expander("📅 7-Day Meal Plan (Preview)", expanded=False):
                    st.write(results["meal_plan"])

                # 4) BUILD PDF WITH FULL CONTENT
                def build_plan_pdf(translation, diet_text, meal_plan_text):
                    """Generate PDF with bordered foods table"""
                    import re
                    pdf = FPDF()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.set_margins(left=15, top=15, right=15)
                    pdf.add_page()
                    pdf.set_font("Times", "B", 16)
                    pdf.cell(0, 10, "AI Diet Recommendation Report", ln=True, align="C")
                    pdf.ln(3)
                    pdf.set_font("Times", "I", 10)
                    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
                    pdf.ln(5)
                    pdf.set_font("Times", "B", 14)
                    pdf.cell(0, 10, "Medical Summary", ln=True)
                    pdf.set_font("Times", "", 10)
                    pdf.ln(3)
                    pdf.multi_cell(0, 5, clean_for_pdf(translation))
                    pdf.ln(5)
                    pdf.add_page()
                    pdf.set_font("Times", "B", 14)
                    pdf.cell(0, 10, "Foods to Eat & Avoid", ln=True)
                    pdf.ln(5)
                    eat_list = []
                    avoid_list = []
                    avoid_section = False
                    for line in diet_text.split("\n"):
                        line = line.strip()
                        lower_line = line.lower()
                        if "avoid" in lower_line or "limit" in lower_line:
                            if not line.startswith(("-", "•", "*")):
                                avoid_section = True
                                continue
                        elif "include" in lower_line or "eat more" in lower_line:
                            if not line.startswith(("-", "•", "*")):
                                avoid_section = False
                                continue
                        if not line.startswith(("-", "•", "*")):
                            continue
                        food = re.sub(r'^[-•*]\s*', '', line)
                        food = re.sub(r'\s*[:(].*$', '', food)
                        food = re.sub(r'(avoid|limit|eat|include)', '', food, flags=re.IGNORECASE)
                        food = food.strip()
                        if not food or len(food) > 60 or len(food) < 3:
                            continue
                        if avoid_section:
                            avoid_list.append(food)
                        else:
                            eat_list.append(food)
                    if not eat_list and not avoid_list:
                        eat_list = ["No items detected"]
                        avoid_list = [""]
                    max_rows = max(len(eat_list), len(avoid_list))
                    while len(eat_list) < max_rows:
                        eat_list.append("")
                    while len(avoid_list) < max_rows:
                        avoid_list.append("")
                    col_w = 90
                    row_h = 7
                    pdf.set_font("Times", "B", 11)
                    pdf.set_fill_color(220, 220, 220)
                    pdf.cell(col_w, 8, "Foods to Eat", border=1, fill=True, align="C")
                    pdf.cell(col_w, 8, "Foods to Avoid", border=1, fill=True, align="C", ln=True)
                    pdf.set_font("Times", "", 10)
                    for eat, avoid in zip(eat_list, avoid_list):
                        pdf.cell(col_w, row_h, clean_for_pdf(eat)[:45], border=1, align="L")
                        pdf.cell(col_w, row_h, clean_for_pdf(avoid)[:45], border=1, align="L", ln=True)
                    pdf.ln(5)
                    pdf.add_page()
                    pdf.set_font("Times", "B", 14)
                    pdf.cell(0, 10, "Complete Diet Recommendations", ln=True)
                    pdf.set_font("Times", "", 10)
                    pdf.ln(3)
                    pdf.multi_cell(0, 5, clean_for_pdf(diet_text))
                    pdf.add_page()
                    pdf.set_font("Times", "B", 14)
                    pdf.cell(0, 10, "7-Day Meal Plan", ln=True)
                    pdf.set_font("Times", "", 10)
                    pdf.ln(3)
                    pdf.multi_cell(0, 5, clean_for_pdf(meal_plan_text))
                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    pdf.output(tmp_file.name)
                    return tmp_file.name

                # Generate PDF
                # Generate PDF
                pdf_path = build_plan_pdf(
                    results["translation"],
                    results["diet_recommendation"],
                    results["meal_plan"],
                )

                # Read PDF bytes
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                # Download button
                st.download_button(
                    label="📥 Download Complete Diet Plan (PDF)",
                    data=pdf_bytes,
                    file_name="diet_plan_complete.pdf",
                    mime="application/pdf",
                )

                # Show PDF inline
                b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

                # Cleanup temp file
                try:
                    os.remove(pdf_path)
                except OSError:
                    pass

                st.balloons()
            else:
                st.warning("Please provide medical information (at least 10 characters)")
# ASK QUESTIONS PAGE
elif page == "Ask Questions":
    st.header("Ask Questions About Your Diet")
    
    if not st.session_state.get('agents_initialized', False):
        st.warning("Please initialize agents first!")
        st.info("Click the button in the sidebar to initialize agents")
    else:
        st.info("Ask any questions about your diet plan or medical report.")
        
        user_question = st.text_area(
            "Your Question:",
            height=100,
            placeholder="Example: Can I eat rice if I have diabetes?",
            key="user_question_input"
        )
        
        if st.button("Get Answer", type="primary", key="ask_button"):
            if user_question and len(user_question.strip()) > 5:
                with st.spinner("Thinking..."):
                    # Use your QA agent to answer
                    if hasattr(st.session_state, 'qa_bot'):
                        answer = st.session_state.qa_bot.answer_question(user_question)
                        st.success("Answer:")
                        st.write(answer)
                    else:
                        st.error("QA agent not initialized")
            else:
                st.warning("Please enter a question (at least 5 characters)")

    # ABOUT PAGE
elif page == "About":
    
    # Clean Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #7FD957 0%, #A8E063 100%); 
                padding: 2.5rem; 
                border-radius: 20px; 
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(127, 217, 87, 0.25);">
        <h2 style="color: white; margin: 0; text-align: center; font-size: 2rem;">About This System</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # AI System Explanation
    st.markdown("""
    <div style="background: white; 
                padding: 2.5rem; 
                border-radius: 20px; 
                margin: 2rem 0;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);">
        <h3 style="color: #7FD957;">AI-Powered Multi-Agent System</h3>
        <p style="color: #666; font-size: 1.05rem; line-height: 1.8;">
            This system uses <strong>4 specialized AI agents</strong> working together to provide 
            comprehensive nutrition guidance based on your medical information.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Agent 1 & 2 (full width)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                padding: 2rem; 
                border-radius: 15px; 
                margin: 1rem 0;
                border-left: 5px solid #2196F3;">
        <h4 style="color: #1976D2;">Agent 1: Medical Translator</h4>
        <p style="color: #666;">Translates complex medical terminology into simple language you can understand.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                padding: 2rem; 
                border-radius: 15px; 
                margin: 1rem 0;
                border-left: 5px solid #7FD957;">
        <h4 style="color: #5FA832;">Agent 2: Diet Recommender</h4>
        <p style="color: #666;">Analyzes your health conditions and recommends evidence-based therapeutic diets.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Agents 3 & 4 (in columns)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF9E6 0%, #FFE5CC 100%); 
                    padding: 2rem; 
                    border-radius: 15px; 
                    margin: 1rem 0;
                    border-left: 5px solid #F4A261;">
            <h4 style="color: #E76F51;">Agent 3: Meal Plan Builder</h4>
            <p style="color: #666;">Creates practical, personalized 7-day meal plans with detailed recipes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%); 
                    padding: 2rem; 
                    border-radius: 15px; 
                    margin: 1rem 0;
                    border-left: 5px solid #9C27B0;">
            <h4 style="color: #7B1FA2;">Agent 4: Q&A Support Bot</h4>
            <p style="color: #666;">Answers your questions about diet, nutrition, and your personalized plan.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology Stack (full width)
    st.markdown("""
    <div style="background: white; 
                padding: 2.5rem; 
                border-radius: 20px; 
                margin: 2rem 0;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);">
        <h3 style="color: #7FD957;">Technology Stack</h3>
        <ul style="color: #666; font-size: 1.05rem; line-height: 2;">
            <li><strong>AI Model:</strong> Google Gemini 2.5 Flash</li>
            <li><strong>Framework:</strong> Streamlit (Python)</li>
            <li><strong>Language:</strong> Python 3.x</li>
            <li><strong>Design:</strong> Custom CSS with Green Leafy Theme</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Developer Info (full width)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF9966 0%, #FFAB73 100%); 
                padding: 2.5rem; 
                border-radius: 20px; 
                margin: 2rem 0;
                text-align: center;
                box-shadow: 0 10px 30px rgba(255, 153, 102, 0.3);">
        <h3 style="color: white; margin-bottom: 1rem;">Developer</h3>
        <p style="color: white; font-size: 1.2rem; margin: 0.5rem 0;"><strong>Navya</strong></p>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0;">Data Science & AI Student</p>
        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0;">December 2025</p>
    </div>
    """, unsafe_allow_html=True)
