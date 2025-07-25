# OpenAuditBenchmark: A Dataset for Agentic AI in Smart Contract Vulnerability Detection, Prioritization, and Patch Suggestion

## Abstract

The evolving landscape of decentralized applications (dApps) has amplified the critical need for secure and verifiable smart contracts. While advances in static analyzers and large language models (LLMs) show promise, a core challenge remains: the absence of a comprehensive, standardized dataset that supports the full agentic AI lifecycle—vulnerability detection, severity scoring, patch generation, and patch validation. Existing datasets such as SC-Bench and AutoMESC provide valuable yet fragmented resources, often differing in format, scope, or focus (e.g., synthetic bugs vs. real-world exploits, detection-only vs. fix-pair annotations).

This proposal introduces **OpenAuditBenchmark**, a unified and extensible dataset designed to consolidate and standardize heterogeneous data sources—including SC-Bench, AutoMESC, SWC Registry, and curated real-world exploit examples—into a cohesive schema. The benchmark will feature multi-modal annotations (code, vulnerability tags, severity scores, exploit traces, and fix patches), enabling zero-shot, few-shot, and reinforcement learning paradigms. Our goal is to foster reproducibility, rigorous evaluation, and collaboration across the smart contract security and AI research communities. By harmonizing disparate resources under a common benchmark, **OpenAuditBenchmark** will serve as the foundation for agentic AI systems capable of automated auditing and secure code remediation in the Web3 ecosystem.

---

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

## 3. Literature Review

### SC-Bench: A Large-Scale Dataset for Smart Contract Auditing

**Authors**: Shihao Xia, Mengting He, Linhai Song, Yiying Zhang  
**Year**: 2024  
**Link**: [https://arxiv.org/abs/2410.06176](https://arxiv.org/abs/2410.06176)

SC-Bench provides a large-scale dataset of 5,377 real-world Ethereum contracts annotated with 15,975 violations based on ERC standards. It includes 139 manually identified real violations and over 15,000 synthetically injected ones using six distinct Abstract Syntax Tree (AST) mutation strategies, such as omission of condition checks, faulty return values, and state update bypassing.

To assess its usefulness, the authors tested GPT-4 in two configurations:
- **Zero-shot prompting with full ERC rules**: GPT-4 detected only 0.6% of synthetic and ~29% of real violations.
- **Oracle-assisted prompting (given specific rule + location)**: Detection improved to 22.8% for injected and 42.8% for real vulnerabilities.

These results underscore the challenge of LLM-based detection and the need for well-structured datasets. SC-Bench is publicly available with rule injection scripts and evaluation pipelines and serves as a strong foundation for model benchmarking in compliance-oriented auditing.

### AutoMESC: Automatic Framework for Mining Ethereum Smart Contract Vulnerabilities and Fixes

**Authors**: Majd Soud, Ilham Qasse, Grischa Liebel, Mohammad Hamdaqa  
**Year**: 2022  
**Link**: [https://arxiv.org/abs/2212.10660](https://arxiv.org/abs/2212.10660)

AutoMESC is a comprehensive framework for mining, labeling, and validating smart contract vulnerability-fix pairs. It identifies vulnerability-related commits from GitHub and CVE databases, then uses seven static analyzers (e.g., Slither, Mythril, SmartCheck) to classify up to 36 vulnerability types.

Key contributions:
- Uses a **majority voting scheme** among tools to ensure label quality (at least 50% agreement).
- Automatically links commits to fixes using keyword patterns, and re-validates patched code by rerunning the same detection tools.
- Compiles over 6,700 vulnerability–fix pairs with associated severity metadata and patch explanations.

AutoMESC is highly relevant to patch generation and severity ranking tasks. It offers one of the few public datasets that link vulnerable and fixed versions of smart contracts, making it valuable for training and evaluating LLMs and RL agents on repair tasks.

### 3.1 Comparative Analysis: SC-Bench vs. AutoMESC

| Feature                     | **SC-Bench**                                           | **AutoMESC**                                               |
|----------------------------|--------------------------------------------------------|------------------------------------------------------------|
| Source Type                | Primarily synthetic (AST mutation) + 139 real examples | Real-world data (GitHub, CVEs)                             |
| Volume                     | 5,377 contracts / 15,975 issues                        | ~6,700 vulnerability–fix pairs                             |
| Annotation Style           | Rule-based (88 ERC rules), location tagged             | SWC tags, severity scores, commit diffs                    |
| Patch Availability         | ❌ No patches                                           | ✅ Fixes included                                          |
| Severity Labeling          | ✅ For 139 real cases                                  | ✅ CVSS-style severity across samples                      |
| Tool Agreement Metadata    | ❌                                                    | ✅ Labeled using majority voting among 7 static analyzers  |
| Exploit Trace Support      | ❌                                                    | Partial (in commit or vulnerability history)              |
| Strengths                  | Clean, rule-aligned injection ideal for detection      | Rich, real-world repair data ideal for patching/validation|
| Limitations                | Unrealistic patterns, no fix labels                    | No synthetic data to expand uncommon vulnerabilities       |

This analysis highlights how **SC-Bench** provides a clean, rule-driven evaluation base for detection models, while **AutoMESC** focuses on patch realism, severity scoring, and real-world context. Their integration within **OpenAuditBenchmark** ensures full-spectrum coverage—detection, ranking, and repair—enabling robust agentic AI development and evaluation.

---

## 4. Problem Statement

There is no widely accepted dataset that supports the full cycle of tasks needed by agentic AI frameworks: vulnerability detection, scoring, patch generation, and patch validation. Existing datasets either focus on isolated bug instances (e.g., SWC Registry) or synthetic contracts with limited real-world relevance. This proposal aims to build a dataset that meets the following needs:

- Realistic and diverse smart contracts (real-world + adversarial examples)  
- Multi-modal annotations (code, exploit, patch, metadata, CVSS-like scores)  
- Benchmark compatibility for zero-shot, few-shot, and RL-based learning agents  

---

## 5. Objectives

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

## 6. Methodology

### 6.1 Data Sources

- SWC Registry (Smart Contract Weakness Classification)  
- Real exploits from platforms like **Etherscan**, **Ethernaut**, and **Damn Vulnerable DeFi**  
- GitHub repositories containing audit reports and remediation histories  
- Curated StackOverflow code snippets and bug bounty disclosures  

### 6.2 Annotation Schema

Each sample will include:

- `contract_id`: Unique identifier  
- `source_code`: Original Solidity code  
- `vulnerability`: SWC category and textual description  
- `cvss_score`: Standardized severity score  
- `exploit_trace`: Execution trace from symbolic/concrete execution (if available)  
- `fix_patch`: Human-written or LLM-generated patch  
- `validation_status`: Pass/fail status based on sandbox validation  

### 6.3 Toolchain

- **Static analysis**: Slither, Mythril, Semgrep  
- **Dynamic analysis**: Echidna, Manticore  
- **LLM augmentation**: GPT-4, LLaMA-3, Claude  
- **Manual review**: Validation by security auditors  

### 6.4 Benchmark Tasks

| Task                      | Input            | Output         | Metric                  |
|---------------------------|------------------|----------------|--------------------------|
| T1: Vulnerability Detection | Solidity code     | List of issues | Precision / Recall / F1 |
| T2: Severity Scoring       | Issue description | CVSS score     | MSE, Rank Correlation   |
| T3: Patch Generation       | Code + issue      | Code diff      | Patch Accuracy          |
| T4: Patch Validation       | Patched code      | Pass/Fail      | Test Case Pass Rate     |

---

## 7. Expected Outcomes

- A public benchmark dataset named **OpenAuditBenchmark**  
- Evaluation leaderboards for LLMs, GNNs, and RL agents  
- Research publications demonstrating fine-tuning and zero-shot performance  
- Foundation for future competitions and shared evaluation practices in Web3 security  

---

## 8. Team & Collaboration

We will invite collaboration from:

- Blockchain security researchers  
- Smart contract audit firms (e.g., Trail of Bits, OpenZeppelin)  
- LLM and reinforcement learning researchers  
- Academic labs working on software security and AI4Code  

---

## 9. Impact

This dataset will catalyze research at the intersection of smart contract security and agentic AI. By offering a high-quality benchmark with diverse annotations, it can help establish agentic auditing as a scalable solution in security workflows, while enabling reproducibility, comparability, and openness across future research.

---
