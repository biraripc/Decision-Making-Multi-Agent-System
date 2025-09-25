"""
Unit tests for workflow state management.

Tests the AgentState TypedDict and related state management functions
for LangGraph workflow orchestration.
"""

import pytest
from multi_agent_decision_system.workflow.state import (
    AgentState, create_initial_state, update_state_step,
    add_error_context, validate_state_transition
)
from multi_agent_decision_system.data_processing.models import (
    Document, Option, Analysis, Recommendation
)


class TestCreateInitialState:
    """Test cases for create_initial_state function."""
    
    def test_create_initial_state_valid(self):
        """Test creating valid initial state."""
        documents = [
            Document(content="Test 1", metadata={"source": "test1.txt"}),
            Document(content="Test 2", metadata={"source": "test2.txt"})
        ]
        
        state = create_initial_state("Find best option", documents)
        
        assert state["user_query"] == "Find best option"
        assert state["uploaded_data"] == documents
        assert state["found_options"] == []
        assert state["analyses"] == []
        assert state["recommendations"] == []
        assert state["current_step"] == "option_finder"
        assert state["error_context"] is None
        assert state["processing_metadata"]["total_documents"] == 2
        assert state["processing_metadata"]["workflow_version"] == "1.0"
    
    def test_create_initial_state_empty_query_raises_error(self):
        """Test that empty query raises ValueError."""
        documents = [Document(content="Test", metadata={})]
        
        with pytest.raises(ValueError, match="User query must be a non-empty string"):
            create_initial_state("", documents)
    
    def test_create_initial_state_none_query_raises_error(self):
        """Test that None query raises ValueError."""
        documents = [Document(content="Test", metadata={})]
        
        with pytest.raises(ValueError, match="User query must be a non-empty string"):
            create_initial_state(None, documents)
    
    def test_create_initial_state_empty_data_raises_error(self):
        """Test that empty uploaded data raises ValueError."""
        with pytest.raises(ValueError, match="Uploaded data must be a non-empty list"):
            create_initial_state("Test query", [])
    
    def test_create_initial_state_none_data_raises_error(self):
        """Test that None uploaded data raises ValueError."""
        with pytest.raises(ValueError, match="Uploaded data must be a non-empty list"):
            create_initial_state("Test query", None)
    
    def test_create_initial_state_invalid_documents_raises_error(self):
        """Test that invalid document types raise ValueError."""
        with pytest.raises(ValueError, match="All uploaded data items must be Document instances"):
            create_initial_state("Test query", ["invalid", "documents"])


class TestUpdateStateStep:
    """Test cases for update_state_step function."""
    
    def test_update_state_step_valid(self):
        """Test updating state step with valid step."""
        documents = [Document(content="Test", metadata={})]
        state = create_initial_state("Test query", documents)
        
        updated_state = update_state_step(state, "pros_cons")
        
        assert updated_state["current_step"] == "pros_cons"
        assert updated_state["user_query"] == state["user_query"]  # Other fields preserved
    
    def test_update_state_step_invalid_step_raises_error(self):
        """Test that invalid step raises ValueError."""
        documents = [Document(content="Test", metadata={})]
        state = create_initial_state("Test query", documents)
        
        with pytest.raises(ValueError, match="Invalid step: invalid_step"):
            update_state_step(state, "invalid_step")
    
    def test_update_state_step_all_valid_steps(self):
        """Test all valid step transitions."""
        documents = [Document(content="Test", metadata={})]
        state = create_initial_state("Test query", documents)
        
        valid_steps = ["option_finder", "pros_cons", "decision", "complete", "error"]
        
        for step in valid_steps:
            updated_state = update_state_step(state, step)
            assert updated_state["current_step"] == step


class TestAddErrorContext:
    """Test cases for add_error_context function."""
    
    def test_add_error_context_valid(self):
        """Test adding valid error context."""
        documents = [Document(content="Test", metadata={})]
        state = create_initial_state("Test query", documents)
        
        error_info = {
            "error_type": "LLM_API_ERROR",
            "message": "API rate limit exceeded",
            "timestamp": "2024-01-01T12:00:00"
        }
        
        updated_state = add_error_context(state, error_info)
        
        assert updated_state["error_context"] == error_info
        assert updated_state["current_step"] == "error"
    
    def test_add_error_context_invalid_error_info_raises_error(self):
        """Test that invalid error info raises ValueError."""
        documents = [Document(content="Test", metadata={})]
        state = create_initial_state("Test query", documents)
        
        with pytest.raises(ValueError, match="Error info must be a dictionary"):
            add_error_context(state, "invalid error info")


class TestValidateStateTransition:
    """Test cases for validate_state_transition function."""
    
    def test_validate_state_transition_valid_transitions(self):
        """Test valid state transitions."""
        valid_transitions = [
            ("option_finder", "pros_cons"),
            ("option_finder", "error"),
            ("pros_cons", "decision"),
            ("pros_cons", "error"),
            ("decision", "complete"),
            ("decision", "error"),
            ("error", "option_finder"),
            ("error", "pros_cons"),
            ("error", "decision")
        ]
        
        for current, next_step in valid_transitions:
            assert validate_state_transition(current, next_step) is True
    
    def test_validate_state_transition_invalid_transitions(self):
        """Test invalid state transitions."""
        invalid_transitions = [
            ("option_finder", "decision"),  # Skip pros_cons
            ("pros_cons", "complete"),      # Skip decision
            ("complete", "error"),          # From terminal state
            ("complete", "option_finder"),  # From terminal state
            ("decision", "option_finder"),  # Backward without error
        ]
        
        for current, next_step in invalid_transitions:
            assert validate_state_transition(current, next_step) is False
    
    def test_validate_state_transition_unknown_step(self):
        """Test transition from unknown step."""
        assert validate_state_transition("unknown_step", "pros_cons") is False
    
    def test_validate_state_transition_to_unknown_step(self):
        """Test transition to unknown step."""
        assert validate_state_transition("option_finder", "unknown_step") is False


class TestAgentStateIntegration:
    """Integration tests for AgentState workflow."""
    
    def test_complete_workflow_state_progression(self):
        """Test complete workflow state progression."""
        # Create initial state
        documents = [Document(content="Test option data", metadata={"source": "test.csv"})]
        state = create_initial_state("Find best investment option", documents)
        
        # Progress through workflow steps
        state = update_state_step(state, "pros_cons")
        assert state["current_step"] == "pros_cons"
        
        state = update_state_step(state, "decision")
        assert state["current_step"] == "decision"
        
        state = update_state_step(state, "complete")
        assert state["current_step"] == "complete"
        
        # Verify all original data is preserved
        assert state["user_query"] == "Find best investment option"
        assert len(state["uploaded_data"]) == 1
        assert state["uploaded_data"][0].content == "Test option data"
    
    def test_error_recovery_workflow(self):
        """Test error handling and recovery workflow."""
        documents = [Document(content="Test", metadata={})]
        state = create_initial_state("Test query", documents)
        
        # Simulate error during pros_cons step
        state = update_state_step(state, "pros_cons")
        error_info = {"error": "LLM API failed", "step": "pros_cons"}
        state = add_error_context(state, error_info)
        
        assert state["current_step"] == "error"
        assert state["error_context"] == error_info
        
        # Recovery: retry pros_cons step
        state = update_state_step(state, "pros_cons")
        assert state["current_step"] == "pros_cons"
        # Error context should still be available for debugging
        assert state["error_context"] == error_info