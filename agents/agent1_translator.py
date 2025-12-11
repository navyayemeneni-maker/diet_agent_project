"""
Medical Translator Agent
========================
This agent translates complex medical terminology and reports 
into simple, easy-to-understand language for patients.

Agent Profile:
- Role: Medical Language Translator
- Expertise: Simplifying medical jargon
- Goal: Make health information accessible to everyone
"""

# ============================================================
# LAYER 1: IMPORTS AND CONFIGURATION
# ============================================================

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables (API key from .env file)
load_dotenv()

# Configure Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
# Using gemini-2.5-flash (fast and efficient for translation tasks)
model = genai.GenerativeModel('gemini-2.5-flash')


# ============================================================
# LAYER 2: AGENT DEFINITION
# ============================================================

class MedicalTranslatorAgent:
    """
    An AI agent specialized in translating medical terminology
    into patient-friendly language.
    
    Attributes:
        role: The agent's professional role
        goal: What the agent aims to achieve
        backstory: The agent's expertise and experience
        model: The AI model used for translation
    """
    
    def __init__(self):
        """Initialize the Medical Translator Agent"""
        
        # Agent Identity
        self.role = "Medical Language Translator"
        
        self.goal = """
        Transform complex medical reports, diagnoses, and terminology 
        into simple, clear language that patients can easily understand, 
        while maintaining medical accuracy.
        """
        
        self.backstory = """
        You are an expert medical translator with 15+ years of experience 
        working between healthcare providers and patients. You have:
        
        - Deep knowledge of medical terminology across all specialties
        - Experience explaining complex diagnoses to patients
        - A talent for using analogies and simple examples
        - Understanding of patient anxiety and the importance of clarity
        - Training in health literacy and patient education
        
        Your translations are:
        - Accurate (never lose medical meaning)
        - Simple (use everyday language)
        - Empathetic (consider patient emotions)
        - Actionable (explain what it means for the patient)
        """
        
        self.model = model
        
        print(f"✅ {self.role} Agent initialized successfully!")
    
    
    # ============================================================
    # LAYER 3: TRANSLATION FUNCTION
    # ============================================================
    
    def translate_medical_report(self, medical_text):
        """
        Translate complex medical text into patient-friendly language.
        
        Args:
            medical_text (str): The medical report or terminology to translate
            
        Returns:
            str: Simplified, patient-friendly translation
        """
        
        # Create a detailed prompt for the AI
        prompt = f"""
        You are {self.role}.
        
        YOUR GOAL: {self.goal}
        
        YOUR BACKGROUND: {self.backstory}
        
        TASK: Translate the following medical text into simple language 
        that a patient with no medical background can understand.
        
        GUIDELINES:
        1. Replace medical jargon with everyday words
        2. Explain what terms mean in practical terms
        3. Use analogies when helpful
        4. Keep it accurate but accessible
        5. If there are concerning findings, explain them gently but clearly
        6. Structure the response with clear sections
        
        MEDICAL TEXT TO TRANSLATE:
        {medical_text}
        
        PATIENT-FRIENDLY TRANSLATION:
        """
        
        try:
            # Generate translation using Gemini AI
            print("\n🔄 Translating medical text...")
            response = self.model.generate_content(prompt)
            
            # Extract the translated text
            translation = response.text
            
            print("✅ Translation complete!\n")
            return translation
            
        except Exception as e:
            error_msg = f"❌ Translation failed: {str(e)}"
            print(error_msg)
            return error_msg
    
    
    def translate_medical_term(self, term):
        """
        Translate a single medical term into simple language.
        
        Args:
            term (str): Medical term to translate
            
        Returns:
            str: Simple explanation of the term
        """
        
        prompt = f"""
        You are a medical translator. Explain this medical term in simple 
        language that anyone can understand:
        
        MEDICAL TERM: {term}
        
        Provide:
        1. Simple definition (one sentence)
        2. What it means for the patient (practical impact)
        3. Example in everyday language
        
        Keep it brief and clear.
        """
        
        try:
            print(f"\n🔄 Explaining medical term: '{term}'...")
            response = self.model.generate_content(prompt)
            explanation = response.text
            print("✅ Explanation complete!\n")
            return explanation
            
        except Exception as e:
            error_msg = f"❌ Explanation failed: {str(e)}"
            print(error_msg)
            return error_msg


# ============================================================
# LAYER 4: TEST/DEMO CODE
# ============================================================

def demo_translator():
    """
    Demonstration of the Medical Translator Agent capabilities.
    This function shows how to use the agent with sample medical reports.
    """
    
    print("=" * 60)
    print("🏥 MEDICAL TRANSLATOR AGENT - DEMO")
    print("=" * 60)
    
    # Initialize the agent
    agent = MedicalTranslatorAgent()
    
    # Sample Medical Report 1: Diabetes
    print("\n" + "=" * 60)
    print("📋 EXAMPLE 1: Diabetes Report")
    print("=" * 60)
    
    medical_report_1 = """
    Patient presents with hyperglycemia with fasting blood glucose 
    of 186 mg/dL and HbA1c of 8.2%. Patient exhibits polydipsia, 
    polyuria, and fatigue. Recommend carbohydrate restriction, 
    initiation of metformin 500mg BID, and follow-up in 3 months 
    for glycemic control assessment.
    """
    
    print("\n📄 ORIGINAL MEDICAL TEXT:")
    print(medical_report_1)
    
    translation_1 = agent.translate_medical_report(medical_report_1)
    print("\n👤 PATIENT-FRIENDLY TRANSLATION:")
    print(translation_1)
    
    
    # Sample Medical Report 2: Hypertension
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 2: Blood Pressure Report")
    print("=" * 60)
    
    medical_report_2 = """
    Patient diagnosed with Stage 2 hypertension (BP 164/98 mmHg).
    Recommend lifestyle modifications including DASH diet, sodium 
    restriction to <2g/day, and initiation of ACE inhibitor therapy.
    Monitor for orthostatic hypotension and renal function.
    """
    
    print("\n📄 ORIGINAL MEDICAL TEXT:")
    print(medical_report_2)
    
    translation_2 = agent.translate_medical_report(medical_report_2)
    print("\n👤 PATIENT-FRIENDLY TRANSLATION:")
    print(translation_2)
    
    
    # Sample Medical Term Translation
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 3: Single Term Explanation")
    print("=" * 60)
    
    term = "Hyperlipidemia"
    explanation = agent.translate_medical_term(term)
    print(f"\n📖 TERM: {term}")
    print(f"\n💡 SIMPLE EXPLANATION:")
    print(explanation)
    
    
    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETE!")
    print("=" * 60)


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    """
    This code runs when you execute the file directly.
    It demonstrates the agent's capabilities.
    """
    demo_translator()
