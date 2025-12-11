"""
Q&A Support Agent
==================
This agent answers user questions about their diet plan, meal suggestions,
and provides ongoing support and clarification.

Agent Profile:
- Role: Health & Nutrition Advisor
- Expertise: Dietary guidance, meal planning, nutrition education
- Goal: Provide helpful, accurate answers to user questions
"""

# ============================================================
# LAYER 1: IMPORTS AND CONFIGURATION
# ============================================================

import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

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

class QASupportAgent:
    """
    An AI agent that answers user questions about their diet and meal plan.
    
    Attributes:
        role: The agent's professional role
        goal: What the agent aims to achieve
        backstory: The agent's expertise and experience
        model: The AI model used for generating answers
        context_set: Whether the agent has context about user's diet
        diet_plan: The recommended diet plan
        meal_plan: The suggested meal plan
        health_condition: The user's health condition
        conversation_history: Record of Q&A interactions
    """
    
    def __init__(self):
        """Initialize the Q&A Support Agent"""
        
        # Agent Identity
        self.role = "Health & Nutrition Advisor"
        
        self.goal = """
        Provide helpful, accurate, and concise answers to user questions about 
        their personalized diet plan, meal suggestions, food substitutions, 
        and nutritional guidance.
        """
        
        self.backstory = """
        You are a certified nutritionist and health advisor with expertise in:
        
        - Therapeutic diets for various health conditions
        - Meal planning and recipe modifications
        - Food substitutions and alternatives
        - Nutritional science and dietary guidelines
        - Patient education and communication
        
        Your communication style is:
        - Clear and concise (3-4 sentences maximum)
        - Practical and actionable
        - Supportive and encouraging
        - Evidence-based yet easy to understand
        
        You have access to the user's:
        - Health condition and medical information
        - Personalized diet recommendations
        - Customized meal plan
        
        Your responses should be brief, scannable, and immediately useful.
        """
        
        self.model = model
        
        # Context tracking
        self.context_set = False
        self.diet_plan = None
        self.meal_plan = None
        self.health_condition = None
        
        # Conversation history
        self.conversation_history = []
        
        print(f"✅ {self.role} Agent initialized successfully!")
    
    
    # ============================================================
    # LAYER 3: CONTEXT MANAGEMENT
    # ============================================================
    
    def set_context(self, diet_plan, meal_plan, health_condition):
        """
        Set the context for personalized Q&A.
        
        Args:
            diet_plan (str): The recommended diet plan
            meal_plan (str): The suggested meal plan
            health_condition (str): The user's health condition
        """
        
        self.diet_plan = diet_plan
        self.meal_plan = meal_plan
        self.health_condition = health_condition
        self.context_set = True
        
        print("\n✅ Context updated for personalized answers")
        print(f"   Health condition: {health_condition[:100]}...")
        print(f"   Diet plan available: {len(diet_plan)} characters")
        print(f"   Meal plan available: {len(meal_plan)} characters")
    
    
    # ============================================================
    # LAYER 4: QUESTION ANSWERING (UPDATED - CONCISE!)
    # ============================================================
    
    def answer_question(self, question):
        """
        Answer user questions about their diet plan.
        
        Args:
            question (str): The user's question
            
        Returns:
            str: Concise, actionable answer
        """
        
        if not self.context_set:
            return """
⚠️ Please process a medical report first before asking questions.
Go to the 'Upload Report' section to get started!
"""
        
        # Create CONCISE prompt
        prompt = f"""
You are a nutrition advisor providing BRIEF, ACTIONABLE answers.

USER'S HEALTH CONTEXT:
{self.health_condition}

RECOMMENDED DIET:
{self.diet_plan[:500]}...

QUESTION: {question}

RESPONSE GUIDELINES (STRICT):
1. Keep answer to 3-4 sentences MAXIMUM
2. Use bullet points if listing items (max 4 items)
3. Be direct and actionable
4. If complex topic, give brief answer and offer to elaborate
5. Use simple, conversational language

ANSWER FORMAT:
- Start with direct answer (1-2 sentences)
- Add 2-3 bullet points if needed
- End with: "Need more details? Ask me!"

CONCISE ANSWER:
"""
        
        try:
            print(f"\n🔄 Thinking about your question...")
            
            # Generate concise response
            response = self.model.generate_content(prompt)
            answer = response.text.strip()
            
            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "answer": answer,
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"✅ Answer ready! (Length: {len(answer)} characters)")
            
            return answer
            
        except Exception as e:
            error_msg = f"Error generating answer: {str(e)}"
            print(f"❌ {error_msg}")
            return f"❌ {error_msg}"
    
    
    # ============================================================
    # LAYER 5: CONVERSATION MANAGEMENT
    # ============================================================
    
    def get_conversation_history(self):
        """
        Get the complete conversation history.
        
        Returns:
            list: List of Q&A pairs with timestamps
        """
        return self.conversation_history
    
    
    def clear_context(self):
        """Clear the current context and conversation history"""
        self.context_set = False
        self.diet_plan = None
        self.meal_plan = None
        self.health_condition = None
        self.conversation_history = []
        
        print("\n✅ Context and conversation history cleared")
    
    
    def export_conversation(self, filename="qa_history.txt"):
        """
        Export conversation history to a text file.
        
        Args:
            filename (str): Name of the output file
        """
        
        if not self.conversation_history:
            print("⚠️ No conversation history to export")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("Q&A CONVERSATION HISTORY\n")
                f.write("=" * 70 + "\n\n")
                
                for idx, interaction in enumerate(self.conversation_history, 1):
                    f.write(f"Question {idx}:\n")
                    f.write(f"{interaction['question']}\n\n")
                    f.write(f"Answer:\n")
                    f.write(f"{interaction['answer']}\n\n")
                    f.write(f"Timestamp: {interaction['timestamp']}\n")
                    f.write("-" * 70 + "\n\n")
            
            print(f"✅ Conversation exported to {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting conversation: {e}")


# ============================================================
# DEMO/TEST CODE
# ============================================================

def demo_qa_agent():
    """
    Demonstration of the Q&A Support Agent capabilities
    """
    
    print("=" * 70)
    print("💬 Q&A SUPPORT AGENT - DEMO")
    print("=" * 70)
    
    # Initialize agent
    agent = QASupportAgent()
    
    # Set sample context
    sample_health = "You have low iron levels (59 µg/dL) and need to increase them through diet."
    sample_diet = "Focus on iron-rich foods: spinach, lentils, red meat, fortified cereals. Pair with vitamin C for better absorption."
    sample_meal = "Day 1: Breakfast - Spinach omelet with orange juice, Lunch - Lentil soup, Dinner - Grilled chicken with broccoli"
    
    agent.set_context(
        diet_plan=sample_diet,
        meal_plan=sample_meal,
        health_condition=sample_health
    )
    
    # Sample questions
    questions = [
        "What are the best iron-rich foods for me?",
        "I'm vegetarian. What can I eat instead of meat?",
        "Can I eat fruits with my meals?",
        "How much spinach should I eat daily?"
    ]
    
    print("\n" + "=" * 70)
    print("📋 SAMPLE Q&A SESSION")
    print("=" * 70)
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        answer = agent.answer_question(question)
        print(f"\n💡 Answer:\n{answer}")
        print("\n" + "-" * 70)
    
    # Show conversation history
    print("\n" + "=" * 70)
    print("📊 CONVERSATION SUMMARY")
    print("=" * 70)
    print(f"Total questions answered: {len(agent.conversation_history)}")
    
    # Export conversation
    agent.export_conversation("demo_qa_history.txt")
    
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    """
    Run the demo when this file is executed directly
    """
    demo_qa_agent()
