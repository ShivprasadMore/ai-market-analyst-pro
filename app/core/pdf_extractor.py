"""
Handles text extraction from PDF files.
"""
import logging
import pymupdf.layout  # Must be imported before pymupdf4llm to enable layout analysis
import pymupdf4llm
import pdfplumber
import PyPDF2
from typing import Optional

# Setup logging
logger = logging.getLogger(__name__)

class PDFExtractor:
    """
    Extract text from PDF files using a multi-stage fallback approach.
    Primarily uses PyMuPDF4LLM to generate Markdown for optimal LLM context.
    """
    
    @staticmethod
    def extract_text(file_path: str) -> Optional[str]:
        # 🟢 STAGE 1: PyMuPDF4LLM (Markdown optimization)
        try:
            logger.info(f"Attempting STAGE 1 (Markdown) extraction: {file_path}")
            # to_markdown returns a string of the entire document in markdown format
            md_text = pymupdf4llm.to_markdown(file_path)
            
            if md_text and md_text.strip():
                logger.info(f"PyMuPDF4LLM successful! Extracted {len(md_text)} chars in Markdown.")
                # We return the markdown directly - Gemini handles MD perfectly
                return md_text
        except Exception as e:
            logger.warning(f"STAGE 1 (PyMuPDF4LLM) failed: {str(e)}")
        
        # 🟡 STAGE 2: pdfplumber (Layout fallback)
        try:
            logger.info(f"Attempting STAGE 2 (Layout) extraction: {file_path}")
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num} ---\n{page_text}"
                
                if text.strip():
                    logger.info(f"pdfplumber successful! Extracted {len(text)} characters.")
                    return text
        except Exception as e:
            logger.warning(f"STAGE 2 (pdfplumber) failed: {str(e)}")
        
        # 🔴 STAGE 3: PyPDF2 (Basic fallback)
        try:
            logger.info(f"Attempting STAGE 3 (Basic) extraction: {file_path}")
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page_num, page in enumerate(reader.pages, 1):
                    extracted = page.extract_text()
                    if extracted:
                        text += f"\n--- Page {page_num} ---\n{extracted}"
                
                if text.strip():
                    logger.info(f"PyPDF2 fallback successful! Extracted {len(text)} characters.")
                    return text
        except Exception as e:
            logger.error(f"STAGE 3 (PyPDF2) also failed: {str(e)}")
        
        return None

# For testing (run directly)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_path = "sample_report.pdf"
    extractor = PDFExtractor()
    result = extractor.extract_text(test_path)
    if result:
        logger.info(f"Extraction successful! First 500 chars:\n{result[:500]}")
    else:
        logger.error("Extraction failed.")
