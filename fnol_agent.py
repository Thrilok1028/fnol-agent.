import json

MANDATORY_FIELDS = [
    "policy_number",
    "policyholder_name",
    "policy_effective_dates",
    "incident_date",
    "incident_time",
    "incident_location",
    "incident_description",
    "claimant",
    "third_parties",
    "contact_details",
    "asset_type",
    "asset_id",
    "estimated_damage",
    "claim_type",
    "attachments",
    "initial_estimate",
]


def extract_text_from_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_after_label(text: str, label: str, max_length: int = 60) -> str | None:
    idx = text.find(label)
    if idx == -1:
        return None
    start = idx + len(label)
    snippet = text[start : start + max_length]
    line = snippet.split("
")[0]
    return line.strip() or None


def parse_fields(text: str) -> dict:
    fields = {
        "policy_number": extract_after_label(text, "POLICY NUMBER:"),
        "policyholder_name": extract_after_label(text, "NAME OF INSURED"),
        "policy_effective_dates": None,  # not obvious on ACORD sample
        "incident_date": extract_after_label(text, "DATE OF LOSS"),
        "incident_time": extract_after_label(text, "DATE OF LOSS AND TIME"),
        "incident_location": extract_after_label(text, "LOCATION OF LOSS"),
        "incident_description": extract_after_label(text, "DESCRIPTION OF ACCIDENT"),
        "claimant": extract_after_label(text, "NAME OF CONTACT"),
        "third_parties": None,
        "contact_details": extract_after_label(text, "PRIMARY E-MAIL ADDRESS"),
        "asset_type": "vehicle",
        "asset_id": extract_after_label(text, "V.I.N.:"),
        "estimated_damage": extract_after_label(text, "ESTIMATE AMOUNT"),
        "claim_type": None,
        "attachments": None,
        "initial_estimate": extract_after_label(text, "ESTIMATE AMOUNT"),
    }
    return fields


def find_missing_fields(extracted: dict) -> list[str]:
    missing = []
    for field in MANDATORY_FIELDS:
        val = extracted.get(field)
        if val is None or str(val).strip() == "":
            missing.append(field)
    return missing


def decide_route(extracted: dict, missing_fields: list[str]) -> tuple[str, str]:
    description = (extracted.get("incident_description") or "").lower()
    claim_type = (extracted.get("claim_type") or "").lower()
    est_str = extracted.get("estimated_damage") or ""
    try:
        est = float(est_str.replace(",", "").replace("₹", "").strip())
    except ValueError:
        est = None

    if missing_fields:
        return "Manual review", "Some mandatory fields are missing: " + ", ".join(missing_fields)

    if any(w in description for w in ["fraud", "inconsistent", "staged"]):
        return "Investigation Flag", "Description contains suspicious keywords."

    if claim_type == "injury":
        return "Specialist Queue", "Claim type is injury."

    if est is not None and est < 25000:
        return "Fast-track", "Estimated damage is below 25,000."

    return "Standard Queue", "No special conditions met."


def process_file(file_path: str) -> dict:
    text = extract_text_from_text_file(file_path)
    extracted = parse_fields(text)
    missing = find_missing_fields(extracted)
    route, reason = decide_route(extracted, missing)
    return {
        "extractedFields": extracted,
        "missingFields": missing,
        "recommendedRoute": route,
        "reasoning": reason,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python fnol_agent.py <path-to-text-file>")
        raise SystemExit(1)

    result = process_file(sys.argv[1])
    print(json.dumps(result, indent=2))
