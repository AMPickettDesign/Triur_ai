"""
Sibling AI — Memory System
Handles long-term memory, conversations, and reflections.
Each sibling has its own data directory and file naming:
  Abi:   A_Convo1.json, Diary_1.json
  David: D_Convo1.json, Notebook_1.json
  Quinn: Q_Convo1.json, Journal_1.json
"""

import os
from datetime import datetime
from utils import load_json, save_json, get_sibling_naming


class Memory:
    """Long-term memory system for a sibling AI."""

    def __init__(self, dirs, sibling_id="abi"):
        self.memory_dir = dirs["memory"]
        self.convo_dir = dirs["conversations"]
        self.journal_dir = dirs["journal"]

        # Per-sibling file naming
        naming = get_sibling_naming(sibling_id)
        self.convo_prefix = naming["prefix"]        # A, D, or Q
        self.reflection_name = naming["reflection"]  # Diary, Notebook, or Journal

        self.facts = load_json(os.path.join(self.memory_dir, "facts.json"), {})
        self.opinions = load_json(os.path.join(self.memory_dir, "opinions.json"), {})
        self.events = load_json(os.path.join(self.memory_dir, "events.json"), [])
        self.patterns = load_json(os.path.join(self.memory_dir, "patterns.json"), [])
        self.index = load_json(os.path.join(self.memory_dir, "index.json"), {
            "next_conversation": 1,
            "next_journal_entry": 1,
            "total_messages": 0,
            "total_conversations": 0,
            "total_journal_entries": 0,
            "first_interaction": None,
            "last_interaction": None
        })

        if self.index["first_interaction"] is None:
            self.index["first_interaction"] = datetime.now().isoformat()
            self._save_index()

    def _save(self, filename, data):
        save_json(os.path.join(self.memory_dir, filename), data)

    def _save_index(self):
        self._save("index.json", self.index)

    # ─── FACTS ───

    def remember_fact(self, category, key, value):
        if category not in self.facts:
            self.facts[category] = {}
        existing = self.facts[category].get(key)
        now = datetime.now().isoformat()
        if existing and existing["value"] == value:
            existing["last_confirmed"] = now
            existing["times_referenced"] += 1
        else:
            self.facts[category][key] = {
                "value": value, "learned_at": now,
                "last_confirmed": now, "times_referenced": 0
            }
        self._save("facts.json", self.facts)

    def remember_facts_batch(self, facts_list):
        for f in facts_list:
            self.remember_fact(f["category"], f["key"], f["value"])

    def get_all_facts(self):
        return self.facts

    # ─── OPINIONS ───

    def store_opinion(self, topic, opinion, strength=0.5):
        self.opinions[topic] = {
            "opinion": opinion, "strength": strength,
            "formed_at": datetime.now().isoformat(), "times_expressed": 0
        }
        self._save("opinions.json", self.opinions)

    def store_opinions_batch(self, opinions_list):
        for op in opinions_list:
            self.store_opinion(op["topic"], op["opinion"], op.get("strength", 0.5))

    def get_opinions(self):
        return self.opinions

    # ─── EVENTS ───

    def log_event(self, event_type, description, importance=0.5):
        now = datetime.now()
        self.events.append({
            "type": event_type, "description": description,
            "importance": importance,
            "date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S")
        })
        self.events = self.events[-1000:]
        self._save("events.json", self.events)

    # ─── PATTERNS ───

    def store_pattern(self, pattern_type, description, confidence=0.5):
        for p in self.patterns:
            if p["description"] == description:
                p["confidence"] = min(1.0, p["confidence"] + 0.1)
                p["last_observed"] = datetime.now().isoformat()
                p["times_observed"] += 1
                self._save("patterns.json", self.patterns)
                return
        self.patterns.append({
            "type": pattern_type, "description": description,
            "confidence": confidence,
            "first_observed": datetime.now().isoformat(),
            "last_observed": datetime.now().isoformat(),
            "times_observed": 1
        })
        self.patterns = self.patterns[-200:]
        self._save("patterns.json", self.patterns)

    # ─── CONVERSATIONS ───
    # Files: A_Convo1.json, D_Convo1.json, Q_Convo1.json

    def save_conversation(self, messages):
        now = datetime.now()
        num = self.index["next_conversation"]
        filename = f"{self.convo_prefix}_Convo{num}.json"
        save_json(os.path.join(self.convo_dir, filename), {
            "entry_number": num,
            "date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S"),
            "message_count": len(messages), "messages": messages
        })
        self.index["next_conversation"] = num + 1
        self.index["total_conversations"] += 1
        self.index["total_messages"] += len(messages)
        self.index["last_interaction"] = now.isoformat()
        self._save_index()

    # ─── REFLECTIONS ───
    # Files: Diary_1.json (Abi), Notebook_1.json (David), Journal_1.json (Quinn)

    def save_journal_entry(self, reflection_data):
        now = datetime.now()
        num = self.index["next_journal_entry"]
        filename = f"{self.reflection_name}_{num}.json"
        save_json(os.path.join(self.journal_dir, filename), {
            "entry_number": num,
            "date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S"),
            **reflection_data
        })
        self.index["next_journal_entry"] = num + 1
        self.index["total_journal_entries"] += 1
        self._save_index()

    def get_recent_journal_entries(self, count=3):
        entries = []
        current = self.index["next_journal_entry"] - 1
        while current >= 1 and len(entries) < count:
            filename = f"{self.reflection_name}_{current}.json"
            data = load_json(os.path.join(self.journal_dir, filename))
            if data:
                entries.append(data)
            current -= 1
        return entries

    # ─── CONTEXT ───

    def build_context_summary(self):
        parts = []
        if self.facts:
            parts.append("Things I remember:")
            for cat, items in self.facts.items():
                for key, data in items.items():
                    parts.append(f"  - [{cat}] {key}: {data['value']}")
        if self.opinions:
            parts.append("\nMy current opinions:")
            for topic, data in self.opinions.items():
                parts.append(f"  - {topic}: {data['opinion']} (strength: {data['strength']})")
        strong_patterns = [p for p in self.patterns if p["confidence"] > 0.4]
        if strong_patterns:
            parts.append("\nPatterns I've noticed:")
            for p in strong_patterns[:10]:
                parts.append(f"  - {p['description']} (confidence: {p['confidence']:.1f})")
        for journal in self.get_recent_journal_entries(2):
            if "summary" in journal:
                parts.append(f"\nRecent reflection [{journal['date']}]: {journal['summary']}")
        parts.append(f"\nStats: {self.index['total_conversations']} conversations, {self.index['total_messages']} messages")
        return "\n".join(parts) if parts else "I don't know anything about you yet. This is our first interaction."

    def get_stats(self):
        return self.index

    def get_hours_since_last_chat(self):
        last = self.index.get("last_interaction")
        if last:
            return (datetime.now() - datetime.fromisoformat(last)).total_seconds() / 3600
        return None

    # ─── RESETS ───

    def wipe_memory(self):
        """Erase all user knowledge — facts, opinions, patterns, conversations, reflections.
        Like amnesia. The sibling is still 'them' but doesn't remember the user."""
        import shutil
        self.facts = {}
        self.opinions = {}
        self.events = []
        self.patterns = []
        self.index = {
            "next_conversation": 1, "next_journal_entry": 1,
            "total_messages": 0, "total_conversations": 0,
            "total_journal_entries": 0,
            "first_interaction": datetime.now().isoformat(),
            "last_interaction": None
        }
        self._save("facts.json", self.facts)
        self._save("opinions.json", self.opinions)
        self._save("events.json", self.events)
        self._save("patterns.json", self.patterns)
        self._save_index()
        # Delete conversation and reflection files
        for d in [self.convo_dir, self.journal_dir]:
            for f in os.listdir(d):
                os.remove(os.path.join(d, f))
