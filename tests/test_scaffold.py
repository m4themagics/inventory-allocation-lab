"""Only scaffold invariants are tested before implementation begins."""

from pathlib import Path

import yaml

CONFIG = Path(__file__).resolve().parents[1] / "configs" / "m5.yaml"

REQUIRED_SECTIONS = {
    "data",
    "cohort",
    "operational_layer",
    "forecast",
    "backtest",
    "solver",
}


def test_experiment_config_declares_every_decision_layer() -> None:
    config = yaml.safe_load(CONFIG.read_text())
    assert REQUIRED_SECTIONS <= set(config)


def test_unset_research_decisions_are_visible() -> None:
    config = yaml.safe_load(CONFIG.read_text())
    assert config["data"]["department"] is None
    assert config["backtest"]["seed"] is None
    assert config["solver"]["time_limit_s"] is None


def test_main_experiment_keeps_all_scarcity_regimes() -> None:
    config = yaml.safe_load(CONFIG.read_text())
    assert config["operational_layer"]["scarcity_ratios"] == [0.6, 0.8, 1.0, 1.2]
