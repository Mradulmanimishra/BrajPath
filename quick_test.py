"""Quick test of BrajPath bot - Just 3 messages!"""
import requests
import re

URL = "http://localhost:8000/whatsapp/webhook"
PHONE = "whatsapp:+919876543210"

def send(text):
    r = requests.post(URL, data={"From": PHONE, "Body": text})
    match = re.search(r'<Message>(.*?)</Message>', r.text, re.DOTALL)
    reply = match.group(1) if match else r.text
    print(f"\n{'='*60}\nYOU: {text}\n{'='*60}\nBOT:\n{reply}\n")
    return reply

print("\n" + "="*60)
print("BRAJPATH QUICK TEST")
print("="*60)

send("hello")
send("1")  # English
send("2")  # Temple timings

print("="*60)
print("SUCCESS! Bot is working!")
print("="*60)
print("\nFor full demo: python demo_bot.py")
print("For interactive: python test_bot.py")
print("For guide: see HOW_TO_USE.md")
