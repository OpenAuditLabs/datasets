import json
import logging
import functools
import time
from pathlib import Path
from typing import Dict, Any, Callable, TypeVar, cast
from logging.handlers import RotatingFileHandler

from audit_engine.static_analysis.slither_adapter import SlitherAdapter
from audit_engine.static_analysis.mythril_adapter import MythrilAdapter
from audit_engine.dynamic_analysis.echidna_adapter import EchidnaAdapter
from audit_engine.dynamic_analysis.adversarial_fuzz import AdversarialFuzzer
from audit_engine.scoring.scoring_engine import ScoringEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_logging(log_file='audit_engine.log', max_bytes=10*1024*1024, backup_count=5):
    """
    Sets up logging to a file with rotation and structured (JSON-like) output.
    """
    # Remove default handlers to avoid duplicate logs
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Custom formatter for structured logging
    class StructuredFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "timestamp": self.formatTime(record, self.datefmt),
                "name": record.name,
                "level": record.levelname,
                "message": record.getMessage(),
                "pathname": record.pathname,
                "lineno": record.lineno,
                "funcName": record.funcName
            }
            if record.exc_info:
                log_record["exc_info"] = self.formatException(record.exc_info)
            return json.dumps(log_record)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(StructuredFormatter())
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

# Call setup_logging once to configure it
setup_logging()

R = TypeVar('R') # Return type of the decorated function

class AuditEngineError(Exception):
    """Base exception for AuditEngine errors."""
    pass

class ConfigurationError(AuditEngineError):
    """Exception raised for issues with the configuration file."""
    pass

class ToolExecutionError(AuditEngineError):
    """Exception raised when an external tool fails to execute."""
    pass

class ToolUnavailableError(AuditEngineError):
    """Exception raised when an external tool cannot be initialized or is not found."""
    pass

def retry(attempts: int = 3, delay: float = 1.0, catch_exceptions: tuple = (Exception,)) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """
    A decorator to retry a function call multiple times with a delay.
    Args:
        attempts (int): Number of attempts to make.
        delay (float): Delay between attempts in seconds.
        catch_exceptions (tuple): Exceptions to catch and retry on.
    """
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            for i in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as e:
                    logger.warning(f"Attempt {i}/{attempts} for {func.__name__} failed: {e}")
                    if i < attempts:
                        time.sleep(delay)
            logger.error(f"All {attempts} attempts for {func.__name__} failed.")
            raise ToolExecutionError(f"Failed after {attempts} attempts: {func.__name__}")
        return wrapper
    return decorator


class AuditEngine:
    def __init__(self, config_path: str):
        """
        Initialize the AuditEngine with a path to a JSON configuration file.
        The config should include tool settings, severity thresholds, and
        other pipeline parameters.
        """
        logger.info(f"Initializing AuditEngine with config from {config_path}")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config: Dict[str, Any] = json.load(f)
            logger.info("Configuration loaded successfully.")
        except FileNotFoundError as e:
            logger.error(f"Config file not found: {config_path}")
            raise ConfigurationError(f"Config file not found: {config_path}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file {config_path}: {e}")
            raise ConfigurationError(f"Invalid JSON in config file {config_path}: {e}") from e
        if not isinstance(self.config, dict):
            logger.error("Config root must be a JSON object (dict).")
            raise TypeError("Config root must be a JSON object (dict).")


        # Initialize static analysis tools (fallback if no-arg constructor)
        cfg = self.config
        self.slither = None
        self.mythril = None
        self.echidna = None
        self.fuzzer = None
        self.scorer = None

        try:
            self.slither = SlitherAdapter(cfg.get('slither', {}))
            logger.info("SlitherAdapter initialized.")
        except Exception as e:
            logger.error(f"SlitherAdapter initialization failed: {e}")
            # Graceful degradation: if a tool fails to initialize, set it to None
            # and the run method will handle its unavailability.

        try:
            self.mythril = MythrilAdapter(cfg.get('mythril', {}))
            logger.info("MythrilAdapter initialized.")
        except Exception as e:
            logger.error(f"MythrilAdapter initialization failed: {e}")

        # Initialize dynamic analysis tools (fallback if no-arg constructor)
        try:
            self.echidna = EchidnaAdapter(cfg.get('echidna', {}))
            logger.info("EchidnaAdapter initialized.")
        except Exception as e:
            logger.error(f"EchidnaAdapter initialization failed: {e}")

        try:
            self.fuzzer = AdversarialFuzzer(cfg.get('fuzzer', {}))
            logger.info("AdversarialFuzzer initialized.")
        except Exception as e:
            logger.error(f"AdversarialFuzzer initialization failed: {e}")

        # Initialize scoring engine (fallback if no-arg constructor)
        try:
            self.scorer = ScoringEngine(cfg.get('scoring', {}))
            logger.info("ScoringEngine initialized.")
        except Exception as e:
            logger.error(f"ScoringEngine initialization failed: {e}")

    def run(self, contract_path: str) -> Dict[str, Any]:
        """
        Run the full analysis pipeline on the given Solidity contract.
        Returns a dictionary containing:
          - static_results: combined Slither & Mythril findings
          - dynamic_results: Echidna & fuzzing outputs
          - severity_scores: CVSS-style scores per vulnerability
        """
        logger.info(f"Starting audit for contract: {contract_path}")
        results: Dict[str, Any] = {"errors": {},
                                   "static_results": {'slither': [], 'mythril': []},
                                   "dynamic_results": {'echidna': {}, 'fuzzer': []},
                                   "severity_scores": []}

        # Validate target
        path = Path(contract_path)
        if not path.is_file():
            logger.error(f"Contract file not found: {contract_path}")
            raise FileNotFoundError(f"Contract file not found: {contract_path}")
        logger.info(f"Contract file {contract_path} validated.")

        # 1. Static analysis
        logger.info("Starting static analysis...")
        slither_issues = []
        mythril_issues = []

        if self.slither:
            try:
                @retry(attempts=3, delay=2, catch_exceptions=(ToolExecutionError, Exception))
                def run_slither_analysis():
                    logger.info("Running Slither analysis.")
                    return self.slither.analyze(contract_path)
                slither_issues = run_slither_analysis()
                logger.info("Slither analysis completed successfully.")
            except ToolExecutionError as e:
                logger.error(f"Slither analysis failed after retries: {e}")
                results["errors"]["slither"] = str(e)
            except Exception as e:
                logger.error(f"Slither analysis failed unexpectedly: {e}")
                results["errors"]["slither"] = str(e)
        else:
            logger.warning("SlitherAdapter not initialized. Skipping Slither analysis.")
            results["errors"]["slither"] = "SlitherAdapter not initialized."

        if self.mythril:
            try:
                @retry(attempts=3, delay=2, catch_exceptions=(ToolExecutionError, Exception))
                def run_mythril_analysis():
                    logger.info("Running Mythril analysis.")
                    return self.mythril.analyze(contract_path)
                mythril_issues = run_mythril_analysis()
                logger.info("Mythril analysis completed successfully.")
            except ToolExecutionError as e:
                logger.error(f"Mythril analysis failed after retries: {e}")
                results["errors"]["mythril"] = str(e)
            except Exception as e:
                logger.error(f"Mythril analysis failed unexpectedly: {e}")
                results["errors"]["mythril"] = str(e)
        else:
            logger.warning("MythrilAdapter not initialized. Skipping Mythril analysis.")
            results["errors"]["mythril"] = "MythrilAdapter not initialized."

        results['static_results'] = {
            'slither': slither_issues,
            'mythril': mythril_issues
        }
        logger.info("Static analysis completed.")

        # 2. Dynamic analysis
        logger.info("Starting dynamic analysis...")
        echidna_report = {}
        fuzz_findings = []

        if self.echidna:
            try:
                @retry(attempts=3, delay=2, catch_exceptions=(ToolExecutionError, Exception))
                def run_echidna_tests():
                    logger.info("Running Echidna tests.")
                    return self.echidna.run_tests(contract_path)
                echidna_report = run_echidna_tests()
                logger.info("Echidna tests completed successfully.")
            except ToolExecutionError as e:
                logger.error(f"Echidna tests failed after retries: {e}")
                results["errors"]["echidna"] = str(e)
            except Exception as e:
                logger.error(f"Echidna tests failed unexpectedly: {e}")
                results["errors"]["echidna"] = str(e)
        else:
            logger.warning("EchidnaAdapter not initialized. Skipping Echidna tests.")
            results["errors"]["echidna"] = "EchidnaAdapter not initialized."

        if self.fuzzer:
            try:
                @retry(attempts=3, delay=2, catch_exceptions=(ToolExecutionError, Exception))
                def run_fuzzer():
                    logger.info("Running adversarial fuzzer.")
                    return self.fuzzer.fuzz(contract_path)
                fuzz_findings = run_fuzzer()
                logger.info("Adversarial fuzzing completed successfully.")
            except ToolExecutionError as e:
                logger.error(f"Adversarial fuzzing failed after retries: {e}")
                results["errors"]["fuzzer"] = str(e)
            except Exception as e:
                logger.error(f"Adversarial fuzzing failed unexpectedly: {e}")
                results["errors"]["fuzzer"] = str(e)
        else:
            logger.warning("AdversarialFuzzer not initialized. Skipping fuzzing.")
            results["errors"]["fuzzer"] = "AdversarialFuzzer not initialized."

        results['dynamic_results'] = {
            'echidna': echidna_report,
            'fuzzer': fuzz_findings
        }
        logger.info("Dynamic analysis completed.")

        # 3. Severity scoring
        logger.info("Starting severity scoring...")
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
        severity = []
        if self.scorer:
            try:
                @retry(attempts=3, delay=2, catch_exceptions=(ToolExecutionError, Exception))
                def run_scoring():
                    logger.info("Running scoring engine.")
                    return self.scorer.score(all_issues)
                severity = run_scoring()
                logger.info("Severity scoring completed successfully.")
            except ToolExecutionError as e:
                logger.error(f"Scoring failed after retries: {e}")
                results.setdefault('errors', {})['scoring'] = str(e)
            except Exception as e:
                logger.error(f"Scoring failed unexpectedly: {e}")
                results.setdefault('errors', {})['scoring'] = str(e)
        else:
            logger.warning("ScoringEngine not initialized. Skipping severity scoring.")
            results.setdefault('errors', {})['scoring'] = "ScoringEngine not initialized."

        results['severity_scores'] = severity
        logger.info("Severity scoring completed.")

        logger.info("AuditEngine run completed. Final results available.")
        return results
