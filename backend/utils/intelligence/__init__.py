"""
Intelligence Package - Modular ML Intelligence Engine
"""

from .data_quality import DataQualityAnalyzer
from .model_advice import ModelAdvisor
from .production_checks import ProductionChecker

__all__ = ['DataQualityAnalyzer', 'ModelAdvisor', 'ProductionChecker', 'analyze_with_intelligence']


def analyze_with_intelligence(df, tier: str = "free"):
    """
    Main entry point for intelligence analysis.
    
    Args:
        df: Pandas DataFrame to analyze
        tier: User tier (free, starter, pro, enterprise)
    
    Returns:
        Dictionary with all applicable intelligence features
    """
    from .main import DataIntelligence
    intelligence = DataIntelligence(df, tier)
    return intelligence.analyze()
