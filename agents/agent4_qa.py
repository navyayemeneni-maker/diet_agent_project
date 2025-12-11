"""
Agent 4: Q&A Bot
================
Answers user questions about diet and nutrition.
Model: llama-3.1-8b-instant (fastest for Q&A)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import client
from profile_manager import get_profile, format_profile


def run_agent4(question, diet_plan=None):
    """
    Answer user questions about diet and nutrition.
    
    Args:
        question: User's question
        diet_plan: Their diet recommendations (optional context)
        
    Returns:
        Concise, personalized answer
    """
    
    profile = get_profile()
    profile_str = format_profile(profile) if profile else ""
    
    diet_section = ""
    if diet_plan:
        diet_section = f"\nTHEIR DIET PLAN (for context):\n{diet_plan[:1500]}..."
    
    prompt = f"""
You are a friendly nutrition advisor. Answer this question clearly.

USER PROFILE:
{profile_str}
{diet_section}

QUESTION: {question}

INSTRUCTIONS:
1. Give a DIRECT answer first (1-2 sentences)
2. Add 2-4 bullet points with specific tips if helpful
3. Keep total response under 150 words
4. Use simple, friendly language
5. ALWAYS respect user's dietary restrictions in your answer
6. If user asks about a food they can't eat, explain WHY based on their profile

Example: If vegetarian asks "Can I eat chicken?"
Answer: "Since you follow a vegetarian diet, chicken isn't included in your meal plan. Great protein alternatives for you include lentils, chickpeas, tofu, and paneer!"

ANSWER:
"""
    
    print("🔄 Agent 4: Answering question...")
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    result = response.choices[0].message.content
    print("✅ Agent 4: Answer ready!")
    
    return result
