import math

class ScoringEngine:
    # CVSS v3.1 Metric Group Values
    # Base Metrics
    ATTACK_VECTOR = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20}
    ATTACK_COMPLEXITY = {"L": 0.77, "H": 0.44}
    PRIVILEGES_REQUIRED = {"U": {"N": 0.85, "L": 0.62, "H": 0.27},
                           "C": {"N": 0.50, "L": 0.27, "H": 0.15}} # U: Unchanged, C: Changed Scope
    USER_INTERACTION = {"N": 0.85, "R": 0.62}
    SCOPE = {"U": 6.42, "C": 7.52}
    CONF_INTEG_AVAIL = {"N": 0.0, "L": 0.22, "H": 0.56}

    # Temporal Metrics
    EXPLOIT_CODE_MATURITY = {"X": 1.0, "H": 1.0, "F": 0.97, "P": 0.94, "U": 0.91}
    REMEDIATION_LEVEL = {"X": 1.0, "O": 0.95, "W": 0.96, "U": 0.97}
    REPORT_CONFIDENCE = {"X": 1.0, "C": 0.92, "R": 0.96, "U": 0.96}

    # Environmental Metrics
    CONF_INTEG_AVAIL_REQUIREMENT = {"X": 1.0, "L": 0.5, "M": 1.0, "H": 1.5}

    def _round_up(self, n):
        if n == 0:
            return 0
        integer_part = math.floor(n)
        if n == integer_part:
            return n
        return integer_part + 1 if (n * 100) % 10 == 0 else math.ceil(n * 10) / 10

    def _calculate_impact_subscore(self, C, I, A, S):
        isc_base = 1 - (
            (1 - self.CONF_INTEG_AVAIL[C]) *
            (1 - self.CONF_INTEG_AVAIL[I]) *
            (1 - self.CONF_INTEG_AVAIL[A])
        )
        if S == "U":
            return self.SCOPE["U"] * isc_base
        else: # S == "C"
            return self.SCOPE["C"] * (isc_base - 0.029) - 3.25 * (isc_base - 0.02) ** 15

    def _calculate_exploitability_subscore(self, AV, AC, PR, UI):
        return 8.22 * self.ATTACK_VECTOR[AV] * self.ATTACK_COMPLEXITY[AC] *
               self.PRIVILEGES_REQUIRED[PR] * self.USER_INTERACTION[UI]

    def _calculate_base_score(self, metrics):
        AV, AC, PR, UI, S, C, I, A = (
            metrics["AV"], metrics["AC"], metrics["PR"], metrics["UI"],
            metrics["S"], metrics["C"], metrics["I"], metrics["A"]
        )

        impact_subscore = self._calculate_impact_subscore(C, I, A, S)
        exploitability_subscore = self._calculate_exploitability_subscore(AV, AC, PR[S], UI)

        if impact_subscore <= 0:
            return 0.0
        elif S == "U":
            return self._round_up(min(impact_subscore + exploitability_subscore, 10))
        else: # S == "C"
            return self._round_up(min(1.08 * (impact_subscore + exploitability_subscore), 10))

    def _calculate_temporal_score(self, base_score, metrics):
        E = metrics.get("E", "X") # Exploit Code Maturity
        RL = metrics.get("RL", "X") # Remediation Level
        RC = metrics.get("RC", "X") # Report Confidence

        return self._round_up(
            base_score *
            self.EXPLOIT_CODE_MATURITY[E] *
            self.REMEDIATION_LEVEL[RL] *
            self.REPORT_CONFIDENCE[RC]
        )

    def _calculate_environmental_score(self, base_score, temporal_score, metrics):
        CR = metrics.get("CR", "X") # Confidentiality Requirement
        IR = metrics.get("IR", "X") # Integrity Requirement
        AR = metrics.get("AR", "X") # Availability Requirement

        # Modified Base Metrics (simplified for this implementation, assuming they are provided if different)
        # Otherwise, use base metrics
        mAV = metrics.get("mAV", metrics["AV"])
        mAC = metrics.get("mAC", metrics["AC"])
        mPR = metrics.get("mPR", metrics["PR"])
        mUI = metrics.get("mUI", metrics["UI"])
        mS = metrics.get("mS", metrics["S"])
        mC = metrics.get("mC", metrics["C"])
        mI = metrics.get("mI", metrics["I"])
        mA = metrics.get("mA", metrics["A"])

        # Modified Impact Subscore
        m_isc_base = 1 - (
            (1 - self.CONF_INTEG_AVAIL[mC] * self.CONF_INTEG_AVAIL_REQUIREMENT[CR]) *
            (1 - self.CONF_INTEG_AVAIL[mI] * self.CONF_INTEG_AVAIL_REQUIREMENT[IR]) *
            (1 - self.CONF_INTEG_AVAIL[mA] * self.CONF_INTEG_AVAIL_REQUIREMENT[AR])
        )

        if mS == "U":
            m_impact_subscore = self.SCOPE["U"] * m_isc_base
        else: # mS == "C"
            m_impact_subscore = self.SCOPE["C"] * (m_isc_base - 0.029) - 3.25 * (m_isc_base * 0.9731 - 0.02) ** 13

        # Modified Exploitability Subscore
        m_exploitability_subscore = 8.22 * self.ATTACK_VECTOR[mAV] * self.ATTACK_COMPLEXITY[mAC] *
                                    self.PRIVILEGES_REQUIRED[mPR[mS]] * self.USER_INTERACTION[mUI]

        if m_impact_subscore <= 0:
            modified_base_score = 0.0
        elif mS == "U":
            modified_base_score = self._round_up(min(m_impact_subscore + m_exploitability_subscore, 10))
        else: # mS == "C"
            modified_base_score = self._round_up(min(1.08 * (m_impact_subscore + m_exploitability_subscore), 10))

        # Apply Temporal Metrics to Modified Base Score
        E = metrics.get("E", "X")
        RL = metrics.get("RL", "X")
        RC = metrics.get("RC", "X")

        return self._round_up(
            modified_base_score *
            self.EXPLOIT_CODE_MATURITY[E] *
            self.REMEDIATION_LEVEL[RL] *
            self.REPORT_CONFIDENCE[RC]
        )

    def _classify_severity(self, score):
        if score == 0:
            return "None"
        elif 0.1 <= score <= 3.9:
            return "Low"
        elif 4.0 <= score <= 6.9:
            return "Medium"
        elif 7.0 <= score <= 8.9:
            return "High"
        else: # 9.0 - 10.0
            return "Critical"

    def _assign_confidence(self, finding_data):
        # This is a placeholder for actual confidence scoring logic.
        # In a real scenario, this would depend on the source of the finding,
        # the analysis method, and corroborating evidence.
        # For now, we'll return a static value or derive it simply.
        if finding_data.get("source") == "manual_review":
            return "High"
        elif finding_data.get("tool") == "slither":
            return "Medium"
        else:
            return "Low"

    def score(self, findings):
        results = []
        for finding in findings:
            # Assume 'finding' is a dictionary containing CVSS metric values
            # Example:
            # finding = {
            #     "id": "VULN-001",
            #     "description": "Example vulnerability",
            #     "metrics": {
            #         "AV": "N", "AC": "L", "PR": "N", "UI": "N", "S": "U",
            #         "C": "H", "I": "H", "A": "H",
            #         "E": "H", "RL": "O", "RC": "C",
            #         "CR": "H", "IR": "H", "AR": "H"
            #     },
            #     "source": "slither"
            # }

            metrics = finding.get("metrics", {})
            finding_id = finding.get("id", "unknown")

            base_score = self._calculate_base_score(metrics)
            temporal_score = self._calculate_temporal_score(base_score, metrics)
            environmental_score = self._calculate_environmental_score(base_score, temporal_score, metrics)
            
            severity = self._classify_severity(environmental_score if environmental_score is not None else temporal_score if temporal_score is not None else base_score)
            confidence = self._assign_confidence(finding)

            results.append({
                "finding_id": finding_id,
                "base_score": base_score,
                "temporal_score": temporal_score,
                "environmental_score": environmental_score,
                "severity": severity,
                "confidence": confidence,
                "cvss_version": "3.1"
            })
        return results