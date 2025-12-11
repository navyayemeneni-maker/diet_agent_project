"""
Diet Recommendation System - Web Interface
==========================================
Beautiful web interface for the AI-powered diet recommendation system.

Author: Navya
Date: December 4, 2025
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Add agents folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Import modules
from file_reader import FileReader
from agent1_translator import MedicalTranslatorAgent
from agent2_recommender import DietRecommenderAgent
from agent3_meal_planner import MealPlanBuilderAgent
from agent4_qa import QASupportAgent
from agent5_monitor import MonitorAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Diet Recommendation System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Professional Design
# Green Leafy Vegetable Theme - Professional Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main Background - Soft Cream */
    .main {
        background: linear-gradient(135deg, #F9FBF2 0%, #F5F9E9 100%);
    }
    
    /* Content Container */
    .block-container {
        background: white;
        border-radius: 30px 30px 0 0;
        padding: 3rem 2.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 -10px 50px rgba(0, 0, 0, 0.08);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Sidebar - GREEN LEAFY THEME */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #7FD957 0%, #5FA832 100%) !important;
        box-shadow: 5px 0 30px rgba(127, 217, 87, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stselectbox label {
        background: rgba(255, 255, 255, 0.15);
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stselectbox label:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateX(8px);
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
        color: white;
        border: none;
        width: 100%;
    }
    
    /* Title Styling */
    h1 {
        color: #1a1a2e;
        font-weight: 800;
        font-size: 2.8rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Buttons - Orange/Peach */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.05rem;
        transition: all 0.4s ease;
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.6);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #E8F5E9 0%, #F1F8F4 100%);
        border: 3px dashed #7FD957;
        border-radius: 20px;
        padding: 3rem;
    }
    
    /* Chat Messages */
    .stChatMessage {
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Status Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 6px solid #7FD957;
        border-radius: 15px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 6px solid #ffc107;
        border-radius: 15px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFE5CC 100%);
        border-left: 6px solid #F4A261;
        border-radius: 15px;
    }
    
    /* Tables */
    table {
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }
    
    thead tr {
        background: linear-gradient(135deg, #7FD957 0%, #A8E063 100%);
        color: white;
    }
    
    tbody tr:hover {
        background: linear-gradient(135deg, #F9FBF2 0%, #E8F5E9 100%);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #7FD957;
        box-shadow: 0 0 0 3px rgba(127, 217, 87, 0.15);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
    }
    
    h2 {
        color: #1a1a2e;
        font-weight: 700;
        margin-top: 2.5rem;
    }
    
    h3 {
        color: #7FD957;
        font-weight: 600;
    }
    
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agents_initialized' not in st.session_state:
    st.session_state.agents_initialized = False
    st.session_state.translation = None
    st.session_state.diet_recommendation = None
    st.session_state.meal_plan = None
    st.session_state.chat_history = []


def initialize_agents():
    """Initialize all AI agents"""
    if not st.session_state.agents_initialized:
        with st.spinner("🔄 Initializing AI agents..."):
            try:
                st.session_state.file_reader = FileReader()
                st.session_state.translator = MedicalTranslatorAgent()
                st.session_state.recommender = DietRecommenderAgent()
                st.session_state.meal_planner = MealPlanBuilderAgent()
                st.session_state.qa_bot = QASupportAgent()
                st.session_state.monitor = MonitorAgent()
                st.session_state.agents_initialized = True
                return True
            except Exception as e:
                st.error(f"❌ Error initializing agents: {e}")
                return False
    return True


def process_medical_report(medical_text):
    """Process medical report through all agents"""
    
    results = {}
    
    # Step 1: Translate
    with st.spinner("📝 Step 1/4: Translating medical report..."):
        translation = st.session_state.translator.translate_medical_report(medical_text)
        results['translation'] = translation
        st.session_state.translation = translation
    
    # Step 2: Recommend Diet
    with st.spinner("🥗 Step 2/4: Generating diet recommendations..."):
        diet_recommendation = st.session_state.recommender.recommend_diet(translation)
        results['diet_recommendation'] = diet_recommendation
        st.session_state.diet_recommendation = diet_recommendation
    
    # Step 3: Create Meal Plan
    with st.spinner("🍽️ Step 3/4: Creating personalized meal plan..."):
        meal_plan = st.session_state.meal_planner.create_meal_plan(diet_recommendation, duration_days=3)
        results['meal_plan'] = meal_plan
        st.session_state.meal_plan = meal_plan
    
    # Step 4: Set up Q&A
    with st.spinner("💬 Step 4/4: Setting up Q&A assistant..."):
        st.session_state.qa_bot.set_context(
            diet_plan=diet_recommendation,
            meal_plan=meal_plan,
            health_condition=translation
        )
    
    return results


# Main App
def main():
    
    # Header
    st.title("AI-Powered Diet Recommendation System")
    st.caption("Personalized nutrition guidance powered by artificial intelligence")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        
        page = st.selectbox(
            "Choose a page:",
            ["Home", "Upload Report", "Ask Questions", "About"]
        )
        
        st.markdown("---")
        st.markdown("### 🤖 System Status")
        
        if st.session_state.agents_initialized:
            st.success("✅ All agents ready!")
        else:
            st.warning("⚠️ Agents not initialized")
        
        if st.button("🔄 Initialize Agents"):
            if initialize_agents():
                st.success("✅ Agents initialized!")
                st.rerun()
    
    
    # HOME PAGE
    if page == "Home":
        
        # Hero Section - YOUR EXACT IMAGE
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
        
        # How It Works - SIMPLE ICON LAYOUT (like "My Promise")
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
                st.success("Demo completed!")
                
                with st.expander("Simple Explanation", expanded=True):
                    st.write(results['translation'])
                with st.expander("Diet Recommendations"):
                    st.write(results['diet_recommendation'])
                with st.expander("Meal Plan"):
                    st.write(results['meal_plan'])
            else:
                st.warning("Please select a demo case first!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    
    # UPLOAD REPORT PAGE
    elif page == "Upload Report":
        
        # Clean Header (no icons)
        st.markdown("""
            <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); 
                        padding: 2.5rem; 
                        border-radius: 20px; 
                        margin-bottom: 2rem;
                        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.25);">
                <h2 style="color: white; margin: 0; text-align: center; font-size: 2rem;">Upload Your Medical Report</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Initialize agents if not done
        if not st.session_state.agents_initialized:
            if not initialize_agents():
                st.error("Please initialize agents first!")
                return
        
        # Input method selection
        input_method = st.selectbox(
            "Choose input method:",
            ["Upload File", "Type/Paste Text"]
        )
        
        medical_text = None
        
        if input_method == "Upload File":
            
            st.info("📄 Supported formats: PDF, Word (.docx), Text (.txt)")
            
            uploaded_file = st.file_uploader(
                "Upload your medical report",
                type=['pdf', 'docx', 'txt'],
                label_visibility="collapsed"
            )
            
            if uploaded_file is not None:
                
                # Save uploaded file temporarily with proper extension
                file_extension = uploaded_file.name.split('.')[-1]
                temp_filename = f"temp_upload.{file_extension}"
                
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                # Read the file
                with st.spinner("Reading file..."):
                    medical_text = st.session_state.file_reader.read_file(temp_filename)
                
                # Show extracted text
                if not medical_text.startswith("❌"):
                    st.markdown("### Extracted Text:")
                    st.text_area("Medical Text", medical_text, height=150, disabled=True, label_visibility="collapsed")
                else:
                    st.error(medical_text)
                    medical_text = None
        
        else:  # Type/Paste Text
            
            medical_text = st.text_area(
                "Enter your medical information or health concerns:",
                height=200,
                placeholder="Example: I have high blood sugar (180 mg/dL) and my doctor says I need to change my diet..."
            )
        
        # Process button
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            process_button = st.button("GENERATE DIET PLAN", type="primary", use_container_width=True)
        
        if process_button:
            
            if medical_text and not medical_text.startswith("❌"):
                
                st.markdown("---")
                
                # Processing animation
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #7FD957 0%, #A8E063 100%); 
                                padding: 2rem; 
                                border-radius: 15px; 
                                text-align: center;
                                margin: 2rem 0;
                                box-shadow: 0 8px 25px rgba(127, 217, 87, 0.3);">
                        <h3 style="color: white; margin: 0;">🔄 Processing Your Report...</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                # Process through all agents
                results = process_medical_report(medical_text)
                
                st.success("✅ Analysis Complete!")
                
                # Display results with beautiful boxes
                st.markdown("---")
                
                # Translation - Blue Box
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                                padding: 2.5rem; 
                                border-radius: 20px; 
                                border-left: 6px solid #2196F3;
                                margin: 2rem 0;
                                box-shadow: 0 8px 25px rgba(33, 150, 243, 0.2);">
                        <h3 style="color: #1976D2; margin-top: 0;">📄 Simple Explanation</h3>
                """, unsafe_allow_html=True)
                st.write(results['translation'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Diet Recommendation - Green Box
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                                padding: 2.5rem; 
                                border-radius: 20px; 
                                border-left: 6px solid #7FD957;
                                margin: 2rem 0;
                                box-shadow: 0 8px 25px rgba(127, 217, 87, 0.2);">
                        <h3 style="color: #5FA832; margin-top: 0;">🥗 Your Personalized Diet</h3>
                """, unsafe_allow_html=True)
                st.write(results['diet_recommendation'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Meal Plan - Orange Box
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #FFF9E6 0%, #FFE5CC 100%); 
                                padding: 2.5rem; 
                                border-radius: 20px; 
                                border-left: 6px solid #F4A261;
                                margin: 2rem 0;
                                box-shadow: 0 8px 25px rgba(244, 162, 97, 0.2);">
                        <h3 style="color: #E76F51; margin-top: 0;">📅 3-Day Meal Plan</h3>
                """, unsafe_allow_html=True)
                st.write(results['meal_plan'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.balloons()
                
                st.info("💬 Now you can ask questions in the 'Ask Questions' section!")
                
            else:
                st.warning("⚠️ Please provide medical information first!")
    

    # ASK QUESTIONS PAGE
    elif page == "Ask Questions":
        
        # Clean Header (no icons)
        st.markdown("""
            <div style="background: linear-gradient(135deg, #2196F3 0%, #42A5F5 100%); 
                        padding: 2.5rem; 
                        border-radius: 20px; 
                        margin-bottom: 2rem;
                        box-shadow: 0 10px 30px rgba(33, 150, 243, 0.25);">
                <h2 style="color: white; margin: 0; text-align: center; font-size: 2rem;">Ask Questions About Your Diet</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.agents_initialized:
            st.warning("⚠️ Please initialize agents first!")
            return
        
        if st.session_state.diet_recommendation is None:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #FFF9E6 0%, #FFE5CC 100%); 
                            padding: 2rem; 
                            border-radius: 15px; 
                            border-left: 5px solid #F4A261;
                            margin: 2rem 0;">
                    <p style="color: #E76F51; font-size: 1.1rem; margin: 0;">
                        ⚠️ Please upload and process a medical report first!
                    </p>
                    <p style="color: #666; margin-top: 1rem; margin-bottom: 0;">
                        👉 Go to 'Upload Report' page to get started
                    </p>
                </div>
            """, unsafe_allow_html=True)
            return
        
        # Chat interface
        st.markdown("""
            <div style="background: linear-gradient(135deg, #E8F5E9 0%, #F1F8F4 100%); 
                        padding: 1.5rem; 
                        border-radius: 15px; 
                        margin-bottom: 2rem;
                        border-left: 5px solid #7FD957;">
                <p style="color: #5FA832; font-size: 1.05rem; margin: 0;">
                    💚 Your personalized nutrition assistant is ready!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat['question'])
            with st.chat_message("assistant"):
                st.write(chat['answer'])
        
        # Question input
        question = st.chat_input("Ask your question here...")
        
        if question:
            
            # Add to chat history
            with st.chat_message("user"):
                st.write(question)
            
            # Get answer
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    answer = st.session_state.qa_bot.answer_question(question)
                st.write(answer)
            
            # Save to history
            st.session_state.chat_history.append({
                'question': question,
                'answer': answer
            })
       
    # ABOUT PAGE
    elif page == "About":
        
        # Clean Header (no icons)
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
                    This system uses <strong>5 specialized AI agents</strong> working together to provide 
                    comprehensive nutrition guidance based on your medical information.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Agents Grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                            padding: 2rem; 
                            border-radius: 15px; 
                            margin: 1rem 0;
                            border-left: 5px solid #2196F3;">
                    <h4 style="color: #1976D2;">Agent 1: Medical Translator</h4>
                    <p style="color: #666;">Translates complex medical terminology into simple language.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                            padding: 2rem; 
                            border-radius: 15px; 
                            margin: 1rem 0;
                            border-left: 5px solid #7FD957;">
                    <h4 style="color: #5FA832;">Agent 2: Diet Recommender</h4>
                    <p style="color: #666;">Analyzes health conditions and recommends therapeutic diets.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style="background: linear-gradient(135deg, #FFF9E6 0%, #FFE5CC 100%); 
                            padding: 2rem; 
                            border-radius: 15px; 
                            margin: 1rem 0;
                            border-left: 5px solid #F4A261;">
                    <h4 style="color: #E76F51;">Agent 3: Meal Plan Builder</h4>
                    <p style="color: #666;">Creates practical meal plans with recipes.</p>
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
                    <p style="color: #666;">Answers questions about diet and nutrition.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style="background: linear-gradient(135deg, #FFE5E5 0%, #FFD6D6 100%); 
                            padding: 2rem; 
                            border-radius: 15px; 
                            margin: 1rem 0;
                            border-left: 5px solid #FF6B6B;">
                    <h4 style="color: #E53935;">Agent 5: System Monitor</h4>
                    <p style="color: #666;">Coordinates all agents and ensures quality.</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Technology Stack
        st.markdown("""
            <div style="background: white; 
                        padding: 2.5rem; 
                        border-radius: 20px; 
                        margin: 2rem 0;
                        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);">
                <h3 style="color: #7FD957;">Technology Stack</h3>
                <ul style="color: #666; font-size: 1.05rem; line-height: 2;">
                    <li><strong>AI Model:</strong> Google Gemini 2.5 Flash</li>
                    <li><strong>Framework:</strong> Streamlit</li>
                    <li><strong>Language:</strong> Python</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # Developer Info
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
    
