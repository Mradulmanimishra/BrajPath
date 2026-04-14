"""
Simple BrajPath Bot Demo - No interaction required!
Just run and watch the conversation.
"""
import requests
import time
import re

BASE_URL = "http://localhost:8000/whatsapp/webhook"
PHONE = "whatsapp:+919876543210"

def send_message(text, description=""):
    """Send a message to the bot and display response."""
    try:
        print(f"\n{'='*70}")
        if description:
            print(f"[{description}]")
        print(f"USER: {text}")
        print(f"{'='*70}")
        
        response = requests.post(BASE_URL, data={
            "From": PHONE,
            "Body": text
        })
        
        # Extract bot response from TwiML XML
        match = re.search(r'<Message>(.*?)</Message>', response.text, re.DOTALL)
        bot_reply = match.group(1) if match else response.text
        
        print(f"BOT:\n{bot_reply}")
        
        time.sleep(1.5)  # Pause for readability
        return bot_reply
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server!")
        print("Make sure the server is running on http://localhost:8000")
        print("\nTo start the server, run:")
        print("  python -m uvicorn app.main:app --reload")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)

def main():
    """Run automated demo."""
    print("\n" + "="*70)
    print("BRAJPATH AUTOMATED DEMO")
    print("="*70)
    print("\nThis demo shows how pilgrims interact with the BrajPath bot.")
    print("Watch as we get temple timings and route information!")
    print("\n" + "="*70)
    
    time.sleep(2)
    
    # Scenario 1: Get Temple Timings
    print("\n\nSCENARIO 1: Getting Temple Timings")
    print("-" * 70)
    
    send_message("hello", "User starts conversation")
    send_message("1", "User selects English")
    send_message("2", "User wants temple timings")
    send_message("1", "User selects Vrindavan area")
    send_message("1", "User selects Banke Bihari temple")
    
    # Scenario 2: Get Route Information
    print("\n\nSCENARIO 2: Getting Route Directions")
    print("-" * 70)
    
    send_message("menu", "User goes back to main menu")
    send_message("3", "User wants route information")
    send_message("1", "User selects Vrindavan area")
    send_message("1", "User selects Banke Bihari temple")
    send_message("1", "User is coming from Mathura Junction")
    
    # Scenario 3: Browse Partners
    print("\n\nSCENARIO 3: Browsing Partner Services")
    print("-" * 70)
    
    send_message("menu", "User goes back to main menu")
    send_message("5", "User wants to browse partners")
    send_message("0", "User goes back to menu")
    
    # Summary
    print("\n\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70)
    print("\nWhat you just saw:")
    print("  - Multi-language support (selected English)")
    print("  - Temple timing information")
    print("  - Route directions with transport options")
    print("  - Partner browsing feature")
    print("  - Context-aware navigation")
    print("  - Session management (bot remembers user)")
    print("\nAdditional Features Available:")
    print("  - Fair price guidance for transport")
    print("  - Temple advisories and tips")
    print("  - Support for Hindi, Bengali, Tamil")
    print("  - Currently open temples")
    print("\n" + "="*70)
    print("\nTo test interactively, run: python test_bot.py")
    print("For full guide, see: HOW_TO_USE.md")
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted!")
