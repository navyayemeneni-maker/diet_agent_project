# 🥗 Diet Recommendation System

AI-powered system that reads medical reports and creates **personalized** diet plans based on your dietary preferences, allergies, and restrictions.

## ✨ Features

- **👤 User Profile** - Set diet type, allergies, religious restrictions, cooking time
- **📄 Medical Report Analysis** - Upload PDF, Word, or type text
- **🤖 4 AI Agents** - Specialized agents for translation, diet, meal planning, Q&A
- **📊 Dashboard** - Track all reports, view history, download PDFs
- **🛡️ Personalization** - Respects vegetarian/vegan, Hindu/Muslim restrictions, allergies
- **🎨 Professional UI** - Modern design with custom theme, animations, and polished components

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                         (Streamlit)                             │
├─────────────────────────────────────────────────────────────────┤
│  🏠 Home │ 📊 Dashboard │ 👤 Profile │ 🩺 Analyze │ 💬 Q&A │ ℹ️ About │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CORE MANAGERS                              │
├──────────────────┬──────────────────┬───────────────────────────┤
│  profile_manager │  report_manager  │        llm.py             │
│  (user prefs)    │  (history)       │    (Groq client)          │
└──────────────────┴──────────────────┴───────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AI AGENTS                                │
├────────────┬────────────┬────────────┬──────────────────────────┤
│  Agent 1   │  Agent 2   │  Agent 3   │        Agent 4           │
│ Translator │ Diet Rec   │ Meal Plan  │        Q&A Bot           │
│ (70B)      │ (70B)      │ (8B)       │        (8B)              │
└────────────┴────────────┴────────────┴──────────────────────────┘
```

## 🔄 User Flow

```
┌──────────────┐
│  First Visit │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  Onboarding  │────▶│ Save Profile │
│  (Profile)   │     │   to JSON    │
└──────────────┘     └──────┬───────┘
                            │
       ┌────────────────────┘
       ▼
┌──────────────┐
│   Home Page  │◀─────────────────────────────┐
└──────┬───────┘                              │
       │                                      │
       ▼                                      │
┌──────────────┐                              │
│Analyze Health│                              │
│ (PDF/Text)   │                              │
└──────┬───────┘                              │
       │                                      │
       ▼                                      │
┌──────────────────────────────────────┐      │
│           AI PIPELINE                │      │
│                                      │      │
│  Medical    ──▶  Diet    ──▶  Meal   │      │
│  Text           Rec          Plan    │      │
│    │             │            │      │      │
│    ▼             ▼            ▼      │      │
│  Agent 1     Agent 2      Agent 3    │      │
│  (translate) (recommend)  (plan)     │      │
└──────────────────┬───────────────────┘      │
                   │                          │
                   ▼                          │
┌──────────────────────────────────────┐      │
│            RESULTS                   │      │
│  • Simple Explanation                │      │
│  • Foods to Eat/Avoid Table          │      │
│  • Full Diet Recommendations         │      │
│  • 7-Day Meal Plan                   │      │
│  • PDF Download                      │      │
└──────────────────┬───────────────────┘      │
                   │                          │
                   ▼                          │
┌──────────────────────────────────────┐      │
│  Save to Dashboard (report_manager)  │──────┘
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│            DASHBOARD                 │
│  • View all past reports             │
│  • Track health conditions           │
│  • Re-download PDFs                  │
│  • Delete old reports                │
└──────────────────────────────────────┘
```

## 📁 Project Structure

```
diet-recommendation-system/
├── app.py                  # Main Streamlit app (all pages)
├── llm.py                  # Groq AI client
├── profile_manager.py      # User profile storage
├── report_manager.py       # Report history storage
├── file_reader.py          # PDF/DOCX text extraction
├── requirements.txt        # Python dependencies
├── .env                    # API key (GROQ_API_KEY)
├── .gitignore              # Git ignore rules
│
├── .streamlit/
│   └── config.toml            # Custom theme configuration
│
├── agents/
│   ├── agent1_translator.py   # Medical → Simple language
│   ├── agent2_recommender.py  # Health → Diet recommendations
│   ├── agent3_meal_planner.py # Diet → 7-day meal plan
│   └── agent4_qa.py           # Q&A bot
│
├── data/
│   └── reports/               # Saved report history (auto-created)
│
└── user_profile.json          # Saved user preferences (auto-created)
```

## 🤖 AI Agents

| Agent | Purpose | Model | Speed |
|-------|---------|-------|-------|
| **Agent 1** | Translate medical jargon → simple language | `llama-3.3-70b-versatile` | ~5s |
| **Agent 2** | Create diet recommendations based on health + profile | `llama-3.3-70b-versatile` | ~8s |
| **Agent 3** | Generate 7-day meal plan with recipes | `llama-3.1-8b-instant` | ~3s |
| **Agent 4** | Answer follow-up questions | `llama-3.1-8b-instant` | ~2s |

## 🛡️ Personalization Examples

| User Profile | What AI Does |
|--------------|--------------|
| Vegetarian | Never recommends meat, fish, poultry |
| Hindu | Never recommends beef |
| Muslim/Halal | Never recommends pork |
| Peanut Allergy | Never includes peanuts (dangerous!) |
| Cooking: 15 min | Only quick recipes |
| Budget-friendly | Affordable ingredients |

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <repository-url>
cd diet-recommendation-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Groq API Key (FREE)

1. Go to https://console.groq.com
2. Sign up (no credit card needed)
3. Create API key
4. Create `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

### 3. Run the App

```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

## 📱 Pages

| Page | Description |
|------|-------------|
| 🏠 **Home** | Welcome page with quick stats |
| 📊 **Dashboard** | View all reports, track conditions, download PDFs |
| 👤 **My Profile** | Set diet type, allergies, restrictions |
| 🩺 **Analyze Health** | Upload medical report or enter health data, generate diet plan |
| 💬 **Ask Questions** | Q&A about diet and nutrition |
| ℹ️ **About** | System info and disclaimer |

## 📋 Requirements

```
streamlit
python-dotenv
openai
fpdf
PyPDF2
python-docx
pandas
```

## ⚠️ Disclaimer

This is **not medical advice**. Always consult a healthcare professional before making dietary changes.

## 👩‍💻 Author

**Navya** - Data Science & AI Student  
December 2025
