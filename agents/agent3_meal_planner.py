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
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure Groq AI
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Model fallback list (production-stable models only)
MODEL_FALLBACK = [
    "llama-3.1-8b-instant",         # Fast + creative, perfect for meal plans
    "openai/gpt-oss-20b",           # Heavier model for more detail
    "openai/gpt-oss-120b"           # Fallback with strongest reasoning
]


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
        
        self.client = client
        self.model_fallback = MODEL_FALLBACK
        
        print(f"✅ {self.role} Agent initialized successfully!")
        print(f"   Primary model: {MODEL_FALLBACK[0]}")
        print(f"   Fallback models: {len(MODEL_FALLBACK) - 1}")
    
    
# ============================================================
# LAYER 3: MEAL PLANNING FUNCTIONS
# ============================================================
    def create_meal_plan(self, diet_recommendation):
        """Create a comprehensive 7-day meal plan based on diet recommendations"""
        
        prompt = f"""
You are a professional meal planner. Create a PRACTICAL 7-day meal plan based on these diet recommendations.

DIET RECOMMENDATIONS:
{diet_recommendation}

IMPORTANT INSTRUCTIONS:
1. Keep meals SIMPLE and easy to prepare (under 30 minutes)
2. Use common, affordable ingredients
3. Include portion sizes
4. Make it realistic for busy people

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

## 7-DAY MEAL PLAN

### DAY 1 (Monday)
- Breakfast (7-8 AM): [Meal name] - [Brief description, portion]
- Snack (10 AM): [Snack item]
- Lunch (12-1 PM): [Meal name] - [Brief description, portion]
- Snack (4 PM): [Snack item]
- Dinner (7-8 PM): [Meal name] - [Brief description, portion]

### DAY 2 (Tuesday)
[Same format...]

[Continue for all 7 days]

## QUICK RECIPES (Top 3)

**Recipe 1: [Name]**
- Ingredients: [list]
- Steps: [brief 3-4 steps]
- Time: [X minutes]

**Recipe 2: [Name]**
[Same format]

**Recipe 3: [Name]**
[Same format]

## SHOPPING LIST

**Vegetables:** [comma-separated list]
**Fruits:** [comma-separated list]
**Proteins:** [comma-separated list]
**Grains:** [comma-separated list]
**Dairy:** [comma-separated list]
**Others:** [comma-separated list]

## MEAL PREP TIPS
- [3-4 practical tips for the week]

Keep it organized, practical, and easy to follow!
"""
        
        print("\n🔄 Creating 7-day meal plan...")
        
        for i, model in enumerate(self.model_fallback):
            try:
                if i > 0:
                    print(f"   Trying fallback model {i}: {model}")
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a professional meal planner creating practical, healthy meal plans."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=3000
                )
                
                meal_plan = response.choices[0].message.content
                print(f"✅ Meal plan complete using {model}!\n")
                return meal_plan
                
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
