"""
Core data models for the multi-agent decision system.

This module defines the primary data structures used throughout the system
for representing documents, options, analyses, and recommendations.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import numpy as np


@dataclass
class Document:
    """
    Represents a document with content, metadata, and optional embedding.
    
    Used for storing processed file content with associated metadata
    and vector embeddings for semantic search.
    """
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None
    
    def __post_init__(self):
        """Validate document content and metadata."""
        if not self.content or not isinstance(self.content, str):
            raise ValueError("Document content must be a non-empty string")
        if not isinstance(self.metadata, dict):
            raise ValueError("Document metadata must be a dictionary")


@dataclass
class Option:
    """
    Represents an option found through semantic search.
    
    Contains the option details, associated data, and similarity score
    from the vector search operation.
    """
    id: str
    title: str
    description: str
    data: Dict[str, Any]
    similarity_score: float
    
    def __post_init__(self):
        """Validate option data."""
        if not self.id or not isinstance(self.id, str):
            raise ValueError("Option ID must be a non-empty string")
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Option title must be a non-empty string")
        if not isinstance(self.data, dict):
            raise ValueError("Option data must be a dictionary")
        if not (0.0 <= self.similarity_score <= 1.0):
            raise ValueError("Similarity score must be between 0.0 and 1.0")


@dataclass
class Analysis:
    """
    Represents the pros/cons analysis of an option.
    
    Contains structured analysis results from the LLM including
    pros, cons, summary, and confidence score.
    """
    option_id: str
    pros: List[str]
    cons: List[str]
    summary: str
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate analysis data."""
        if not self.option_id or not isinstance(self.option_id, str):
            raise ValueError("Option ID must be a non-empty string")
        if not isinstance(self.pros, list) or not all(isinstance(p, str) for p in self.pros):
            raise ValueError("Pros must be a list of strings")
        if not isinstance(self.cons, list) or not all(isinstance(c, str) for c in self.cons):
            raise ValueError("Cons must be a list of strings")
        if not self.summary or not isinstance(self.summary, str):
            raise ValueError("Summary must be a non-empty string")
        if not (0.0 <= self.confidence <= 10.0):
            raise ValueError("Confidence must be between 0.0 and 10.0")


@dataclass
class Recommendation:
    """
    Represents a final recommendation with ranking and reasoning.
    
    Contains the option, its analysis, calculated score, reasoning,
    and final ranking position.
    """
    option: Option
    analysis: Analysis
    score: float
    reasoning: str
    rank: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate recommendation data."""
        if not isinstance(self.option, Option):
            raise ValueError("Option must be an Option instance")
        if not isinstance(self.analysis, Analysis):
            raise ValueError("Analysis must be an Analysis instance")
        if self.score < 0.0:
            raise ValueError("Score must be non-negative")
        if not self.reasoning or not isinstance(self.reasoning, str):
            raise ValueError("Reasoning must be a non-empty string")
        if self.rank < 1:
            raise ValueError("Rank must be a positive integer")
        
        # Ensure option and analysis are for the same item
        if self.option.id != self.analysis.option_id:
            raise ValueError("Option ID and Analysis option_id must match")