# AI Market Analyst Pro 📊
*Advanced Market Research Analyst AI Agent*

AI Market Analyst Pro is a high-performance strategic intelligence platform designed to bridge the gap between massive, unstructured corporate data and executive decision-making. By transforming 50-100+ page annual reports and market filings into structured, visually intuitive dashboards, the platform significantly accelerates time-to-insight for consultancy and executive teams.

## 🚀 Core Value Pillars
- **Accuracy**: Multi-stage AI verification ensures that SWOT and Risk metrics are grounded in document facts.
- **Actionability**: Shifts the focus from "What happened?" to "What should we do next?" via automated strategic roadmapping.
- **Agility**: Rapidly digest complex filings to identify market shifts before competitors.

---

## 🏗️ System Architecture

![System Architecture](assets/architecture-diagram.png)

The platform is built on a modern, decoupled architecture designed for high availability and rapid scaling. It features a Tailwind-powered Dashboard communicating with a high-concurrency Flask backend, orchestrated by a 4-tier Gemini AI fallback cluster.

---

## 🎥 Demo Video
A complete walkthrough of the application and the building process is available here:  
**[Watch the Demo Video](https://drive.google.com/file/d/1HrD9APS7GRnf5jS2vHCcErqGi6ZuW2jb/view?usp=sharing)**

---

## 📄 Technical Documentation
For a detailed overview of the architecture, data security protocols, and implementation details, see the [full technical documentation](TECHNICAL_DOCUMENTATION.md). 

> [!NOTE]
> You can also access the [External Google Doc Version](https://docs.google.com/document/d/1U2LAyBHGoTNKFnZybUoNxuNKOBsPnVZpaaCtoSFMqY0/edit?usp=sharing) 

---

## ✨ Key Features

- **🎯 Deep Strategic Analysis**: Extracts KPIs, SWOT breakdowns, and trend vectors from any business PDF.
- **🔥 Interactive Risk Heatmap**: Dynamically plots strategic risks on an Impact vs. Likelihood matrix for immediate prioritization.
- **💬 IntelQuest AI Chat**: Context-aware follow-up assistant that knows your document and can answer deep strategic questions.
- **📽️ Executive Slide Export**: Generates a professional PowerPoint presentation (.pptx) based on the analysis for immediate board-room use.
- **📄 Consultancy-Grade Reports**: Theme-independent PDF exports optimized for high-fidelity printing and sharing.
- **🤖 Multi-Stage Processing**: Combined PyMuPDF4LLM and pdfplumber logic for robust extraction from complex layouts.

---

## 🛡️ Key Implementation Features

### Data Privacy & Security
- **Local-First Processing**: Documents are processed in temporary, secure buffers and cleared immediately.
- **Zero-PII Retention**: Designed to extract business insights without storing sensitive personal data.
- **API Hardening**: All AI communications are encrypted via TLS 1.3.

### High-Availability AI Logic
- **4-Stage Fallback Chain**: Automatically cycles through `Gemini 3.0 Flash`, `3.1 Flash-Lite`, and `2.5 Flash` to maintain zero-latency even during API quota brownouts.
- **JSON-Schema Enforcement**: Uses strict schema enforcement to guarantee that dashboard data always matches the expected technical format.

---

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | Tailwind CSS + Vanilla JS (ES6+) | Responsive UI with Chart.js visualization. |
| **Backend** | Python / Flask | High-concurrency API orchestration. |
| **AI Engine** | Google Gemini 3.0/3.1 | Multimodal reasoning and structured extraction. |
| **Extraction** | PyMuPDF4LLM + pdfplumber | Advanced structural analysis of PDF layouts. |
| **Database** | SQLite | Localized history and session tracking. |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/))

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
   Create a `.env` file in the root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-3-flash-preview
   ```

### Running the App
```bash
python run.py
```
App will launch at `http://127.0.0.1:5000`.

---

## 📈 Future Scalability Roadmap

- **Phase 1: Comparative Intelligence**: Automated "Delta Reports" across multiple years.
- **Phase 2: Predictive Benchmarking**: Real-time market sentiment cross-referencing.
- **Phase 3: Global Multi-User SaaS**: Migration to Google Cloud Run and Firebase Auth.

---

## 📄 License
MIT
