"""
Report Manager - Store and Load Generated Reports
==================================================
Saves all generated diet plans for dashboard history.
"""

import os
import json
import time
from datetime import datetime

REPORTS_DIR = "data/reports"


def ensure_dir():
    """Create reports directory if it doesn't exist."""
    os.makedirs(REPORTS_DIR, exist_ok=True)


def save_report(medical_text, translation, diet_rec, meal_plan, pdf_path=None):
    """
    Save a generated report to disk.
    
    Args:
        medical_text: Original medical report text
        translation: Agent 1 output
        diet_rec: Agent 2 output
        meal_plan: Agent 3 output
        pdf_path: Path to generated PDF (optional)
        
    Returns:
        report_id: Unique ID of saved report
    """
    ensure_dir()
    
    report_id = int(time.time())
    
    # Extract conditions from translation (simple keyword detection)
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
    
    path = f"{REPORTS_DIR}/report_{report_id}.json"
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Report saved: {path}")
    return report_id


def load_reports():
    """
    Load all saved reports.
    
    Returns:
        List of reports sorted by date (newest first)
    """
    ensure_dir()
    
    reports = []
    
    for file in os.listdir(REPORTS_DIR):
        if file.endswith(".json"):
            try:
                with open(f"{REPORTS_DIR}/{file}", "r", encoding="utf-8") as f:
                    reports.append(json.load(f))
            except Exception as e:
                print(f"⚠️ Error loading {file}: {e}")
    
    # Sort by timestamp (newest first)
    reports.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    
    return reports


def get_report(report_id):
    """Get a specific report by ID."""
    path = f"{REPORTS_DIR}/report_{report_id}.json"
    
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    return None


def delete_report(report_id):
    """Delete a report by ID."""
    path = f"{REPORTS_DIR}/report_{report_id}.json"
    
    if os.path.exists(path):
        os.remove(path)
        print(f"✅ Report deleted: {report_id}")
        return True
    
    return False


def get_stats():
    """
    Get dashboard statistics.
    
    Returns:
        dict with stats
    """
    reports = load_reports()
    
    if not reports:
        return {
            "total_reports": 0,
            "conditions": [],
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
