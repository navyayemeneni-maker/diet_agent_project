"""
Agent 1: Medical Translator
===========================
Translates medical reports into simple language.
Model: llama-3.3-70b-versatile (best medical reasoning)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import client
from profile_manager import get_profile, format_profile


def run_agent1(medical_text):
    """
    Translate medical report into simple language.
    
    Args:
        medical_text: Raw medical report text
        
    Returns:
        Simple explanation (150-200 words)
    """
    
    profile = get_profile()
    profile_str = format_profile(profile) if profile else ""
    
    prompt = f"""
You are a medical translator. Explain this medical report in SIMPLE language.

USER PROFILE:
{profile_str}

MEDICAL REPORT:
{medical_text}

INSTRUCTIONS:
1. Keep it SHORT - maximum 150-200 words
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

Keep it friendly, reassuring, and easy to understand.
"""
    
    print("🔄 Agent 1: Translating medical report...")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    
    result = response.choices[0].message.content
    print("✅ Agent 1: Translation complete!")
    
    return result
