"""The reply-bearing ``call_kind`` list is duplicated; hold the copies together.

A drift between the chat loop's declared ``call_kind`` set and
``deeptutor.core.trace.ANSWER_BEARING_CALL_KINDS`` fails silently and in the
worst possible way: the text streams, the trace shows it, and the message body
drops it. Nothing raises, no test that stubs one side notices, and the turn
looks like the model returned nothing.
"""

from __future__ import annotations

from pathlib import Path
import re

from deeptutor.core.trace import ANSWER_BEARING_CALL_KINDS

_REPO_ROOT = Path(__file__).resolve().parents[2]
_AGENT_LOOP_PY = _REPO_ROOT / "deeptutor" / "agents" / "loop" / "agent_loop.py"


def test_the_chat_loop_only_streams_answers_under_declared_kinds() -> None:
    """Every ``call_kind`` the chat loop labels its own rounds with is declared.

    The loop is the one place that streams a user-facing reply through this
    filter, so a kind it introduces without declaring here would have its text
    dropped from the message body.
    """
    source = _AGENT_LOOP_PY.read_text(encoding="utf-8")
    used = set(re.findall(r'call_kind="([a-z_]+)"', source))
    assert used, "expected the chat loop to label its rounds"
    assert used <= set(ANSWER_BEARING_CALL_KINDS), sorted(used - ANSWER_BEARING_CALL_KINDS)
