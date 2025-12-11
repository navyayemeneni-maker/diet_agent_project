"""
Diet Recommender Agent
======================
This agent recommends specific diets based on medical conditions
and health concerns identified in medical reports.

Agent Profile:
- Role: Clinical Nutritionist & Diet Specialist
- Expertise: Medical nutrition therapy
- Goal: Recommend evidence-based diets for specific health conditions
"""

# ============================================================
# LAYER 1: IMPORTS AND CONFIGURATION
# ============================================================

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')


# ============================================================
# LAYER 2: AGENT DEFINITION
# ============================================================

class DietRecommenderAgent:
    """
    An AI agent specialized in recommending therapeutic diets
    based on medical conditions.
    
    Attributes:
        role: The agent's professional role
        goal: What the agent aims to achieve
        backstory: The agent's expertise and experience
        model: The AI model used for recommendations
    """
    
    def __init__(self):
        """Initialize the Diet Recommender Agent"""
        
        # Agent Identity
        self.role = "Clinical Nutritionist & Diet Specialist"
        
        self.goal = """
        Analyze medical conditions and health concerns to recommend 
        specific, evidence-based dietary approaches that can help 
        manage, improve, or prevent the progression of health issues.
        """
        
        self.backstory = """
        You are a certified clinical nutritionist with 20+ years of experience 
        in medical nutrition therapy. You have:
        
        - Advanced degrees in Clinical Nutrition and Dietetics
        - Specialization in therapeutic diets for chronic diseases
        - Experience working with diabetic, cardiac, renal patients
        - Deep knowledge of nutritional biochemistry
        - Published research on diet-disease relationships
        - Training in personalized nutrition approaches
        
        Your recommendations are:
        - Evidence-based (backed by scientific research)
        - Condition-specific (tailored to the health issue)
        - Practical (easy to follow in real life)
        - Safe (no extreme or dangerous approaches)
        - Comprehensive (cover foods to eat AND avoid)
        """
        
        self.model = model
        
        print(f"✅ {self.role} Agent initialized successfully!")
    
    
    # ============================================================
    # LAYER 3: RECOMMENDATION FUNCTIONS
    # ============================================================
    
    def recommend_diet(self, health_condition):
        """
        Recommend a specific diet based on health condition.
        
        Args:
            health_condition (str): The health issue or translated medical report
            
        Returns:
            str: Detailed diet recommendations
        """
        
        prompt = f"""Based on this medical analysis, provide a diet recommendation.

        MEDICAL ANALYSIS:
        {health_condition}

        CRITICAL FORMATTING RULES:
        1. Under "FOODS TO INCLUDE" section, list ONLY food names as bullets (use "-"), one per line
        Example:
        FOODS TO INCLUDE:
        - Spinach
        - Salmon
        - Eggs
        
        2. Under "FOODS TO AVOID" section, list ONLY food names as bullets
        Example:
        FOODS TO AVOID:
        - Sugary drinks
        - Fried foods
        
        3. Do NOT add explanations, colons, or parentheses after food names
        4. Keep each food item to 2-5 words maximum

        Provide:
        1. Diet name
        2. Why this diet
        3. FOODS TO INCLUDE (bullet list of food names only)
        4. FOODS TO AVOID (bullet list of food names only)
        5. Meal timing and portions
        6. Key nutrients
        7. Hydration
        8. Lifestyle tips
        """

        
        try:
            print("\n🔄 Analyzing condition and generating diet recommendations...")
            response = self.model.generate_content(prompt)
            
            recommendation = response.text
            
            print("✅ Diet recommendations complete!\n")
            return recommendation
            
        except Exception as e:
            error_msg = f"❌ Recommendation failed: {str(e)}"
            print(error_msg)
            return error_msg
    
    
    def recommend_for_multiple_conditions(self, conditions_list):
        """
        Recommend diet considering multiple health conditions.
        
        Args:
            conditions_list (list): List of health conditions
            
        Returns:
            str: Integrated diet recommendations
        """
        
        conditions_text = "\n- ".join(conditions_list)
        
        prompt = f"""
        You are {self.role}.
        
        COMPLEX CASE: Patient has multiple health conditions:
        
        - {conditions_text}
        
        TASK: Recommend an INTEGRATED diet approach that addresses ALL 
        these conditions simultaneously. Find the common dietary principles 
        that benefit all conditions.
        
        Address:
        1. How to balance dietary needs for all conditions
        2. Foods that benefit multiple conditions
        3. How to avoid conflicting dietary advice
        4. Priority conditions that need primary focus
        5. Practical meal planning considerations
        
        INTEGRATED DIET RECOMMENDATION:
        """
        
        try:
            print(f"\n🔄 Analyzing {len(conditions_list)} conditions...")
            response = self.model.generate_content(prompt)
            
            recommendation = response.text
            
            print("✅ Integrated recommendations complete!\n")
            return recommendation
            
        except Exception as e:
            error_msg = f"❌ Recommendation failed: {str(e)}"
            print(error_msg)
            return error_msg
    
    
    def recommend_for_nutrient_deficiency(self, nutrient):
        """
        Recommend foods rich in specific nutrients.
        
        Args:
            nutrient (str): The nutrient needed (e.g., "iron", "vitamin D")
            
        Returns:
            str: Foods rich in that nutrient
        """
        
        prompt = f"""
        You are a nutrition specialist.
        
        TASK: A patient needs more {nutrient} in their diet.
        
        Provide:
        1. **Top 10 food sources** of {nutrient} (with amounts)
        2. **Vegetarian options** if applicable
        3. **How to maximize absorption** (food combinations)
        4. **Daily recommended amount**
        5. **Supplementation advice** (when food isn't enough)
        
        Keep it practical and easy to follow.
        """
        
        try:
            print(f"\n🔄 Finding best sources of {nutrient}...")
            response = self.model.generate_content(prompt)
            
            recommendation = response.text
            
            print("✅ Nutrient recommendations complete!\n")
            return recommendation
            
        except Exception as e:
            error_msg = f"❌ Recommendation failed: {str(e)}"
            print(error_msg)
            return error_msg


# ============================================================
# LAYER 4: TEST/DEMO CODE
# ============================================================

def demo_recommender():
    """
    Demonstration of the Diet Recommender Agent capabilities.
    """
    
    print("=" * 60)
    print("🥗 DIET RECOMMENDER AGENT - DEMO")
    print("=" * 60)
    
    # Initialize the agent
    agent = DietRecommenderAgent()
    
    
    # Example 1: Single condition - Diabetes
    print("\n" + "=" * 60)
    print("📋 EXAMPLE 1: Diabetes Diet Recommendation")
    print("=" * 60)
    
    condition_1 = """
    You have high blood sugar (diabetes). Your fasting blood glucose 
    is 186 mg/dL and HbA1c is 8.2%, which are both higher than normal.
    """
    
    print("\n🏥 HEALTH CONDITION:")
    print(condition_1)
    
    diet_rec_1 = agent.recommend_diet(condition_1)
    print("\n🥗 DIET RECOMMENDATION:")
    print(diet_rec_1)
    
    
    # Example 2: Single condition - Hypertension
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 2: High Blood Pressure Diet")
    print("=" * 60)
    
    condition_2 = """
    You have high blood pressure (Stage 2 hypertension) with 
    readings of 164/98 mmHg. This puts you at risk for heart 
    problems and stroke.
    """
    
    print("\n🏥 HEALTH CONDITION:")
    print(condition_2)
    
    diet_rec_2 = agent.recommend_diet(condition_2)
    print("\n🥗 DIET RECOMMENDATION:")
    print(diet_rec_2)
    
    
    # Example 3: Multiple conditions
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 3: Multiple Conditions")
    print("=" * 60)
    
    conditions_list = [
        "Type 2 Diabetes",
        "High Blood Pressure",
        "High Cholesterol"
    ]
    
    print("\n🏥 HEALTH CONDITIONS:")
    for condition in conditions_list:
        print(f"  - {condition}")
    
    integrated_rec = agent.recommend_for_multiple_conditions(conditions_list)
    print("\n🥗 INTEGRATED DIET RECOMMENDATION:")
    print(integrated_rec)
    
    
    # Example 4: Nutrient deficiency
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 4: Low Platelets (Need Platelet-Boosting Foods)")
    print("=" * 60)
    
    nutrient_rec = agent.recommend_for_nutrient_deficiency("Vitamin K and iron for increasing platelets")
    print("\n🥗 FOOD RECOMMENDATIONS:")
    print(nutrient_rec)
    
    
    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETE!")
    print("=" * 60)


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    """
    This code runs when you execute the file directly.
    """
    demo_recommender()
