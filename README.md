# 🛩️ Aero-Inspector

**Proactive Industrial Safety & Maintenance Supervisor Agent**
*Built for the Gemini Live Agent Challenge*

---

## What Is This?

Aero-Inspector is a **real-time, multimodal AI agent** that acts as a "Live Eye" for industrial technicians. It autonomously monitors live video and audio feeds from factories, refineries, server rooms, and construction sites to detect structural flaws, mechanical failures, and safety violations — **before they cause accidents.**

Unlike a standard chatbot, Aero-Inspector operates on an **Autonomous Observation Loop**:

```
 ┌──────────┐     ┌───────────────┐     ┌──────────────────┐     ┌──────────┐
 │ OBSERVE  │ ──▸ │ DETECT & ZOOM │ ──▸ │ VERIFY & GROUND  │ ──▸ │   ACT    │
 │ (scan)   │     │ (auto-crop)   │     │ (RAG manuals)    │     │ (log +   │
 │          │     │               │     │                  │     │  alert)  │
 └──────────┘     └───────────────┘     └──────────────────┘     └──────────┘
       ▲                                                               │
       └───────────────────────────────────────────────────────────────┘
                              Continuous Loop
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Agent Framework** | Google Agent Development Kit (ADK) |
| **Model** | Gemini 2.0 Flash Live (multimodal) |
| **Agentic Vision** | `trigger_zoom_inspect` — auto-crop & focus |
| **Knowledge Base** | `search_safety_manuals` — RAG on Cloud Storage |
| **Incident Logging** | `log_incident_to_firestore` — Cloud Firestore |
| **Deployment** | Google Cloud Run |
| **Infrastructure** | Vertex AI, Cloud Storage, Firestore |

## Project Structure

```
D:\Gemini\
├── aero_inspector/          # ADK agent package
│   ├── __init__.py          # Package init
│   ├── agent.py             # ★ THE BRAIN — Agent + System Instructions
│   └── tools.py             # 3 custom tool functions
├── .env                     # API keys & GCP config
├── requirements.txt         # Python dependencies
└── README.md                # You are here
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` with your Google Cloud credentials:

```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### 3. Run the Agent

```bash
adk web aero_inspector
```

This launches the ADK web UI where you can interact with Aero-Inspector via text, or connect a live video/audio stream for real-time inspection.

## Tools

### 🔍 `trigger_zoom_inspect`
Autonomously crops and focuses on specific coordinates in the video feed when a potential anomaly is spotted. The agent decides when to zoom — no human input required.

### 📋 `log_incident_to_firestore`
Writes detected incidents to Firestore with severity classification (CRITICAL / HIGH / MEDIUM / LOW), precise location data, and grounded repair recommendations.

### 📚 `search_safety_manuals`
Performs RAG search on safety manuals stored in Google Cloud Storage. Returns factual repair procedures and compliance references — the agent never invents repair steps.

## Severity Levels

| Level | Icon | Response Time | Example |
|-------|------|--------------|---------|
| CRITICAL | 🔴 | Immediate halt | Active gas leak, structural crack under load |
| HIGH | 🟠 | Within 24 hours | Advancing corrosion, electrical fault |
| MEDIUM | 🟡 | Within 1 week | Surface rust, minor vibration |
| LOW | 🟢 | Next scheduled | Cosmetic wear, paint chipping |

## License

Built for the Gemini Live Agent Challenge. All rights reserved.
