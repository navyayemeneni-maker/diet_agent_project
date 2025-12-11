# Test Setup Script
# This checks if everything is installed and working correctly

import os
from dotenv import load_dotenv

print("=" * 50)
print("TESTING YOUR PROJECT SETUP")
print("=" * 50)

# Test 1: Load .env file and check API key
print("\n1. Testing .env file...")
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print("   ✅ SUCCESS! API key loaded")
    print(f"   Key starts with: {api_key[:10]}...")
else:
    print("   ❌ FAILED! API key not found")
    print("   Check your .env file")
    exit()

# Test 2: Check CrewAI installation
print("\n2. Testing CrewAI installation...")
try:
    import crewai
    print(f"   ✅ SUCCESS! CrewAI is installed")
except ImportError:
    print("   ❌ FAILED! CrewAI not installed")
    print("   Run: pip install crewai")
    exit()

# Test 3: Check LangChain installation
print("\n3. Testing LangChain installation...")
try:
    import langchain
    print(f"   ✅ SUCCESS! LangChain is installed")
except ImportError:
    print("   ❌ FAILED! LangChain not installed")
    print("   Run: pip install langchain")
    exit()

# Test 4: Check if we can connect to Google Gemini
print("\n4. Testing Google Gemini connection...")
try:
    import google.generativeai as genai
    
    # Configure Gemini with API key
    genai.configure(api_key=api_key)
    
    # Use the working model name
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Try a simple test
    response = model.generate_content("Say 'Hello from Gemini!' if you can read this")
    print(f"   ✅ SUCCESS! Gemini responded")
    print(f"   Response: {response.text}")
    
except Exception as e:
    print(f"   ❌ FAILED! Error: {str(e)}")
    print("   Check your API key is correct")
    exit()

# All tests passed!
print("\n" + "=" * 50)
print("🎉 ALL TESTS PASSED!")
print("You're ready to build your agents!")
print("=" * 50)
