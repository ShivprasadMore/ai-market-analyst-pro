"""
Handles text extraction from PDF files.
"""
import PyPDF2
from typing import Optional

class PDFExtractor:
    """Extract text from PDF files with error handling."""
    
    @staticmethod
    def extract_text(file_path: str) -> Optional[str]:
        """
        Extract all text from a PDF file.
        
        Args:
            file_path: Path to the PDF file.
            
        Returns:
            Extracted text as string, or None if extraction fails.
        """
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page_num, page in enumerate(reader.pages, 1):
                    extracted = page.extract_text()
                    if extracted:
                        text += f"--- Page {page_num} ---\n{extracted}\n"
                return text if text.strip() else None
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return None

# For testing (run directly)
if __name__ == "__main__":
    # Test with a sample PDF (replace with actual path)
    test_path = "sample.pdf"  # You'll need a real PDF here
    extractor = PDFExtractor()
    result = extractor.extract_text(test_path)
    if result:
        print("Extraction successful! First 500 chars:")
        print(result[:500])
    else:
        print("Extraction failed.")
