"""Tests for HealthSim MCP Profile Server."""

import pytest
import json
from pathlib import Path
from unittest.mock import patch
import tempfile

from healthsim.mcp.profile_server import (
    format_profile_summary,
    format_profile_list,
    format_template_list,
    format_execution_result,
    format_error,
    format_success,
    handle_build_profile,
    handle_save_profile,
    handle_load_profile,
    handle_list_profiles,
    handle_list_profile_templates,
    handle_list_journey_templates,
    handle_get_journey_template,
)
from healthsim.generation.profile_schema import (
    ProfileSpecification,
    GenerationSpec,
    DemographicsSpec,
    DistributionSpec,
    DistributionType,
    ClinicalSpec,
    ConditionSpec,
)
from healthsim.generation.profile_executor import ExecutionResult, ValidationReport


class TestFormatProfileSummary:
    """Tests for format_profile_summary."""

    def test_basic_profile(self):
        """Test formatting a basic profile."""
        profile = ProfileSpecification(
            id="test-profile-001",
            name="Test Profile",
            version="1.0",
            generation=GenerationSpec(count=50, products=["patientsim"]),
        )
        result = format_profile_summary(profile)
        
        assert "Test Profile" in result
        assert "test-profile-001" in result
        assert "50" in result
        assert "patientsim" in result

    def test_profile_with_demographics(self):
        """Test formatting profile with demographics."""
        profile = ProfileSpecification(
            id="test-demo-001",
            name="Demo Profile",
            generation=GenerationSpec(count=100),
            demographics=DemographicsSpec(
                age=DistributionSpec(
                    type=DistributionType.NORMAL,
                    mean=72.0,
                    std_dev=8.0,
                )
            ),
        )
        result = format_profile_summary(profile)
        
        assert "Demographics" in result
        assert "72" in result

    def test_profile_with_clinical(self):
        """Test formatting profile with clinical specs."""
        profile = ProfileSpecification(
            id="test-clinical-001",
            name="Clinical Profile",
            clinical=ClinicalSpec(
                primary_condition=ConditionSpec(
                    code="E11",
                    description="Type 2 Diabetes",
                )
            ),
        )
        result = format_profile_summary(profile)
        
        assert "Clinical" in result
        assert "E11" in result
        assert "Diabetes" in result


class TestFormatProfileList:
    """Tests for format_profile_list."""

    def test_empty_list(self):
        """Test formatting empty profile list."""
        result = format_profile_list([])
        assert "No saved profiles" in result

    def test_profile_list(self):
        """Test formatting profile list."""
        profiles = [
            {"name": "Profile 1", "id": "profile-1", "description": "First profile"},
            {"name": "Profile 2", "id": "profile-2"},
        ]
        result = format_profile_list(profiles)
        
        assert "Profile 1" in result
        assert "profile-1" in result
        assert "First profile" in result
        assert "Profile 2" in result


class TestFormatTemplateList:
    """Tests for format_template_list."""

    def test_template_list(self):
        """Test formatting template list."""
        templates = {
            "medicare-standard": {"description": "Medicare population"},
            "commercial-family": {"name": "Family Coverage"},
        }
        result = format_template_list(templates, "profile")
        
        assert "Profile Templates" in result
        assert "medicare-standard" in result
        assert "commercial-family" in result


class TestFormatExecutionResult:
    """Tests for format_execution_result."""

    def test_basic_result(self):
        """Test formatting execution result."""
        result = ExecutionResult(
            profile_id="test-profile-001",
            count=100,
            seed=12345,
            entities=[],  # Empty for this test
            duration_seconds=1.5,
            validation=ValidationReport(),  # Empty report = passed
        )
        formatted = format_execution_result(result)
        
        assert "100" in formatted
        assert "12345" in formatted
        assert "1.5" in formatted
        assert "Passed" in formatted

    def test_result_with_warnings(self):
        """Test formatting result with warnings."""
        result = ExecutionResult(
            profile_id="test-profile-002",
            count=50,
            seed=42,
            entities=[],
            duration_seconds=0.8,
            validation=ValidationReport(
                warnings=["Age distribution slightly skewed"],
            ),
        )
        formatted = format_execution_result(result)
        
        assert "Warnings: 1" in formatted


class TestUtilityFormatters:
    """Tests for utility formatting functions."""

    def test_format_error(self):
        """Test error message formatting."""
        result = format_error("Something went wrong")
        assert "Error" in result
        assert "Something went wrong" in result

    def test_format_success(self):
        """Test success message formatting."""
        result = format_success("Operation completed")
        assert "✓" in result
        assert "Operation completed" in result


@pytest.mark.asyncio
class TestBuildProfileHandler:
    """Tests for build_profile handler."""

    async def test_build_basic_profile(self):
        """Test building a basic profile."""
        result = await handle_build_profile({"name": "Test Profile"})
        
        assert len(result) == 1
        text = result[0].text
        assert "Test Profile" in text
        assert "test-profile" in text

    async def test_build_profile_with_id(self):
        """Test building profile with custom ID."""
        result = await handle_build_profile({
            "name": "My Profile",
            "id": "custom-id-001",
        })
        
        text = result[0].text
        assert "custom-id-001" in text

    async def test_build_profile_with_demographics(self):
        """Test building profile with demographics."""
        result = await handle_build_profile({
            "name": "Demo Profile",
            "age_mean": 65,
            "age_std": 10,
            "age_min": 50,
            "age_max": 85,
        })
        
        text = result[0].text
        assert "Demographics" in text

    async def test_build_profile_with_clinical(self):
        """Test building profile with clinical specs."""
        result = await handle_build_profile({
            "name": "Clinical Profile",
            "primary_condition_code": "E11",
            "primary_condition_name": "Type 2 Diabetes",
        })
        
        text = result[0].text
        assert "E11" in text


@pytest.mark.asyncio
class TestSaveLoadProfileHandlers:
    """Tests for save/load profile handlers."""

    async def test_save_and_list_profiles(self):
        """Test saving and listing profiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            profiles_dir = Path(tmpdir)
            
            # Patch the storage directory
            with patch("healthsim.mcp.profile_server.PROFILES_DIR", profiles_dir):
                # Create a profile
                profile = ProfileSpecification(
                    id="test-save-001",
                    name="Test Save Profile",
                    generation=GenerationSpec(count=10),
                )
                
                # Save it
                result = await handle_save_profile({
                    "profile_json": profile.to_json(),
                })
                
                assert "✓" in result[0].text or "Saved" in result[0].text

    async def test_load_profile_not_found(self):
        """Test loading non-existent profile."""
        with tempfile.TemporaryDirectory() as tmpdir:
            profiles_dir = Path(tmpdir)
            
            with patch("healthsim.mcp.profile_server.PROFILES_DIR", profiles_dir):
                result = await handle_load_profile({"name": "nonexistent"})
                
                text = result[0].text
                assert "not found" in text.lower() or "error" in text.lower()


@pytest.mark.asyncio
class TestTemplateHandlers:
    """Tests for template listing handlers."""

    async def test_list_profile_templates(self):
        """Test listing profile templates."""
        result = await handle_list_profile_templates({})
        
        text = result[0].text
        assert "Template" in text

    async def test_list_journey_templates(self):
        """Test listing journey templates."""
        result = await handle_list_journey_templates({})
        
        text = result[0].text
        assert "Template" in text or "journey" in text.lower()

    async def test_get_journey_template_not_found(self):
        """Test getting non-existent journey template."""
        result = await handle_get_journey_template({
            "template_name": "nonexistent-template"
        })
        
        text = result[0].text
        assert "not found" in text.lower() or "error" in text.lower()
