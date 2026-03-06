# API Documentation - AI Market Research Analyst Pro

This document provides technical details for the REST API endpoints used in the AI Market Research Analyst Pro application.

## Base URL
The application runs locally at: `http://127.0.0.1:5000`

---

## Endpoints

### 1. Analyze Report
Extracts text from uploaded PDF(s) and provides AI-powered strategic analysis.

- **URL**: `/api/analyze`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Request Body**:
    - `file` (File, required): One or two PDF files to analyze.
    - `persona` (String, optional): The expert persona to use (`general`, `ceo`, `auditor`, `marketing`). Defaults to `general`.
    - `market_topic` (String, optional): A topic to perform live market research on via Google Search.
- **Success Response (200 OK)**:
    ```json
    {
      "success": true,
      "data": {
        "current_business_situation": "...",
        "strong_points": ["...", "..."],
        "weak_points": ["...", "..."],
        "smart_suggestions": ["...", "..."],
        "next_strategic_moves": ["...", "..."],
        "is_comparison": false
      },
      "report_id": 1
    }
    ```

### 2. Follow-up Chat (IntelQuest)
Asks follow-up questions about the analyzed report.

- **URL**: `/api/chat`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
    ```json
    {
      "query": "What is the projected revenue growth?",
      "context": "Extracted text content from the PDF..."
    }
    ```
- **Success Response (200 OK)**:
    ```json
    {
      "success": true,
      "response": "Based on the report, the projected revenue growth is 15% YOY..."
    }
    ```

### 3. Fetch History
Retrieves a list of all historical analyses.

- **URL**: `/api/history`
- **Method**: `GET`
- **Success Response (200 OK)**:
    ```json
    {
      "success": true,
      "history": [
        {
          "id": 1,
          "filename": "report.pdf",
          "timestamp": "2026-02-26 18:00:00",
          "persona": "ceo"
        }
      ]
    }
    ```

### 4. Fetch Specific Report
Retrieves detailed analysis data for a single report.

- **URL**: `/api/history/<id>`
- **Method**: `GET`
- **Success Response (200 OK)**:
    ```json
    {
      "success": true,
      "data": { ... }
    }
    ```

### 5. Export PowerPoint
Generates a professional PowerPoint presentation from analysis result.

- **URL**: `/api/export/slides`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
    ```json
    {
      "results": { ... analysis data ... },
      "filename": "Strategic_Analysis.pptx"
    }
    ```
- **Response**: Binary stream for `.pptx` file.

---

## Error Handling
The API returns structured JSON error responses with appropriate HTTP status codes (400, 429, 500).

Example error:
```json
{
  "success": false,
  "error": "API quota exceeded. Please try again soon."
}
```

---

## 🛠️ How it Works (Workflow)

The AI Market Analyst Pro follows a strictly orchestrated 5-step workflow:

1.  **Extraction**: The `PDFExtractor` converts the uploaded binary PDF into clean, structured text.
2.  **Context Construction**: The `routes.py` logic combines the extracted text with a specific **Persona** (e.g., CEO) and optional **Market Intelligence** (Google Search).
3.  **AI Analysis**: The `GeminiClient` sends a highly structured prompt to the Gemini 2.5 Flash model, enforcing a strict JSON response.
4.  **Database Persistence**: Results are saved to a local SQLite database for history tracking and future retrieval.
5.  **Reactive Visualization**: The frontend JavaScript parses the JSON response and dynamically updates the **Chart.js** visualizations and **IntelQuest Chat** context.
