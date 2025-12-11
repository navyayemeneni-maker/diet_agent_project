"""
Agent 3: Meal Planner
=====================
Creates 7-day meal plan based on diet recommendations.
Model: llama-3.1-8b-instant (fast, creative)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import client
from profile_manager import get_profile, format_profile


def run_agent3(diet_recommendations):
    """
    Create 7-day meal plan based on diet recommendations.
    
    Args:
        diet_recommendations: Output from Agent 2
        
    Returns:
        7-day meal plan with recipes and shopping list
    """
    
    profile = get_profile()
    profile_str = format_profile(profile) if profile else ""
    
    prompt = f"""
You are a meal planner. Create a PRACTICAL 7-day meal plan.

USER PROFILE:
{profile_str}

DIET RECOMMENDATIONS:
{diet_recommendations}

⚠️ STRICT RULES:
- ALL meals must fit within cooking time preference
- NEVER include allergenic foods
- NEVER include restricted foods (diet type, religious)
- Consider budget when suggesting ingredients

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

## 7-DAY MEAL PLAN

### DAY 1 (Monday)
- Breakfast (7-8 AM): [Meal] - [brief description, portion]
- Snack (10 AM): [Snack]
- Lunch (12-1 PM): [Meal] - [brief description, portion]
- Snack (4 PM): [Snack]
- Dinner (7-8 PM): [Meal] - [brief description, portion]

### DAY 2 (Tuesday)
[Same format...]

[Continue for all 7 days]

## QUICK RECIPES (Top 3)

**Recipe 1: [Name]**
- Ingredients: [list]
- Steps: [3-4 steps]
- Time: [X minutes]

**Recipe 2: [Name]**
[Same format]

**Recipe 3: [Name]**
[Same format]

## SHOPPING LIST

**Vegetables:** [list]
**Fruits:** [list]
**Proteins:** [list]
**Grains:** [list]
**Dairy/Alternatives:** [list]
**Others:** [list]

## MEAL PREP TIPS
- [3-4 tips]

Keep it practical and respect ALL user restrictions!
"""
    
    print("🔄 Agent 3: Creating 7-day meal plan...")
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=3000
    )
    
    result = response.choices[0].message.content
    print("✅ Agent 3: Meal plan complete!")
    
    return result
