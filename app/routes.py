"""
API routes for the application.
"""
import json
import re
from flask import Blueprint, request, jsonify, render_template

# Import our modules
from .core.pdf_extractor import PDFExtractor
from .core.gemini_client import GeminiClient
from .models.schemas import AnalysisResult
from .utils.file_handler import FileHandler
from .config import Config

# Create blueprint
main_bp = Blueprint('main', __name__)

# System prompt for Gemini (designed to force JSON output)
SYSTEM_PROMPT = """
You are an expert market research analyst with 15+ years of experience analyzing business reports.

Analyze the business report text provided below and extract the following information in JSON format:

{
  "current_business_situation": "A concise 2-3 sentence summary of the company's current overall situation",
  "strong_points": ["List 3-5 key strengths with specific evidence from the report"],
  "weak_points": ["List 3-5 key weaknesses or risks mentioned"],
  "smart_suggestions": ["List 3-5 actionable suggestions for improvement"],
  "next_strategic_moves": ["List 3-5 strategic moves the company should take"]
}

RULES:
1. Return ONLY the JSON object - no markdown, no code blocks, no additional text
2. Base your analysis strictly on the report content
3. Be specific and use data from the report where possible
4. Keep each point concise but informative
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
        "version": "1.0.0"
    })

@main_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Endpoint to upload PDF and get analysis.
    
    Expects: multipart/form-data with 'file' field containing PDF
    Returns: JSON with analysis results or error message
    """
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "error": "No file provided"
        }), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "success": False,
            "error": "No file selected"
        }), 400
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({
            "success": False,
            "error": "File must be a PDF"
        }), 400
    
    temp_path = None
    try:
        # Save uploaded file temporarily
        temp_path = FileHandler.save_temp_file(file)
        print(f"File saved to: {temp_path}")
        
        # Extract text from PDF
        extractor = PDFExtractor()
        text = extractor.extract_text(temp_path)
        
        if not text:
            return jsonify({
                "success": False,
                "error": "Could not extract text from PDF. Ensure it's not scanned or encrypted."
            }), 400
        
        print(f"Extracted {len(text)} characters from PDF")
        
        # Initialize Gemini client
        client = GeminiClient(api_key=Config.GEMINI_API_KEY)
        
        # Send to Gemini for analysis
        print("Sending to Gemini API...")
        response_text = client.generate_content(SYSTEM_PROMPT, text)
        
        if not response_text:
            return jsonify({
                "success": False,
                "error": "Gemini API call failed"
            }), 500
        
        print("Received response from Gemini")
        
        # Parse JSON from response (handle potential markdown)
        json_str = response_text.strip()
        
        # Remove markdown code fences if present
        json_str = re.sub(r'^```json\s*', '', json_str)
        json_str = re.sub(r'^```\s*', '', json_str)
        json_str = re.sub(r'\s*```$', '', json_str)
        
        # Find JSON object boundaries (in case there's extra text)
        json_match = re.search(r'({.*})', json_str, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        
        # Parse JSON
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Raw response: {response_text[:500]}")
            return jsonify({
                "success": False,
                "error": "Invalid JSON response from AI",
                "raw_response": response_text[:500]  # Include snippet for debugging
            }), 500
        
        # Validate with our schema
        try:
            result = AnalysisResult.from_dict(data)
            return jsonify({
                "success": True,
                "data": result.to_dict()
            })
        except Exception as e:
            print(f"Validation error: {e}")
            return jsonify({
                "success": False,
                "error": f"Data validation error: {str(e)}",
                "raw_data": data
            }), 500
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500
        
    finally:
        # Clean up temporary file
        if temp_path:
            FileHandler.cleanup(temp_path)
