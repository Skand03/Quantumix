# 🤖 AI Chatbot Setup Guide

## Current Status

Your chatbot is **WORKING NOW** with a fallback system!

- ✅ **Without API Key**: Uses smart rule-based responses
- ✅ **With API Key**: Uses real AI (Gemini, OpenAI, or Hugging Face)

---

## 🚀 Quick Start (No API Key Needed)

The chatbot works immediately with intelligent fallback responses!

Just go to: **http://127.0.0.1:8000/research/**

---

## ⭐ Upgrade to Real AI (FREE)

### Option 1: Gemini AI by Google (RECOMMENDED - FREE)

**Why Gemini?**
- ✅ Completely FREE
- ✅ Generous usage limits
- ✅ High quality responses
- ✅ Easy to set up

**Setup Steps:**

1. **Get API Key** (2 minutes):
   - Go to: https://makersuite.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

2. **Add to Your Project**:
   - Open `.env` file (or create it in project root)
   - Add this line:
   ```env
   GEMINI_API_KEY=your-api-key-here
   ```

3. **Restart Server**:
   ```bash
   python manage.py runserver
   ```

4. **Done!** Your chatbot now uses real AI! 🎉

---

### Option 2: OpenAI GPT (Paid but Excellent)

**Cost**: ~$0.002 per 1K tokens (very cheap)

**Setup:**

1. Get API key: https://platform.openai.com/api-keys
2. Add to `.env`:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```
3. Restart server

---

### Option 3: Hugging Face (FREE)

**Setup:**

1. Get token: https://huggingface.co/settings/tokens
2. Add to `.env`:
   ```env
   HUGGINGFACE_API_KEY=your-token-here
   ```
3. Restart server

---

## 🎯 How It Works

### Smart Fallback System

The chatbot tries AI providers in this order:

1. **Gemini AI** (if API key provided)
2. **OpenAI** (if API key provided)
3. **Hugging Face** (if API key provided)
4. **Fallback** (smart rule-based responses)

You'll always get a response, even without any API keys!

---

## 💬 Test Your Chatbot

### Without API Key (Fallback Mode):
- Answers common questions about bionic hands
- Provides detailed information on key topics
- Works offline
- No cost

### With API Key (AI Mode):
- Understands natural language
- Answers ANY question intelligently
- Learns from context
- More conversational

---

## 🧪 Testing

### Test Questions:

```
"What is EMG signal processing?"
"How do I build a bionic hand?"
"Explain machine learning in prosthetics"
"What components do I need?"
"Tell me about 3D printing materials"
"How much does it cost?"
```

### Check AI Status:

Visit: **http://127.0.0.1:8000/api/chatbot-status/**

This shows which AI providers are active.

---

## 📊 Comparison

| Feature | Fallback | Gemini AI | OpenAI | Hugging Face |
|---------|----------|-----------|--------|--------------|
| Cost | FREE | FREE | Paid | FREE |
| Quality | Good | Excellent | Excellent | Good |
| Speed | Instant | Fast | Fast | Medium |
| Setup | None | 2 min | 5 min | 5 min |
| Offline | ✅ Yes | ❌ No | ❌ No | ❌ No |

---

## 🔧 Troubleshooting

### "Chatbot not responding"
- Check browser console (F12) for errors
- Verify server is running
- Fallback mode should always work

### "API key not working"
- Check `.env` file exists in project root
- Verify API key is correct (no extra spaces)
- Restart Django server
- Check API status: `/api/chatbot-status/`

### "Slow responses"
- AI APIs can take 1-3 seconds
- This is normal for real AI processing
- Fallback mode is instant

---

## 🎨 Customization

### Change Chatbot Personality

Edit `bionic_app/chatbot_ai.py`:

```python
prompt = f"""You are a [YOUR PERSONALITY HERE] assistant...
```

### Add More Fallback Responses

Edit `bionic_app/templates/research.html`:

```javascript
function generateResponse(question) {
    // Add your custom responses here
}
```

---

## 📈 Usage Limits

### Gemini AI (FREE):
- 60 requests per minute
- 1,500 requests per day
- More than enough for personal use!

### OpenAI (Paid):
- Pay as you go
- ~$0.002 per 1K tokens
- $5 credit lasts months

### Hugging Face (FREE):
- 30,000 characters per month
- Good for testing

---

## 🎉 Recommended Setup

**For Best Experience:**

1. **Start with Fallback** (works now!)
2. **Add Gemini API** (takes 2 minutes, FREE)
3. **Enjoy real AI responses!**

---

## 💡 Pro Tips

1. **Gemini is FREE** - No reason not to use it!
2. **Fallback is smart** - Works great without API
3. **Test both modes** - Compare responses
4. **Multiple APIs** - System tries all available
5. **No installation** - Just add API key to `.env`

---

## 🔗 Quick Links

- **Gemini API**: https://makersuite.google.com/app/apikey
- **OpenAI API**: https://platform.openai.com/api-keys
- **Hugging Face**: https://huggingface.co/settings/tokens
- **Chatbot Status**: http://127.0.0.1:8000/api/chatbot-status/
- **Research Page**: http://127.0.0.1:8000/research/

---

## ✅ Current Status

Your chatbot is **LIVE and WORKING**!

- 🤖 Chatbot: Active
- 💬 Fallback: Working
- 🔌 API: Ready (add key to enable)
- 🌐 Server: Running

**Go test it now:** http://127.0.0.1:8000/research/

Click the purple chat button in the bottom-right corner! 💬

---

**Made with ❤️ for Quantumix Bionic Hand Project**
