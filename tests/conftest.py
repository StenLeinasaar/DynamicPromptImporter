import json
from pathlib import Path


def pytest_configure(config):
    """Initialise storage for test results."""
    config._results = []


import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Collect outcome information for each test."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        item.config._results.append({
            "nodeid": report.nodeid,
            "outcome": report.outcome,
            "duration": getattr(report, "duration", None),
            "longrepr": str(report.longrepr) if report.failed else "",
        })


def pytest_sessionfinish(session, exitstatus):
    """Write a simple JSON report when the session finishes."""
    path = Path(session.config.rootdir) / "test_report.json"
    data = {"exitstatus": exitstatus, "results": session.config._results}
    path.write_text(json.dumps(data, indent=2))
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if reporter:
        reporter.write_line(f"JSON report written to {path}")
