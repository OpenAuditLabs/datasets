from pydantic import BaseModel, Field, conlist
from typing import List, Dict, Any, Optional

# Define schema version
CURRENT_SCHEMA_VERSION = "1.0.0"

class Source(BaseModel):
    source_code: str
    source_type: str
    origin: str

class ToolLabels(BaseModel):
    slither: bool
    mythril: bool
    smartcheck: bool

class SeverityScore(BaseModel):
    cvss_v3: float
    confidence: float

class Location(BaseModel):
    lines: conlist(int, min_length=1)
    ast_nodes: conlist(str, min_length=1)

class Vulnerability(BaseModel):
    swc_id: str
    description: str
    tool_labels: ToolLabels
    severity_score: SeverityScore
    location: Location

class ExploitTrace(BaseModel):
    available: bool
    trace_steps: List[str]
    tool: str

class Patch(BaseModel):
    available: bool
    type: str
    diff: str
    validation_status: str
    test_coverage: float

class TaxonomyLinks(BaseModel):
    cve: Optional[str] = None
    erc_standard: Optional[str] = None

class UnifiedContractSchema(BaseModel):
    schema_version: str = Field(CURRENT_SCHEMA_VERSION, const=True)
    contract_id: str
    source: Source
    vulnerability: Vulnerability
    exploit_trace: ExploitTrace
    patch: Patch
    taxonomy_links: TaxonomyLinks

# Migration Utilities (Placeholder)
def migrate_schema(data: Dict[str, Any], target_version: str) -> Dict[str, Any]:
    """
    Migrates the given data to the target schema version.
    This is a placeholder and would contain actual migration logic.
    """
    current_version = data.get("schema_version")
    if not current_version:
        # Assume a very old version if not specified
        current_version = "0.0.0" 

    if current_version == target_version:
        return data
    
    # Example migration logic (this would be much more complex in a real scenario)
    if current_version < "1.0.0" and target_version == "1.0.0":
        # Apply changes needed to upgrade from pre-1.0.0 to 1.0.0
        # For now, just ensure the schema_version is set
        data["schema_version"] = "1.0.0"
    
    return data

# Example Usage and Validation
if __name__ == "__main__":
    # Example of valid data
    valid_data = {
        "contract_id": "0x123abc",
        "source": {
            "source_code": "pragma solidity ^0.8.0; contract MyContract {}",
            "source_type": "solidity",
            "origin": "etherscan"
        },
        "vulnerability": {
            "swc_id": "SWC-101",
            "description": "Integer Overflow",
            "tool_labels": {
                "slither": True,
                "mythril": False,
                "smartcheck": True
            },
            "severity_score": {
                "cvss_v3": 7.8,
                "confidence": 0.9
            },
            "location": {
                "lines": [10, 12],
                "ast_nodes": ["FunctionDefinition", "BinaryOperation"]
            }
        },
        "exploit_trace": {
            "available": True,
            "trace_steps": ["call foo()", "transfer ether"],
            "tool": "custom_exploit_tool"
        },
        "patch": {
            "available": True,
            "type": "source_code_diff",
            "diff": "--- a/contract.sol\n+++ b/contract.sol\n@@ -9,4 +9,5 @@\n",
            "validation_status": "verified",
            "test_coverage": 0.85
        },
        "taxonomy_links": {
            "cve": "CVE-2023-1234",
            "erc_standard": "ERC-20"
        }
    }

    try:
        contract = UnifiedContractSchema(**valid_data)
        print("Valid data parsed successfully:")
        print(contract.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error parsing valid data: {e}")

    # Example of invalid data
    invalid_data = {
        "contract_id": "0x123abc",
        "source": {
            "source_code": "pragma solidity ^0.8.0; contract MyContract {}",
            "source_type": "solidity",
            "origin": "etherscan"
        },
        "vulnerability": {
            "swc_id": "SWC-101",
            "description": "Integer Overflow",
            "tool_labels": {
                "slither": True,
                "mythril": False,
                "smartcheck": True
            },
            "severity_score": {
                "cvss_v3": 7.8,
                "confidence": 0.9
            },
            "location": {
                "lines": [], # Invalid: min_length=1
                "ast_nodes": ["FunctionDefinition"]
            }
        },
        "exploit_trace": {
            "available": True,
            "trace_steps": ["call foo()", "transfer ether"],
            "tool": "custom_exploit_tool"
        },
        "patch": {
            "available": True,
            "type": "source_code_diff",
            "diff": "--- a/contract.sol\n+++ b/contract.sol\n@@ -9,4 +9,5 @@\n",
            "validation_status": "verified",
            "test_coverage": 0.85
        },
        "taxonomy_links": {
            "cve": "CVE-2023-1234",
            "erc_standard": "ERC-20"
        }
    }

    print("\nAttempting to parse invalid data:")
    try:
        UnifiedContractSchema(**invalid_data)
    except Exception as e:
        print(f"Error parsing invalid data (as expected): {e}")

    # Example of migration
    old_data = {
        "contract_id": "0xold",
        "source": {
            "source_code": "old code",
            "source_type": "solidity",
            "origin": "old_source"
        },
        "vulnerability": {
            "swc_id": "SWC-000",
            "description": "Old vulnerability",
            "tool_labels": {
                "slither": False,
                "mythril": False,
                "smartcheck": False
            },
            "severity_score": {
                "cvss_v3": 0.0,
                "confidence": 0.0
            },
            "location": {
                "lines": [1],
                "ast_nodes": ["OldNode"]
            }
        },
        "exploit_trace": {
            "available": False,
            "trace_steps": [],
            "tool": ""
        },
        "patch": {
            "available": False,
            "type": "",
            "diff": "",
            "validation_status": "",
            "test_coverage": 0.0
        },
        "taxonomy_links": {}
    }
    print("\nAttempting to migrate old data:")
    migrated_data = migrate_schema(old_data, CURRENT_SCHEMA_VERSION)
    print(f"Migrated data (schema_version): {migrated_data.get('schema_version')}")
    try:
        UnifiedContractSchema(**migrated_data)
        print("Migrated data validated successfully.")
    except Exception as e:
        print(f"Error validating migrated data: {e}")
