"""
Interactive BrajPath Bot Tester
Run this to test the bot locally without WhatsApp!
"""
import requests
import time
import re

BASE_URL = "http://localhost:8000/whatsapp/webhook"
PHONE = "whatsapp:+919876543210"

def send_message(text):
    """Send a message to the bot and get response."""
    try:
        response = requests.post(BASE_URL, data={
            "From": PHONE,
            "Body": text
        })
        
        # Extract bot response from TwiML XML
        match = re.search(r'<Message>(.*?)</Message>', response.text, re.DOTALL)
        bot_reply = match.group(1) if match else response.text
        
        print(f"\n{'='*70}")
        print(f"📱 YOU: {text}")
        print(f"{'='*70}")
        print(f"🤖 BOT:")
        print(bot_reply)
        print(f"{'='*70}")
        
        time.sleep(0.5)  # Small delay for readability
        return bot_reply
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server!")
        print("Make sure the server is running on http://localhost:8000")
        exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

def demo_conversation():
    """Run a demo conversation with the bot."""
    print("\n" + "="*70)
    print("🕉️  BRAJPATH DEMO - WhatsApp Temple Guide Assistant")
    print("="*70)
    print("\nThis demo will show you how the bot works!")
    print("The bot helps pilgrims find temple timings, routes, and more.\n")
    
    input("Press Enter to start the demo...")
    
    # Demo flow
    print("\n\n🎬 DEMO SCENARIO: Getting Temple Timings")
    print("-" * 70)
    
    send_message("hello")
    input("\n👆 Bot shows language options. Press Enter to select English...")
    
    send_message("1")
    input("\n👆 Bot shows main menu. Press Enter to get temple timings...")
    
    send_message("2")
    input("\n👆 Bot asks for area. Press Enter to select Vrindavan...")
    
    send_message("1")
    input("\n👆 Bot shows temples in Vrindavan. Press Enter to select Banke Bihari...")
    
    send_message("1")
    input("\n👆 Bot shows temple timings! Press Enter to go back to menu...")
    
    send_message("menu")
    input("\n👆 Back at main menu. Press Enter to try routes...")
    
    send_message("3")
    input("\n👆 Bot asks for area. Press Enter to select Vrindavan...")
    
    send_message("1")
    input("\n👆 Select temple. Press Enter for Banke Bihari...")
    
    send_message("1")
    input("\n👆 Bot asks starting point. Press Enter for Mathura Junction...")
    
    send_message("1")
    input("\n👆 Bot shows route with transport options! Press Enter to finish...")
    
    print("\n\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    print("\nYou've seen:")
    print("  ✅ Language selection")
    print("  ✅ Temple timings")
    print("  ✅ Route directions")
    print("  ✅ Context-aware navigation")
    print("\nThe bot also supports:")
    print("  • Fair price guidance")
    print("  • Partner browsing (hotels, guides)")
    print("  • Temple advisories")
    print("  • Multi-language support (Hindi, Bengali, Tamil)")
    print("\n" + "="*70)

def interactive_mode():
    """Let user interact with bot freely."""
    print("\n" + "="*70)
    print("🕉️  BRAJPATH - Interactive Mode")
    print("="*70)
    print("\nYou can now chat with the bot!")
    print("Type 'quit' to exit, 'demo' to run demo again\n")
    
    # Start with hello
    send_message("hello")
    
    while True:
        try:
            user_input = input("\n📱 Your message: ").strip()
            
            if user_input.lower() == 'quit':
                print("\n👋 Goodbye!")
                break
            elif user_input.lower() == 'demo':
                demo_conversation()
                continue
            elif not user_input:
                continue
                
            send_message(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

def main():
    """Main function."""
    print("\n" + "="*70)
    print("🕉️  BRAJPATH BOT TESTER")
    print("="*70)
    print("\nChoose an option:")
    print("  1. Run Demo (Guided tour)")
    print("  2. Interactive Mode (Chat freely)")
    print("  3. Quick Test (Just check if it works)")
    
    choice = input("\nYour choice (1-3): ").strip()
    
    if choice == "1":
        demo_conversation()
        
        cont = input("\n\nWant to try interactive mode? (y/n): ").strip().lower()
        if cont == 'y':
            interactive_mode()
            
    elif choice == "2":
        interactive_mode()
        
    elif choice == "3":
        print("\n🧪 Quick Test...")
        send_message("hello")
        print("\n✅ Bot is working! Choose option 1 or 2 to explore more.")
        
    else:
        print("Invalid choice. Run the script again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
