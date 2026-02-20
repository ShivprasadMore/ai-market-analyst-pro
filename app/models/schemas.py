"""
Data schemas for the application using dataclasses.
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AnalysisResult:
    """Represents the structured analysis output."""
    current_business_situation: str
    strong_points: List[str]
    weak_points: List[str]
    smart_suggestions: List[str]
    next_strategic_moves: List[str]
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create an instance from a dictionary (parsed JSON)."""
        return cls(
            current_business_situation=data.get("current_business_situation", ""),
            strong_points=data.get("strong_points", []),
            weak_points=data.get("weak_points", []),
            smart_suggestions=data.get("smart_suggestions", []),
            next_strategic_moves=data.get("next_strategic_moves", [])
        )
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "current_business_situation": self.current_business_situation,
            "strong_points": self.strong_points,
            "weak_points": self.weak_points,
            "smart_suggestions": self.smart_suggestions,
            "next_strategic_moves": self.next_strategic_moves
        }
