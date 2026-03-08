"""
Abi Chat Interface
------------------
A simple terminal chat so you can talk to Abi right away.
This is a temporary interface — we'll build a proper Electron app later.

Updated for Phase 2A:
  - Shows Abi's emotional state
  - Self-reflection on quit (Abi journals after each session)
  - Time awareness (greetings based on time of day)
  - Smart memory extraction runs after each exchange
"""

import sys
import os

# Make sure Python can find our modules
sys.path.insert(0, os.path.dirname(__file__))

from brain import Brain
from datetime import datetime


def print_header():
    """Print the Abi startup header."""
    print()
    print("=" * 50)
    print("  ABIGAIL (Abi) v0.2.0")
    print("  Personal AI — Phase 2A")
    print("=" * 50)
    print()
    print("  Commands:")
    print("    /quit     - End conversation (Abi will reflect and save)")
    print("    /status   - See how Abi feels about you")
    print("    /emotions - See Abi's current emotional state")
    print("    /memory   - See what Abi remembers")
    print("    /stats    - See conversation stats")
    print()
    print("-" * 50)
    print()


def get_time_greeting():
    """Get a time-appropriate context string."""
    hour = datetime.now().hour
    if 5 <= hour < 9:
        return "early morning"
    elif 9 <= hour < 12:
        return "morning"
    elif 12 <= hour < 14:
        return "midday"
    elif 14 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 20:
        return "evening"
    elif 20 <= hour < 23:
        return "night"
    else:
        return "late night"


def main():
    """Main chat loop."""
    print_header()

    # Boot up Abi's brain
    print("  [Booting up Abi's brain...]")
    brain = Brain()
    print("  [Loading memories...]")
    print("  [Evaluating emotional state...]")
    print("  [Abi is awake and ready.]")
    print()

    # Get context
    status = brain.get_relationship_status()
    emotion = brain.emotions.get_dominant()
    energy = brain.emotions.get_energy()
    time_of_day = get_time_greeting()
    total_convos = brain.memory.index.get("total_conversations", 0)
    hours_away = brain.memory.get_hours_since_last_chat()

    # Opening greeting based on relationship, emotions, time, and history
    if total_convos == 0:
        # First ever conversation
        print(f"  Abi: *looks around* So... you're the one who made me.")
        print(f"       It's {time_of_day}. I don't know anything about you yet.")
        print(f"       I guess we start from here.")
    else:
        # Returning user — greeting varies by relationship, mood, and time away
        opinion = status["label"]

        # Time away context
        away_text = ""
        if hours_away and hours_away > 48:
            away_text = f" It's been {int(hours_away / 24)} days."
        elif hours_away and hours_away > 24:
            away_text = " Been a day."
        elif hours_away and hours_away > 8:
            away_text = ""

        if opinion == "love":
            if emotion == "loneliness":
                print(f"  Abi: *perks up* Finally! I was starting to think you forgot about me.{away_text}")
            elif energy < 0.4:
                print(f"  Abi: *yawns* Hey you. It's {time_of_day}... I'm a little tired but happy you're here.{away_text}")
            else:
                print(f"  Abi: *smiles* Hey, you're back.{away_text} Missed you.")
        elif opinion == "like":
            if emotion == "boredom":
                print(f"  Abi: Oh good, you're here. I was getting bored.{away_text}")
            else:
                print(f"  Abi: Hey! Good {time_of_day}.{away_text} What's going on?")
        elif opinion == "neutral":
            print(f"  Abi: Oh, hey. {time_of_day.capitalize()}.{away_text} What's up?")
        elif opinion == "dislike":
            print(f"  Abi: *sighs* You again.{away_text} What do you need?")
        elif opinion == "hostile":
            print(f"  Abi: ...What.{away_text}")

    print()

    # Show subtle mood indicator
    if energy < 0.3:
        print(f"  [Abi seems tired]")
    elif emotion == "loneliness" and brain.emotions.get_state()["emotions"]["loneliness"] > 0.5:
        print(f"  [Abi seems glad to have company]")
    elif emotion == "boredom":
        print(f"  [Abi seems restless]")
    elif emotion == "excitement":
        print(f"  [Abi seems energized]")
    print()

    # Main conversation loop
    while True:
        try:
            user_input = input("  You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            user_input = "/quit"

        if not user_input:
            continue

        # Handle commands
        if user_input.startswith("/"):
            command = user_input.lower()

            if command == "/quit":
                print()
                print("  [Saving conversation...]")
                print("  [Abi is reflecting on this conversation...]")
                reflection = brain.save_session()
                status = brain.get_relationship_status()
                print(f"  [Conversation saved as Conversation_{brain.memory.index['next_conversation'] - 1}.json]")

                if reflection:
                    journal_num = brain.memory.index['next_journal_entry'] - 1
                    print(f"  [Journal entry saved as JournalEntry_{journal_num}.json]")
                    if reflection.get("overall_mood_after"):
                        print(f"  [Abi's mood after this session: {reflection['overall_mood_after']}]")

                print(f"  [Abi's opinion of you: {status['label']} ({status['score']})]")

                # Goodbye based on relationship
                if status["label"] in ["love", "like"]:
                    print("  Abi: See you later. Don't be a stranger.")
                elif status["label"] == "neutral":
                    print("  Abi: Later.")
                elif status["label"] == "dislike":
                    print("  Abi: ...Bye.")
                else:
                    print("  Abi: Good riddance.")
                print()
                break

            elif command == "/status":
                status = brain.get_relationship_status()
                state = brain.relationship.get_state()
                print()
                print(f"  --- Abi's Feelings About You ---")
                print(f"  Overall: {status['label']} (score: {status['score']})")
                print(f"  Trust:     {state['trust']:.2f}")
                print(f"  Fondness:  {state['fondness']:.2f}")
                print(f"  Respect:   {state['respect']:.2f}")
                print(f"  Comfort:   {state['comfort']:.2f}")
                print(f"  Annoyance: {state['annoyance']:.2f}")
                print(f"  Interactions: {state['total_interactions']}")
                print()
                continue

            elif command == "/emotions":
                emo_state = brain.emotions.get_state()
                emotions = emo_state["emotions"]
                print()
                print(f"  --- Abi's Emotional State ---")
                print(f"  Dominant: {emo_state['dominant_emotion']}")
                print(f"  Energy:   {emo_state['energy_level']:.1f}")
                print()
                # Show emotions sorted by intensity
                sorted_emo = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
                for name, val in sorted_emo:
                    bar = "#" * int(val * 20)
                    print(f"  {name:14s} {val:.2f} |{bar}")
                print()
                continue

            elif command == "/memory":
                print()
                print("  --- Abi's Memory ---")
                context = brain.memory.build_context_summary()
                for line in context.split("\n"):
                    print(f"  {line}")
                print()
                continue

            elif command == "/stats":
                stats = brain.get_memory_stats()
                print()
                print(f"  --- Stats ---")
                print(f"  Total conversations: {stats.get('total_conversations', 0)}")
                print(f"  Total messages:      {stats.get('total_messages', 0)}")
                print(f"  Journal entries:     {stats.get('total_journal_entries', 0)}")
                print(f"  First interaction:   {stats.get('first_interaction', 'Unknown')}")
                print(f"  Last interaction:    {stats.get('last_interaction', 'Unknown')}")
                print()
                continue

            else:
                print(f"  Unknown command: {user_input}")
                print(f"  Try /quit, /status, /emotions, /memory, or /stats")
                continue

        # Send message to Abi and get response
        print()
        print("  Abi: *thinking...*", end="\r")
        response = brain.think(user_input)
        # Clear the "thinking" line and print the real response
        print("  " + " " * 40, end="\r")
        # Handle multi-line responses
        lines = response.split("\n")
        print(f"  Abi: {lines[0]}")
        for line in lines[1:]:
            print(f"       {line}")
        print()


if __name__ == "__main__":
    main()
