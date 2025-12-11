"""
Profile Manager - Central User Profile Access
==============================================
Single source of truth for user profile.
All agents import from here.
"""

import streamlit as st
import json
import os

PROFILE_PATH = "user_profile.json"


def get_profile():
    """Get user profile from session state or file."""
    # First check session state
    if "user_profile" in st.session_state and st.session_state.user_profile:
        return st.session_state.user_profile
    
    # Try loading from file
    try:
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, 'r') as f:
                profile = json.load(f)
                st.session_state.user_profile = profile
                return profile
    except:
        pass
    
    return None


def save_profile(profile):
    """Save profile to session state and file."""
    st.session_state.user_profile = profile
    
    try:
        with open(PROFILE_PATH, 'w') as f:
            json.dump(profile, f, indent=2)
        return True
    except:
        return False


def delete_profile():
    """Delete profile from session state and file."""
    st.session_state.user_profile = None
    
    try:
        if os.path.exists(PROFILE_PATH):
            os.remove(PROFILE_PATH)
    except:
        pass


def has_profile():
    """Check if profile exists."""
    return get_profile() is not None


def format_profile(profile):
    """Format profile as string for AI prompts."""
    if not profile:
        return "No user profile available."
    
    lines = []
    
    if profile.get('name'):
        lines.append(f"Name: {profile['name']}")
    
    if profile.get('diet_type'):
        lines.append(f"Diet Type: {profile['diet_type']}")
    
    if profile.get('religious_restrictions') and profile['religious_restrictions'] != 'None':
        lines.append(f"Religious: {profile['religious_restrictions']}")
    
    if profile.get('allergies'):
        lines.append(f"ALLERGIES: {', '.join(profile['allergies'])}")
    
    if profile.get('disliked_foods'):
        lines.append(f"Dislikes: {', '.join(profile['disliked_foods'])}")
    
    if profile.get('cooking_time'):
        lines.append(f"Cooking Time: {profile['cooking_time']}")
    
    if profile.get('budget'):
        lines.append(f"Budget: {profile['budget']}")
    
    if profile.get('activity_level'):
        lines.append(f"Activity: {profile['activity_level']}")
    
    if profile.get('weight_goal'):
        lines.append(f"Goal: {profile['weight_goal']}")
    
    return "\n".join(lines)
