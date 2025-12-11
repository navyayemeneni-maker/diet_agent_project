# Production-Stable Models Configuration

## ✅ Current Setup (2025)

Your Diet Recommendation System now uses **only production-stable models** from Groq's official list. This ensures:

- ✅ No deprecation surprises
- ✅ Actively maintained and supported
- ✅ Best performance and reliability
- ✅ Future-proof application

## 📊 Model Assignment by Agent

### Agent 1: Medical Translator
**Task:** Understand medical reports & translate to simple language

**Models (in priority order):**
1. `llama-3.3-70b-versatile` - Best reasoning for medical context
2. `openai/gpt-oss-120b` - Excellent general reasoning
3. `openai/gpt-oss-20b` - Good fallback, cheaper

**Why:** Medical terminology requires strong reasoning and context understanding.

---

### Agent 2: Diet Recommender
**Task:** Analyze conditions → recommend foods to eat/avoid

**Models (in priority order):**
1. `llama-3.3-70b-versatile` - Top choice for complex diet rules
2. `openai/gpt-oss-120b` - Strong logic + flexibility
3. `openai/gpt-oss-20b` - Lower cost fallback

**Why:** Requires conditional logic to merge multiple health conditions.

---

### Agent 3: Meal Planner
**Task:** Generate creative 7-day meal plans with recipes

**Models (in priority order):**
1. `llama-3.1-8b-instant` - Fast + creative, perfect for meal plans
2. `openai/gpt-oss-20b` - Heavier model for more detail
3. `openai/gpt-oss-120b` - Fallback with strongest reasoning

**Why:** Creative task benefits from speed; fallbacks provide quality if needed.

---

### Agent 4: Q&A Bot
**Task:** Answer follow-up questions interactively

**Models (in priority order):**
1. `llama-3.1-8b-instant` - Best ultra-fast chat
2. `openai/gpt-oss-20b` - Good conversational fallback
3. `openai/gpt-oss-120b` - Fallback with strong comprehension

**Why:** Chat requires instant responses; 8B model is perfect for this.

---

## 🚫 Deprecated Models (Removed)

The following models were **removed** from your system because they're deprecated:

| Model | Status | Replacement |
|-------|--------|-------------|
| `deepseek-r1-distill-llama-70b` | ❌ Deprecated | `llama-3.3-70b-versatile` |
| `llama3-8b-8192` | ❌ Deprecated | `llama-3.1-8b-instant` |
| `llama3-70b-8192` | ❌ Deprecated | `llama-3.3-70b-versatile` |
| `gemma2-9b-it` | ❌ Deprecated | `llama-3.1-8b-instant` |
| `qwen/*` models | ⚠️ Not in production list | OpenAI GPT-OSS models |

---

## 🔄 Automatic Fallback System

Each agent tries models in order:

```
Primary Model (Best for task)
    ↓ (if fails)
Fallback 1 (Alternative)
    ↓ (if fails)
Fallback 2 (Last resort)
    ↓
Success or Error
```

**Example Console Output:**
```
🔄 Translating medical text...
   ⚠️ Model llama-3.3-70b-versatile failed: Rate limit exceeded
   Trying fallback model 1: openai/gpt-oss-120b
✅ Translation complete using openai/gpt-oss-120b!
```

---

## 📈 Performance Characteristics

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| `llama-3.1-8b-instant` | ⚡⚡⚡ Ultra Fast | ✅ Good | 💰 Cheapest | Chat, Creative |
| `llama-3.3-70b-versatile` | ⚡⚡ Fast | ✅✅ Excellent | 💰💰 Moderate | Reasoning, Medical |
| `openai/gpt-oss-20b` | ⚡⚡ Fast | ✅ Good | 💰💰 Moderate | General Purpose |
| `openai/gpt-oss-120b` | ⚡ Slower | ✅✅✅ Best | 💰💰💰 Higher | Complex Reasoning |

---

## 🎯 Why This Configuration?

### Optimized for Your Use Case:

1. **Medical Understanding** (Agent 1)
   - Needs strong reasoning → 70B models
   - Fallback to GPT-OSS for reliability

2. **Diet Logic** (Agent 2)
   - Complex conditional logic → 70B models
   - Multiple fallbacks for high availability

3. **Creative Meal Plans** (Agent 3)
   - Speed matters → 8B instant first
   - Quality fallbacks if needed

4. **Fast Chat** (Agent 4)
   - Instant responses critical → 8B instant
   - Heavier models as backup

---

## 🔮 Future-Proofing

### How to Stay Updated:

1. **Check Groq's Production Models:**
   - Visit: https://console.groq.com/docs/models
   - Look for "Production Models" section

2. **Dynamic Model Fetching (Optional):**
   ```python
   # Get latest production models
   models = client.models.list()
   active = [m for m in models.data if not m.deprecated]
   ```

3. **Monitor Console Logs:**
   - Watch which models are being used
   - If fallbacks trigger often, primary might be deprecated

---

## ✅ Verification Checklist

- [x] All models are from Groq's production list
- [x] No deprecated models in use
- [x] 3-tier fallback for each agent
- [x] Optimized for speed vs quality per task
- [x] Console logging shows which model was used
- [x] Documentation updated

---

## 📞 Support

If you encounter issues:

1. **Check Model Status:** https://console.groq.com/docs/models
2. **Groq Discord:** https://groq.com/discord
3. **Groq Documentation:** https://console.groq.com/docs

---

**Last Updated:** December 2025  
**Groq API Version:** v1  
**Production Models Verified:** ✅
