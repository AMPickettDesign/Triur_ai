"""
Sibling AI — Gossip System
Siblings share info with each other between sessions.
Not everything — just what they'd naturally mention.
Info spreads with a delay and gets filtered through each sibling's personality.
"""

import os
from datetime import datetime
from utils import DATA_DIR, load_json, save_json

GOSSIP_DIR = os.path.join(DATA_DIR, "gossip")
os.makedirs(GOSSIP_DIR, exist_ok=True)

SIBLINGS = ["abi", "david", "quinn"]


def get_outbox(sibling_id):
    """Get messages a sibling wants to share with others."""
    return load_json(os.path.join(GOSSIP_DIR, f"{sibling_id}_outbox.json"), [])


def get_inbox(sibling_id):
    """Get messages other siblings have shared with this one."""
    return load_json(os.path.join(GOSSIP_DIR, f"{sibling_id}_inbox.json"), [])


def clear_inbox(sibling_id):
    """Mark all inbox messages as read."""
    inbox = get_inbox(sibling_id)
    for msg in inbox:
        msg["read"] = True
    save_json(os.path.join(GOSSIP_DIR, f"{sibling_id}_inbox.json"), inbox)


def send_gossip(from_id, message, importance=0.5, about_user=True):
    """
    A sibling shares something with their siblings.
    Only goes to the OTHER siblings, not back to self.
    """
    gossip = {
        "from": from_id,
        "message": message,
        "importance": importance,
        "about_user": about_user,
        "timestamp": datetime.now().isoformat(),
        "read": False
    }
    # Add to sender's outbox for record
    outbox = get_outbox(from_id)
    outbox.append(gossip)
    outbox = outbox[-100:]  # Cap
    save_json(os.path.join(GOSSIP_DIR, f"{from_id}_outbox.json"), outbox)

    # Deliver to other siblings' inboxes
    for sib in SIBLINGS:
        if sib != from_id:
            inbox = get_inbox(sib)
            inbox.append(gossip)
            inbox = inbox[-100:]  # Cap
            save_json(os.path.join(GOSSIP_DIR, f"{sib}_inbox.json"), inbox)


def get_unread_gossip(sibling_id):
    """Get gossip this sibling hasn't seen yet."""
    inbox = get_inbox(sibling_id)
    return [msg for msg in inbox if not msg.get("read", False)]


def build_gossip_context(sibling_id):
    """
    Build a text summary of gossip for the system prompt.
    This is how a sibling learns what their siblings told them.
    """
    unread = get_unread_gossip(sibling_id)
    if not unread:
        return ""

    parts = ["Things your siblings mentioned to you recently:"]
    for msg in unread[-10:]:  # Last 10 unread
        parts.append(f"  - {msg['from'].capitalize()} said: \"{msg['message']}\"")
    parts.append("(You can reference this naturally in conversation — don't announce it like a list.)")
    return "\n".join(parts)
