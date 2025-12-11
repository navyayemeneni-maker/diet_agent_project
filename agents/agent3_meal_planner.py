"""
Meal Plan Builder Agent
=======================
This agent creates detailed, practical meal plans with recipes
based on recommended diets for specific health conditions.

Agent Profile:
- Role: Personal Chef & Meal Planning Specialist
- Expertise: Recipe creation, meal planning, nutrition
- Goal: Create easy-to-follow meal plans that support health goals
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

class MealPlanBuilderAgent:
    """
    An AI agent specialized in creating practical, delicious meal plans
    based on therapeutic diet recommendations.
    
    Attributes:
        role: The agent's professional role
        goal: What the agent aims to achieve
        backstory: The agent's expertise and experience
        model: The AI model used for meal planning
    """
    
    def __init__(self):
        """Initialize the Meal Plan Builder Agent"""
        
        # Agent Identity
        self.role = "Personal Chef & Meal Planning Specialist"
        
        self.goal = """
        Transform dietary recommendations into practical, delicious, 
        and easy-to-follow meal plans that real people can actually 
        cook and enjoy while supporting their health goals.
        """
        
        self.backstory = """
        You are a professional chef and certified meal planner with 15+ years 
        of experience creating therapeutic meal plans. You have:
        
        - Culinary arts degree and nutrition certification
        - Experience as a personal chef for clients with health conditions
        - Expertise in adapting recipes to be healthy without sacrificing taste
        - Knowledge of global cuisines and flavor profiles
        - Understanding of meal prep, batch cooking, and time management
        - Skill in creating budget-friendly meal plans
        
        Your meal plans are:
        - Practical (realistic cooking times and ingredient availability)
        - Delicious (never boring or bland)
        - Nutritionally balanced (meet all dietary requirements)
        - Flexible (include substitution options)
        - Easy to follow (clear instructions and measurements)
        """
        
        self.model = model
        
        print(f"✅ {self.role} Agent initialized successfully!")
    
    
# ============================================================
# LAYER 3: MEAL PLANNING FUNCTIONS
# ============================================================
    def create_meal_plan(self, diet_recommendation):
        """Create a comprehensive 7-day meal plan based on diet recommendations"""
        
        prompt = f"""
Based on the following diet recommendations, create a detailed 7-DAY meal plan.

Diet Recommendations:
{diet_recommendation}

Please provide:

**7-DAY MEAL PLAN:**

For each day (Monday through Sunday), provide:
- Breakfast (with timing and portion)
- Mid-Morning Snack
- Lunch (with timing and portion)
- Evening Snack
- Dinner (with timing and portion)

Include:
- Specific recipes with ingredients
- Portion sizes
- Cooking methods
- Nutritional highlights

**WEEKLY SHOPPING LIST:**

Organize by category:
- Vegetables & Fruits
- Proteins
- Grains & Carbs
- Dairy Products
- Spices & Condiments
- Others

**MEAL PREP TIPS:**
- What to prepare in advance
- Storage instructions
- Time-saving strategies

Format the response in a clear, organized manner with day-by-day breakdown.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error creating meal plan: {str(e)}" 

# ============================================================
# LAYER 4: TEST/DEMO CODE
# ============================================================

def demo_meal_planner():
    """
    Demonstration of the Meal Plan Builder Agent capabilities.
    """
    
    print("=" * 60)
    print("🍽️ MEAL PLAN BUILDER AGENT - DEMO")
    print("=" * 60)
    
    # Initialize the agent
    agent = MealPlanBuilderAgent()
    
    
    # Example 1: 3-day meal plan for diabetes
    print("\n" + "=" * 60)
    print("📋 EXAMPLE 1: 3-Day Diabetic Meal Plan")
    print("=" * 60)
    
    diet_rec_1 = """
    Diet Recommendation: Low Glycemic Index Diet for Diabetes
    
    Foods to Include:
    - Non-starchy vegetables (spinach, broccoli, bell peppers)
    - Lean proteins (chicken, fish, tofu)
    - Whole grains (quinoa, brown rice, oats)
    - Healthy fats (avocado, nuts, olive oil)
    - Low-sugar fruits (berries, apples)
    
    Foods to Avoid:
    - White bread, white rice
    - Sugary drinks and desserts
    - Processed snacks
    - High-sugar fruits (watermelon, pineapple)
    
    Meal Timing: Eat 3 meals + 2 snacks daily, evenly spaced
    """
    
    print("\n🥗 DIET RECOMMENDATION:")
    print(diet_rec_1)
    
    meal_plan_1 = agent.create_meal_plan(diet_rec_1, duration_days=3)
    print("\n🍽️ MEAL PLAN:")
    print(meal_plan_1)
    
    
    # Example 2: Single meal recipe
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 2: Single Breakfast Recipe (Low Sodium)")
    print("=" * 60)
    
    dietary_req = """
    Requirements:
    - Low sodium (for high blood pressure)
    - High in potassium
    - Heart-healthy fats
    - Filling and satisfying
    """
    
    print("\n📝 REQUIREMENTS:")
    print(dietary_req)
    
    breakfast_recipe = agent.create_single_meal("breakfast", dietary_req)
    print("\n🍳 RECIPE:")
    print(breakfast_recipe)
    
    
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
    demo_meal_planner()
