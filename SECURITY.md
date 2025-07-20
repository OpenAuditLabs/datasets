# Security Policy

## Overview

OpenAuditLabs is committed to maintaining the highest standards of security for our datasets repository. This document outlines our security policies, vulnerability reporting procedures, and data protection practices for the `openauditlabs/datasets` repository.

**Important Notice:** This repository contains audit-related datasets that may include sensitive organizational information, compliance data, and potentially confidential audit findings. All security considerations must account for the sensitive nature of audit data and applicable data protection regulations.

## Supported Versions

We currently provide security updates for the following versions of the datasets repository:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting Security Vulnerabilities

### How to Report

**Please do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.**

Instead, please report security vulnerabilities responsibly through one of the following methods:

1. **Email (Preferred):** Send details to `security@openauditlabs.org`
   - Use our PGP key (available at `https://openauditlabs.org/security/pgp-key.asc`) for encrypted communication
   - Include "SECURITY VULNERABILITY" in the subject line

2. **Security Advisory:** Use GitHub's [private security advisory reporting feature](https://github.com/OpenAuditLabs/datasets/security/advisories/new)

### What to Include in Your Report

To help us understand and resolve the issue quickly, please provide as much of the following information as possible:

- **Type of vulnerability** (e.g., data exposure, injection, authentication bypass)
- **Location of the affected code** (specific file paths, line numbers, or URLs)
- **Step-by-step instructions** to reproduce the vulnerability
- **Proof of concept code** (if applicable and safe to share)
- **Potential impact** including how an attacker might exploit the vulnerability
- **Any potential data exposure risks** specific to audit datasets
- **Suggested mitigation** (if you have recommendations)
- **Your contact information** for follow-up questions

### What You Can Expect From Us

When you report a security vulnerability, we commit to:

- **Initial Response:** Acknowledge receipt of your report within **72 hours**
- **Detailed Response:** Provide a detailed response indicating our evaluation and next steps within **7 business days**
- **Progress Updates:** Keep you informed of our progress if resolution takes longer than expected
- **Resolution Notification:** Notify you when the vulnerability is resolved
- **Public Disclosure:** Coordinate with you on the timing and content of public disclosure

## Data Security Considerations

### Data Classification

This repository may contain multiple types of audit-related data with varying sensitivity levels:

- **Public Data:** General audit methodologies, anonymized datasets, public compliance frameworks
- **Internal Data:** Organizational audit processes, internal procedures, configuration examples
- **Confidential Data:** Actual audit findings, organizational vulnerabilities, sensitive compliance data
- **Restricted Data:** Personal identifiable information (PII), financial data, legally protected information

### Data Protection Measures

#### For Dataset Contributors:
- **Data Sanitization:** All datasets must be thoroughly reviewed and sanitized before inclusion
- **PII Removal:** Remove all personally identifiable information, financial account numbers, and sensitive identifiers
- **Anonymization:** Apply appropriate anonymization techniques for sensitive organizational data
- **Classification Labels:** Clearly label datasets with appropriate sensitivity classifications
- **Access Controls:** Ensure appropriate access controls are maintained for different data classifications

#### For Dataset Users:
- **Authorized Use Only:** Use datasets only for legitimate audit research and compliance purposes
- **Data Protection:** Implement appropriate security measures when handling downloaded datasets
- **No Re-identification:** Do not attempt to re-identify anonymized data subjects
- **Compliance:** Ensure usage complies with applicable data protection regulations (GDPR, CCPA, HIPAA, etc.)

## Responsible Disclosure Guidelines

We follow responsible disclosure principles and ask that security researchers do the same:

### For Security Researchers:
- **Private Reporting:** Report vulnerabilities privately before any public disclosure
- **Reasonable Timeframe:** Allow us a reasonable time to investigate and remediate issues
- **No Data Access:** Do not access, modify, or delete data beyond what is necessary to demonstrate the vulnerability
- **No Service Disruption:** Avoid actions that could disrupt the repository or its users
- **Legal Compliance:** Ensure all testing activities comply with applicable laws and regulations
- **Confidentiality:** Maintain confidentiality of discovered vulnerabilities until coordinated disclosure

### Our Commitments:
- **No Legal Action:** We will not pursue legal action against researchers who follow these guidelines
- **Good Faith Recognition:** We recognize and appreciate good faith security research efforts
- **Coordinated Disclosure:** We will work with you to coordinate appropriate public disclosure timing
- **Credit Attribution:** We will publicly acknowledge your contribution (unless you prefer to remain anonymous)

## Security Best Practices

### For Repository Maintainers:
- Regular security assessments of datasets and repository infrastructure
- Implementation of automated security scanning for contributed datasets
- Maintenance of detailed audit logs for all repository activities
- Regular review and updates of access permissions
- Incident response procedures for potential data breaches

### For External Contributors:
- Follow secure coding practices when contributing analysis tools or scripts
- Use encrypted communication channels when discussing sensitive security matters
- Implement proper authentication and authorization for any contributed applications
- Follow the principle of least privilege when requesting repository access

## Compliance and Legal Considerations

This repository operates under various compliance frameworks and legal requirements:

- **Data Protection Laws:** GDPR, CCPA, and other applicable privacy regulations
- **Industry Standards:** SOC 2, ISO 27001, NIST Cybersecurity Framework
- **Audit Standards:** PCAOB, COSO, and relevant auditing standards
- **Export Controls:** Compliance with applicable export control regulations

### Data Retention and Deletion

- Security vulnerability reports are retained for a minimum of 7 years for compliance purposes
- Remediated vulnerability data is archived according to our data retention policy
- Personal information in security reports is handled according to applicable privacy laws

## Incident Response

In the event of a confirmed security incident:

1. **Immediate Assessment:** Evaluate the scope and impact of the incident
2. **Containment:** Implement immediate containment measures to limit exposure
3. **Investigation:** Conduct thorough investigation with appropriate forensic procedures
4. **Notification:** Notify affected parties and regulatory authorities as required by law
5. **Remediation:** Implement comprehensive remediation measures
6. **Documentation:** Maintain detailed incident documentation for compliance and learning
7. **Post-Incident Review:** Conduct thorough post-incident analysis and improve security measures

## Contact Information

For security-related questions or concerns:

- **Security Team Email:** security@openauditlabs.org
- **General Support:** support@openauditlabs.org
- **Business Hours:** Monday-Friday, 9:00 AM - 5:00 PM (UTC)

For urgent security matters outside business hours, please indicate "URGENT SECURITY MATTER" in your email subject line.

## Security Advisory Process

We use GitHub Security Advisories to communicate security vulnerabilities and their resolutions:

1. **Private Advisory Creation:** Initial vulnerability assessment in private advisory
2. **Stakeholder Notification:** Notification of affected parties and maintainers
3. **Resolution Development:** Development and testing of security fixes
4. **Coordinated Disclosure:** Public disclosure coordinated with the reporting researcher
5. **Advisory Publication:** Publication of security advisory with details and remediation steps

## Updates to This Policy

This security policy is reviewed and updated regularly. Significant changes will be communicated through:
- Repository notifications for contributors and maintainers
- Security advisory notifications for critical policy updates
- Community announcements for major policy revisions

## Acknowledgments

We appreciate the security research community's efforts to improve the security of open-source projects. We are grateful to all researchers who have reported vulnerabilities responsibly and helped make OpenAuditLabs datasets more secure.

---

**Last Updated:** July 2025
**Version:** 1.0

For questions about this security policy, please contact security@openauditlabs.org.
