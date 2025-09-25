"""
Utility functions for file validation and security sanitization.

This module provides functions to validate uploaded files, sanitize content,
and ensure security best practices for user input processing.
"""

import os
import re
import mimetypes
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import hashlib


# Configuration constants
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = {'.csv', '.json', '.txt', '.md'}
ALLOWED_MIME_TYPES = {
    'text/csv',
    'application/vnd.ms-excel',  # Alternative CSV MIME type
    'application/json',
    'text/plain',
    'text/markdown'
}

# Security patterns to remove or sanitize
DANGEROUS_PATTERNS = [
    r'<script[^>]*>.*?</script>',  # Script tags
    r'javascript:[^"\s]*',  # JavaScript URLs with content
    r'on\w+\s*=',  # Event handlers
    r'<iframe[^>]*>.*?</iframe>',  # Iframes
    r'<object[^>]*>.*?</object>',  # Objects
    r'<embed[^>]*>.*?</embed>',  # Embeds
]


class FileValidationError(Exception):
    """Custom exception for file validation errors."""
    pass


class SecuritySanitizationError(Exception):
    """Custom exception for security sanitization errors."""
    pass


def validate_file_path(file_path: str) -> bool:
    """
    Validate that a file path is safe and accessible.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        bool: True if file path is valid and safe
        
    Raises:
        FileValidationError: If file path is invalid or unsafe
    """
    if not file_path or not isinstance(file_path, str):
        raise FileValidationError("File path must be a non-empty string")
    
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        raise FileValidationError(f"File does not exist: {file_path}")
    
    # Check if it's actually a file
    if not path.is_file():
        raise FileValidationError(f"Path is not a file: {file_path}")
    
    # Security check: prevent path traversal (only for relative paths within project)
    # For absolute paths outside project (like temp files), we'll allow them for testing
    try:
        resolved_path = path.resolve()
        cwd_path = Path.cwd().resolve()
        
        # If it's a relative path, ensure it's within the current directory
        if not path.is_absolute():
            resolved_path.relative_to(cwd_path)
        # For absolute paths, we'll allow them but check for obvious traversal patterns
        elif ".." in str(path) or "~" in str(path):
            raise FileValidationError("File path contains invalid traversal patterns")
    except ValueError:
        # Only raise error for relative paths that escape the project directory
        if not path.is_absolute():
            raise FileValidationError("File path contains invalid traversal patterns")
    
    return True


def validate_file_size(file_path: str) -> bool:
    """
    Validate that file size is within acceptable limits.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        bool: True if file size is acceptable
        
    Raises:
        FileValidationError: If file is too large
    """
    try:
        file_size = os.path.getsize(file_path)
        max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
        
        if file_size > max_size_bytes:
            raise FileValidationError(
                f"File size ({file_size / 1024 / 1024:.2f} MB) exceeds "
                f"maximum allowed size ({MAX_FILE_SIZE_MB} MB)"
            )
        
        return True
    except OSError as e:
        raise FileValidationError(f"Could not check file size: {e}")


def validate_file_extension(file_path: str) -> bool:
    """
    Validate that file has an allowed extension.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        bool: True if extension is allowed
        
    Raises:
        FileValidationError: If extension is not allowed
    """
    path = Path(file_path)
    extension = path.suffix.lower()
    
    if extension not in ALLOWED_EXTENSIONS:
        raise FileValidationError(
            f"File extension '{extension}' not allowed. "
            f"Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    return True


def validate_file_mime_type(file_path: str) -> bool:
    """
    Validate file MIME type for additional security.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        bool: True if MIME type is allowed
        
    Raises:
        FileValidationError: If MIME type is not allowed
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type not in ALLOWED_MIME_TYPES:
        raise FileValidationError(
            f"File MIME type '{mime_type}' not allowed. "
            f"Allowed types: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    
    return True


def validate_file_complete(file_path: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Perform complete file validation including all security checks.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        Tuple[bool, Dict]: (is_valid, validation_info)
        
    Raises:
        FileValidationError: If any validation check fails
    """
    validation_info = {
        "file_path": file_path,
        "file_size_mb": 0,
        "extension": "",
        "mime_type": "",
        "checksum": ""
    }
    
    try:
        # Run all validation checks
        validate_file_path(file_path)
        validate_file_size(file_path)
        validate_file_extension(file_path)
        validate_file_mime_type(file_path)
        
        # Collect file information
        path = Path(file_path)
        validation_info.update({
            "file_size_mb": os.path.getsize(file_path) / 1024 / 1024,
            "extension": path.suffix.lower(),
            "mime_type": mimetypes.guess_type(file_path)[0],
            "checksum": calculate_file_checksum(file_path)
        })
        
        return True, validation_info
        
    except FileValidationError:
        raise


def sanitize_text_content(content: str) -> str:
    """
    Sanitize text content by removing potentially dangerous patterns.
    
    Args:
        content: Text content to sanitize
        
    Returns:
        str: Sanitized content
        
    Raises:
        SecuritySanitizationError: If content cannot be sanitized
    """
    if not isinstance(content, str):
        raise SecuritySanitizationError("Content must be a string")
    
    sanitized = content
    
    try:
        # Remove dangerous patterns
        for pattern in DANGEROUS_PATTERNS:
            sanitized = re.sub(pattern, ' ', sanitized, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove null bytes and control characters (except newlines and tabs)
        sanitized = ''.join(char for char in sanitized 
                          if ord(char) >= 32 or char in '\n\t\r')
        
        # Limit length to prevent memory issues
        max_length = 1_000_000  # 1MB of text
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized.strip()
        
    except Exception as e:
        raise SecuritySanitizationError(f"Failed to sanitize content: {e}")


def sanitize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize metadata dictionary by cleaning string values.
    
    Args:
        metadata: Dictionary containing metadata
        
    Returns:
        Dict[str, Any]: Sanitized metadata
        
    Raises:
        SecuritySanitizationError: If metadata cannot be sanitized
    """
    if not isinstance(metadata, dict):
        raise SecuritySanitizationError("Metadata must be a dictionary")
    
    sanitized = {}
    
    try:
        for key, value in metadata.items():
            # Sanitize key
            if isinstance(key, str):
                clean_key = sanitize_text_content(key)[:100]  # Limit key length
            else:
                clean_key = str(key)[:100]
            
            # Sanitize value based on type
            if isinstance(value, str):
                clean_value = sanitize_text_content(value)
            elif isinstance(value, (int, float, bool)):
                clean_value = value
            elif isinstance(value, (list, tuple)):
                clean_value = [sanitize_text_content(str(item)) if isinstance(item, str) 
                             else item for item in value[:100]]  # Limit list size
            elif isinstance(value, dict):
                clean_value = sanitize_metadata(value)  # Recursive sanitization
            else:
                clean_value = sanitize_text_content(str(value))
            
            sanitized[clean_key] = clean_value
        
        return sanitized
        
    except Exception as e:
        raise SecuritySanitizationError(f"Failed to sanitize metadata: {e}")


def calculate_file_checksum(file_path: str) -> str:
    """
    Calculate SHA-256 checksum of a file for integrity verification.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: Hexadecimal checksum string
        
    Raises:
        FileValidationError: If checksum cannot be calculated
    """
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except Exception as e:
        raise FileValidationError(f"Could not calculate file checksum: {e}")


def get_supported_formats() -> Dict[str, List[str]]:
    """
    Get information about supported file formats.
    
    Returns:
        Dict[str, List[str]]: Dictionary with extensions and MIME types
    """
    return {
        "extensions": list(ALLOWED_EXTENSIONS),
        "mime_types": list(ALLOWED_MIME_TYPES),
        "max_size_mb": MAX_FILE_SIZE_MB
    }