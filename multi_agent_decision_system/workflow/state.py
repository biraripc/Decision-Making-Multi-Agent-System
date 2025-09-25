"""
State management for LangGraph workflow orchestration.

This module defines the AgentState TypedDict and related state management
utilities for coordinating the multi-agent decision-making workflow.
"""

from typing import TypedDict, List, Optional, Dict, Any
from multi_agent_decision_system.data_processing.models import (
    Document, Option, Analysis, Recommendation
)


class AgentState(TypedDict):
    """
    State dictionary for LangGraph workflow management.
    
    Tracks the current state of the multi-agent workflow including
    user input, processed data, and results from each agent.
    """
    # User inputs
    user_query: str
    uploaded_data: List[Document]
    
    # Agent outputs
    found_options: List[Option]
    analyses: List[Analysis]
    recommendations: List[Recommendation]
    
    # Workflow management
    current_step: str
    error_context: Optional[Dict[str, Any]]
    
    # Processing metadata
    processing_metadata: Dict[str, Any]


def create_initial_state(user_query: str, uploaded_data: List[Document]) -> AgentState:
    """
    Create an initial AgentState for workflow execution.
    
    Args:
        user_query: The user's decision-making query
        uploaded_data: List of processed documents from file upload
        
    Returns:
        AgentState: Initial state dictionary for LangGraph workflow
        
    Raises:
        ValueError: If user_query is empty or uploaded_data is invalid
    """
    if not user_query or not isinstance(user_query, str):
        raise ValueError("User query must be a non-empty string")
    
    if not uploaded_data or not isinstance(uploaded_data, list):
        raise ValueError("Uploaded data must be a non-empty list")
    
    if not all(isinstance(doc, Document) for doc in uploaded_data):
        raise ValueError("All uploaded data items must be Document instances")
    
    return AgentState(
        user_query=user_query,
        uploaded_data=uploaded_data,
        found_options=[],
        analyses=[],
        recommendations=[],
        current_step="option_finder",
        error_context=None,
        processing_metadata={
            "start_time": None,
            "total_documents": len(uploaded_data),
            "workflow_version": "1.0"
        }
    )


def update_state_step(state: AgentState, new_step: str) -> AgentState:
    """
    Update the current workflow step in the state.
    
    Args:
        state: Current AgentState
        new_step: New workflow step name
        
    Returns:
        AgentState: Updated state with new step
    """
    valid_steps = ["option_finder", "pros_cons", "decision", "complete", "error"]
    
    if new_step not in valid_steps:
        raise ValueError(f"Invalid step: {new_step}. Must be one of {valid_steps}")
    
    updated_state = state.copy()
    updated_state["current_step"] = new_step
    return updated_state


def add_error_context(state: AgentState, error_info: Dict[str, Any]) -> AgentState:
    """
    Add error context to the state for debugging and recovery.
    
    Args:
        state: Current AgentState
        error_info: Dictionary containing error details
        
    Returns:
        AgentState: Updated state with error context
    """
    if not isinstance(error_info, dict):
        raise ValueError("Error info must be a dictionary")
    
    updated_state = state.copy()
    updated_state["error_context"] = error_info
    updated_state["current_step"] = "error"
    return updated_state


def validate_state_transition(current_step: str, next_step: str) -> bool:
    """
    Validate that a state transition is allowed in the workflow.
    
    Args:
        current_step: Current workflow step
        next_step: Proposed next step
        
    Returns:
        bool: True if transition is valid, False otherwise
    """
    valid_transitions = {
        "option_finder": ["pros_cons", "error"],
        "pros_cons": ["decision", "error"],
        "decision": ["complete", "error"],
        "error": ["option_finder", "pros_cons", "decision"],  # Allow recovery
        "complete": []  # Terminal state
    }
    
    return next_step in valid_transitions.get(current_step, [])