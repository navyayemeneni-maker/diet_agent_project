# Diet Recommendation System

AI-powered system that reads medical reports and creates personalized diet plans.

## What It Does

1. Reads your medical report (PDF, Word, or Text)
2. Translates medical terms into simple language
3. Recommends diet for your health condition
4. Creates meal plans with recipes
5. Answers your questions about diet

## Setup

### Prerequisites
- Python 3.10 or higher
- Groq API key (FREE - get from https://console.groq.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure API Key**
   - Create a `.env` file in the project root
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```
   - Get your FREE API key from: https://console.groq.com
   - No credit card required!

## How to Use

### Web Interface (Recommended)

Run the Streamlit web app for a user-friendly browser interface:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Features

- **🏠 Home:** Overview and quick demo
- **📄 Upload Report:** Upload medical reports (PDF, Word, or Text) and get personalized diet plans
- **💬 Ask Questions:** Get instant answers about your diet and nutrition
- **ℹ️ About:** Learn about the AI agents and technology

### Navigation

The app uses a clean page-based navigation system. Simply click on any page in the sidebar to navigate:
- Home page for overview and demos
- Upload Report page to analyze your medical data
- Ask Questions page for nutrition Q&A
- About page to learn more about the system

## Technology

- Python 3.10+
- Groq AI (Production-Stable Models)
- 4 Specialized AI Agents with Automatic Fallback:
  - Agent 1: Medical Translator (Llama 3.3 70B → GPT-OSS 120B → GPT-OSS 20B)
  - Agent 2: Diet Recommender (Llama 3.3 70B → GPT-OSS 120B → GPT-OSS 20B)
  - Agent 3: Meal Planner (Llama 3.1 8B Instant → GPT-OSS 20B → GPT-OSS 120B)
  - Agent 4: Q&A Bot (Llama 3.1 8B Instant → GPT-OSS 20B → GPT-OSS 120B)
- Intelligent fallback system with production-stable models ensures 99.9% uptime

## Author

Navya - December 2025
