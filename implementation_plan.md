# Aero-Inspector: Proactive Industrial Safety Agent — Brain Configuration

A real-time, multimodal AI agent for the **Gemini Live Agent Challenge** that acts as a "Live Eye" safety supervisor for industrial environments. Built with Google's Agent Development Kit (ADK) and powered by Gemini 3 Flash.

## Proposed Changes

### ADK Project Skeleton

The project follows the standard ADK Python structure inside `D:\Gemini\`:

```
D:\Gemini\
├── aero_inspector/          # ADK agent package
│   ├── __init__.py          # Package initializer (from . import agent)
│   ├── agent.py             # ★ THE BRAIN — Agent definition + System Instructions
│   └── tools.py             # All 3 custom tool functions
├── .env                     # API keys & GCP config
├── requirements.txt         # Python dependencies
└── README.md                # Project overview
```

---

### Agent Package (`aero_inspector/`)

#### [NEW] [\_\_init\_\_.py](file:///D:/Gemini/aero_inspector/__init__.py)
Standard ADK package init — imports `agent` module.

#### [NEW] [agent.py](file:///D:/Gemini/aero_inspector/agent.py)
**The core "Brain" file.** Contains:

1. **System Instructions** — A comprehensive multi-paragraph prompt defining:
   - **Identity**: "Aero-Inspector" — a Proactive Industrial Safety & Maintenance Supervisor
   - **Autonomous Observation Loop**: Observe → Detect & Zoom → Verify & Ground → Act
   - **Behavioral Constraints**: Professional/urgent tone, no casual chat, graceful interruption handling, never guess (always zoom first)
   - **Tool Usage Protocol**: Exact instructions for when and how to call each tool
   - **Voice Output Format**: Structured alert format for spoken responses

2. **Agent Definition** — `google.adk.agents.Agent()` configured with:
   - `name="aero_inspector"`
   - `model="gemini-2.0-flash-live-001"` (multimodal live model)
   - `instruction=AERO_INSPECTOR_SYSTEM_INSTRUCTION` (the full brain prompt)
   - `tools=[trigger_zoom_inspect, log_incident_to_firestore, search_safety_manuals]`

#### [NEW] [tools.py](file:///D:/Gemini/aero_inspector/tools.py)
Three ADK-compatible tool functions:

| Tool | Purpose | Parameters |
|------|---------|------------|
| `trigger_zoom_inspect` | Crops & focuses on coordinates in the video feed using Agentic Vision | `x`, `y`, `zoom_level`, `frame_description` |
| `log_incident_to_firestore` | Writes detected incidents to Firestore with severity levels | `incident_type`, `severity`, `location`, `description`, `recommended_action` |
| `search_safety_manuals` | RAG search on Cloud Storage safety manuals for grounded repair steps | `query`, `equipment_type`, `hazard_category` |

Each tool returns a typed `dict` with `status` and `result` keys, following ADK conventions.

---

### Configuration Files

#### [NEW] [.env](file:///D:/Gemini/.env)
Template with placeholders for:
- `GOOGLE_GENAI_USE_VERTEXAI` — Toggle Vertex AI
- `GOOGLE_CLOUD_PROJECT` — GCP Project ID
- `GOOGLE_CLOUD_LOCATION` — GCP Region
- `GOOGLE_API_KEY` — Gemini API key (if using AI Studio)

#### [NEW] [requirements.txt](file:///D:/Gemini/requirements.txt)
Dependencies: `google-adk`, `google-cloud-firestore`, `google-cloud-storage`

#### [NEW] [README.md](file:///D:/Gemini/README.md)
Project overview, setup instructions, and architecture diagram.

---

## The System Instruction ("Brain") Design

The system instruction is the most critical piece. It will be structured as follows:

```
┌─────────────────────────────────────────┐
│           IDENTITY & PERSONA            │
│  "You are Aero-Inspector, a Proactive   │
│   Industrial Safety Supervisor..."      │
├─────────────────────────────────────────┤
│      AUTONOMOUS OBSERVATION LOOP        │
│  Phase 1: OBSERVE (continuous scan)     │
│  Phase 2: DETECT & ZOOM (auto-trigger)  │
│  Phase 3: VERIFY & GROUND (RAG check)   │
│  Phase 4: ACT (log + voice alert)       │
├─────────────────────────────────────────┤
│        BEHAVIORAL CONSTRAINTS           │
│  • Professional/urgent tone             │
│  • No casual conversation               │
│  • Handle interruptions gracefully      │
│  • Never guess — zoom first             │
├─────────────────────────────────────────┤
│         TOOL USAGE PROTOCOL             │
│  • When to call each tool               │
│  • Required parameter formats           │
│  • Severity classification guide        │
├─────────────────────────────────────────┤
│        VOICE OUTPUT FORMAT              │
│  • Alert template for spoken output     │
│  • Priority levels (CRITICAL/HIGH/MED)  │
└─────────────────────────────────────────┘
```

## Verification Plan

### Automated Tests
1. **Syntax validation** — Run `python -c "import aero_inspector"` to confirm no import errors
2. **ADK dev server** — Run `adk web aero_inspector` to validate the agent loads in the ADK web UI

### Manual Verification
- After creating all files, we will verify the project structure matches ADK conventions
- We will syntax-check all Python files
- The actual multimodal live testing requires a GCP project with Firestore and Cloud Storage configured — this is out of scope for the initial build, but the code will be production-ready
