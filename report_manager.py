"""
Report Manager - Store and Load Generated Reports
==================================================
Saves all generated diet plans for dashboard history.

Session-based storage - works on Streamlit Cloud.
Each user gets their own reports during their session.
"""

import streamlit as st
import time
from datetime import datetime


def _get_reports_list():
    """Get reports list from session state."""
    if "reports" not in st.session_state:
        st.session_state.reports = []
    return st.session_state.reports


def save_report(medical_text, translation, diet_rec, meal_plan, pdf_path=None):
    """
    Save a generated report to session state.
    
    Args:
        medical_text: Original medical report text
        translation: Agent 1 output
        diet_rec: Agent 2 output
        meal_plan: Agent 3 output
        pdf_path: Path to generated PDF (optional)
        
    Returns:
        report_id: Unique ID of saved report
    """
    report_id = int(time.time())
    
    # Extract conditions from translation
    conditions = extract_conditions(translation + " " + diet_rec)
    
    report = {
        "report_id": report_id,
        "timestamp": time.time(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "medical_text": medical_text[:500] + "..." if len(medical_text) > 500 else medical_text,
        "simple_explanation": translation,
        "diet_recommendations": diet_rec,
        "meal_plan": meal_plan,
        "conditions_found": conditions,
        "pdf_path": pdf_path
    }
    
    reports = _get_reports_list()
    reports.insert(0, report)  # Add to beginning (newest first)
    st.session_state.reports = reports
    
    return report_id


def load_reports():
    """
    Load all saved reports from session state.
    
    Returns:
        List of reports sorted by date (newest first)
    """
    return _get_reports_list()


def get_report(report_id):
    """Get a specific report by ID."""
    reports = _get_reports_list()
    for report in reports:
        if report.get("report_id") == report_id:
            return report
    return None


def delete_report(report_id):
    """Delete a report by ID."""
    reports = _get_reports_list()
    st.session_state.reports = [r for r in reports if r.get("report_id") != report_id]
    return True


def get_stats():
    """
    Get dashboard statistics.
    
    Returns:
        dict with stats
    """
    reports = _get_reports_list()
    
    if not reports:
        return {
            "total_reports": 0,
            "conditions": [],
            "condition_counts": {},
            "most_common_condition": "None",
            "first_report_date": None,
            "last_report_date": None
        }
    
    # Count conditions
    all_conditions = []
    for r in reports:
        all_conditions.extend(r.get("conditions_found", []))
    
    # Find most common
    condition_counts = {}
    for c in all_conditions:
        condition_counts[c] = condition_counts.get(c, 0) + 1
    
    most_common = max(condition_counts, key=condition_counts.get) if condition_counts else "None"
    
    return {
        "total_reports": len(reports),
        "conditions": list(set(all_conditions)),
        "condition_counts": condition_counts,
        "most_common_condition": most_common,
        "first_report_date": reports[-1].get("date") if reports else None,
        "last_report_date": reports[0].get("date") if reports else None
    }


def extract_conditions(text):
    """
    Extract health conditions from text using keyword matching.
    
    Args:
        text: Text to analyze
        
    Returns:
        List of detected conditions
    """
    text_lower = text.lower()
    
    condition_keywords = {
        "Diabetes": ["diabetes", "blood sugar", "glucose", "hba1c", "hyperglycemia", "insulin"],
        "High Cholesterol": ["cholesterol", "ldl", "hdl", "triglycerides", "lipid"],
        "Hypertension": ["hypertension", "blood pressure", "bp", "high pressure"],
        "Anemia": ["anemia", "iron", "hemoglobin", "ferritin", "low iron"],
        "Thyroid": ["thyroid", "tsh", "t3", "t4", "hypothyroid", "hyperthyroid"],
        "Kidney": ["kidney", "creatinine", "urea", "renal", "gfr"],
        "Liver": ["liver", "alt", "ast", "bilirubin", "hepatic"],
        "Vitamin D Deficiency": ["vitamin d", "vit d", "25-oh"],
        "Vitamin B12 Deficiency": ["vitamin b12", "b12", "cobalamin"],
        "Obesity": ["obesity", "bmi", "overweight", "weight loss"],
        "Heart Disease": ["heart", "cardiac", "cardiovascular", "coronary"],
        "PCOS": ["pcos", "polycystic", "ovarian"],
        "Uric Acid": ["uric acid", "gout", "urate"]
    }
    
    detected = []
    
    for condition, keywords in condition_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                if condition not in detected:
                    detected.append(condition)
                break
    
    return detected if detected else ["General Health"]
