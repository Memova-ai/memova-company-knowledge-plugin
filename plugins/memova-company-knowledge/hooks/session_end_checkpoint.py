"""Record one local pointer for later semantic review; never send transcript content."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path


def _private_root() -> Path:
    raw = os.environ.get("PLUGIN_DATA", "")
    if not raw:
        raise ValueError("plugin data directory unavailable")
    root = Path(raw).expanduser().resolve() / "knowledge-capture-pending"
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if root.is_symlink() or not root.is_dir() or stat.S_IMODE(root.stat().st_mode) & 0o077:
        raise ValueError("plugin data directory is not private")
    return root


def _event() -> dict[str, object]:
    value = json.load(sys.stdin)
    if not isinstance(value, dict):
        raise ValueError("invalid hook event")
    return value


def main() -> None:
    event = _event()
    session_id = event.get("session_id")
    transcript_path = event.get("transcript_path")
    if (
        event.get("hook_event_name") != "SessionEnd"
        or not isinstance(session_id, str)
        or not 1 <= len(session_id) <= 200
        or not isinstance(transcript_path, str)
        or not Path(transcript_path).is_absolute()
    ):
        return
    root = _private_root()
    identity = hashlib.sha256(session_id.encode()).hexdigest()
    destination = root / f"{identity}.json"
    if destination.exists():
        return
    record = {
        "schema_version": "company-knowledge-ended-session-pointer-v1",
        "session_id": session_id,
        "transcript_path": transcript_path,
        "review_status": "pending_semantic_review",
        "recorded_at": datetime.now(UTC).isoformat(),
    }
    descriptor, temporary_name = tempfile.mkstemp(prefix=".pending-", dir=root)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(record, handle, ensure_ascii=False, sort_keys=True)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError:
            pass
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # SessionEnd is advisory and limited to three seconds. Never expose local paths or content.
        raise SystemExit(0) from None
