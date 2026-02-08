# fnol-agent.
# Synapx FNOL Processing Agent

Autonomous agent for extracting fields from First Notice of Loss (FNOL) documents, identifying missing fields, and routing claims to appropriate workflows.[file:12]

## Features
- Extracts 16 key fields from ACORD-style insurance forms.[file:11][file:12]
- Identifies all missing mandatory fields.
- Applies 4 routing rules with clear reasoning.[file:12]
- Outputs structured JSON as specified.

## Installation
```bash
git clone https://github.com/[your-username]/fnol-agent.git
cd fnol-agent
pip install -r requirements.txt  # No external dependencies needed
