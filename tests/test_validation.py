"""
Unit tests for validation utilities.

Tests file validation and security sanitization functions
to ensure proper input handling and security measures.
"""

import pytest
import tempfile
import os
from pathlib import Path
from multi_agent_decision_system.utils.validation import (
    validate_file_path, validate_file_size, validate_file_extension,
    validate_file_mime_type, validate_file_complete, sanitize_text_content,
    sanitize_metadata, calculate_file_checksum, get_supported_formats,
    FileValidationError, SecuritySanitizationError
)


class TestValidateFilePath:
    """Test cases for validate_file_path function."""
    
    def test_validate_file_path_valid_file(self):
        """Test validation of valid file path."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("test content")
            temp_path = f.name
        
        try:
            assert validate_file_path(temp_path) is True
        finally:
            os.unlink(temp_path)
    
    def test_validate_file_path_empty_string_raises_error(self):
        """Test that empty string raises FileValidationError."""
        with pytest.raises(FileValidationError, match="File path must be a non-empty string"):
            validate_file_path("")
    
    def test_validate_file_path_none_raises_error(self):
        """Test that None raises FileValidationError."""
        with pytest.raises(FileValidationError, match="File path must be a non-empty string"):
            validate_file_path(None)
    
    def test_validate_file_path_nonexistent_file_raises_error(self):
        """Test that non-existent file raises FileValidationError."""
        with pytest.raises(FileValidationError, match="File does not exist"):
            validate_file_path("nonexistent_file.txt")
    
    def test_validate_file_path_directory_raises_error(self):
        """Test that directory path raises FileValidationError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(FileValidationError, match="Path is not a file"):
                validate_file_path(temp_dir)


class TestValidateFileSize:
    """Test cases for validate_file_size function."""
    
    def test_validate_file_size_small_file(self):
        """Test validation of small file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("small content")
            temp_path = f.name
        
        try:
            assert validate_file_size(temp_path) is True
        finally:
            os.unlink(temp_path)
    
    def test_validate_file_size_large_file_raises_error(self):
        """Test that oversized file raises FileValidationError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            # Create a file larger than MAX_FILE_SIZE_MB (50MB)
            large_content = "x" * (51 * 1024 * 1024)  # 51MB
            f.write(large_content)
            temp_path = f.name
        
        try:
            with pytest.raises(FileValidationError, match="File size .* exceeds maximum allowed size"):
                validate_file_size(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_validate_file_size_nonexistent_file_raises_error(self):
        """Test that non-existent file raises FileValidationError."""
        with pytest.raises(FileValidationError, match="Could not check file size"):
            validate_file_size("nonexistent_file.txt")


class TestValidateFileExtension:
    """Test cases for validate_file_extension function."""
    
    def test_validate_file_extension_allowed_extensions(self):
        """Test validation of allowed file extensions."""
        allowed_files = [
            "test.csv",
            "test.json",
            "test.txt",
            "test.md",
            "TEST.CSV",  # Case insensitive
        ]
        
        for file_path in allowed_files:
            assert validate_file_extension(file_path) is True
    
    def test_validate_file_extension_disallowed_extension_raises_error(self):
        """Test that disallowed extension raises FileValidationError."""
        disallowed_files = [
            "test.exe",
            "test.pdf",
            "test.docx",
            "test.py"
        ]
        
        for file_path in disallowed_files:
            with pytest.raises(FileValidationError, match="File extension .* not allowed"):
                validate_file_extension(file_path)


class TestValidateFileMimeType:
    """Test cases for validate_file_mime_type function."""
    
    def test_validate_file_mime_type_allowed_types(self):
        """Test validation of allowed MIME types."""
        allowed_files = [
            "test.csv",
            "test.json",
            "test.txt",
            "test.md"
        ]
        
        for file_path in allowed_files:
            assert validate_file_mime_type(file_path) is True
    
    def test_validate_file_mime_type_disallowed_type_raises_error(self):
        """Test that disallowed MIME type raises FileValidationError."""
        with pytest.raises(FileValidationError, match="File MIME type .* not allowed"):
            validate_file_mime_type("test.exe")


class TestValidateFileComplete:
    """Test cases for validate_file_complete function."""
    
    def test_validate_file_complete_valid_file(self):
        """Test complete validation of valid file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("test content")
            temp_path = f.name
        
        try:
            is_valid, info = validate_file_complete(temp_path)
            
            assert is_valid is True
            assert info["file_path"] == temp_path
            assert info["file_size_mb"] > 0
            assert info["extension"] == ".txt"
            assert info["mime_type"] == "text/plain"
            assert len(info["checksum"]) == 64  # SHA-256 hex length
        finally:
            os.unlink(temp_path)
    
    def test_validate_file_complete_invalid_file_raises_error(self):
        """Test complete validation of invalid file."""
        with pytest.raises(FileValidationError):
            validate_file_complete("nonexistent_file.txt")


class TestSanitizeTextContent:
    """Test cases for sanitize_text_content function."""
    
    def test_sanitize_text_content_clean_text(self):
        """Test sanitization of clean text."""
        clean_text = "This is clean text with numbers 123 and symbols !@#"
        result = sanitize_text_content(clean_text)
        assert result == clean_text
    
    def test_sanitize_text_content_removes_script_tags(self):
        """Test removal of script tags."""
        malicious_text = "Clean text <script>alert('xss')</script> more text"
        result = sanitize_text_content(malicious_text)
        assert "<script>" not in result
        assert "alert" not in result
        assert "Clean text" in result
        assert "more text" in result
    
    def test_sanitize_text_content_removes_javascript_urls(self):
        """Test removal of JavaScript URLs."""
        malicious_text = "Click here: javascript:alert('xss') for more info"
        result = sanitize_text_content(malicious_text)
        assert "javascript:" not in result
        assert "alert" not in result
        assert "Click here:" in result
        assert "for more info" in result
    
    def test_sanitize_text_content_removes_event_handlers(self):
        """Test removal of event handlers."""
        malicious_text = "Text with onclick=alert('xss') handler"
        result = sanitize_text_content(malicious_text)
        assert "onclick=" not in result
    
    def test_sanitize_text_content_removes_control_characters(self):
        """Test removal of control characters."""
        text_with_nulls = "Text with\x00null\x01control\x02chars"
        result = sanitize_text_content(text_with_nulls)
        assert "\x00" not in result
        assert "\x01" not in result
        assert "\x02" not in result
        assert result == "Text withnullcontrolchars"
    
    def test_sanitize_text_content_preserves_newlines_tabs(self):
        """Test preservation of newlines and tabs."""
        text_with_whitespace = "Line 1\nLine 2\tTabbed"
        result = sanitize_text_content(text_with_whitespace)
        assert result == text_with_whitespace
    
    def test_sanitize_text_content_limits_length(self):
        """Test length limiting for very long content."""
        very_long_text = "x" * 1_000_001  # Longer than 1MB limit
        result = sanitize_text_content(very_long_text)
        assert len(result) == 1_000_000
    
    def test_sanitize_text_content_invalid_input_raises_error(self):
        """Test that non-string input raises SecuritySanitizationError."""
        with pytest.raises(SecuritySanitizationError, match="Content must be a string"):
            sanitize_text_content(123)


class TestSanitizeMetadata:
    """Test cases for sanitize_metadata function."""
    
    def test_sanitize_metadata_clean_data(self):
        """Test sanitization of clean metadata."""
        clean_metadata = {
            "title": "Clean Title",
            "count": 42,
            "active": True,
            "tags": ["tag1", "tag2"]
        }
        result = sanitize_metadata(clean_metadata)
        assert result == clean_metadata
    
    def test_sanitize_metadata_sanitizes_string_values(self):
        """Test sanitization of string values in metadata."""
        dirty_metadata = {
            "title": "Title with <script>alert('xss')</script>",
            "description": "Description with javascript:alert('xss')"
        }
        result = sanitize_metadata(dirty_metadata)
        
        assert "<script>" not in result["title"]
        assert "javascript:" not in result["description"]
    
    def test_sanitize_metadata_handles_nested_dict(self):
        """Test sanitization of nested dictionaries."""
        nested_metadata = {
            "info": {
                "title": "Title with <script>alert('xss')</script>",
                "nested": {
                    "deep": "Deep value with javascript:alert('xss')"
                }
            }
        }
        result = sanitize_metadata(nested_metadata)
        
        assert "<script>" not in result["info"]["title"]
        assert "javascript:" not in result["info"]["nested"]["deep"]
    
    def test_sanitize_metadata_limits_list_size(self):
        """Test limiting of large lists."""
        large_list_metadata = {
            "tags": ["tag"] * 150  # Larger than 100 item limit
        }
        result = sanitize_metadata(large_list_metadata)
        assert len(result["tags"]) == 100
    
    def test_sanitize_metadata_limits_key_length(self):
        """Test limiting of long keys."""
        long_key_metadata = {
            "x" * 150: "value"  # Longer than 100 char limit
        }
        result = sanitize_metadata(long_key_metadata)
        
        long_key = list(result.keys())[0]
        assert len(long_key) == 100
    
    def test_sanitize_metadata_invalid_input_raises_error(self):
        """Test that non-dict input raises SecuritySanitizationError."""
        with pytest.raises(SecuritySanitizationError, match="Metadata must be a dictionary"):
            sanitize_metadata("not a dict")


class TestCalculateFileChecksum:
    """Test cases for calculate_file_checksum function."""
    
    def test_calculate_file_checksum_valid_file(self):
        """Test checksum calculation for valid file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("test content for checksum")
            temp_path = f.name
        
        try:
            checksum = calculate_file_checksum(temp_path)
            assert len(checksum) == 64  # SHA-256 hex length
            assert isinstance(checksum, str)
            
            # Verify consistency
            checksum2 = calculate_file_checksum(temp_path)
            assert checksum == checksum2
        finally:
            os.unlink(temp_path)
    
    def test_calculate_file_checksum_nonexistent_file_raises_error(self):
        """Test that non-existent file raises FileValidationError."""
        with pytest.raises(FileValidationError, match="Could not calculate file checksum"):
            calculate_file_checksum("nonexistent_file.txt")


class TestGetSupportedFormats:
    """Test cases for get_supported_formats function."""
    
    def test_get_supported_formats_returns_correct_info(self):
        """Test that supported formats info is correct."""
        formats = get_supported_formats()
        
        assert "extensions" in formats
        assert "mime_types" in formats
        assert "max_size_mb" in formats
        
        assert ".csv" in formats["extensions"]
        assert ".json" in formats["extensions"]
        assert ".txt" in formats["extensions"]
        assert ".md" in formats["extensions"]
        
        assert "text/csv" in formats["mime_types"]
        assert "application/json" in formats["mime_types"]
        assert "text/plain" in formats["mime_types"]
        
        assert formats["max_size_mb"] == 50