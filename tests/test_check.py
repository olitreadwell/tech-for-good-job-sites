"""Tests for link-check fallback classification. Run with: pytest"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import scripts.check as check
from scripts.check import failed_urls


def test_failed_urls_reads_error_statuses_from_stderr():
    output = "[503] https://example.com/a (at 1:1) | Service unavailable"
    assert failed_urls(output) == {"https://example.com/a"}


def test_failed_urls_reads_errors_and_timeouts_from_stdout():
    output = "\n".join(
        [
            "[ERROR] https://example.com/b (at 2:1) | TLS failure",
            "[TIMEOUT] https://example.com/c (at 3:1) | Timed out",
        ]
    )
    assert failed_urls(output) == {"https://example.com/b", "https://example.com/c"}


def test_main_fails_when_lychee_errors_without_parsed_urls(monkeypatch, capsys):
    monkeypatch.setattr(check, "live_urls", lambda: ["https://example.com"])
    monkeypatch.setattr(
        check.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 1, "", "lychee crashed"),
    )

    assert check.main() == 1
    assert "without parseable failures" in capsys.readouterr().err


def test_main_accepts_timeout_when_fallback_returns_200(monkeypatch, capsys):
    def fake_run(cmd, *args, **kwargs):
        if cmd[0] == "lychee":
            return subprocess.CompletedProcess(
                cmd, 1, "[TIMEOUT] https://example.com (at 1:1) | timed out", ""
            )
        return subprocess.CompletedProcess(cmd, 0, "200", "")

    monkeypatch.setattr(check, "live_urls", lambda: ["https://example.com"])
    monkeypatch.setattr(check.subprocess, "run", fake_run)

    assert check.main() == 0
    assert "fallback ok: https://example.com (200)" in capsys.readouterr().out


def test_main_rejects_failure_when_fallback_cannot_connect(monkeypatch, capsys):
    def fake_run(cmd, *args, **kwargs):
        if cmd[0] == "lychee":
            return subprocess.CompletedProcess(
                cmd, 1, "[ERROR] https://example.com (at 1:1) | TLS failure", ""
            )
        return subprocess.CompletedProcess(cmd, 7, "000", "Could not connect")

    monkeypatch.setattr(check, "live_urls", lambda: ["https://example.com"])
    monkeypatch.setattr(check.subprocess, "run", fake_run)

    assert check.main() == 1
    assert "still failing: https://example.com (no response)" in capsys.readouterr().out
