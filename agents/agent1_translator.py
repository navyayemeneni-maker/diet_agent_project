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
from openai import OpenAI

# Load environment variables (API key from .env file)
load_dotenv()

# Configure Groq AI (using OpenAI SDK)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Model fallback list (production-stable models only)
MODEL_FALLBACK = [
    "llama-3.3-70b-versatile",      # Best reasoning for medical context
    "openai/gpt-oss-120b",          # Excellent general reasoning
    "openai/gpt-oss-20b"            # Good fallback, cheaper
]


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
        
        self.client = client
        self.model_fallback = MODEL_FALLBACK
        
        print(f"✅ {self.role} Agent initialized successfully!")
        print(f"   Primary model: {MODEL_FALLBACK[0]}")
        print(f"   Fallback models: {len(MODEL_FALLBACK) - 1}")
    
    
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
        
        # Create a concise prompt for simple explanations
        prompt = f"""
        You are a medical translator. Your job is to explain medical reports in SIMPLE, SHORT language.

        MEDICAL TEXT:
        {medical_text}

        INSTRUCTIONS:
        1. Keep it SHORT - maximum 150-200 words total
        2. Use simple everyday language (5th grade reading level)
        3. NO medical jargon - replace all technical terms
        4. Focus on what the patient NEEDS to know

        FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

        **What Your Report Shows:**
        [2-3 sentences explaining the main findings in simple words]

        **What This Means For You:**
        [2-3 sentences explaining the practical impact on their health]

        **Key Numbers:**
        - [Test name]: [Value] ([Normal/High/Low] - normal is [range])
        - [Only include 2-4 most important values]

        **Next Steps:**
        [1-2 sentences on what they should do]

        Keep it friendly, reassuring, and easy to understand. Avoid scary language.
        """
        
        # Try each model in fallback list
        print("\n🔄 Translating medical text...")
        
        for i, model in enumerate(self.model_fallback):
            try:
                if i > 0:
                    print(f"   Trying fallback model {i}: {model}")
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a medical translator who explains medical reports in simple language."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                translation = response.choices[0].message.content
                print(f"✅ Translation complete using {model}!\n")
                return translation
                
            except Exception as e:
                print(f"   ⚠️ Model {model} failed: {str(e)}")
                if i == len(self.model_fallback) - 1:
                    # Last model failed
                    error_msg = f"❌ All models failed. Last error: {str(e)}"
                    print(error_msg)
                    return error_msg
                continue
    
    
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
        
        print(f"\n🔄 Explaining medical term: '{term}'...")
        
        for i, model in enumerate(self.model_fallback):
            try:
                if i > 0:
                    print(f"   Trying fallback model {i}: {model}")
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a medical translator."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                explanation = response.choices[0].message.content
                print(f"✅ Explanation complete using {model}!\n")
                return explanation
                
            except Exception as e:
                print(f"   ⚠️ Model {model} failed: {str(e)}")
                if i == len(self.model_fallback) - 1:
                    error_msg = f"❌ All models failed. Last error: {str(e)}"
                    print(error_msg)
                    return error_msg
                continue


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
