"""
Agent 2: Diet Recommender
=========================
Recommends diet based on health condition + user profile.
Model: llama-3.3-70b-versatile (deep diet logic)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import client
from profile_manager import get_profile, format_profile


def run_agent2(simple_explanation):
    """
    Recommend diet based on health condition and user preferences.
    
    Args:
        simple_explanation: Output from Agent 1
        
    Returns:
        Diet recommendations with foods to eat/avoid
    """
    
    profile = get_profile()
    profile_str = format_profile(profile) if profile else ""
    
    prompt = f"""
You are a clinical nutritionist. Create diet recommendations.

USER PROFILE:
{profile_str}

HEALTH EXPLANATION:
{simple_explanation}

⚠️ STRICT RULES:
- NEVER recommend foods the user is allergic to (dangerous!)
- NEVER recommend meat/fish for vegetarians/vegans
- NEVER recommend beef for Hindus, pork for Muslims
- AVOID foods the user dislikes
- Consider cooking time and budget preferences

Provide recommendations with these sections:

## RECOMMENDED DIET
Name the diet approach (e.g., DASH Diet, Mediterranean Diet)

## WHY THIS DIET
2-3 sentences explaining why.

## FOODS TO INCLUDE
List 10-15 specific foods. Format as bullet points:
- Food name
- Food name

## FOODS TO AVOID
List 10-15 specific foods to avoid. Format as bullet points:
- Food name
- Food name

## MEAL TIMING
When and how often to eat.

## KEY NUTRIENTS
Most important nutrients for this condition.

## HYDRATION
Water and fluid recommendations.

## LIFESTYLE TIPS
3-5 practical tips.

REMEMBER: All recommendations must respect the user's dietary profile!
"""
    
    print("🔄 Agent 2: Creating diet recommendations...")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=2000
    )
    
    result = response.choices[0].message.content
    print("✅ Agent 2: Diet recommendations complete!")
    
    return result
