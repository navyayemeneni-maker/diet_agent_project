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
from openai import OpenAI
from datetime import datetime

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
    "llama-3.1-8b-instant",         # Best ultra-fast chat
    "openai/gpt-oss-20b",           # Good conversational fallback
    "openai/gpt-oss-120b"           # Fallback with strong comprehension
]


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
        
        self.client = client
        self.model_fallback = MODEL_FALLBACK
        
        # Context tracking
        self.context_set = False
        self.diet_plan = None
        self.meal_plan = None
        self.health_condition = None
        
        # Conversation history
        self.conversation_history = []
        
        print(f"✅ {self.role} Agent initialized successfully!")
        print(f"   Primary model: {MODEL_FALLBACK[0]}")
        print(f"   Fallback models: {len(MODEL_FALLBACK) - 1}")
    
    
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
        
        # If no context, still answer general nutrition questions
        context_info = ""
        if self.context_set:
            context_info = f"""
USER'S HEALTH CONTEXT:
{self.health_condition[:500] if self.health_condition else 'Not provided'}

THEIR RECOMMENDED DIET (summary):
{self.diet_plan[:800] if self.diet_plan else 'Not provided'}
"""
        else:
            context_info = "No specific health context provided. Give general nutrition advice."
        
        # Create CONCISE prompt
        prompt = f"""
You are a friendly nutrition advisor. Answer this question clearly and helpfully.

{context_info}

QUESTION: {question}

INSTRUCTIONS:
1. Give a DIRECT answer first (1-2 sentences)
2. If helpful, add 2-4 bullet points with specific tips
3. Keep total response under 150 words
4. Use simple, friendly language
5. If the question relates to their health condition, personalize the answer
6. Be encouraging and supportive

FORMAT:
[Direct answer in 1-2 sentences]

[If needed, bullet points:]
- Tip 1
- Tip 2
- Tip 3

[Optional: One encouraging closing sentence]

ANSWER:
"""
        
        print(f"\n🔄 Thinking about your question...")
        
        for i, model in enumerate(self.model_fallback):
            try:
                if i > 0:
                    print(f"   Trying fallback model {i}: {model}")
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a friendly nutrition advisor providing brief, helpful answers."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                answer = response.choices[0].message.content.strip()
                
                # Store in conversation history
                self.conversation_history.append({
                    "question": question,
                    "answer": answer,
                    "timestamp": datetime.now().isoformat(),
                    "model": model
                })
                
                print(f"✅ Answer ready using {model}! (Length: {len(answer)} characters)")
                return answer
                
            except Exception as e:
                print(f"   ⚠️ Model {model} failed: {str(e)}")
                if i == len(self.model_fallback) - 1:
                    error_msg = f"❌ All models failed. Last error: {str(e)}"
                    print(error_msg)
                    return error_msg
                continue
    
    
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
