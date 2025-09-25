"""
Unit tests for core data models.

Tests the Document, Option, Analysis, and Recommendation data classes
to ensure proper validation and functionality.
"""

import pytest
import numpy as np
from datetime import datetime
from multi_agent_decision_system.data_processing.models import (
    Document, Option, Analysis, Recommendation
)


class TestDocument:
    """Test cases for Document data model."""
    
    def test_document_creation_valid(self):
        """Test creating a valid Document instance."""
        doc = Document(
            content="Test content",
            metadata={"source": "test.txt", "type": "text"}
        )
        
        assert doc.content == "Test content"
        assert doc.metadata == {"source": "test.txt", "type": "text"}
        assert doc.embedding is None
    
    def test_document_with_embedding(self):
        """Test Document with embedding array."""
        embedding = np.array([0.1, 0.2, 0.3])
        doc = Document(
            content="Test content",
            metadata={"source": "test.txt"},
            embedding=embedding
        )
        
        assert np.array_equal(doc.embedding, embedding)
    
    def test_document_empty_content_raises_error(self):
        """Test that empty content raises ValueError."""
        with pytest.raises(ValueError, match="Document content must be a non-empty string"):
            Document(content="", metadata={})
    
    def test_document_none_content_raises_error(self):
        """Test that None content raises ValueError."""
        with pytest.raises(ValueError, match="Document content must be a non-empty string"):
            Document(content=None, metadata={})
    
    def test_document_invalid_metadata_raises_error(self):
        """Test that invalid metadata raises ValueError."""
        with pytest.raises(ValueError, match="Document metadata must be a dictionary"):
            Document(content="Test", metadata="invalid")


class TestOption:
    """Test cases for Option data model."""
    
    def test_option_creation_valid(self):
        """Test creating a valid Option instance."""
        option = Option(
            id="opt_1",
            title="Test Option",
            description="A test option",
            data={"value": 100, "category": "test"},
            similarity_score=0.85
        )
        
        assert option.id == "opt_1"
        assert option.title == "Test Option"
        assert option.description == "A test option"
        assert option.data == {"value": 100, "category": "test"}
        assert option.similarity_score == 0.85
    
    def test_option_empty_id_raises_error(self):
        """Test that empty ID raises ValueError."""
        with pytest.raises(ValueError, match="Option ID must be a non-empty string"):
            Option(
                id="",
                title="Test",
                description="Test",
                data={},
                similarity_score=0.5
            )
    
    def test_option_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Option title must be a non-empty string"):
            Option(
                id="opt_1",
                title="",
                description="Test",
                data={},
                similarity_score=0.5
            )
    
    def test_option_invalid_data_raises_error(self):
        """Test that invalid data raises ValueError."""
        with pytest.raises(ValueError, match="Option data must be a dictionary"):
            Option(
                id="opt_1",
                title="Test",
                description="Test",
                data="invalid",
                similarity_score=0.5
            )
    
    def test_option_invalid_similarity_score_raises_error(self):
        """Test that invalid similarity score raises ValueError."""
        with pytest.raises(ValueError, match="Similarity score must be between 0.0 and 1.0"):
            Option(
                id="opt_1",
                title="Test",
                description="Test",
                data={},
                similarity_score=1.5
            )
        
        with pytest.raises(ValueError, match="Similarity score must be between 0.0 and 1.0"):
            Option(
                id="opt_1",
                title="Test",
                description="Test",
                data={},
                similarity_score=-0.1
            )


class TestAnalysis:
    """Test cases for Analysis data model."""
    
    def test_analysis_creation_valid(self):
        """Test creating a valid Analysis instance."""
        analysis = Analysis(
            option_id="opt_1",
            pros=["Pro 1", "Pro 2"],
            cons=["Con 1", "Con 2"],
            summary="Test summary",
            confidence=8.5
        )
        
        assert analysis.option_id == "opt_1"
        assert analysis.pros == ["Pro 1", "Pro 2"]
        assert analysis.cons == ["Con 1", "Con 2"]
        assert analysis.summary == "Test summary"
        assert analysis.confidence == 8.5
        assert isinstance(analysis.timestamp, datetime)
    
    def test_analysis_empty_option_id_raises_error(self):
        """Test that empty option_id raises ValueError."""
        with pytest.raises(ValueError, match="Option ID must be a non-empty string"):
            Analysis(
                option_id="",
                pros=["Pro 1"],
                cons=["Con 1"],
                summary="Test",
                confidence=5.0
            )
    
    def test_analysis_invalid_pros_raises_error(self):
        """Test that invalid pros raises ValueError."""
        with pytest.raises(ValueError, match="Pros must be a list of strings"):
            Analysis(
                option_id="opt_1",
                pros="invalid",
                cons=["Con 1"],
                summary="Test",
                confidence=5.0
            )
        
        with pytest.raises(ValueError, match="Pros must be a list of strings"):
            Analysis(
                option_id="opt_1",
                pros=[1, 2, 3],
                cons=["Con 1"],
                summary="Test",
                confidence=5.0
            )
    
    def test_analysis_invalid_cons_raises_error(self):
        """Test that invalid cons raises ValueError."""
        with pytest.raises(ValueError, match="Cons must be a list of strings"):
            Analysis(
                option_id="opt_1",
                pros=["Pro 1"],
                cons="invalid",
                summary="Test",
                confidence=5.0
            )
    
    def test_analysis_empty_summary_raises_error(self):
        """Test that empty summary raises ValueError."""
        with pytest.raises(ValueError, match="Summary must be a non-empty string"):
            Analysis(
                option_id="opt_1",
                pros=["Pro 1"],
                cons=["Con 1"],
                summary="",
                confidence=5.0
            )
    
    def test_analysis_invalid_confidence_raises_error(self):
        """Test that invalid confidence raises ValueError."""
        with pytest.raises(ValueError, match="Confidence must be between 0.0 and 10.0"):
            Analysis(
                option_id="opt_1",
                pros=["Pro 1"],
                cons=["Con 1"],
                summary="Test",
                confidence=11.0
            )
        
        with pytest.raises(ValueError, match="Confidence must be between 0.0 and 10.0"):
            Analysis(
                option_id="opt_1",
                pros=["Pro 1"],
                cons=["Con 1"],
                summary="Test",
                confidence=-1.0
            )


class TestRecommendation:
    """Test cases for Recommendation data model."""
    
    def test_recommendation_creation_valid(self):
        """Test creating a valid Recommendation instance."""
        option = Option(
            id="opt_1",
            title="Test Option",
            description="Test",
            data={},
            similarity_score=0.8
        )
        
        analysis = Analysis(
            option_id="opt_1",
            pros=["Pro 1"],
            cons=["Con 1"],
            summary="Test summary",
            confidence=7.0
        )
        
        recommendation = Recommendation(
            option=option,
            analysis=analysis,
            score=85.5,
            reasoning="Test reasoning",
            rank=1
        )
        
        assert recommendation.option == option
        assert recommendation.analysis == analysis
        assert recommendation.score == 85.5
        assert recommendation.reasoning == "Test reasoning"
        assert recommendation.rank == 1
        assert isinstance(recommendation.timestamp, datetime)
    
    def test_recommendation_invalid_option_raises_error(self):
        """Test that invalid option raises ValueError."""
        analysis = Analysis(
            option_id="opt_1",
            pros=["Pro 1"],
            cons=["Con 1"],
            summary="Test",
            confidence=7.0
        )
        
        with pytest.raises(ValueError, match="Option must be an Option instance"):
            Recommendation(
                option="invalid",
                analysis=analysis,
                score=85.5,
                reasoning="Test",
                rank=1
            )
    
    def test_recommendation_invalid_analysis_raises_error(self):
        """Test that invalid analysis raises ValueError."""
        option = Option(
            id="opt_1",
            title="Test",
            description="Test",
            data={},
            similarity_score=0.8
        )
        
        with pytest.raises(ValueError, match="Analysis must be an Analysis instance"):
            Recommendation(
                option=option,
                analysis="invalid",
                score=85.5,
                reasoning="Test",
                rank=1
            )
    
    def test_recommendation_negative_score_raises_error(self):
        """Test that negative score raises ValueError."""
        option = Option(
            id="opt_1",
            title="Test",
            description="Test",
            data={},
            similarity_score=0.8
        )
        
        analysis = Analysis(
            option_id="opt_1",
            pros=["Pro 1"],
            cons=["Con 1"],
            summary="Test",
            confidence=7.0
        )
        
        with pytest.raises(ValueError, match="Score must be non-negative"):
            Recommendation(
                option=option,
                analysis=analysis,
                score=-10.0,
                reasoning="Test",
                rank=1
            )
    
    def test_recommendation_empty_reasoning_raises_error(self):
        """Test that empty reasoning raises ValueError."""
        option = Option(
            id="opt_1",
            title="Test",
            description="Test",
            data={},
            similarity_score=0.8
        )
        
        analysis = Analysis(
            option_id="opt_1",
            pros=["Pro 1"],
            cons=["Con 1"],
            summary="Test",
            confidence=7.0
        )
        
        with pytest.raises(ValueError, match="Reasoning must be a non-empty string"):
            Recommendation(
                option=option,
                analysis=analysis,
                score=85.5,
                reasoning="",
                rank=1
            )
    
    def test_recommendation_invalid_rank_raises_error(self):
        """Test that invalid rank raises ValueError."""
        option = Option(
            id="opt_1",
            title="Test",
            description="Test",
            data={},
            similarity_score=0.8
        )
        
        analysis = Analysis(
            option_id="opt_1",
            pros=["Pro 1"],
            cons=["Con 1"],
            summary="Test",
            confidence=7.0
        )
        
        with pytest.raises(ValueError, match="Rank must be a positive integer"):
            Recommendation(
                option=option,
                analysis=analysis,
                score=85.5,
                reasoning="Test",
                rank=0
            )
    
    def test_recommendation_mismatched_ids_raises_error(self):
        """Test that mismatched option and analysis IDs raise ValueError."""
        option = Option(
            id="opt_1",
            title="Test",
            description="Test",
            data={},
            similarity_score=0.8
        )
        
        analysis = Analysis(
            option_id="opt_2",  # Different ID
            pros=["Pro 1"],
            cons=["Con 1"],
            summary="Test",
            confidence=7.0
        )
        
        with pytest.raises(ValueError, match="Option ID and Analysis option_id must match"):
            Recommendation(
                option=option,
                analysis=analysis,
                score=85.5,
                reasoning="Test",
                rank=1
            )