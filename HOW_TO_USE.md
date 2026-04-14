# 🕉️ How to Use BrajPath - Complete Guide

## 📱 What is BrajPath?

BrajPath is a **WhatsApp chatbot** that helps pilgrims visiting Mathura and Vrindavan by providing:
- Temple timings
- Route directions
- Fair price guidance
- Temple advisories
- Partner services (hotels, guides, transport)

---

## 🎯 Three Ways to Use BrajPath

### **Option 1: Test Locally (Right Now!)**
Test the bot on your computer without WhatsApp

### **Option 2: Connect to WhatsApp via Twilio**
Make it work with real WhatsApp messages

### **Option 3: Deploy to Production**
Host it online for public use

---

## 🧪 OPTION 1: Test Locally (Easiest!)

The server is already running! Let's test it right now.

### Method A: Using Browser + Postman/Thunder Client

1. **Install a REST client:**
   - Postman: https://www.postman.com/downloads/
   - Or use Thunder Client extension in VS Code
   - Or use curl in terminal

2. **Test the conversation:**

**Step 1 - Say Hello:**
```
POST http://localhost:8000/whatsapp/webhook
Content-Type: application/x-www-form-urlencoded

From=whatsapp:+919876543210
Body=hello
```

**Response:** You'll get the welcome message with language options!

**Step 2 - Select Language (English):**
```
POST http://localhost:8000/whatsapp/webhook
Content-Type: application/x-www-form-urlencoded

From=whatsapp:+919876543210
Body=1
```

**Response:** Main menu with 7 options!

**Step 3 - Get Temple Timings:**
```
POST http://localhost:8000/whatsapp/webhook
Content-Type: application/x-www-form-urlencoded

From=whatsapp:+919876543210
Body=2
```

Continue the conversation by sending more messages!

---

### Method B: Using Python Script

I can create a test script for you:

```python
import requests

BASE_URL = "http://localhost:8000/whatsapp/webhook"
PHONE = "whatsapp:+919876543210"

def send_message(text):
    response = requests.post(BASE_URL, data={
        "From": PHONE,
        "Body": text
    })
    print(f"\n📱 You: {text}")
    print(f"🤖 Bot: {response.text}")
    return response.text

# Start conversation
send_message("hello")
send_message("1")  # Select English
send_message("2")  # Temple timings
send_message("1")  # Vrindavan area
send_message("1")  # Banke Bihari temple
```

---

### Method C: Using curl (Command Line)

```bash
# Step 1: Say hello
curl -X POST http://localhost:8000/whatsapp/webhook \
  -d "From=whatsapp:+919876543210" \
  -d "Body=hello"

# Step 2: Select English
curl -X POST http://localhost:8000/whatsapp/webhook \
  -d "From=whatsapp:+919876543210" \
  -d "Body=1"

# Step 3: Get temple timings
curl -X POST http://localhost:8000/whatsapp/webhook \
  -d "From=whatsapp:+919876543210" \
  -d "Body=2"
```

---

## 📱 OPTION 2: Connect to Real WhatsApp

To make this work with actual WhatsApp messages:

### Step 1: Get Twilio Account

1. Sign up at https://www.twilio.com
2. Go to Console → Messaging → Try it out → WhatsApp
3. Join the Twilio Sandbox (for testing)
4. Note your credentials:
   - Account SID
   - Auth Token
   - WhatsApp number (usually +1 415 523 8886)

### Step 2: Configure BrajPath

Edit your `.env` file:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
APP_ENV=development
```

### Step 3: Expose Your Local Server

Since Twilio needs to reach your computer, use **ngrok**:

```bash
# Install ngrok: https://ngrok.com/download

# Run ngrok
ngrok http 8000
```

You'll get a URL like: `https://abc123.ngrok.io`

### Step 4: Configure Twilio Webhook

1. Go to Twilio Console → Messaging → Settings → WhatsApp Sandbox
2. Set "When a message comes in" to:
   ```
   https://abc123.ngrok.io/whatsapp/webhook
   ```
3. Save

### Step 5: Test on WhatsApp!

1. Send the join code to the Twilio WhatsApp number
2. Then send: "hello"
3. The bot will respond! 🎉

---

## 🌐 OPTION 3: Deploy to Production

### Deploy to Heroku (Free Tier)

1. **Install Heroku CLI:**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App:**
   ```bash
   cd braj_sahayak
   heroku login
   heroku create brajpath-app
   ```

3. **Add PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables:**
   ```bash
   heroku config:set APP_ENV=production
   heroku config:set TWILIO_ACCOUNT_SID=ACxxxxx
   heroku config:set TWILIO_AUTH_TOKEN=your_token
   heroku config:set TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   ```

5. **Create Procfile:**
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

6. **Deploy:**
   ```bash
   git push heroku main
   ```

7. **Initialize Database:**
   ```bash
   heroku run python -m scripts.init_db
   heroku run python -m scripts.run_seed
   ```

8. **Configure Twilio:**
   Set webhook to: `https://brajpath-app.herokuapp.com/whatsapp/webhook`

---

## 🎮 Interactive Demo Script

Let me create a test script you can run right now!

Save this as `test_bot.py`:

```python
import requests
import time

BASE_URL = "http://localhost:8000/whatsapp/webhook"
PHONE = "whatsapp:+919876543210"

def send(text):
    response = requests.post(BASE_URL, data={
        "From": PHONE,
        "Body": text
    })
    # Extract bot response from TwiML
    import re
    match = re.search(r'<Message>(.*?)</Message>', response.text, re.DOTALL)
    bot_reply = match.group(1) if match else response.text
    
    print(f"\n{'='*60}")
    print(f"📱 YOU: {text}")
    print(f"{'='*60}")
    print(f"🤖 BOT:\n{bot_reply}")
    time.sleep(1)
    return bot_reply

print("🕉️  BRAJPATH DEMO - Temple Guide Assistant")
print("="*60)

# Demo conversation
send("hello")
send("1")  # English
send("2")  # Temple timings
send("1")  # Vrindavan
send("1")  # Banke Bihari
send("menu")  # Back to menu
send("3")  # Routes
send("1")  # Vrindavan
send("1")  # Banke Bihari
send("1")  # From Mathura Junction

print("\n✅ Demo complete!")
```

Run it:
```bash
python test_bot.py
```

---

## 🗺️ Conversation Flow

```
User: "hello"
Bot: Welcome! Select language:
     1. English
     2. हिंदी (Hindi)
     3. বাংলা (Bengali)
     4. தமிழ் (Tamil)

User: "1"
Bot: Main Menu:
     1. Temples Open Now
     2. Temple Timings
     3. Routes & Directions
     4. Fair Price Guide
     5. Browse Partners
     6. Temple Advisories
     7. Change Language
     0. Resend Menu

User: "2"
Bot: Select Area:
     1. Vrindavan
     2. Mathura
     3. Raman Reti
     4. Gokul
     0. Back to Menu

User: "1"
Bot: Select Temple:
     1. Shri Banke Bihari Mandir
     2. Prem Mandir
     3. ISKCON Temple
     0. Back

User: "1"
Bot: 🕉️ Shri Banke Bihari Mandir
     
     Summer Timings:
     Morning: 7:45 AM - 12:00 PM
     Evening: 5:30 PM - 9:30 PM
     
     Winter Timings:
     Morning: 8:45 AM - 1:00 PM
     Evening: 4:30 PM - 9:00 PM
     
     [More details...]
```

---

## 🎯 Quick Test Commands

Try these in sequence:

```bash
# 1. Start conversation
curl -X POST http://localhost:8000/whatsapp/webhook \
  -d "From=whatsapp:+919876543210" -d "Body=hello"

# 2. English
curl -X POST http://localhost:8000/whatsapp/webhook \
  -d "From=whatsapp:+919876543210" -d "Body=1"

# 3. Temple timings
curl -X POST http://localhost:8000/whatsapp/webhook \
  -d "From=whatsapp:+919876543210" -d "Body=2"

# 4. Vrindavan
curl -X POST http://localhost:8000/whatsapp/webhook \
  -d "From=whatsapp:+919876543210" -d "Body=1"

# 5. Banke Bihari
curl -X POST http://localhost:8000/whatsapp/webhook \
  -d "From=whatsapp:+919876543210" -d "Body=1"
```

---

## 📊 What You Can Test

1. **Language Selection** - Try all 4 languages
2. **Temple Timings** - Get opening hours
3. **Routes** - Get directions from railway station
4. **Fair Prices** - See transport pricing
5. **Partners** - Browse hotels, guides (NEW - just fixed!)
6. **Advisories** - Get temple tips
7. **Context Memory** - Bot remembers your preferences

---

## 🐛 Troubleshooting

**Server not responding?**
```bash
# Check if server is running
curl http://localhost:8000/health
```

**Database errors?**
```bash
cd braj_sahayak
python -m scripts.init_db
python -m scripts.run_seed
```

**Want to see logs?**
Check the terminal where the server is running

---

## 📞 Need Help?

- Check `SERVER_RUNNING.md` for server details
- Check `BUGS_FIXED.md` for recent fixes
- Check `README.md` for architecture details

---

**Ready to test? The server is running on http://localhost:8000!** 🚀
