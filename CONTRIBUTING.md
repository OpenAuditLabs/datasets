# Contributing to OpenAuditLabs **Datasets** Repository

Thank you for your interest in improving the OpenAuditLabs **datasets** collection. We welcome new datasets, bug fixes, documentation, and tooling improvements. This guide explains the standards and workflow that keep the repository reliable, reproducible, and legally compliant.

---

## 📑 Table of Contents
1. [What You Can Contribute](#what-you-can-contribute)
2. [Before You Start](#before-you-start)
3. [Contribution Workflow](#contribution-workflow)
4. [Dataset Directory Structure](#dataset-directory-structure)
5. [Metadata & Documentation](#metadata--documentation)
6. [Licensing Requirements](#licensing-requirements)
7. [Data Ethics & Privacy](#data-ethics--privacy)
8. [Code & Script Style](#code--script-style)
9. [Pull-Request Review Checklist](#pull-request-review-checklist)
10. [Community Support](#community-support)
11. [Code of Conduct](#code-of-conduct)

---

## What You Can Contribute

| Contribution Type | Examples |
|-------------------|----------|
| **New dataset**   | CSV, JSON, Parquet, images, audio, or mixed-modality data that fits the lab’s audit & transparency mission |
| **Dataset update**| Additional years, corrected records, richer metadata |
| **Bug fix**       | Bad links, schema errors, typos in docs |
| **Tooling**       | Validation scripts, data loaders, notebooks |
| **Documentation** | Tutorials, usage examples, improved READMEs |

> ⚠️  **Proprietary or personally identifying data is **NOT** accepted.**

---

## Before You Start
1. **Search first** – Avoid duplicates by checking the [datasets index](./datasets/README.md).
2. **Open an issue** – Briefly describe the dataset or change you plan to contribute. Core maintainers will confirm fit & scope.
3. **Sign the CLA** – We require a one-time [Contributor License Agreement](https://opensource.org/licenses/Apache-2.0) covering code & docs.

---

## Contribution Workflow

```text
┌─▶ fork ─▶ clone ─▶ create-branch ─▶ commit ─▶ push ─▶ pull-request ─┐
└────────────────────── maintainer review & merge ────────────────────┘
```

1. **Fork** the repo to your GitHub account and `git clone` it locally.
2. **Create a feature branch** using the pattern
   ```bash
   git checkout -b feat/<short-dataset-name>
   ```
3. **Add your dataset** under `datasets/<dataset-name>/` (see structure below).
4. **Run tests & linters**:
   ```bash
   make validate     # dataset schema & license check
   make lint         # black + flake8 on scripts
   ```
5. **Commit small, logical changes** with conventional messages, e.g.
   ```
   feat(municipal-audit-2024): initial upload of CSV & metadata
   ````
6. **Push** to your fork and open a **Pull Request (PR)** against `main`.
7. Complete the PR template, linking to the tracking issue and describing
   • dataset source  • license  • validation results.
8. Respond to review comments promptly; maintainers may request changes.
9. When approved, a maintainer will **squash-merge** your PR.

---

## Dataset Directory Structure

```
datasets/
└── <dataset-name>/
    ├── data/            # Raw or minimally processed files
    │   └── ...
    ├── README.md        # Human-readable overview (see template below)
    ├── metadata.yaml    # Machine-readable metadata (schema v1.0)
    ├── LICENSE          # Dataset license (plain-text)
    └── scripts/         # (optional) ingestion or processing code
```
*Use lowercase, hyphen-separated `dataset-name`.*

### `metadata.yaml` required keys
| Key | Description |
|-----|-------------|
| `title` | Descriptive title |
| `source_url` | Canonical public URL |
| `license` | SPDX identifier (e.g. `CC-BY-4.0`) |
| `date_retrieved` | ISO-8601 date |
| `contact` | Name/email of upstream provider |
| `tasks` | e.g. `nlp`, `cv`, `speech` |
| `num_records` | Integer or `unknown` |
| `columns` | List of `{name, dtype, description}` |

Run `python scripts/validate_metadata.py metadata.yaml` before committing.

---

## Metadata & Documentation
Every dataset **must** include:
1. **README.md** – 200-500 words covering purpose, collection methodology,
   data fields, usage examples, and citation.
2. **metadata.yaml** – Structured metadata described above.
3. **LICENSE** – Plain-text copy of the dataset’s license.

Optional but encouraged:
* **Sample notebook** in `examples/` showing loading & basic exploration.
* **Data dictionary** (CSV/MD) for complex schemas.

---

## Licensing Requirements
* Prefer **permissive open licenses** (`CC0`, `CC-BY`, `ODC-BY`, `MIT`).
* Ensure you have the **legal right to redistribute** the data.
* Include any required **attribution** in `README.md`.

Submissions lacking clear licensing will be rejected.

---

## Data Ethics & Privacy
* **Do not submit** personal data that can identify individuals.
* Remove sensitive attributes or aggregate to protect privacy.
* Disclose any **known biases** or limitations in the README.
* Follow relevant regulations (GDPR, CCPA, etc.).

---

## Code & Script Style
* Python ≥3.9, formatted with **black** & checked by **flake8**.
* Provide a `requirements.txt` for extra dependencies.
* Scripts should be **idempotent** and runnable via
  ```bash
  python scripts/download.py  # -> downloads to data/
  ```

---

## Pull-Request Review Checklist
Maintainers will verify:
- [ ] Dataset is non-proprietary & license file present
- [ ] Folder structure matches template
- [ ] `metadata.yaml` passes validation
- [ ] README covers source, schema, citation
- [ ] No PII or restricted data
- [ ] CI pipeline (`make validate`) is green

---

## Community Support
* **Questions?** Open a GitHub *Discussion* under **Q&A**.
* **Bugs?** File an *Issue* with the `bug` label.

---

## Code of Conduct
This project adheres to the [OpenAuditLabs Code of Conduct](../CODE_OF_CONDUCT.md). By participating you agree to follow its terms.

---

*Last updated: 07-13-2025*
