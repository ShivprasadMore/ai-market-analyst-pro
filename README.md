# AI Market Analyst Pro 📊

**Strategic Intelligence, Decoded by Gemini 2.0.**

AI Market Analyst Pro is a professional-grade strategic intelligence tool that transforms complex business reports into actionable insight dashboards. Powered by Google Gemini 2.0, it performs deep document analysis to surface risks, opportunities, and strategic roadmaps instantly.

## ✨ Features

- **🎯 Deep Strategic Analysis**: Extracts KPIs, SWOT breakdowns, and trend vectors from any business PDF.
- **🔥 Interactive Risk Heatmap**: Automatically plots strategic risks on an Impact vs. Likelihood matrix for immediate prioritization.
- **💬 IntelQuest AI Chat**: Context-aware follow-up assistant that knows your document and can answer deep strategic questions.
- **📽️ Executive Slide Export**: Generates a professional PowerPoint presentation (.pptx) based on the analysis for immediate board-room use.
- **📄 Professional PDF Reports**: High-contrast, structured PDF export optimized for printing and sharing.
- **🤖 Multi-Stage PDF Extraction**: Combined PyMuPDF4LLM and pdfplumber logic for robust text extraction even from complex layouts.
- **🕰️ Analysis History**: Persistent local history tracking to revisit past reports and strategic findings.

## 🛠️ Tech Stack

- **Backend**: Python (Flask)
- **AI Engine**: Google Gemini 2.0 Flash (via `google-genai` SDK)
- **PDF Processing**: `pymupdf4llm`, `pdfplumber`, `PyPDF2`
- **Visualization**: Chart.js, Tailwind CSS
- **Presentation**: `python-pptx`
- **Database**: SQLite (SQLAlchemy)

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Google Gemini API Key (Get one at [Google AI Studio](https://aistudio.google.com/))

### Installation

1. **Clone & Enter**:
   ```bash
   git clone <repo-url>
   cd ai-market-analyst-pro
   ```

2. **Environment Setup**:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Credentials**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-2.0-flash
   ```

### Running the App

```bash
python run.py
```
The application will launch at `http://127.0.0.1:5000`.

## 📁 Project Structure

```text
.
├── app/
│   ├── core/           # Gemini Client, PDF Extractor, Slide Generator
│   ├── models/         # Data Schemas & SQLAlchemy Models
│   ├── utils/          # File Handling & JSON normalization
│   ├── templates/      # High-end Jinja2 Dashboards
│   └── routes.py       # API Endpoints
├── run.py              # Entry Point
└── requirements.txt    # Project Dependencies
```

## 📄 License
MIT
