# API Documentation - AI Market Research Analyst Pro

This document provides technical details for the REST API endpoints used in the AI Market Research Analyst Pro application.

## Base URL
The application runs locally at: `http://127.0.0.1:5000`

---

## Endpoints

### 1. Health Check
Quickly verify the service status and version.

- **URL**: `/api/health`
- **Method**: `GET`
- **Success Response (200 OK)**:
    ```json
    {
      "status": "healthy",
      "service": "AI Market Research Analyst",
      "version": "1.2.0"
    }
    ```

### 2. Analyze Report (Agent Core)
The primary entry point for the Market Research Analyst. It accepts one or dual PDFs and returns a structured JSON strategic analysis.

- **URL**: `/api/analyze`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Request Body**:
    - `file` (File, required): One or two PDF business reports.
- **Success Response (200 OK)**:
    ```json
    {
      "success": true,
      "data": {
        "summary_title": "...",
        "current_business_situation": "...",
        "strong_points": [{"content": "...", "category": "..."}],
        "weak_points": [{"content": "...", "category": "..."}],
        "risks": [{"title": "...", "impact": 5, "likelihood": 3, "description": "..."}],
        "is_comparison": false
      }
    }
    ```

### 3. IntelQuest AI Chat
Enables follow-up strategic questioning using the analyzed report as context.

- **URL**: `/api/chat`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
    ```json
    {
      "query": "What are the top 3 financial risks?",
      "context": "Extracted text...",
      "analysis_data": { ... previous analysis JSON ... }
    }
    ```
- **Success Response (200 OK)**:
    ```json
    {
      "success": true,
      "response": "The top 3 financial risks identified are..."
    }
    ```

### 4. Fetch Analysis History
Retrieves a summary list of all previously analyzed reports stored in the local SQLite database.

- **URL**: `/api/history`
- **Method**: `GET`
- **Success Response (200 OK)**:
    ```json
    {
      "success": true,
      "history": [
        { "id": 1, "filename": "Annual_Report_2025.pdf", "timestamp": "2026-03-07T..." }
      ]
    }
    ```

### 5. Fetch Specific Report Data
Retrieves the full JSON analysis data for a historical report.

- **URL**: `/api/history/<id>`
- **Method**: `GET`
- **Success Response (200 OK)**:
    ```json
    {
      "success": true,
      "data": { ... full analysis JSON ... }
    }
    ```

### 6. Delete Report
Removes a specific analysis from the history.

- **URL**: `/api/history/<id>`
- **Method**: `DELETE`
- **Success Response (200 OK)**:
    ```json
    { "success": true, "message": "Report deleted" }
    ```

### 7. Clear All History
Wipes the local analysis database.

- **URL**: `/api/history/clear`
- **Method**: `DELETE`
- **Success Response (200 OK)**:
    ```json
    { "success": true, "message": "History cleared" }
    ```

### 8. Executive Slide Export
Converts the structured JSON analysis into a professional PowerPoint file.

- **URL**: `/api/export/slides`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
    ```json
    {
      "results": { ... analysis data ... },
      "filename": "Strategic_Update.pptx"
    }
    ```
- **Response**: Binary `.pptx` stream.

---

## 🛠️ Internal Mechanics & Workflow

The AI Market Analyst Pro operates as a sophisticated **Document-to-Insight Engine**:

1.  **Ingestion & Extraction**: Uses `PyMuPDF4LLM` to extract text while preserving layout cues. This ensures the AI understands tables and headings.
2.  **Persona-Driven Prompting**: The agent doesn't just "summarize"—it adopts the persona of a Strategic Analyst. It focuses on KPIs, SWOT markers, and Risk signals.
3.  **Strict JSON Output**: The core engine uses **Pydantic-style schema enforcement**. If the AI tries to return plain text, the `json_utils` layer cleans and forces it into the valid JSON structure expected by the Dashboard.
4.  **Fallback Cluster**: If the primary Gemini model hits a rate limit, the `GeminiClient` automatically rolls over to secondary models to ensure the "Market Research" never stops.
5.  **Relational Persistence**: Every insight is mapped back to the document source in a local SQLite instance, ensuring traceability.
