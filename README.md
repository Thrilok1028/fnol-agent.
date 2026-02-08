# Synapx FNOL Processing Agent

Autonomous agent that extracts key fields from FNOL documents, identifies missing fields, and routes claims.[file:12]

## Features
- Extracts policy info, incident details, parties, assets, claim type from ACORD forms.[file:11][file:12]
- Detects missing mandatory fields.
- Routes using 4 rules (damage threshold, missing fields, fraud keywords, injury claims).[file:12]
- JSON output format.

## Installation
```bash
git clone https://github.com/Thik102/fnol-agent.git
cd fnol-agent
# No dependencies - pure Python
