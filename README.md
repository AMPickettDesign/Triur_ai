# Triur_ai

Three AI siblings with real personalities. They remember things, talk to each other, and reach out on their own.

---

## What is this?

Triur_ai (Gaelic for "three") gives you three AI companions:

- **Abi** — Sharp, direct, dry humor. Says what everyone's thinking.
- **David** — Steady, calm, protective. The one who actually shows up.
- **Quinn** — Chaotic, curious, texts at 3am with "okay hear me out."

They're not chatbots. They have memories, opinions, feelings, and they'll start conversations with you unprompted. They talk to each other about you too.

---

## Prerequisites

Before running, you need:

1. **Python 3.14+** — [python.org](https://www.python.org/)
2. **Node.js 18+** — [nodejs.org](https://nodejs.org/)
3. **Ollama** — [ollama.com](https://ollama.com/)
4. **Ollama model** — Run this command after installing Ollama:
   ```
   ollama pull dolphin-llama3:8b
   ```

---

## Quick Start

1. **Clone or download this repo**
2. **Install Python dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Install Node dependencies:**
   ```
   cd app
   npm install
   ```
4. **Run it:**
   ```
   start.bat
   ```

---

## First Run

On first launch, you'll see an onboarding screen. It asks about you (name, interests, etc.) so the siblings know who they're talking to. This makes conversations feel more real from the start.

You can pick which sibling to talk to, or let them decide.

---

## Features

- **Multi-sibling system** — Switch between Abi, David, and Quinn anytime
- **Real memory** — They remember what you tell them across sessions
- **Self-initiated messaging** — They reach out unprompted when you're quiet
- **Sibling gossip** — They talk to each other about you
- **Adaptive personality** — Their personalities evolve based on your interactions
- **Colorblind modes** — Protanopia, Deuteranopia, Tritanopia support
- **Day/night themes** — Auto-switches at 6am/6pm

---

## Troubleshooting

**"Can't connect to brain server"**
- Make sure Ollama is running: `ollama serve`
- Check the model is pulled: `ollama list`

**"Python not found"**
- Install Python from python.org (make sure to add to PATH)

**Electron won't start**
- Make sure you ran `npm install` in the `app` folder

---

## Credits

Built with:
- Electron
- Flask
- Ollama (dolphin-llama3:8b)
- Claude (Anthropic)

---

## Disclaimer

This is experimental software. The AI runs locally on your machine — nothing is sent to external servers. But use your best judgment about what you share.
