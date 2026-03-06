"""
Data schemas for the application using dataclasses.
"""
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Risk:
    """Represents a specific strategic risk."""
    title: str
    impact: int  # 1-5
    likelihood: int  # 1-5
    description: str

@dataclass
class CategorizedInsight:
    """A SWOT-style insight with a business category."""
    content: str
    category: str # e.g., Financial, Operational, Market

@dataclass
class StrategicMove:
    """A prioritized move with a timeframe."""
    action: str
    priority: str # High, Medium, Low
    timeframe: str # Short-term, Mid-term, Long-term

@dataclass
class AnalysisResult:
    """Represents the structured analysis output."""
    summary_title: str
    current_business_situation: str
    key_takeaways: List[str]
    strong_points: List[CategorizedInsight]
    weak_points: List[CategorizedInsight]
    smart_suggestions: List[CategorizedInsight]
    next_strategic_moves: List[StrategicMove]
    risks: List[Risk]
    comparison_summary: Optional[str] = None
    comparison_delta: Optional[List[str]] = None
    is_comparison: bool = False
    
    # Metadata — populated by routes after DB save
    report_id: Optional[int] = None
    generated_at: Optional[str] = None
    filename: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create an instance from a dictionary (parsed JSON)."""
        risks_data = data.get("risks", [])
        risks = [
            Risk(
                title=r.get("title", ""),
                impact=int(r.get("impact", 3)),
                likelihood=int(r.get("likelihood", 3)),
                description=r.get("description", "")
            ) for r in risks_data
        ]

        def parse_categorized(items):
            if not items: return []
            return [CategorizedInsight(
                content=i.get("content", str(i)) if isinstance(i, dict) else str(i),
                category=i.get("category", "General") if isinstance(i, dict) else "General"
            ) for i in items]

        def parse_moves(items):
            if not items: return []
            return [StrategicMove(
                action=m.get("action", str(m)) if isinstance(m, dict) else str(m),
                priority=m.get("priority", "Medium") if isinstance(m, dict) else "Medium",
                timeframe=m.get("timeframe", "Mid-term") if isinstance(m, dict) else "Mid-term"
            ) for m in items]
        
        return cls(
            summary_title=data.get("summary_title", "Business Analysis"),
            current_business_situation=data.get("current_business_situation", ""),
            key_takeaways=data.get("key_takeaways", []),
            strong_points=parse_categorized(data.get("strong_points")),
            weak_points=parse_categorized(data.get("weak_points")),
            smart_suggestions=parse_categorized(data.get("smart_suggestions")),
            next_strategic_moves=parse_moves(data.get("next_strategic_moves")),
            risks=risks,
            comparison_summary=data.get("comparison_summary"),
            comparison_delta=data.get("comparison_delta"),
            is_comparison=data.get("is_comparison", False),
            report_id=data.get("report_id"),
            generated_at=data.get("generated_at"),
            filename=data.get("filename"),
        )
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            # --- Metadata ---
            "summary_title": self.summary_title,
            "report_id": self.report_id,
            "generated_at": self.generated_at,
            "filename": self.filename,
            "is_comparison": self.is_comparison,
            # --- Core Analysis ---
            "current_business_situation": self.current_business_situation,
            "key_takeaways": self.key_takeaways,
            "strong_points": [vars(i) for i in self.strong_points],
            "weak_points": [vars(i) for i in self.weak_points],
            "smart_suggestions": [vars(i) for i in self.smart_suggestions],
            "next_strategic_moves": [vars(m) for m in self.next_strategic_moves],
            "risks": [vars(r) for r in self.risks],
            # --- Optional Fields ---
            "comparison_summary": self.comparison_summary,
            "comparison_delta": self.comparison_delta,
        }
