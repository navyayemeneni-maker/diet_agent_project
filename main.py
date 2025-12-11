"""
Diet Recommendation System - Main Orchestration
================================================
This is the main file that coordinates all 5 agents to provide
a complete diet recommendation workflow.

Workflow:
1. User provides medical information
2. Agent 1 translates medical jargon → simple language
3. Agent 2 recommends appropriate diet
4. Agent 3 creates detailed meal plan
5. Agent 4 answers user questions
6. Agent 5 monitors the entire process

Author: Navya
Date: December 4, 2025
"""

# ============================================================
# IMPORTS
# ============================================================

import os
import sys
from dotenv import load_dotenv

# Add agents folder to path so we can import our agents
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
from file_reader import FileReader

# Import all our agents
from agent1_translator import MedicalTranslatorAgent
from agent2_recommender import DietRecommenderAgent
from agent3_meal_planner import MealPlanBuilderAgent
from agent4_qa import QASupportAgent
from agent5_monitor import MonitorAgent

# Load environment variables
load_dotenv()


# ============================================================
# MAIN SYSTEM CLASS
# ============================================================

class DietRecommendationSystem:
    """
    Main system that orchestrates all agents to provide
    complete diet recommendations based on medical reports.
    """
    
    def __init__(self):
        """Initialize all agents"""
        
        print("=" * 70)
        print("🏥 DIET RECOMMENDATION SYSTEM")
        print("=" * 70)
        print("\n🔄 Initializing agents...\n")
        
        # Initialize all 5 agents
        try:
            self.translator = MedicalTranslatorAgent()
            self.recommender = DietRecommenderAgent()
            self.meal_planner = MealPlanBuilderAgent()
            self.qa_bot = QASupportAgent()
            self.monitor = MonitorAgent()
            self.file_reader = FileReader()

            print("\n✅ All agents initialized successfully!")
            self.monitor.log_event("System initialized with all 5 agents", "SUCCESS")
            
        except Exception as e:
            print(f"\n❌ Error initializing agents: {e}")
            self.monitor.log_event(f"Initialization error: {e}", "ERROR")
            raise
    
    
    def process_medical_report(self, medical_text):
        """
        Complete workflow: Process medical report through all agents.
        
        Args:
            medical_text (str): The medical report or health concern
            
        Returns:
            dict: Results from each agent
        """
        
        print("\n" + "=" * 70)
        print("🎯 STARTING COMPLETE WORKFLOW")
        print("=" * 70)
        
        results = {}
        
        try:
            # ===== STEP 1: TRANSLATE MEDICAL REPORT =====
            print("\n" + "-" * 70)
            print("📝 STEP 1: MEDICAL TRANSLATION")
            print("-" * 70)
            
            self.monitor.update_agent_status("agent1_translator", "Running")
            
            print("\n📄 ORIGINAL MEDICAL TEXT:")
            print(medical_text)
            
            translation = self.translator.translate_medical_report(medical_text)
            results['translation'] = translation
            
            self.monitor.update_agent_status("agent1_translator", "Completed")
            
            print("\n👤 SIMPLIFIED EXPLANATION:")
            print(translation)
            
            
            # ===== STEP 2: RECOMMEND DIET =====
            print("\n" + "-" * 70)
            print("🥗 STEP 2: DIET RECOMMENDATION")
            print("-" * 70)
            
            self.monitor.update_agent_status("agent2_recommender", "Running")
            
            diet_recommendation = self.recommender.recommend_diet(translation)
            results['diet_recommendation'] = diet_recommendation
            
            self.monitor.update_agent_status("agent2_recommender", "Completed")
            
            print("\n💡 RECOMMENDED DIET:")
            print(diet_recommendation)
            
            
            # ===== STEP 3: CREATE MEAL PLAN =====
            print("\n" + "-" * 70)
            print("🍽️ STEP 3: MEAL PLAN CREATION")
            print("-" * 70)
            
            self.monitor.update_agent_status("agent3_meal_planner", "Running")
            
            meal_plan = self.meal_planner.create_meal_plan(diet_recommendation, duration_days=3)
            results['meal_plan'] = meal_plan
            
            self.monitor.update_agent_status("agent3_meal_planner", "Completed")
            
            print("\n📅 3-DAY MEAL PLAN:")
            print(meal_plan)
            
            
            # ===== STEP 4: Q&A READY =====
            print("\n" + "-" * 70)
            print("💬 STEP 4: Q&A SUPPORT READY")
            print("-" * 70)
            
            self.monitor.update_agent_status("agent4_qa", "Ready")
            
            # Set context for Q&A agent
            self.qa_bot.set_context(
                diet_plan=diet_recommendation,
                meal_plan=meal_plan,
                health_condition=translation
            )
            
            print("\n✅ Q&A Bot is ready to answer your questions!")
            results['qa_ready'] = True
            
            
            # ===== STEP 5: FINAL MONITORING =====
            print("\n" + "-" * 70)
            print("📊 STEP 5: SYSTEM MONITORING")
            print("-" * 70)
            
            health_report = self.monitor.check_system_health()
            results['system_health'] = health_report
            
            
            # ===== WORKFLOW COMPLETE =====
            print("\n" + "=" * 70)
            print("✅ WORKFLOW COMPLETED SUCCESSFULLY!")
            print("=" * 70)
            
            self.monitor.log_event("Complete workflow finished successfully", "SUCCESS")
            
            return results
            
        except Exception as e:
            print(f"\n❌ Error in workflow: {e}")
            self.monitor.log_event(f"Workflow error: {e}", "ERROR")
            raise
    
    
    def interactive_qa_session(self):
        """
        Start an interactive Q&A session after processing.
        """
        
        print("\n" + "=" * 70)
        print("💬 INTERACTIVE Q&A SESSION")
        print("=" * 70)
        print("\nYou can now ask questions about your diet and meal plan!")
        print("Type 'exit', 'quit', or 'done' to end the session.\n")
        
        while True:
            try:
                question = input("❓ Your question: ").strip()
                
                if question.lower() in ['exit', 'quit', 'done', 'bye', '']:
                    print("\n✅ Thank you for using the Diet Recommendation System!")
                    print("Stay healthy! 🌟\n")
                    break
                
                if not question:
                    continue
                
                # Get answer from Q&A agent
                answer = self.qa_bot.answer_question(question)
                print(f"\n💡 ANSWER:\n{answer}\n")
                print("-" * 70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n✅ Session ended. Stay healthy! 🌟\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    
    def generate_final_report(self):
        """
        Generate a final system activity report.
        """
        self.monitor.generate_system_report()


# ============================================================
# DEMO WORKFLOWS
# ============================================================

def demo_workflow_diabetes():
    """
    Demo: Complete workflow for a diabetes case
    """
    
    print("\n" + "=" * 70)
    print("📋 DEMO: DIABETES CASE")
    print("=" * 70)
    
    # Initialize system
    system = DietRecommendationSystem()
    
    # Sample medical report
    medical_report = """
    Patient presents with hyperglycemia with fasting blood glucose 
    of 186 mg/dL and HbA1c of 8.2%. Patient exhibits polydipsia, 
    polyuria, and fatigue. Recommend carbohydrate restriction, 
    initiation of metformin 500mg BID, and follow-up in 3 months 
    for glycemic control assessment.
    """
    
    # Process through all agents
    results = system.process_medical_report(medical_report)
    
    # Interactive Q&A session
    print("\n" + "=" * 70)
    print("💬 Would you like to ask questions about your diet plan?")
    print("=" * 70)
    
    choice = input("\nStart Q&A session? (yes/no): ").strip().lower()
    
    if choice in ['yes', 'y']:
        system.interactive_qa_session()
    
    # Final report
    print("\n" + "=" * 70)
    print("📊 GENERATING FINAL SYSTEM REPORT")
    print("=" * 70)
    system.generate_final_report()


def demo_workflow_hypertension():
    """
    Demo: Complete workflow for a high blood pressure case
    """
    
    print("\n" + "=" * 70)
    print("📋 DEMO: HYPERTENSION (HIGH BLOOD PRESSURE) CASE")
    print("=" * 70)
    
    # Initialize system
    system = DietRecommendationSystem()
    
    # Sample medical report
    medical_report = """
    Patient diagnosed with Stage 2 hypertension (BP 164/98 mmHg).
    Recommend lifestyle modifications including DASH diet, sodium 
    restriction to <2g/day, and initiation of ACE inhibitor therapy.
    Monitor for orthostatic hypotension and renal function.
    """
    
    # Process through all agents
    results = system.process_medical_report(medical_report)
    
    # Final report
    system.generate_final_report()


def demo_simple_input():
    """
    Demo: Simple user input (not a full medical report)
    """
    
    print("\n" + "=" * 70)
    print("📋 DEMO: SIMPLE USER INPUT")
    print("=" * 70)
    
    # Initialize system
    system = DietRecommendationSystem()
    
    # Simple health concern
    user_input = "I have low platelets and need to improve my blood count."
    
    # Process through all agents
    results = system.process_medical_report(user_input)
    
    # Final report
    system.generate_final_report()


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():
    """
    Interactive menu for users to choose demo workflow
    """
    
    print("\n" + "=" * 70)
    print("🏥 DIET RECOMMENDATION SYSTEM - MAIN MENU")
    print("=" * 70)
    
    print("\nChoose a demo workflow:\n")
    print("1. Diabetes Case (Full medical report)")
    print("2. Hypertension Case (High blood pressure)")
    print("3. Simple Input (Low platelets)")
    print("4. Custom Input (Enter your own medical information)")
    print("5. 📁 Upload File (PDF, Word, Text, Image)")
    print("6. Exit")

    
    choice = input("\nYour choice (1-6): ").strip()
    
    if choice == '1':
        demo_workflow_diabetes()
    elif choice == '2':
        demo_workflow_hypertension()
    elif choice == '3':
        demo_simple_input()
    elif choice == '4':
        custom_workflow()
    elif choice == '5':
        file_upload_workflow()
    elif choice == '6':
        print("\n✅ Thank you for using the Diet Recommendation System!")
        print("Stay healthy! 🌟\n")
    else:
        print("\n❌ Invalid choice. Please try again.")
        main_menu()


def custom_workflow():
    """
    Allow user to enter their own medical information
    """
    
    print("\n" + "=" * 70)
    print("📋 CUSTOM WORKFLOW")
    print("=" * 70)
    
    print("\nEnter your medical information or health concern:")
    print("(You can paste a medical report or describe your condition)")
    print("(Press Enter twice when done)\n")
    
    lines = []
    empty_count = 0
    
    while empty_count < 1:
        line = input()
        if line:
            lines.append(line)
            empty_count = 0
        else:
            empty_count += 1
    
    user_input = "\n".join(lines)
    
    if not user_input.strip():
        print("\n❌ No input provided. Returning to menu.")
        main_menu()
        return
    
    # Initialize system and process
    system = DietRecommendationSystem()
    results = system.process_medical_report(user_input)
    
    # Ask if user wants Q&A
    choice = input("\nStart Q&A session? (yes/no): ").strip().lower()
    if choice in ['yes', 'y']:
        system.interactive_qa_session()
    
    # Final report
    system.generate_final_report()


def file_upload_workflow():
    """
    Allow user to upload a file (PDF, Word, Text, Image)
    """
    
    print("\n" + "=" * 70)
    print("📁 FILE UPLOAD WORKFLOW")
    print("=" * 70)
    
    print("\n✅ Supported file formats:")
    print("   - PDF files (.pdf)")
    print("   - Word documents (.docx)")
    print("   - Text files (.txt)")
    print("   - Images (.jpg, .png) - requires OCR")
    
    file_path = input("\n📂 Enter file path: ").strip()
    
    # Remove quotes if user copied path with quotes
    file_path = file_path.strip('"').strip("'")
    
    if not file_path:
        print("\n❌ No file path provided. Returning to menu.")
        main_menu()
        return
    
    # Initialize system
    system = DietRecommendationSystem()
    
    # Read file
    print("\n" + "=" * 70)
    print("📄 READING FILE")
    print("=" * 70)
    
    medical_text = system.file_reader.read_file(file_path)
    
    # Check if reading was successful
    if medical_text.startswith("❌"):
        print(medical_text)
        print("\n⚠️ File reading failed. Please try again with a valid file.")
        
        retry = input("\nTry another file? (yes/no): ").strip().lower()
        if retry in ['yes', 'y']:
            file_upload_workflow()
        else:
            main_menu()
        return
    
    # Show extracted text
    print("\n📄 EXTRACTED TEXT:")
    print("-" * 70)
    print(medical_text[:500] + ("..." if len(medical_text) > 500 else ""))
    print("-" * 70)
    
    # Confirm processing
    proceed = input("\n✅ Text extracted successfully! Process with agents? (yes/no): ").strip().lower()
    
    if proceed not in ['yes', 'y']:
        print("\n⚠️ Processing cancelled. Returning to menu.")
        main_menu()
        return
    
    # Process through all agents
    results = system.process_medical_report(medical_text)
    
    # Ask if user wants Q&A
    choice = input("\n💬 Start Q&A session? (yes/no): ").strip().lower()
    if choice in ['yes', 'y']:
        system.interactive_qa_session()
    
    # Final report
    system.generate_final_report()
    
    # Return to menu
    print("\n")
    main_menu()

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    """
    Main entry point of the application
    """
    
    try:
        # Run main menu
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n✅ Program terminated. Stay healthy! 🌟\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
