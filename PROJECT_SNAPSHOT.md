# Triur.ai — Project Snapshot

> Reference document for AI sessions. Last updated: v0.1.0 (March 2026)

## Tech Stack

| Layer | Technology |
|---|---|
| Desktop shell | Tauri v2 (Rust) — frameless window, NSIS/MSI/DMG installers |
| Frontend | HTML + CSS + vanilla JS — glassmorphism bento layout, canvas sprites |
| Backend | Python 3.11 + Flask — REST API on localhost:5000 |
| LLM | Ollama (dolphin-llama3:8b) — local inference at localhost:11434 |
| Build (Python) | PyInstaller — onedir mode, bundles into `triur-brain/` |
| Build (App) | Tauri CLI via `npm run build` |
| CI/CD | GitHub Actions — auto-build Win + Mac, auto-release on version tags |
| World APIs | wttr.in (weather), BBC RSS (news), DuckDuckGo Instant (search) — all free |
| GIF API | GIPHY (key in renderer.js) |
| Sprites | Craftpix.net Fantasy Chibi Characters — 6 characters, 6 animations each |

---

## Project Structure

```
Triur_ai/
├── .claude/CLAUDE.md              # Project context for AI sessions
├── .github/workflows/
│   ├── build.yml                  # CI: Python→PyInstaller→Node→Rust→Tauri (Win+Mac)
│   └── python-package.yml         # CI: lint + test (Python 3.9-3.11)
├── app/
│   ├── package.json               # Node scripts: dev, build, start (Tauri)
│   ├── src-tauri/
│   │   ├── Cargo.toml             # tauri 2, tauri-plugin-shell 2, serde
│   │   ├── tauri.conf.json        # Window config, CSP, resource bundling
│   │   ├── src/main.rs            # Spawn Python server, window controls (minimize/maximize/close)
│   │   └── icons/                 # Platform icons (png, ico, icns)
│   └── web/
│       ├── index.html             # Bento layout, boot screen, welcome screen
│       ├── renderer.js            # All UI logic (~1569 lines)
│       ├── styles.css             # Two-layer CSS system (~1864 lines)
│       └── assets/
│           ├── icon.ico / icon.png
│           └── sprites/           # 6 character folders (Enchantress, Knight, etc.)
├── build/
│   ├── triur.spec                 # PyInstaller spec (onedir, entry: src/server.py)
│   ├── build-backend.bat/.sh      # PyInstaller build scripts
│   └── prepare-python.bat/.sh     # Embedded Python download scripts
├── config/
│   ├── personality.json           # Abi — warm rose (#c4687a)
│   ├── personality_david.json     # David — slate blue (#5b8db8)
│   ├── personality_quinn.json     # Quinn (they/them) — lavender (#8b6ba8)
│   ├── relationship.json          # Relationship schema definition
│   └── user_profile.json          # User's saved profile + settings
├── data/                          # Runtime data (gitignored)
│   ├── {abi,david,quinn}/
│   │   ├── memory/                # user_facts, user_opinions, user_patterns, events, emotional_state, relationship_state, shared_facts, index
│   │   ├── conversations/         # {A,D,Q}_Convo{N}.json
│   │   ├── journal/               # {Diary,Notebook,Journal}_{N}.json
│   │   └── personality/           # my_facts, my_opinions, my_patterns, evolved_traits, timeline
│   ├── gossip/                    # {sibling}_outbox.json, {sibling}_inbox.json
│   ├── sibling_relationships/     # {from}_about_{to}.json
│   └── world_cache/               # world_state.json
├── src/
│   ├── server.py                  # Flask API server (all endpoints)
│   ├── brain.py                   # Core AI engine (system prompt, LLM calls, post-processing)
│   ├── memory.py                  # UserMemory + SelfMemory + legacy Memory wrapper
│   ├── emotions.py                # 13-dimension emotional state with decay + weather/time effects
│   ├── relationship.py            # 5-metric relationship with grace period + growth stages
│   ├── gossip.py                  # Inter-sibling messaging (casual gossip + flagged events)
│   ├── sibling_relationship.py    # How siblings feel about each other (bond floor: 0.5)
│   ├── world.py                   # Weather, news, search — all free APIs
│   ├── actions.py                 # PC actions: SAFE/DANGEROUS/BLOCKED tiers
│   ├── chat.py                    # Terminal chat interface (legacy, pre-Tauri)
│   ├── utils.py                   # Path resolution, JSON helpers, PyInstaller detection
│   └── test_core.py               # Basic import tests
├── requirements.txt               # flask, flask-cors, requests, ollama, feedparser, pyinstaller
├── README.md                      # Public-facing docs (Tauri, correct structure, roadmap)
├── start.bat / start.sh           # Dev launchers
└── PROJECT_SNAPSHOT.md            # This file
```

---

## Python Backend (src/)

### server.py — Flask API Server
Bridges Tauri frontend to Python brain. Boots all 3 siblings at startup (~40s). Manages active sibling switching, nudge cooldowns, and session state.

### brain.py — Core AI Engine
One `Brain` instance per sibling. Builds dynamic system prompts from personality + memory + emotions + relationship + gossip + world context. Post-processing after every message: memory extraction, emotion evaluation, relationship adjustment, gossip evaluation, and natural personality evolution. Key constants:
- `ANTI_AI_RULES` — injected into every prompt, prevents AI patterns + enforces consent/boundaries
- `PERSONALITY_FILES` — maps sibling_id to config filename
- Temperature: 0.8 for chat, 0.1-0.3 for analysis tasks

### memory.py — Long-Term Memory
Two separate stores per sibling:
- **UserMemory** — facts/opinions/patterns the user shared, conversations, journal entries, shared facts from siblings
- **SelfMemory** — the AI's own facts, opinions, behavior patterns, evolved traits, timeline milestones

### emotions.py — Emotional State
13 emotions (happiness, curiosity, frustration, amusement, boredom, affection, anxiety, pride, sadness, excitement, annoyance, confidence, loneliness) each 0.0-1.0. Decays toward resting values. Affected by time-of-day, hours away, and weather. Behavioral cues injected into prompt based on thresholds.

### relationship.py — User Relationship
5 metrics: trust, fondness, respect, comfort, annoyance. 15-interaction grace period (80% dampening on negatives). Max 0.03 adjustment per interaction. Growth stages: stranger → acquaintance → friend → close_friend → best_friend. Each stage unlocks behaviors (initiating conversations, sharing personal info, etc.).

### gossip.py — Sibling Communication
Two message types:
- **Casual gossip** — interesting info shared between sessions
- **Flagged events** — significant interactions (user_rude, user_kind, user_manipulative, etc.) that carry relationship metric impacts to other siblings

### sibling_relationship.py — Inter-Sibling Bonds
Tracks bond, trust, irritation, worry, pride between each sibling pair. Bond floor at 0.5 (always family). Reset events trigger worry in other siblings.

### world.py — World Awareness
Free APIs only: wttr.in for weather (cached 60min), BBC RSS for news (cached 60min), DuckDuckGo Instant Answer for search.

### actions.py — PC Actions
Three safety tiers: SAFE (auto-run: open_app, open_url, search_files, etc.), DANGEROUS (ask permission: run_command, delete_file, etc.), BLOCKED (never: format_drive, modify_registry, etc.).

### utils.py — Shared Utilities
Path resolution with PyInstaller detection (`sys.frozen` → `sys._MEIPASS` for `_internal/config/`). JSON load/save helpers. Per-sibling naming conventions and data directory creation.

---

## API Endpoints (server.py)

| Method | Path | Purpose |
|---|---|---|
| POST | /api/chat | Send message to active sibling, get response + state |
| GET | /api/status | Full state: emotions, relationship, memory stats, time |
| GET | /api/memory | Facts, opinions, fact count, context summary |
| GET | /api/personality | Self-memory: my_facts, my_opinions, patterns, evolved traits, timeline |
| POST | /api/save | Save session (conversation + journal reflection) |
| GET | /api/greeting | Relationship-aware greeting based on mood/time/history |
| POST | /api/react | Sibling evaluates emoji reaction to a message |
| GET/POST | /api/profile | Get/save user profile |
| POST | /api/switch | Switch active sibling (saves current session first) |
| GET | /api/siblings | Info about all siblings (for switcher UI) |
| GET | /api/sibling/status | Daily status message for hover tooltip |
| POST | /api/first-message | First-ever message to new user after onboarding |
| GET | /api/nudge | Check if sibling wants to say something unprompted |
| POST | /api/reset | Reset sibling: memory, personality, or full |
| POST | /api/action/classify | Safety classification for a PC action |
| POST | /api/action/execute | Execute a PC action (blocked = 403) |
| GET | /api/ping | Health check |
| GET | /api/world | Weather + news headlines |
| GET | /api/sibling-relationships | Inter-sibling relationship states |

---

## Frontend (app/web/)

### renderer.js — UI Logic (~1569 lines)
- **Boot sequence** — polls /api/ping up to 90s with progressive status messages, detects first-run
- **Welcome/onboarding screen** — sibling cards, profile setup, shows only on first launch
- **Chat** — sends to /api/chat, handles action mode `[ACTION:type:{params}]` parsing
- **Sibling switching** — saves session, clears chat, fetches new greeting, applies accent theme
- **Emoji reactions** — user click + sibling auto-reaction via /api/react
- **Nudge polling** — checks /api/nudge every 45-90s after 120-240s initial delay
- **Sprite controller** — canvas-based sprite sheet animation, event-driven reactions (thinking/response/emotion), click/drag interactions
- **Settings modal** — profile form, theme modes (system/light/dark), colorblind toggles, per-sibling reset + sprite switch
- **GIF picker** — GIPHY integration (trending + search)
- **Bottom tabs** — opinions, howIRoll, growth timeline dropdowns from /api/personality
- **Memory panel** — facts + opinions with junk filtering (< 3 chars, > 120 chars, all-punctuation)

### styles.css — Two-Layer Color System (~1864 lines)
- **Layer 1 (Base UI)** — never changes per sibling. Glass panels, backgrounds, text colors, borders
- **Layer 2 (Sibling Accent)** — swaps via `[data-sibling]` attribute. Only affects: name label, send button, mood underline, feeling bars, avatar ring, status dot
- **Settings modal** — NEVER inherits sibling accent colors
- **Sibling palettes:** Abi = #c4687a (warm rose), David = #5b8db8 (slate blue), Quinn = #8b6ba8 (lavender)
- **Theme modes:** `[data-theme="dark"]` + `body.nighttime` (legacy). System mode = auto by time-of-day
- **Colorblind:** protanopia, deuteranopia, tritanopia CSS class overrides
- **Accessibility:** WCAG high contrast media query, prefers-reduced-motion

---

## Tauri Shell (app/src-tauri/)

### main.rs
- `get_repo_root()` — dev mode path resolution (4 ancestors up from exe)
- `get_bundle_dir()` — production path resolution (parent of exe)
- `start_python_server()` — dev: `python src/server.py`; production: `triur-brain/triur-brain.exe` from bundle dir
- IPC commands: `minimize_window`, `maximize_window`, `close_window`

### tauri.conf.json
- Resources: `{"../../dist/triur-brain/": "triur-brain"}` — copies PyInstaller output into app bundle
- Window: 1100x750, min 800x600, frameless, decorations off
- Identifier: `com.ampickettdesign.triur`

---

## Build System

### PyInstaller (build/triur.spec)
- **Mode:** onedir (COLLECT, not onefile)
- **Entry:** `src/server.py`
- **Bundles:** `config/` → `_internal/config/`
- **Output:** `dist/triur-brain/triur-brain.exe` + `dist/triur-brain/_internal/`
- **Excludes:** tkinter, matplotlib, numpy, pandas, scipy, PIL, cv2

### CI/CD (.github/workflows/build.yml)
- **Triggers:** push to main, version tags (v*), manual dispatch
- **Build order:** Python → PyInstaller → Node → Rust → Tauri
- **Caching:** pip packages + Rust target/cargo (both platforms)
- **Artifacts:** Windows (NSIS .exe + MSI), Mac (DMG) — 30-day retention
- **Release job:** downloads both artifacts on v* tags, creates GitHub Release with auto-generated notes

### Installed App Structure (Windows)
```
C:\Users\{user}\AppData\Local\Triur.ai\
├── triur-ai.exe           # Tauri app
├── triur-brain\            # PyInstaller bundle (resource)
│   ├── triur-brain.exe
│   └── _internal\          # Python runtime + bundled data
│       ├── config\         # personality.json, etc.
│       ├── python311.dll
│       └── ...
└── uninstall.exe
```

---

## Personality Configs

Each sibling has a JSON config with: name, version, seed_trait, core_traits (10-12 traits 0.0-1.0), values, communication_style (default_tone, avoids, prefers), emotional_range, conversation_patterns (silence_comfort, double_texts), quirks, flaws, sibling_dynamics, growth_stages (stranger → best_friend with behavior/humor/honesty/initiates/shares_personal/unlocks), and system_prompt_base.

| Sibling | Seed Trait | Tone | Silence Comfort | Double Texts |
|---|---|---|---|---|
| Abi (Abigail) | curiosity | confident/funny/unfiltered | 0.4 | absolutely |
| David | warmth | relaxed/warm/easygoing | 0.9 | sometimes |
| Quinn (they/them) | groundedness | direct/grounded/quietly warm | 0.6 | sometimes |

---

## Key Design Decisions

1. **Uncensored model (dolphin-llama3)** — no corporate filter, but siblings enforce their own boundaries via ANTI_AI_RULES
2. **Grace period (15 interactions)** — prevents snap negative judgments from tech-habit communication style
3. **Gossip system** — siblings share info AND emotional reactions to user behavior across sessions
4. **Natural evolution** — personality traits shift max 0.005 per 20 messages; opinions form after 3+ expressions
5. **Two-layer CSS** — base UI is constant, only accent colors change per sibling; settings modal exempt
6. **PyInstaller onedir** — needed for Tauri resource bundling (Tauri can't bundle single-file executables as directories)
7. **No Rust locally** — Ashley doesn't have Rust installed; builds only happen in CI via GitHub Actions
