import json
from typing import Dict, Any

from audit_engine.static_analysis.slither_adapter import SlitherAdapter
from audit_engine.static_analysis.mythril_adapter import MythrilAdapter
from audit_engine.dynamic_analysis.echidna_adapter import EchidnaAdapter
from audit_engine.dynamic_analysis.adversarial_fuzz import AdversarialFuzzer
from audit_engine.scoring.scoring_engine import ScoringEngine


class AuditEngine:
    def __init__(self, config_path: str):
        """
        Initialize the AuditEngine with a path to a JSON configuration file.
        The config should include tool settings, severity thresholds, and
        other pipeline parameters.
        """
        with open(config_path, 'r') as f:
            self.config: Dict[str, Any] = json.load(f)

        # Initialize static analysis tools
        self.slither = SlitherAdapter(self.config.get('slither', {}))
        self.mythril = MythrilAdapter(self.config.get('mythril', {}))

        # Initialize dynamic analysis tools
        self.echidna = EchidnaAdapter(self.config.get('echidna', {}))
        self.fuzzer = AdversarialFuzzer(self.config.get('fuzzer', {}))

        # Initialize scoring engine
        self.scorer = ScoringEngine(self.config.get('scoring', {}))

    def run(self, contract_path: str) -> Dict[str, Any]:
        """
        Run the full analysis pipeline on the given Solidity contract.
        Returns a dictionary containing:
          - static_results: combined Slither & Mythril findings
          - dynamic_results: Echidna & fuzzing outputs
          - severity_scores: CVSS-style scores per vulnerability
        """
        results: Dict[str, Any] = {}

        # 1. Static analysis
        slither_issues = self.slither.analyze(contract_path)
        mythril_issues = self.mythril.analyze(contract_path)
        results['static_results'] = {
            'slither': slither_issues,
            'mythril': mythril_issues
        }

        # 2. Dynamic analysis
        echidna_report = self.echidna.run_tests(contract_path)
        fuzz_findings = self.fuzzer.fuzz(contract_path)
        results['dynamic_results'] = {
            'echidna': echidna_report,
            'fuzzer': fuzz_findings
        }

        # 3. Severity scoring
        all_issues = slither_issues + mythril_issues
        severity = self.scorer.score(all_issues)
        results['severity_scores'] = severity

        return results
