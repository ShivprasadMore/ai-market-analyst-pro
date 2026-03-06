"""
Database models and setup for SQLAlchemy.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class ReportAnalysis(db.Model):
    """Stores the results of report analyses."""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_comparison = db.Column(db.Boolean, default=False)
    
    # Store results as JSON text
    analysis_data = db.Column(db.Text, nullable=False)
    
    # Store original extracted text for IntelQuest
    extracted_text = db.Column(db.Text, nullable=True)

    def to_dict(self):
        """Convert to dictionary for API response."""
        data = json.loads(self.analysis_data)
        return {
            "id": self.id,
            "filename": self.filename,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "is_comparison": self.is_comparison,
            "data": data,
            "extracted_text": self.extracted_text
        }

    def to_summary_dict(self):
        """Convert to a lightweight dictionary for history list."""
        data = json.loads(self.analysis_data)
        return {
            "id": self.id,
            "filename": self.filename,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "is_comparison": self.is_comparison,
            "business_summary": data.get("current_business_situation", "")[:100] + "..."
        }
