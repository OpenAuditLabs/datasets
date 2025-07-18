# OpenAuditBenchmark: A Dataset for Agentic AI in Smart Contract Vulnerability Detection, Prioritization, and Patch Suggestion

## 1. Title

**OpenAuditBenchmark: A Dataset for Agentic AI in Smart Contract Vulnerability Detection, Prioritization, and Patch Suggestion**

---

## 2. Background and Motivation

The rapid expansion of decentralized applications (dApps) has elevated the role of smart contract security. Despite advances in detection tools and large language models (LLMs), a key bottleneck in developing autonomous (agentic) systems for vulnerability detection and remediation remains the lack of standardized, high-quality datasets that include:

- Real-world vulnerability patterns  
- Ground-truth severity scores  
- Human-curated and machine-generated patch suggestions  
- Execution traces or exploit payloads  

Without such a benchmark, evaluating and training agentic systems becomes inconsistent, biased, or fragmented. This proposal aims to fill that gap by designing and curating a public dataset tailored for agentic AI research in the blockchain security domain.

---

## 3. Problem Statement

There is no widely accepted dataset that supports the full cycle of tasks needed by agentic AI frameworks: vulnerability detection, scoring, patch generation, and patch validation. Existing datasets either focus on isolated bug instances (e.g., SWC Registry) or synthetic contracts with limited real-world relevance. This proposal aims to build a dataset that meets the following needs:

- Realistic and diverse smart contracts (real-world + adversarial examples)  
- Multi-modal annotations (code, exploit, patch, metadata, CVSS-like scores)  
- Benchmark compatibility for zero-shot, few-shot, and RL-based learning agents  

---

## 4. Objectives

- **O1**: Primarily, we aim to identify and evaluate existing smart contract datasets that align with the Smart Contract Weakness Classification (SWC) registry. These include datasets containing real-world or synthetic smart contracts labeled with specific vulnerability types defined by the SWC taxonomy.

- **O2**: If existing datasets prove insufficient—due to lack of vulnerability diversity, outdated formats, missing severity scores, or lack of exploit/fix annotations—we will proceed to curate our own dataset of smart contracts and augment it with necessary metadata.

- **O3**: Annotate each contract with SWC-based vulnerability tags, severity scores (inspired by CVSS), and corresponding fix rationales (either human-authored or LLM-generated).

- **O4**: Include exploit traces, dynamic execution metrics, and sandbox test results to enable patch validation and downstream reinforcement learning.

- **O5**: Provide a standardized benchmark format that supports multiple downstream tasks, including:  
  - Vulnerability classification  
  - Severity scoring  
  - Patch generation  
  - Patch verification

- **O6**: Release the dataset as **OpenAuditBenchmark**, alongside evaluation scripts, baseline models, and documentation to foster reproducible research and open collaboration in agentic AI for smart contract security.

---

## 5. Methodology

### 5.1 Data Sources

- SWC Registry (Smart Contract Weakness Classification)  
- Real exploits from platforms like **Etherscan**, **Ethernaut**, and **Damn Vulnerable DeFi**  
- GitHub repositories containing audit reports and remediation histories  
- Curated StackOverflow code snippets and bug bounty disclosures  

### 5.2 Annotation Schema

Each sample will include:

- `contract_id`: Unique identifier  
- `source_code`: Original Solidity code  
- `vulnerability`: SWC category and textual description  
- `cvss_score`: Standardized severity score  
- `exploit_trace`: Execution trace from symbolic/concrete execution (if available)  
- `fix_patch`: Human-written or LLM-generated patch  
- `validation_status`: Pass/fail status based on sandbox validation  

### 5.3 Toolchain

- **Static analysis**: Slither, Mythril, Semgrep  
- **Dynamic analysis**: Echidna, Manticore  
- **LLM augmentation**: GPT-4, LLaMA-3, Claude  
- **Manual review**: Validation by security auditors  

### 5.4 Benchmark Tasks

| Task                      | Input            | Output         | Metric                  |
|---------------------------|------------------|----------------|--------------------------|
| T1: Vulnerability Detection | Solidity code     | List of issues | Precision / Recall / F1 |
| T2: Severity Scoring       | Issue description | CVSS score     | MSE, Rank Correlation   |
| T3: Patch Generation       | Code + issue      | Code diff      | Patch Accuracy          |
| T4: Patch Validation       | Patched code      | Pass/Fail      | Test Case Pass Rate     |

---

## 6. Expected Outcomes

- A public benchmark dataset named **OpenAuditBenchmark**  
- Evaluation leaderboards for LLMs, GNNs, and RL agents  
- Research publications demonstrating fine-tuning and zero-shot performance  
- Foundation for future competitions and shared evaluation practices in Web3 security  

---

## 7. Team & Collaboration

We will invite collaboration from:

- Blockchain security researchers  
- Smart contract audit firms (e.g., Trail of Bits, OpenZeppelin)  
- LLM and reinforcement learning researchers  
- Academic labs working on software security and AI4Code  

---

## 8. Impact

This dataset will catalyze research at the intersection of smart contract security and agentic AI. By offering a high-quality benchmark with diverse annotations, it can help establish agentic auditing as a scalable solution in security workflows, while enabling reproducibility, comparability, and openness across future research.

---
