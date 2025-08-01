# Search Router with Environment Configuration

This project implements a FastAPI search router with configurable solution IDs for different environments.

## Environment Configuration

The application supports multiple environments with different solution IDs:

- **Local/Development**: Uses `.env` file
- **QA**: Uses `.env.qa` file  
- **Production**: Uses `.env.prod` file

### Environment Files

Each environment file contains:
```
EXPEDITE_SOLUTION_ID=<solution_id_for_expedite_tool>
MANUAL_SOLUTION_ID=<solution_id_for_manual_tool>
ENVIRONMENT=<environment_name>
```

### Usage

1. **For Local Development:**
   ```bash
   # Uses .env file by default
   uvicorn main:app --reload
   ```

2. **For QA Environment:**
   ```bash
   # Copy QA config to .env or set environment variables
   cp .env.qa .env
   uvicorn main:app --reload
   ```

3. **For Production Environment:**
   ```bash
   # Copy Production config to .env or set environment variables
   cp .env.prod .env
   uvicorn main:app --reload
   ```

### API Endpoint

- `GET /search/fallback` - Returns fallback tools with environment-specific solution IDs

### Response Format

```json
[
  {
    "name": "Expedite",
    "description": "A tool to expedite processes and enhance efficiency.",
    "category": "Productivity",
    "tags": ["efficiency", "automation", "productivity"],
    "solution_id": "qa_expedite_001"
  },
  {
    "name": "Manual", 
    "description": "A tool to find insights from data and provide actionable recommendations.",
    "category": "Analytics",
    "tags": ["data analysis", "insights", "recommendations"],
    "solution_id": "qa_manual_002"
  }
]
```

## Installation

```bash
pip install -r requirements.txt
```