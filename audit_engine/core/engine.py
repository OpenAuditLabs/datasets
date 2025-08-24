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
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config: Dict[str, Any] = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Config file not found: {config_path}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file {config_path}: {e}") from e
        if not isinstance(self.config, dict):
            raise TypeError("Config root must be a JSON object (dict).")


        # Initialize static analysis tools (fallback if no-arg constructor)
        cfg = self.config
        try:
            self.slither = SlitherAdapter(cfg.get('slither', {}))
        except TypeError:
            self.slither = SlitherAdapter()
        try:
            self.mythril = MythrilAdapter(cfg.get('mythril', {}))
        except TypeError:
            self.mythril = MythrilAdapter()

        # Initialize dynamic analysis tools (fallback if no-arg constructor)
        try:
            self.echidna = EchidnaAdapter(cfg.get('echidna', {}))
        except TypeError:
            self.echidna = EchidnaAdapter()
        try:
            self.fuzzer = AdversarialFuzzer(cfg.get('fuzzer', {}))
        except TypeError:
            self.fuzzer = AdversarialFuzzer()

        # Initialize scoring engine (fallback if no-arg constructor)
        try:
            self.scorer = ScoringEngine(cfg.get('scoring', {}))
        except TypeError:
            self.scorer = ScoringEngine()

    def run(self, contract_path: str) -> Dict[str, Any]:
        """
        Run the full analysis pipeline on the given Solidity contract.
        Returns a dictionary containing:
          - static_results: combined Slither & Mythril findings
          - dynamic_results: Echidna & fuzzing outputs
          - severity_scores: CVSS-style scores per vulnerability
        """
        results: Dict[str, Any] = {"errors": {}}

        # Validate target
        path = Path(contract_path)
        if not path.is_file():
            raise FileNotFoundError(f"Contract file not found: {contract_path}")

        # 1. Static analysis
        try:
            slither_issues = self.slither.analyze(contract_path)
        except Exception as e:
            results["errors"]["slither"] = str(e)
            slither_issues = []
        try:
            mythril_issues = self.mythril.analyze(contract_path)
        except Exception as e:
            results["errors"]["mythril"] = str(e)
            mythril_issues = []
        results['static_results'] = {
            'slither': slither_issues,
            'mythril': mythril_issues
        }

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
        def _coerce_findings(f):
            if not f:
                return []
            if isinstance(f, list):
                return f
            if isinstance(f, dict):
                return [f]
            try:
                return list(f)
            except TypeError:
                return [f]

        all_issues = _coerce_findings(slither_issues) + _coerce_findings(mythril_issues)
        try:
            severity = self.scorer.score(all_issues)
        except Exception as e:
            results.setdefault('errors', {})['scoring'] = str(e)
            severity = []
        results['severity_scores'] = severity


        return results
