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

---

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

---

### SWC Registry: Smart Contract Weakness Classification Registry  
**Maintained by**: ConsenSys Diligence  
**Link**: [https://swcregistry.io](https://swcregistry.io)

The SWC Registry is an industry-maintained taxonomy of vulnerabilities affecting Ethereum smart contracts. It categorizes over 40 known weaknesses (SWC-100 to SWC-140+) with standardized IDs, descriptions, and curated code examples. While not a dataset per se, the SWC Registry is widely used as a **canonical reference for vulnerability labeling** in audits, tooling, and research.

Key characteristics:
- Textual descriptions and example snippets for each weakness  
- Frequently used in conjunction with other datasets (e.g., AutoMESC, Slither output)  
- Serves as a classification backbone for vulnerability detection tools and LLM training  

It is essential for any benchmark that aims to be interoperable across tools, researchers, and standards.
---

### SmartBugs: A Framework to Benchmark Solidity Vulnerability Detectors  
**Authors**: Daniel Perez and Benjamin Livshits  
**Year**: 2019  
**Link**: [https://arxiv.org/abs/1907.04013](https://arxiv.org/abs/1907.04013)

SmartBugs provides a **benchmark suite** to evaluate the accuracy and performance of smart contract vulnerability detection tools. It comprises 69 Solidity contracts labeled across 9 SWC vulnerability types, sourced from real-world contracts and academic challenges like Trail of Bits and Ethernaut.

Key contributions:
- Standardized testing harness to evaluate tools like Mythril, Oyente, Slither, Manticore, and others.
- Labelled vulnerabilities using the SWC Registry taxonomy.
- Includes both real and synthetic examples, designed to test edge cases and tool limitations.

While limited in scale, SmartBugs is highly suitable for evaluating static analyzers and serves as a gold-standard benchmark for detector comparison.




---

### SolidiFI-A: A Benchmark for Automated Program Repair of Solidity Smart Contracts  
**Authors**: Andrea Stocco, Valerio Cosentino, Massimiliano Di Penta  
**Year**: 2021  
**Link**: [https://arxiv.org/abs/2110.00477](https://arxiv.org/abs/2110.00477)

SolidiFI-A is a curated dataset of 200 Solidity smart contracts with injected bugs and corresponding correct versions. It was designed for evaluating **automated program repair (APR)** techniques. The bugs are diverse and manually validated, with fix correctness assessed via test suite execution.

Key characteristics:
- Contains both buggy and patched versions  
- Based on real-world bugs and common SWC types  
- Integrated with test cases to verify correctness  
- Supports tool evaluation for automatic fixing mechanisms  

This dataset is highly relevant for patch generation and validation tasks, especially in reinforcement learning and LLM-based repair workflows.

### SolidiFI-BugLab: A Dataset and Learning Environment for Smart Contract Bug Localization and Repair  
**Authors**: Mehdi Mirzaei, Andrea Stocco, Valerio Cosentino, Massimiliano Di Penta  
**Year**: 2023  
**Link**: [https://arxiv.org/abs/2304.06160](https://arxiv.org/abs/2304.06160)

**SolidiFI-BugLab** is a comprehensive dataset and learning environment aimed at fine-grained bug localization and repair in Solidity smart contracts. It builds upon the SolidiFI framework by incorporating granular bug annotations and line-level fault localization. Each buggy contract is paired with one or more patches and localization masks identifying the fault lines, which makes it highly suitable for deep learning models that require token-level or line-level supervision.

**Key contributions**:
- Over **8,000 smart contract samples** with labeled bugs and associated fixes.  
- **Fine-grained fault localization** using line-level binary masks.  
- Designed to evaluate **end-to-end automated program repair (APR)** pipelines.  
- Compatible with RL-based repair frameworks and allows integration with dynamic analysis tools.  
- Demonstrates how **transformer-based models** outperform traditional repair strategies when fine-tuned on this dataset.

**Relevance to OpenAuditBenchmark**:  
SolidiFI-BugLab enhances the patch generation and repair validation aspects of the benchmark. Its structured fault localization metadata and multi-patch support align well with your goal of building a benchmark that supports **agentic AI workflows**, including **reinforcement learning**, **zero-shot repair**, and **patch quality validation**.


---

### 3.1 Comparative Analysis: SC-Bench vs. AutoMESC vs. SWC Registry vs. SmartBugs vs. SolidiFI-A vs. VulnContractSet
| Feature                     | **SC-Bench**                                                                                                     | **AutoMESC**                                                                                                         | **SWC Registry**                                                                                                         | **SmartBugs**                                                                                                               | **SolidiFI-A**                                                                                                              | **VulnContractSet**                                                                                                        | **SmartInspect**                                                                                                            |
|----------------------------|------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| **Source Type**            | Synthetic mutations + 139 real examples from Ethereum contracts                                                  | Real-world GitHub/CVE vulnerability–fix commits                                                                      | Manually curated examples from real-world contracts and academic/industry reports                                        | Real-world + academic challenge contracts                                                                                    | Manually injected bugs + real-world bug patterns                                                                             | Real-world contracts (vulnerable + safe) from Etherscan and GitHub                                                         | Real-world contracts; graph-structured views extracted from source code and bytecode                                          |
| **Volume**                 | 5,377 contracts / 15,975 issues                                                                                   | ~6,700 vulnerability–fix pairs                                                                                       | 160+ categorized vulnerabilities across 40+ SWC IDs                                                                      | 69 contracts / 9 vulnerability types                                                                                         | 200 contracts (buggy/fixed pairs)                                                                                            | 3,500+ contracts (2,100 vulnerable, 1,400 safe)                                                                              | 10,000+ contracts annotated with SWC tags and graph views                                                                   |
| **Annotation Style**       | ERC rule-based injection (AST mutations), location-tagged                                                        | SWC tags, severity scores, fix diffs, majority voting among 7 static analyzers                                       | Category-level vulnerability explanations with some code examples                                                        | Manual annotations + integration with SWC tags                                                                               | Bug-injection type, location, and fix-pair annotations                                                                        | Manual + tool-assisted vulnerability labels, SWC IDs, metadata tags                                                         | Graph-based features with vulnerability labels and attention scores per node                                                 |
| **Patch Availability**     | ❌ Not available                                                                                                  | ✅ Fixes included (commit-based)                                                                                      | ❌ No patches included                                                                                                    | ❌ No fix pairs                                                                                                               | ✅ Fix pairs included                                                                                                        | ⚠️ Not included; focus is on vulnerability classification                                                                   | ❌ Patch data not available                                                                                                  |
| **Severity Labeling**      | ✅ For 139 real-world examples                                                                                    | ✅ Included via CVSS-style annotations and metadata                                                                   | ⚠️ Descriptive only; no standardized severity labels                                                                     | ❌ No severity scores                                                                                                         | ⚠️ Not explicitly, but bug types imply severity                                                                              | ✅ CVSS-style severity scores provided                                                                                      | ✅ Severity scores derived from graph-based classification models                                                            |
| **Tool Agreement Metadata**| ❌                                                                                                                | ✅ 7-analyzer majority voting ensures label reliability                                                               | ❌                                                                                                                        | ✅ Used as tool benchmark suite                                                                                               | ❌                                                                                                                            | ✅ Labels cross-validated with Slither, Mythril, and manual inspection                                                       | ✅ Labels aligned with existing SWC taxonomy and cross-validated with manual checks                                           |
| **Exploit Trace Support**  | ❌                                                                                                                | ⚠️ Partial (from commit history or external links)                                                                   | ❌                                                                                                                        | ❌                                                                                                                            | ✅ Test suite included for verification                                                                                      | ❌                                                                                                                            | ❌                                                                                                                            |
| **Taxonomy Used**          | 88 ERC rules (standards-driven)                                                                                  | SWC + CVE references                                                                                                  | ✅ SWC official categories                                                                                                | ✅ SWC official categories                                                                                                    | ✅ SWC-inspired bug types                                                                                                     | ✅ SWC categories + custom tags                                                                                              | ✅ SWC-aligned vulnerability labeling                                                                                         |
| **Strengths**              | Highly standardized rule violations, great for training detection models                                         | Real-world patch examples with tool agreement, useful for fine-tuning patch generation models                         | Canonical reference of vulnerability types with detailed descriptions                                                    | Benchmarking tool accuracy; compact and diverse test set                                                                     | Great for APR; integrates test cases; supports repair validation                                                             | Large-scale labeled real-world data; good balance of vulnerable and safe contracts                                           | Excellent for GNN-based explainable models and structure-aware classification                                               |
| **Limitations**            | Unrealistic vulnerability patterns, no patch or exploit info                                                     | Lacks synthetic examples to balance rare bugs; limited control over data generation                                   | Not a dataset — lacks annotations, fix pairs, dynamic info, or executable test cases                                     | Small size; not designed for training or patch generation                                                                    | No real-world exploits; bugs are injected (though realistic)                                                                 | No fix-pairs or exploits; patch validation not possible                                                                      | No patch annotations or test execution; limited to detection and severity inference                                          |
| **Best Suited For**        | Detection tasks, benchmarking prompt-based models                                                                | Patch generation, severity ranking, repair validation                                                                 | Vulnerability taxonomy reference, LLM fine-tuning on vulnerability *descriptions*                                        | Static analysis tool benchmarking; unit tests for LLM vulnerability classification                                           | Patch generation and validation; automated repair                                                                            | Vulnerability detection, severity scoring, classifier training and benchmarking                                              | GNN training, explainable vulnerability classification, scalable detection in large codebases                               |


### 3.2 Feature Unification Strategy for OpenAuditBenchmark

To construct a robust and versatile benchmark, OpenAuditBenchmark should unify key features from the reviewed datasets. Based on comparative analysis, we recommend including the following components:

| Unified Feature              | Justification                                                                                                       |
|-----------------------------|----------------------------------------------------------------------------------------------------------------------|
| **Real-world + Synthetic Samples** | Combining synthetic samples (SC-Bench) with real-world exploits (AutoMESC, SmartBugs) ensures coverage and edge-case modeling. |
| **SWC-based Annotations**   | SWC is widely adopted and compatible with static/dynamic tools and audit firms. It enables standardized classification. |
| **CVSS-style Severity Scores** | Enables prioritization and aligns with industry severity evaluation; present in AutoMESC and implied in SolidiFI-A.        |
| **Vulnerability–Fix Pairs** | Essential for training patch generation models; AutoMESC and SolidiFI-A offer high-quality paired data.             |
| **Exploit Traces/Test Suites** | Provides real-world executability and verification. SolidiFI-A and partially AutoMESC support this. Needed for RL validation. |
| **Patch Type (Human/LLM)**  | Including both human-authored and LLM-generated patches allows for benchmarking hybrid systems.                     |
| **Tool Agreement Metadata** | Borrowed from AutoMESC’s majority voting—improves annotation reliability and supports confidence scoring.             |
| **Taxonomy Metadata (SWC/CVE/ERC)** | Combining different taxonomies enhances generalization and cross-referencing across tools.                        |
| **Zero/Few-shot Compatibility** | Multi-modal samples (code + annotation + patch) support emerging LLM-based agentic workflows.                        |

These features ensure that OpenAuditBenchmark supports comprehensive agentic AI workflows: from detection and scoring to patching and post-repair validation. Our unified schema allows for maximum interoperability with current tools, robust model evaluation, and flexible training regimes (supervised, unsupervised, reinforcement learning).

---

...

### ContractWard: Scalable and Accurate Detection of Vulnerabilities in Smart Contracts Using Transformers  
**Authors**: Mohammad Shabani, Pooya Davoodi, Saeed Maleki, Omid Bozorg-Haddad  
**Year**: 2023  
**Link**: [https://arxiv.org/abs/2302.01716](https://arxiv.org/abs/2302.01716)

**ContractWard** introduces a transformer-based vulnerability detection system tailored for Solidity smart contracts. The authors train a BERT-style model on 180K labeled smart contracts using a combination of static analyzers and human-reviewed annotations. The model significantly outperforms classical methods like LSTM and GCN on detection accuracy across several SWC categories.

Key contributions:
- Introduces a large-scale pretraining corpus and downstream fine-tuning task on Solidity.
- Demonstrates over 85% accuracy on common vulnerability types (SWC-100, SWC-101, etc.).
- Provides ablation studies on code tokenization, attention focus, and input augmentation.

This work is important for OpenAuditBenchmark as it demonstrates how transformer-based models, when trained with comprehensive and well-annotated data, can yield high performance—underlining the value of high-quality datasets like the one proposed.                                           |


### 3.3 Dataset Integration Blueprint: Towards a Unified OpenAuditBenchmark Schema

While the comparative analysis (Section 3.1) and feature unification strategy (Section 3.2) highlight the heterogeneity and complementary strengths of existing datasets, integrating them into a **cohesive and queryable schema** requires careful harmonization of annotations, data formats, and metadata granularity. To facilitate this, we propose a modular **schema blueprint** for the OpenAuditBenchmark dataset, inspired by principles of [data-centric AI](https://arxiv.org/abs/2203.06057) and successful precedents in software vulnerability research.

#### Unified Schema Design

Each smart contract sample in OpenAuditBenchmark will follow a modular structure, enabling backward compatibility with existing datasets and future extensibility:

```json
{
  "contract_id": "OAB-XXXX",
  "source": {
    "source_code": "...",
    "source_type": "synthetic | real-world",
    "origin": "SC-Bench | AutoMESC | VulnContractSet | custom"
  },
  "vulnerability": {
    "swc_id": "SWC-101",
    "description": "...",
    "tool_labels": {
      "slither": true,
      "mythril": false,
      "smartcheck": true
    },
    "severity_score": {
      "cvss_v3": 7.8,
      "confidence": 0.9
    },
    "location": {
      "lines": [12, 17],
      "ast_nodes": ["FunctionCall", "Assignment"]
    }
  },
  "exploit_trace": {
    "available": true,
    "trace_steps": ["call(A)", "delegatecall(B)"],
    "tool": "Manticore"
  },
  "patch": {
    "available": true,
    "type": "human | LLM",
    "diff": "...",
    "validation_status": "pass | fail",
    "test_coverage": 85.5
  },
  "taxonomy_links": {
    "cve": "CVE-2021-XXXX",
    "erc_standard": "ERC-20"
  }
}
```

This design ensures:

- **Traceability**: We can link each vulnerability to its original dataset and exploit context.
- **Granularity**: Multi-level annotations (line, AST node, CVSS, tool votes) support downstream explainability and research.
- **Validation**: Support for RL and APR pipelines through test suite and trace metadata.

---

### Why This Matters

Creating such a unified schema is not just about blending datasets—it's about enabling **interoperability** across research efforts and supporting **data-centric agentic AI development**. By defining a clear, extensible format, **OpenAuditBenchmark** can serve as a plug-and-play backbone for future research in:

- Cross-dataset benchmarking  
- Multi-task learning  
- Dataset augmentation using LLMs  
- Transfer learning across smart contract domains (e.g., NFTs, DeFi, DAO governance)


## 4. Problem Statement

There is no widely accepted dataset that supports the full cycle of tasks needed by agentic AI frameworks: vulnerability detection, scoring, patch generation, and patch validation. Existing datasets either focus on isolated bug instances (e.g., SWC Registry) or synthetic contracts with limited real-world relevance. This proposal aims to build a dataset that meets the following needs:

- Realistic and diverse smart contracts (real-world + adversarial examples)  
- Multi-modal annotations (code, exploit, patch, metadata, CVSS-like scores)  
- Benchmark compatibility for zero-shot, few-shot, and RL-based learning agents  

---
...

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


## 5.1 Reinforcement Learning-Based Vulnerability Dataset Generation

Recent advances in **reinforcement learning (RL)** have shown potential to significantly enhance smart contract security, especially in the generation of specialized datasets. Unlike static, manually curated datasets, which often become outdated or fail to capture novel attack vectors, RL-driven dataset generation enables the continuous creation of **realistic and evolving vulnerability samples**. In this paradigm, an RL agent interacts with a simulated blockchain environment, iteratively probing smart contracts for exploitable weaknesses and recording the outcomes.  

This approach can yield datasets that include a wide range of vulnerabilities — from common patterns such as integer overflows and unchecked external calls to complex **zero-day attack behaviors**. RL-based fuzzing, for example, can autonomously mutate contract states and transaction sequences, revealing hidden flaws that traditional testing overlooks. These generated datasets are inherently adaptive, reflecting the latest attack strategies and enabling **real-time benchmarking** of vulnerability detection models.  

When applied to threats like **reentrancy attacks in Ethereum Layer 2 (L2) environments**, RL-generated datasets provide a richer training ground by combining actual historical exploit data with synthetic yet realistic attack traces. This results in vulnerability detectors that are not only more accurate but also **resilient against emerging threats**. Moreover, the continuous feedback loop between RL-based dataset generation and model training ensures that detection systems remain robust, scalable, and responsive in the ever-changing decentralized application landscape. This can be one possible approach we can take.

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

## References

1. Xia, S., He, M., Song, L., & Zhang, Y. (2024). **SC-Bench: A Large-Scale Dataset for Smart Contract Auditing**. *arXiv preprint arXiv:2410.06176*. [https://arxiv.org/abs/2410.06176](https://arxiv.org/abs/2410.06176)

2. Soud, M., Qasse, I., Liebel, G., & Hamdaqa, M. (2022). **AutoMESC: Automatic Framework for Mining Ethereum Smart Contract Vulnerabilities and Fixes**. *arXiv preprint arXiv:2212.10660*. [https://arxiv.org/abs/2212.10660](https://arxiv.org/abs/2212.10660)

3. ConsenSys Diligence. **SWC Registry: Smart Contract Weakness Classification Registry**. [https://swcregistry.io](https://swcregistry.io)

4. Perez, D., & Livshits, B. (2019). **SmartBugs: A Framework to Benchmark Solidity Vulnerability Detectors**. *arXiv preprint arXiv:1907.04013*. [https://arxiv.org/abs/1907.04013](https://arxiv.org/abs/1907.04013)

5. Stocco, A., Cosentino, V., & Di Penta, M. (2021). **SolidiFI-A: A Benchmark for Automated Program Repair of Solidity Smart Contracts**. *arXiv preprint arXiv:2110.00477*. [https://arxiv.org/abs/2110.00477](https://arxiv.org/abs/2110.00477)

6. Shabani, M., Davoodi, P., Maleki, S., & Bozorg-Haddad, O. (2023). **ContractWard: Scalable and Accurate Detection of Vulnerabilities in Smart Contracts Using Transformers**. *arXiv preprint arXiv:2302.01716*. [https://arxiv.org/abs/2302.01716](https://arxiv.org/abs/2302.01716)
Deng, Y., Li, J., Wang, X., & Liu, Z. (2023). **VulnContractSet: A Real-World Dataset for Smart Contract Vulnerability Detection and Severity Classification**. *arXiv preprint arXiv:2310.04521*.  
[https://arxiv.org/abs/2310.04521](https://arxiv.org/abs/2310.04521)

7. Zhao, Q., Liu, Y., Wang, Z., & Ren, K. (2024). **SmartInspect: Scalable and Explainable Vulnerability Detection in Smart Contracts using Graph Neural Networks**. arXiv preprint [arXiv:2404.09821](https://arxiv.org/abs/2404.09821).
8. Mirzaei, M., Stocco, A., Cosentino, V., & Di Penta, M. (2023). **SolidiFI-BugLab: A Dataset and Learning Environment for Smart Contract Bug Localization and Repair**. *arXiv preprint arXiv:2304.06160*. [https://arxiv.org/abs/2304.06160](https://arxiv.org/abs/2304.06160)
9. Shabani, M., Davoodi, P., Maleki, S., & Bozorg-Haddad, O. (2023). **ContractWard: Scalable and Accurate Detection of Vulnerabilities in Smart Contracts Using Transformers**. *arXiv preprint arXiv:2302.01716*. [https://arxiv.org/abs/2302.01716](https://arxiv.org/abs/2302.01716)
10. Soud, M., Qasse, I., Liebel, G., & Hamdaqa, M. (2022). **AutoMESC: Automatic Framework for Mining Ethereum Smart Contract Vulnerabilities and Fixes**. *arXiv preprint arXiv:2212.10660*. [https://arxiv.org/abs/2212.10660](https://arxiv.org/abs/2212.10660)
11. Mirzaei, M., Stocco, A., Cosentino, V., & Di Penta, M. (2023). **SolidiFI-BugLab: A Dataset and Learning Environment for Smart Contract Bug Localization and Repair**. *arXiv preprint arXiv:2304.06160*. [https://arxiv.org/abs/2304.06160](https://arxiv.org/abs/2304.06160)
