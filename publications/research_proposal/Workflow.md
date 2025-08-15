# Workflow for Building the OpenAuditBenchmark Dataset

**Key Recommendation:**  
Establish clear, phased milestones — from initial dataset assessment through public release — ensuring **modularity**, **reproducibility**, and **governance** at every step.

---

## Phase 1: Assessment & Planning

### 1. Inventory Existing Sources
- Collect metadata and access points for:
  - SC-Bench
  - AutoMESC
  - VulnContractSet
  - SolidiFI-A
  - SolidiFI-BugLab
  - SWC Registry
  - SmartBugs
  - ContractWard
  - Any in-house audit repositories

### 2. Gap Analysis
- Compare coverage across:
  - SWC IDs
  - Real vs. synthetic samples
  - Patch availability
  - Severity labels
  - Exploit traces
  - Test suites
- Identify underrepresented domains:
  - L2 rollups
  - NFTs
  - DAOs

### 3. Specification of Requirements
- Finalize unified schema fields:
  - `contract_id`
  - `source`
  - Vulnerability metadata
  - `exploit_trace`
  - `patch`
  - `taxonomy_links`
- Define quality metrics:
  - AAS (Annotation Accuracy Score)
  - DDI (Data Diversity Index)
  - PVR (Patch Validation Rate)
  - SDB (Schema Definition Baseline)
- Define release tiers:
  - Public
  - Research
  - Red Team

### 4. Project Kickoff & Governance
- Form cross-functional team:
  - Security auditors
  - Data engineers
  - LLM specialists
- Establish steering committee to approve:
  - Access controls
  - Redaction policies
  - Release protocols

---

## Phase 2: Data Ingestion & Harmonization

### 1. Automated Harvesters
- Implement connectors to fetch:
  - Code
  - Annotations
  - Fixes
  - Traces from each source
- Create normalization scripts to convert formats (JSON, CSV, AST dumps) into the unified schema

### 2. Schema Validation Engine
- Build a lightweight pipeline to verify:
  - Required fields
  - Type constraints
  - Provenance tags
- Reject or flag records missing critical annotations (e.g., missing SWC tag or patch diff)

### 3. Multi-Tool Label Aggregation
- Run tools on every sample:
  - Slither
  - Mythril
  - SmartCheck
  - Semgrep
- Populate `tool_labels`
- Compute:
  - Majority-vote fields
  - Confidence scores
