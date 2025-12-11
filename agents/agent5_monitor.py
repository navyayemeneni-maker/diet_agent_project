"""
Monitor Agent
==============
This agent monitors and coordinates the entire diet recommendation system,
ensuring all agents work correctly and the workflow runs smoothly.

Agent Profile:
- Role: System Coordinator & Quality Controller
- Expertise: Workflow management, error handling, quality assurance
- Goal: Ensure smooth operation of all agents and user satisfaction
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

class MonitorAgent:
    """
    An AI agent that monitors and coordinates the entire system.
    
    Attributes:
        role: The agent's professional role
        goal: What the agent aims to achieve
        backstory: The agent's expertise and experience
        model: The AI model used for monitoring
        logs: System activity logs
        agent_status: Status of each agent
    """
    
    def __init__(self):
        """Initialize the Monitor Agent"""
        
        # Agent Identity
        self.role = "System Coordinator & Quality Controller"
        
        self.goal = """
        Monitor the entire diet recommendation system, coordinate between
        agents, ensure quality outputs, handle errors gracefully, and
        provide a smooth user experience.
        """
        
        self.backstory = """
        You are an experienced system coordinator with expertise in:
        
        - Multi-agent system management
        - Quality assurance and testing
        - Error detection and handling
        - User experience optimization
        - Workflow coordination
        - Performance monitoring
        
        Your responsibilities:
        - Ensure all agents are functioning correctly
        - Coordinate information flow between agents
        - Detect and report errors
        - Verify output quality
        - Provide system status updates
        - Guide users through the process
        """
        
        self.model = model
        
        # System tracking
        self.logs = []
        self.agent_status = {
            "agent1_translator": "Not Started",
            "agent2_recommender": "Not Started",
            "agent3_meal_planner": "Not Started",
            "agent4_qa": "Not Started"
        }
        
        print(f"✅ {self.role} Agent initialized successfully!")
        self.log_event("Monitor Agent initialized")
    
    
    # ============================================================
    # LAYER 3: MONITORING FUNCTIONS
    # ============================================================
    
    def log_event(self, event, event_type="INFO"):
        """
        Log system events.
        
        Args:
            event (str): Description of the event
            event_type (str): Type of event (INFO, SUCCESS, WARNING, ERROR)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "type": event_type,
            "event": event
        }
        self.logs.append(log_entry)
        
        # Visual indicators for different event types
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌"
        }
        
        icon = icons.get(event_type, "•")
        print(f"[{timestamp}] {icon} {event}")
    
    
    def update_agent_status(self, agent_name, status):
        """
        Update the status of a specific agent.
        
        Args:
            agent_name (str): Name of the agent
            status (str): Current status
        """
        if agent_name in self.agent_status:
            self.agent_status[agent_name] = status
            self.log_event(f"{agent_name}: {status}", "INFO")
    
    
    def check_system_health(self):
        """
        Check the health status of all system components.
        
        Returns:
            dict: System health report
        """
        print("\n" + "=" * 60)
        print("🔍 SYSTEM HEALTH CHECK")
        print("=" * 60)
        
        health_report = {
            "overall_status": "Healthy",
            "agents": {},
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Check each agent
        for agent_name, status in self.agent_status.items():
            agent_display = agent_name.replace("_", " ").title()
            print(f"\n{agent_display}:")
            print(f"  Status: {status}")
            
            health_report["agents"][agent_name] = {
                "status": status,
                "healthy": status not in ["Error", "Failed"]
            }
        
        # Overall system status
        failed_agents = [name for name, info in health_report["agents"].items() 
                        if not info["healthy"]]
        
        if failed_agents:
            health_report["overall_status"] = "Degraded"
            print(f"\n⚠️ Warning: {len(failed_agents)} agent(s) need attention")
        else:
            print(f"\n✅ All systems operational!")
        
        print("=" * 60)
        
        return health_report
    
    
    def verify_output_quality(self, output_text, expected_content):
        """
        Verify the quality of agent output using AI.
        
        Args:
            output_text (str): The output to verify
            expected_content (str): What should be in the output
            
        Returns:
            dict: Quality assessment
        """
        prompt = f"""
        You are a quality assurance specialist.
        
        TASK: Verify if this output meets expectations.
        
        EXPECTED CONTENT:
        {expected_content}
        
        ACTUAL OUTPUT:
        {output_text[:500]}...
        
        Evaluate:
        1. Does it address the expected content? (Yes/No)
        2. Is it complete and comprehensive? (Yes/No)
        3. Is it clear and understandable? (Yes/No)
        4. Quality score (1-10)
        5. Any issues or suggestions?
        
        Respond in this format:
        Addresses Content: Yes/No
        Complete: Yes/No
        Clear: Yes/No
        Quality Score: X/10
        Issues: [list any issues or "None"]
        """
        
        try:
            response = self.model.generate_content(prompt)
            assessment = response.text
            
            # Simple pass/fail based on response
            passed = "Yes" in assessment and ("10" in assessment or "9" in assessment or "8" in assessment)
            
            return {
                "passed": passed,
                "assessment": assessment
            }
            
        except Exception as e:
            return {
                "passed": False,
                "assessment": f"Quality check failed: {str(e)}"
            }
    
    
    def generate_system_report(self):
        """
        Generate a comprehensive system activity report.
        
        Returns:
            str: Formatted system report
        """
        print("\n" + "=" * 60)
        print("📊 SYSTEM ACTIVITY REPORT")
        print("=" * 60)
        
        report = f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"\nTotal Events Logged: {len(self.logs)}\n"
        
        # Count event types
        event_counts = {}
        for log in self.logs:
            event_type = log["type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        report += "\nEvent Breakdown:\n"
        for event_type, count in event_counts.items():
            report += f"  {event_type}: {count}\n"
        
        # Agent status
        report += "\nAgent Status:\n"
        for agent_name, status in self.agent_status.items():
            agent_display = agent_name.replace("_", " ").title()
            report += f"  {agent_display}: {status}\n"
        
        # Recent activity
        report += "\nRecent Activity (Last 5 events):\n"
        for log in self.logs[-5:]:
            report += f"  [{log['timestamp']}] {log['type']}: {log['event']}\n"
        
        print(report)
        print("=" * 60)
        
        return report
    
    
    def coordinate_workflow(self, user_input):
        """
        Coordinate the entire workflow across all agents.
        
        Args:
            user_input (str): User's medical information or health concern
            
        Returns:
            dict: Results from each agent
        """
        print("\n" + "=" * 60)
        print("🎯 WORKFLOW COORDINATION")
        print("=" * 60)
        
        workflow_results = {}
        
        # Simulate workflow (in actual implementation, would call real agents)
        steps = [
            ("agent1_translator", "Translating medical information"),
            ("agent2_recommender", "Generating diet recommendations"),
            ("agent3_meal_planner", "Creating meal plan"),
            ("agent4_qa", "Ready for questions")
        ]
        
        for agent_name, description in steps:
            self.log_event(f"{description}...", "INFO")
            self.update_agent_status(agent_name, "Running")
            
            # Simulate success (in real implementation, would check actual output)
            self.update_agent_status(agent_name, "Completed")
            self.log_event(f"{description} - Success!", "SUCCESS")
            
            workflow_results[agent_name] = "Completed"
        
        print("\n✅ Workflow completed successfully!")
        
        return workflow_results


# ============================================================
# LAYER 4: TEST/DEMO CODE
# ============================================================

def demo_monitor_agent():
    """
    Demonstration of the Monitor Agent capabilities.
    """
    
    print("=" * 60)
    print("📊 MONITOR AGENT - DEMO")
    print("=" * 60)
    
    # Initialize the monitor
    monitor = MonitorAgent()
    
    print("\n" + "=" * 60)
    print("📋 EXAMPLE 1: System Health Check")
    print("=" * 60)
    
    # Initial health check
    monitor.check_system_health()
    
    
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 2: Simulating Workflow")
    print("=" * 60)
    
    # Simulate a user request
    user_input = "Patient has high blood sugar (diabetes)"
    
    print(f"\n👤 User Input: {user_input}\n")
    
    workflow_results = monitor.coordinate_workflow(user_input)
    
    
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 3: Final Health Check")
    print("=" * 60)
    
    # Health check after workflow
    monitor.check_system_health()
    
    
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 4: System Activity Report")
    print("=" * 60)
    
    # Generate activity report
    monitor.generate_system_report()
    
    
    print("\n\n" + "=" * 60)
    print("📋 EXAMPLE 5: Quality Verification")
    print("=" * 60)
    
    sample_output = """
    Your blood sugar is too high (diabetes). You should eat fewer 
    sugary foods and more vegetables, lean proteins, and whole grains.
    """
    
    print("\n🔍 Verifying output quality...")
    quality = monitor.verify_output_quality(
        sample_output,
        "Simple explanation of diabetes and dietary recommendations"
    )
    
    print(f"\n✅ Quality Check: {'PASSED' if quality['passed'] else 'FAILED'}")
    print(f"\nAssessment:\n{quality['assessment']}")
    
    
    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETE!")
    print("=" * 60)


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    """
    This code runs when you execute the file directly.
    """
    demo_monitor_agent()
