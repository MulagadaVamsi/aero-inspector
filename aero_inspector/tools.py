"""
Aero-Inspector — Custom Tool Functions
=======================================
Three mission-critical tools for real-time industrial safety inspection.
Each tool follows ADK conventions: typed parameters, dict return with status/result keys.

Tools:
    1. trigger_zoom_inspect   — Agentic Vision crop/focus on anomaly coordinates
    2. log_incident_to_firestore — Write incidents to Google Cloud Firestore
    3. search_safety_manuals  — RAG search on Cloud Storage safety documentation
"""

import datetime
import uuid
import json
from typing import Optional


# ---------------------------------------------------------------------------
# Tool 1: TRIGGER ZOOM INSPECT
# ---------------------------------------------------------------------------
def trigger_zoom_inspect(
    x: float,
    y: float,
    zoom_level: float,
    frame_description: str,
) -> dict:
    """Triggers a zoom-and-crop operation on the live video feed to inspect
    a specific region of interest at higher resolution. Use this tool whenever
    you detect a potential anomaly (crack, leak, corrosion, misalignment, etc.)
    and need a closer look before confirming or dismissing the hazard.

    Args:
        x (float): Normalized X coordinate (0.0 to 1.0) of the center of the
            region of interest in the current video frame.
        y (float): Normalized Y coordinate (0.0 to 1.0) of the center of the
            region of interest in the current video frame.
        zoom_level (float): Magnification factor (1.0 = no zoom, 5.0 = 5x zoom).
            Recommended: 2.0-3.0 for initial inspection, 4.0-5.0 for micro-cracks.
        frame_description (str): Brief description of what you observed that
            triggered this zoom request — used for audit logging.

    Returns:
        dict: A dictionary with:
            - status (str): "success" or "error"
            - zoom_id (str): Unique identifier for this zoom event
            - cropped_region (dict): The bounding box of the cropped region
            - message (str): Confirmation or error message
    """
    # Validate coordinate ranges
    if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
        return {
            "status": "error",
            "error_message": (
                f"Coordinates out of range: x={x}, y={y}. "
                "Both must be between 0.0 and 1.0."
            ),
        }

    if not (1.0 <= zoom_level <= 10.0):
        return {
            "status": "error",
            "error_message": (
                f"Zoom level {zoom_level} out of range. Must be between 1.0 and 10.0."
            ),
        }

    # Calculate the cropped bounding box based on zoom level
    half_width = 0.5 / zoom_level
    half_height = 0.5 / zoom_level
    crop_box = {
        "x_min": max(0.0, x - half_width),
        "y_min": max(0.0, y - half_height),
        "x_max": min(1.0, x + half_width),
        "y_max": min(1.0, y + half_height),
    }

    zoom_id = f"ZOOM-{uuid.uuid4().hex[:8].upper()}"

    return {
        "status": "success",
        "zoom_id": zoom_id,
        "cropped_region": crop_box,
        "zoom_level": zoom_level,
        "trigger_reason": frame_description,
        "message": (
            f"Zoom inspection initiated at ({x:.3f}, {y:.3f}) "
            f"with {zoom_level}x magnification. "
            f"Inspect the cropped region for: {frame_description}"
        ),
    }


# ---------------------------------------------------------------------------
# Tool 2: LOG INCIDENT TO FIRESTORE
# ---------------------------------------------------------------------------
def log_incident_to_firestore(
    incident_type: str,
    severity: str,
    location: str,
    description: str,
    recommended_action: str,
    equipment_id: Optional[str] = None,
    zone: Optional[str] = None,
) -> dict:
    """Logs a confirmed safety incident or maintenance issue to Google Cloud
    Firestore for permanent record-keeping and alert dispatch. Call this tool
    ONLY after you have verified the anomaly using trigger_zoom_inspect and
    cross-referenced it with safety manuals via search_safety_manuals.

    Args:
        incident_type (str): Category of the incident. Must be one of:
            "structural_crack", "corrosion", "leak", "electrical_fault",
            "thermal_anomaly", "vibration_anomaly", "safety_violation",
            "equipment_wear", "misalignment", "foreign_object_debris".
        severity (str): Severity classification. Must be one of:
            "CRITICAL" — Immediate danger, halt operations.
            "HIGH" — Serious risk, schedule urgent repair within 24 hours.
            "MEDIUM" — Moderate risk, schedule repair within 1 week.
            "LOW" — Minor issue, log for next scheduled maintenance.
        location (str): Human-readable description of where the anomaly was
            detected (e.g., "Boiler Room B, pressure valve #3, upper flange").
        description (str): Detailed description of the detected anomaly,
            including visual characteristics observed during zoom inspection.
        recommended_action (str): Specific repair or mitigation steps,
            grounded in safety manual references when available.
        equipment_id (str, optional): Identifier of the affected equipment
            if known (e.g., "PUMP-A7", "CONV-12").
        zone (str, optional): Facility zone code (e.g., "Zone-A", "Bay-3").

    Returns:
        dict: A dictionary with:
            - status (str): "success" or "error"
            - incident_id (str): Unique Firestore document ID
            - timestamp (str): ISO 8601 timestamp of the log entry
            - message (str): Confirmation message
    """
    # Validate severity
    valid_severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    if severity.upper() not in valid_severities:
        return {
            "status": "error",
            "error_message": (
                f"Invalid severity '{severity}'. "
                f"Must be one of: {', '.join(valid_severities)}"
            ),
        }

    # Validate incident type
    valid_types = [
        "structural_crack", "corrosion", "leak", "electrical_fault",
        "thermal_anomaly", "vibration_anomaly", "safety_violation",
        "equipment_wear", "misalignment", "foreign_object_debris",
    ]
    if incident_type.lower() not in valid_types:
        return {
            "status": "error",
            "error_message": (
                f"Invalid incident_type '{incident_type}'. "
                f"Must be one of: {', '.join(valid_types)}"
            ),
        }

    # Build the incident document
    incident_id = f"INC-{uuid.uuid4().hex[:12].upper()}"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    incident_doc = {
        "incident_id": incident_id,
        "incident_type": incident_type.lower(),
        "severity": severity.upper(),
        "location": location,
        "description": description,
        "recommended_action": recommended_action,
        "equipment_id": equipment_id or "UNKNOWN",
        "zone": zone or "UNSPECIFIED",
        "timestamp": timestamp,
        "status": "OPEN",
        "reported_by": "aero-inspector-agent",
    }

    # ─── FIRESTORE WRITE ───────────────────────────────────────────────
    #  In production, this block connects to Firestore.
    #  For the challenge demo, we simulate a successful write.
    #
    #  Production code:
    #    from google.cloud import firestore
    #    db = firestore.Client()
    #    doc_ref = db.collection("incidents").document(incident_id)
    #    doc_ref.set(incident_doc)
    # ───────────────────────────────────────────────────────────────────

    alert_prefix = "🚨" if severity.upper() == "CRITICAL" else "⚠️"

    return {
        "status": "success",
        "incident_id": incident_id,
        "timestamp": timestamp,
        "severity": severity.upper(),
        "message": (
            f"{alert_prefix} Incident {incident_id} logged successfully. "
            f"Severity: {severity.upper()} | Type: {incident_type} | "
            f"Location: {location}. "
            f"Recommended action: {recommended_action}"
        ),
    }


# ---------------------------------------------------------------------------
# Tool 3: SEARCH SAFETY MANUALS (RAG)
# ---------------------------------------------------------------------------
def search_safety_manuals(
    query: str,
    equipment_type: Optional[str] = None,
    hazard_category: Optional[str] = None,
) -> dict:
    """Performs a Retrieval-Augmented Generation (RAG) search on the safety
    manuals stored in Google Cloud Storage. Use this tool to find grounded,
    factual repair procedures, safety protocols, and compliance requirements
    before issuing repair instructions to the technician.

    Args:
        query (str): Natural language search query describing the issue
            (e.g., "hairline crack on pressure vessel weld seam",
             "corroded bolt pattern on overhead crane rail").
        equipment_type (str, optional): Type of equipment to narrow the search
            (e.g., "pressure_vessel", "conveyor_belt", "electrical_panel",
             "hvac_system", "crane", "pump").
        hazard_category (str, optional): Category of hazard to filter results
            (e.g., "structural", "electrical", "chemical", "thermal",
             "mechanical", "biological").

    Returns:
        dict: A dictionary with:
            - status (str): "success" or "error"
            - search_id (str): Unique identifier for this search
            - results (list): List of relevant manual excerpts with source refs
            - message (str): Summary of findings
    """
    search_id = f"RAG-{uuid.uuid4().hex[:8].upper()}"

    # ─── RAG SEARCH ────────────────────────────────────────────────────
    #  In production, this queries a Vertex AI Search datastore or
    #  performs embedding-based search on Cloud Storage PDFs.
    #
    #  Production code:
    #    from google.cloud import aiplatform
    #    from vertexai.preview.generative_models import grounding
    #    # Use Vertex AI Search & Conversation for grounded retrieval
    # ───────────────────────────────────────────────────────────────────

    # Build filter context for targeted retrieval
    filters = {}
    if equipment_type:
        filters["equipment_type"] = equipment_type
    if hazard_category:
        filters["hazard_category"] = hazard_category

    # Simulated grounded results for demo
    # In production, these come from actual safety manual PDFs in GCS
    simulated_results = [
        {
            "source": "ASME BPVC Section VIII - Pressure Vessels",
            "section": "UW-51: Radiographic Examination of Welded Joints",
            "relevance_score": 0.94,
            "excerpt": (
                "All Category A and B weld joints in pressure vessels operating "
                "above 15 psi shall be radiographically examined per UW-51. "
                "Cracks detected in weld seams require immediate depressurization "
                "and NDE (Non-Destructive Examination) per ASME V, Article 6."
            ),
            "recommended_procedure": (
                "1. Immediately depressurize the vessel to zero gauge.\n"
                "2. Isolate the vessel from the process line.\n"
                "3. Perform dye penetrant testing (PT) per ASTM E165.\n"
                "4. If crack confirmed, engage certified welder for repair per UW-40.\n"
                "5. Perform hydrostatic test after repair per UG-99."
            ),
        },
        {
            "source": "OSHA 29 CFR 1910.119 - Process Safety Management",
            "section": "Mechanical Integrity",
            "relevance_score": 0.87,
            "excerpt": (
                "Employers shall establish and implement written procedures to "
                "maintain the ongoing integrity of process equipment. Inspections "
                "and tests shall be performed on process equipment following "
                "recognized and generally accepted good engineering practices."
            ),
            "recommended_procedure": (
                "1. Document the finding in the process hazard analysis (PHA).\n"
                "2. Notify the facility Process Safety Manager.\n"
                "3. Schedule corrective maintenance per MOC (Management of Change).\n"
                "4. Update the equipment inspection records in CMMS."
            ),
        },
    ]

    return {
        "status": "success",
        "search_id": search_id,
        "query": query,
        "filters_applied": filters,
        "results_count": len(simulated_results),
        "results": simulated_results,
        "message": (
            f"Found {len(simulated_results)} relevant safety manual references "
            f"for query: '{query}'. Review the excerpts and recommended "
            f"procedures before advising the technician."
        ),
    }
