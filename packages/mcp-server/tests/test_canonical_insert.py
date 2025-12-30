"""
Test canonical table insertion to diagnose why entities aren't appearing in canonical tables.
"""

import sys
from pathlib import Path
import json

# Add paths
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "mcp-server"))

from healthsim.state.serializers import get_serializer, get_table_info, serialize_member, serialize_patient


def test_member_serializer_columns():
    """Check what columns serialize_member produces."""
    # Sample member data similar to what we have in scenario
    test_member = {
        "member_id": "RW-MBR-001",
        "patient_id": "RW-SD-001",
        "subscriber_id": "RW-SUB-001",
        "given_name": "John",
        "family_name": "Doe",
        "birth_date": "1980-01-15",
        "gender": "M",
        "plan_code": "BSCA-PPO-2024",
        "coverage_start": "2024-01-01",
        "relationship_code": "18"
    }
    
    serialized = serialize_member(test_member, {})
    print("=== Member Serializer Output ===")
    print(f"Keys produced: {sorted(serialized.keys())}")
    print(f"Values: {json.dumps({k: str(v) for k, v in serialized.items()}, indent=2)}")
    
    # Expected columns from table
    expected_columns = [
        'id', 'member_id', 'subscriber_id', 'relationship_code', 'ssn',
        'given_name', 'middle_name', 'family_name', 'birth_date', 'gender',
        'street_address', 'city', 'state', 'postal_code', 'phone', 'email',
        'group_id', 'plan_code', 'coverage_start', 'coverage_end', 'pcp_npi',
        'created_at', 'source_type', 'source_system', 'skill_used', 'generation_seed',
        'scenario_id'
    ]
    
    serialized_keys = set(serialized.keys())
    expected_keys = set(expected_columns)
    
    print("\n=== Column Analysis ===")
    missing_in_serializer = expected_keys - serialized_keys
    extra_in_serializer = serialized_keys - expected_keys
    
    print(f"Missing in serializer (expected by table): {missing_in_serializer}")
    print(f"Extra in serializer (not in table): {extra_in_serializer}")
    
    # This is the bug!
    if 'group_number' in extra_in_serializer and 'group_id' in missing_in_serializer:
        print("\n*** FOUND BUG: Serializer uses 'group_number' but table expects 'group_id' ***")


def test_patient_serializer_columns():
    """Check what columns serialize_patient produces."""
    test_patient = {
        "patient_id": "RW-SD-001",
        "mrn": "MRN-001",
        "given_name": "John",
        "family_name": "Doe",
        "birth_date": "1980-01-15",
        "gender": "male",
        "address": {
            "line1": "123 Main St",
            "city": "San Diego",
            "state": "CA",
            "postalCode": "92101"
        }
    }
    
    serialized = serialize_patient(test_patient, {})
    print("\n=== Patient Serializer Output ===")
    print(f"Keys produced: {sorted(serialized.keys())}")


def test_get_table_info():
    """Test table info mapping."""
    print("\n=== Table Info Mapping ===")
    for entity_type in ['patients', 'members', 'pcp_assignments', 'claims']:
        table_name, id_col = get_table_info(entity_type)
        serializer = get_serializer(entity_type)
        has_serializer = "✅" if serializer else "❌"
        print(f"{entity_type}: table={table_name}, id_col={id_col}, serializer={has_serializer}")


if __name__ == "__main__":
    test_member_serializer_columns()
    test_patient_serializer_columns()
    test_get_table_info()
