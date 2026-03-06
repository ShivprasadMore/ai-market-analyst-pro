"""
API routes for the application.
"""
import logging
import threading
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, render_template, send_file
from google.api_core import exceptions
import io

# Import our modules
from .core.pdf_extractor import PDFExtractor
from .core.gemini_client import GeminiClient
from .models.schemas import AnalysisResult
from .models.database import db, ReportAnalysis
from .utils.file_handler import FileHandler
from .utils.json_utils import clean_and_parse_json
from .core.slide_generator import SlideGenerator
from .config import Config
import json

# Setup logging
logger = logging.getLogger(__name__)

# Create blueprint
main_bp = Blueprint('main', __name__)

# Base prompt (designed for high-value strategic output)
BASE_PROMPT = """
Analyze the provided business report(s) and return a JSON object with this precise structure:
- summary_title: a concise 6-10 word professional title for the overall finding.
- current_business_situation: a 2-3 sentence executive summary.
- key_takeaways: 4-8 critical, high-impact business findings that summarize the most important points.
- strong_points: a comprehensive list (typically 5-10) of objects with:
    - content: the strength
    - category: business pillar (e.g. Financial, Market, Operational, Brand, Technical)
- weak_points: a comprehensive list (typically 5-10) of objects with:
    - content: the weakness
    - category: business pillar
- smart_suggestions: a comprehensive list (typically 5-10) of objects with:
    - content: actionable opportunity or recommendation
    - category: business pillar
- next_strategic_moves: a comprehensive list (typically 5-10) of objects with:
    - action: specific strategic step
    - priority: "High", "Medium", or "Low"
    - timeframe: "Short-term", "Mid-term", or "Long-term"
- risks: a comprehensive list (typically 5-10) of strategic risks, each with:
    - title: short name (2-4 words)
    - impact: integer from 1 (Low) to 5 (Critical)
    - likelihood: integer from 1 (Unlikely) to 5 (Certain)
    - description: 1-sentence explanation of why it's a risk.
- comparison_summary: (Required ONLY if comparing two reports) a 2-3 sentence summary of the key differences/trends between the two reports.
- comparison_delta: (Required ONLY if comparing two reports) a detailed list of strategic shifts identified between Report 1 and Report 2.

Return ONLY valid JSON, no other text. Include as many high-quality items as relevant; don't force a limit if the document is rich in information.
"""

@main_bp.route('/')
def index():
    """Serve the main upload page."""
    return render_template('index.html')

@main_bp.route('/results')
def results():
    """Serve the analysis results page."""
    return render_template('results.html')

@main_bp.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "AI Market Research Analyst",
        "version": "1.2.0"
    })

@main_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Endpoint to upload one or two PDFs and get analysis.
    """
    files = request.files.getlist('file')
    if not files or all(f.filename == '' for f in files):
        logger.warning("Analyze request received without valid files")
        return jsonify({"success": False, "error": "No files provided. Please select a PDF to upload."}), 400

    # Validate file types up front
    pdf_files = [f for f in files if f.filename.lower().endswith('.pdf')]
    if not pdf_files:
        return jsonify({"success": False, "error": "Invalid file type. Only PDF files are accepted."}), 400

    is_comparison = len(pdf_files) > 1

    # Max characters sent to Gemini
    MAX_INPUT_CHARS = Config.MAX_INPUT_CHARS

    temp_paths = []
    try:
        combined_text = ""
        for i, file in enumerate(pdf_files[:2]):  # Limit to 2 files
            # Check for empty / zero-byte file
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            file.seek(0)  # Reset
            if file_size == 0:
                return jsonify({"success": False, "error": f"'{file.filename}' is an empty file. Please upload a valid PDF."}), 400

            temp_path = FileHandler.save_temp_file(file)
            temp_paths.append(temp_path)

            extractor = PDFExtractor()
            text = extractor.extract_text(temp_path)
            if text:
                report_label = f"REPORT {i+1} ({file.filename})" if is_comparison else "REPORT"
                combined_text += f"\n\n=== {report_label} ===\n{text}"
            else:
                logger.warning(f"No text extracted from {file.filename}")

        # Truncate to avoid excessive token usage — keeps the most valuable content (start of docs)
        if len(combined_text) > MAX_INPUT_CHARS:
            logger.info(f"Truncating input from {len(combined_text)} to {MAX_INPUT_CHARS} chars for speed")
            combined_text = combined_text[:MAX_INPUT_CHARS] + "\n\n[Content truncated for processing speed]"

        if not combined_text.strip():
            return jsonify({"success": False, "error": "Could not extract any text from the uploaded file(s). Please ensure the PDF is text-based (not a scanned image). Scanned PDFs are not supported."}), 400

        # Detect likely scanned/image-only PDF (very little extractable text)
        if len(combined_text.strip()) < 150:
            return jsonify({"success": False, "error": "The PDF appears to contain very little text. It may be a scanned image. Please upload a text-based PDF for accurate analysis."}), 400

        client = GeminiClient(api_key=Config.GEMINI_API_KEY, model=Config.GEMINI_MODEL)
        
        try:
            logger.info(f"Calling Gemini API (Comparison: {is_comparison})...")
            response_text = client.generate_content(BASE_PROMPT, combined_text)
            
            if not response_text:
                return jsonify({"success": False, "error": "Gemini API returned empty response"}), 500
                
        except exceptions.ResourceExhausted as e:
            return jsonify({"success": False, "error": "API rate limit reached. Please wait a moment and try again."}), 429
        except Exception as e:
            err_str = str(e).lower()
            if "network" in err_str or "connection" in err_str or "timeout" in err_str:
                return jsonify({"success": False, "error": "Network error — could not reach the AI service. Please check your connection and try again."}), 503
            return jsonify({"success": False, "error": f"AI service error: {str(e)}"}), 500
        
        try:
            data = clean_and_parse_json(response_text)
            # Ensure is_comparison flag is correct from server side logic even if AI misses it
            data['is_comparison'] = is_comparison
        except Exception as e:
            logger.error(f"Failed to parse AI response: {str(e)}")
            logger.error(f"Raw response (first 500 chars): {repr(response_text[:500])}")
            return jsonify({"success": False, "error": "Unexpected response format from AI. Please try again."}), 500
        
        try:
            result = AnalysisResult.from_dict(data)
            
            report_filename = ", ".join([f.filename for f in files[:2]])
            result.generated_at = datetime.now(timezone.utc).isoformat()
            result.filename = report_filename
            result_dict = result.to_dict()

            # Save to DB in a background thread so the response is returned immediately
            def _save_to_db(app_ctx, res_dict, filename, is_comp, text):
                with app_ctx:
                    try:
                        new_report = ReportAnalysis(
                            filename=filename,
                            is_comparison=is_comp,
                            analysis_data=json.dumps(res_dict),
                            extracted_text=text
                        )
                        db.session.add(new_report)
                        db.session.commit()
                        logger.info(f"Analysis saved to DB in background with ID: {new_report.id}")
                    except Exception as db_err:
                        logger.error(f"Background DB save failed: {db_err}")
                        db.session.rollback()

            from flask import current_app
            threading.Thread(
                target=_save_to_db,
                args=(current_app._get_current_object().app_context(), result_dict, report_filename, is_comparison, combined_text),
                daemon=True
            ).start()

            return jsonify({
                "success": True, 
                "data": result_dict,
                "extracted_text": combined_text,  # Return this for IntelQuest context
                "meta": {"comparison": is_comparison}
            })
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return jsonify({"success": False, "error": "Validation failed"}), 500
            
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return jsonify({"success": False, "error": "Server error occurred."}), 500
        
    finally:
        for p in temp_paths:
            FileHandler.cleanup(p)

@main_bp.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint for follow-up questions about the report.
    """
    try:
        data = request.json
        query = data.get('query')
        context = data.get('context') # This is the extracted text from sessionStorage
        analysis_data = data.get('analysis_data') # Structured AI analysis JSON
        
        if not query or not context:
            return jsonify({"success": False, "error": "Query and context are required"}), 400
        
        # Build the analysis summary section if structured data is available
        analysis_summary = ""
        if analysis_data:
            try:
                ad = analysis_data if isinstance(analysis_data, dict) else json.loads(analysis_data)
                
                def fmt_list(items, key='content'):
                    if not items: return "None identified."
                    return "\n".join(f"  - [{item.get('category', 'General')}] {item.get(key, str(item))}" 
                                     if isinstance(item, dict) else f"  - {item}" for item in items)
                
                analysis_summary = f"""
        The AI has already analyzed the report(s) and produced these structured findings:
        --- AI ANALYSIS FINDINGS ---
        SUMMARY TITLE: {ad.get('summary_title', 'N/A')}
        EXECUTIVE SUMMARY: {ad.get('current_business_situation', 'N/A')}
        
        KEY TAKEAWAYS:
        {chr(10).join(f'  - {t}' for t in (ad.get('key_takeaways') or []))}
        
        STRENGTHS (Strong Points):
        {fmt_list(ad.get('strong_points', []))}
        
        WEAKNESSES (Weak Points):
        {fmt_list(ad.get('weak_points', []))}
        
        OPPORTUNITIES (Smart Suggestions):
        {fmt_list(ad.get('smart_suggestions', []))}
        
        STRATEGIC RISKS:
        {chr(10).join(f"  - [{r.get('title','Risk')}] Impact:{r.get('impact')}/5, Likelihood:{r.get('likelihood')}/5 — {r.get('description','')}" for r in (ad.get('risks') or []))}
        
        NEXT STRATEGIC MOVES:
        {chr(10).join(f"  - [{m.get('priority','?')} | {m.get('timeframe','?')}] {m.get('action', str(m))}" for m in (ad.get('next_strategic_moves') or []))}
        --- END AI ANALYSIS ---
        """
            except Exception as parse_err:
                logger.warning(f"Could not parse analysis_data for chat context: {parse_err}")
            
        chat_prompt = f"""
        You are IntelQuest, an expert AI market analyst assistant.
        The user is reviewing an analysis of one or more business reports.
        {analysis_summary}
        Below is the original extracted text from the reports (for deeper reference):
        --- START RAW REPORT TEXT ---
        {context}
        --- END RAW REPORT TEXT ---
        
        Using the AI analysis findings above (and the raw text for deeper detail), answer the following follow-up question clearly and helpfully.
        If asked about weaknesses, strengths, risks, suggestions, or strategic moves, refer to the structured findings above.
        If the answer is not available in any provided context, politely say so.
        Keep your response professional, insightful, and concise.
        IMPORTANT: Provide your answer in plain text. Do NOT use Markdown formatting (like `**` for bold), and do NOT include the internal category brackets (like `[Market]` or `[Risk]`) from the context above in your final answer.
        
        User's question: {query}
        """
        
        client = GeminiClient(api_key=Config.GEMINI_API_KEY, model=Config.GEMINI_MODEL)
        response_text = client.generate_content(chat_prompt, "Please answer the user's question based on the context.")
        
        return jsonify({
            "success": True,
            "response": response_text
        })
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({"success": False, "error": "Failed to generate chat response"}), 500

@main_bp.route('/api/history', methods=['GET'])
def get_history():
    """Fetch all analysis history."""
    try:
        reports = ReportAnalysis.query.order_by(ReportAnalysis.timestamp.desc()).all()
        return jsonify({
            "success": True,
            "history": [r.to_summary_dict() for r in reports]
        })
    except Exception as e:
        logger.error(f"Failed to fetch history: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@main_bp.route('/api/history/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """Fetch specific report details."""
    try:
        report = ReportAnalysis.query.get_or_404(report_id)
        return jsonify({
            "success": True,
            "data": report.to_dict()
        })
    except Exception as e:
        logger.error(f"Failed to fetch report {report_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@main_bp.route('/api/history/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """Delete a report from history."""
    try:
        report = ReportAnalysis.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        return jsonify({"success": True, "message": "Report deleted"})
    except Exception as e:
        logger.error(f"Failed to delete report {report_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@main_bp.route('/api/history/clear', methods=['DELETE'])
def clear_history():
    """Clear all history."""
    try:
        ReportAnalysis.query.delete()
        db.session.commit()
        return jsonify({"success": True, "message": "History cleared"})
    except Exception as e:
        logger.error(f"Failed to clear history: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@main_bp.route('/api/export/slides', methods=['POST'])
def export_slides():
    """Generates and returns a PowerPoint presentation."""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        analysis_results = data.get('results')
        filename = data.get('filename', 'Strategic_Analysis.pptx')
        
        if not analysis_results:
            return jsonify({"success": False, "error": "Analysis results missing"}), 400
            
        generator = SlideGenerator()
        pptx_io = generator.generate(analysis_results, filename)
        
        return send_file(
            pptx_io,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            as_attachment=True,
            download_name=f"Executive_Summary_{filename.replace(' ', '_')}.pptx"
        )
    except Exception as e:
        logger.error(f"Slide generation failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
