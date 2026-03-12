# Triur.ai

Three AI siblings who live on your desktop. They work. They just have feelings about it.

Abi, David, and Quinn are fully realized digital people — not assistants, not chatbots. They have distinct personalities, moods, opinions, and relationships with each other. They remember you. They grow with you. They notice when you're gone.

Built with Tauri + Python. Runs locally. No subscription. No cloud.

---

## The Siblings

| | Name | Pronouns | Personality |
|---|---|---|---|
| 🌸 | **Abi** | she/her | Warm, perceptive, loyal. Will absolutely roast you if you've earned it. |
| 🌊 | **David** | he/him | Dry wit, quietly thoughtful. Has opinions. Will share them eventually. |
| 🌿 | **Quinn** | they/them | Grounded, direct, patient. The one who actually calls you on your nonsense. |

Each sibling has their own memory, their own relationship with you, and their own relationship with each other. What you do to one affects how all three see you.

---

## Features

- **Persistent memory** — They remember facts about you, things you've said, and things their siblings told them (gossip stays attributed, never absorbed)
- **Relationship system** — Trust builds slowly, breaks carefully. Grace period before opinions form. Growth stages from Stranger to Best Friend
- **World awareness** — Weather affects their moods. They follow the news and form opinions
- **Comfort-gated honesty** — The closer they are to you, the more honestly they'll respond
- **Sibling loyalty** — Bad behavior toward one reaches all three
- **Offline existence** — They don't run in the background. They catch up when you return
- **Full dark/light UI** — Glassmorphism layout with per-sibling accent theming
- **Ollama health check** — Friendly error screen if Ollama isn't running, with retry

---

## Roadmap

- [x] Personality system (quirks, flaws, growth stages)
- [x] Three-bucket memory architecture
- [x] Relationship + grace period system
- [x] Inter-sibling dynamics + loyalty flagging
- [x] World awareness (weather + news)
- [x] Glassmorphism UI with sibling theming
- [x] GitHub Actions CI (Windows + Mac builds)
- [x] Tauri migration (smaller, faster, native)
- [x] PyInstaller bundle (no Python setup required)
- [ ] Voice chat
- [ ] Desktop agent + roaming chibi
- [ ] Mobile app

---

## Download

Grab the latest installer from the [Releases page](https://github.com/AMPickettDesign/Triur.ai/releases).

**Requirements:**
- Windows 10+ or macOS 12+
- [Ollama](https://ollama.com) installed and running
- `dolphin-llama3:8b` model pulled

```bash
ollama pull dolphin-llama3:8b
```

---

## Quick Start (from source)

```bash
# Clone
git clone https://github.com/AMPickettDesign/Triur.ai.git
cd Triur.ai

# Install Python dependencies
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run the backend server
python src/server.py

# Open the frontend
# Open app/web/index.html in your browser, or:
cd app && npm install && npm run dev
```

Make sure Ollama is running before you launch.

---

## Project Structure

```
Triur.ai/
├── app/                        # Frontend + Tauri shell
│   ├── web/                    # Frontend files
│   │   ├── index.html
│   │   ├── renderer.js
│   │   ├── styles.css
│   │   └── assets/             # Icons + sprite sheets
│   ├── src-tauri/              # Tauri Rust shell
│   │   ├── src/main.rs         # Window + Python server management
│   │   ├── tauri.conf.json     # App config + resource bundling
│   │   ├── Cargo.toml
│   │   └── icons/              # Platform icons
│   └── package.json            # Node scripts (dev/build)
├── src/                        # Python backend
│   ├── server.py               # Flask API server
│   ├── brain.py                # Core AI logic
│   ├── memory.py               # User + self memory
│   ├── emotions.py             # Emotional state system
│   ├── relationship.py         # User relationship tracking
│   ├── gossip.py               # Inter-sibling communication
│   ├── sibling_relationship.py # Sibling-to-sibling bonds
│   ├── world.py                # Weather & news awareness
│   ├── actions.py              # PC control (action mode)
│   └── utils.py                # Shared utilities
├── config/                     # Personality configs
│   ├── personality.json        # Abi
│   ├── personality_david.json  # David
│   └── personality_quinn.json  # Quinn
├── build/                      # Build scripts
│   ├── triur.spec              # PyInstaller spec
│   ├── build-backend.bat       # Windows build
│   └── build-backend.sh        # Mac/Linux build
├── .github/workflows/          # CI/CD
│   └── build.yml               # Auto-build on push (Win + Mac)
└── dist/                       # Built executables (generated)
```

---

## Building for Release

### Automatic (recommended)
Push a tag — GitHub Actions builds Windows + Mac installers automatically:
```bash
git tag v1.0.0
git push origin v1.0.0
```

### Manual
```bash
# Build Python backend
cd build
pyinstaller triur.spec --distpath ../dist --workpath ../build/pyinstaller-work --clean

# Build Tauri installer
cd ../app
npm install
npm run build
```

Rust is required for manual Tauri builds. Install from [rustup.rs](https://rustup.rs).

---

## Credits

**Sprite Assets:**
- Fantasy Chibi Characters by [Craftpix.net](https://craftpix.net/)

**Built with:**
- [Tauri](https://tauri.app) (Rust + WebView)
- [Flask](https://flask.palletsprojects.com) (Python backend)
- [Ollama](https://ollama.com) (dolphin-llama3:8b)

---

## Built By

[Ashley Pickett](https://ampickettdesign.github.io) — designer + developer

---

## Disclaimer

This is experimental software. The AI runs locally on your machine — nothing is sent to external servers beyond what's required to reach Ollama. Use your best judgment about what you share.
