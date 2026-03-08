"""
Sibling AI — Relationship System
Tracks how a sibling feels about the user over time.
"""

import os
from datetime import datetime
from utils import load_json, save_json


class Relationship:
    """Manages a sibling's feelings toward the user."""

    OPINION_LABELS = [
        (0.8, "love"), (0.6, "like"), (0.4, "neutral"),
        (0.2, "dislike"), (0.0, "hostile")
    ]

    def __init__(self, memory_dir):
        self.filepath = os.path.join(memory_dir, "relationship_state.json")
        self.state = load_json(self.filepath) or {
            "trust": 0.5, "fondness": 0.5, "respect": 0.5,
            "comfort": 0.3, "annoyance": 0.0,
            "interaction_history": [],
            "last_interaction": None, "total_interactions": 0
        }

    def _save(self):
        save_json(self.filepath, self.state)

    @staticmethod
    def _clamp(v):
        return max(0.0, min(1.0, v))

    def adjust(self, metric, amount, reason=""):
        if metric in self.state and isinstance(self.state[metric], (int, float)):
            old = self.state[metric]
            self.state[metric] = self._clamp(old + amount)
            self.state["interaction_history"].append({
                "metric": metric, "old": round(old, 3),
                "new": round(self.state[metric], 3),
                "change": round(amount, 3), "reason": reason,
                "timestamp": datetime.now().isoformat()
            })
            self.state["interaction_history"] = self.state["interaction_history"][-200:]
            self._save()

    def record_interaction(self):
        self.state["total_interactions"] += 1
        self.state["last_interaction"] = datetime.now().isoformat()
        self.adjust("comfort", 0.005, "familiarity grows")
        if self.state["annoyance"] > 0:
            self.adjust("annoyance", -0.02, "cooling off")
        self._save()

    def get_overall_opinion(self):
        score = self._clamp(
            self.state["trust"] * 0.25 + self.state["fondness"] * 0.30 +
            self.state["respect"] * 0.25 + self.state["comfort"] * 0.10 -
            self.state["annoyance"] * 0.10
        )
        label = "hostile"
        for threshold, lbl in self.OPINION_LABELS:
            if score >= threshold:
                label = lbl
                break
        return {"score": round(score, 3), "label": label}

    def get_mood_context(self):
        opinion = self.get_overall_opinion()
        s = self.state
        guidance = {
            "love": "I genuinely care about this person. I'm warm, open, and protective.",
            "like": "I enjoy talking to this person. I'm friendly and engaged.",
            "neutral": "I don't have strong feelings yet. I'm professional but reserved.",
            "dislike": "I'm not a fan. I'm curt and do the minimum.",
            "hostile": "I really don't like this person. Cold and blunt."
        }
        return (
            f"My feelings about this person (overall: {opinion['label']}, score: {opinion['score']}):\n"
            f"  Trust: {s['trust']:.2f} | Fondness: {s['fondness']:.2f} | Respect: {s['respect']:.2f}\n"
            f"  Comfort: {s['comfort']:.2f} | Annoyance: {s['annoyance']:.2f}\n"
            f"  Total interactions: {s['total_interactions']}\n"
            f"  {guidance.get(opinion['label'], '')}"
        )

    def get_state(self): return self.state
