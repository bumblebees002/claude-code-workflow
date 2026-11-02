#!/usr/bin/env python3
"""Recover an accessible Claude Code artifact from a Chromium disk cache."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


UUID_RE = re.compile(
    r"(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"
)
DOCTYPE_RE = re.compile(br"<!doctype\s+html[^>]*>", re.IGNORECASE)


def parse_artifact_uuid(value: str) -> str:
    match = UUID_RE.search(value)
    if not match:
        raise ValueError("Expected a Claude artifact URL or UUID.")
    artifact_uuid = match.group("uuid").lower()
    if "/code/artifact/" in value:
        parsed = urlparse(value)
        if parsed.scheme != "https" or parsed.hostname not in {"claude.ai", "www.claude.ai"}:
            raise ValueError("Artifact URL must use https://claude.ai/code/artifact/<uuid>.")
    return artifact_uuid


def default_cache_roots() -> list[Path]:
    home = Path.home()
    return [
        home / "Library/Caches/Google/Chrome",
        home / "Library/Caches/BraveSoftware/Brave-Browser",
    ]


def matching_url_pattern(artifact_uuid: str) -> re.Pattern[bytes]:
    host = re.escape(artifact_uuid.encode("ascii"))
    return re.compile(
        rb"https://"
        + host
        + rb"\.frame\.claudeusercontent\.com/_f/"
        + rb"[A-Za-z0-9._-]+/\?__frame_(?:v=manifest\.[A-Za-z0-9._-]+\.json|t=[A-Za-z0-9._~-]+)"
    )


def scan_file(path: Path, pattern: re.Pattern[bytes]) -> set[str]:
    matches: set[str] = set()
    overlap = b""
    try:
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                block = overlap + chunk
                matches.update(match.group(0).decode("ascii") for match in pattern.finditer(block))
                overlap = block[-2048:]
    except (OSError, PermissionError):
        return set()
    return matches


def find_frame_url(artifact_uuid: str, roots: list[Path], since_minutes: int) -> str:
    pattern = matching_url_pattern(artifact_uuid)
    cutoff = time.time() - since_minutes * 60 if since_minutes > 0 else None
    cache_files: list[tuple[float, Path]] = []
    for root in roots:
        if not root.is_dir():
            continue
        for directory, _, filenames in os.walk(root):
            if not (directory.endswith("Cache_Data") or "/Cache_Data/" in directory):
                continue
            for filename in filenames:
                path = Path(directory) / filename
                try:
                    stat = path.stat()
                except OSError:
                    continue
                if cutoff is not None and stat.st_mtime < cutoff:
                    continue
                cache_files.append((stat.st_mtime, path))
    cache_files.sort(reverse=True)
    for _, path in cache_files:
        matches = scan_file(path, pattern)
        if matches:
            return sorted(matches)[-1]
    raise FileNotFoundError(
        f"No recent Chrome/Brave cache entry was found for artifact {artifact_uuid}. "
        "Open the artifact successfully in the browser, then retry."
    )


def download_html(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 Chrome/152 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content_type = response.headers.get_content_type()
            payload = response.read()
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Artifact frame download failed with HTTP {error.code}.") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Artifact frame download failed: {error.reason}") from error
    if content_type not in {"text/html", "application/xhtml+xml"}:
        raise RuntimeError(f"Expected HTML but received {content_type}.")
    if not DOCTYPE_RE.search(payload):
        raise RuntimeError("Downloaded response does not contain an HTML document.")
    return payload


def authored_html(payload: bytes) -> bytes:
    doctypes = list(DOCTYPE_RE.finditer(payload))
    return payload[doctypes[1].start() :] if len(doctypes) >= 2 else payload


def write_atomic(destination: Path, payload: bytes, force: bool) -> None:
    destination = destination.expanduser().resolve()
    if destination.exists() and not force:
        raise FileExistsError(f"Output already exists: {destination}; use --force to replace it.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            if not payload.endswith(b"\n"):
                handle.write(b"\n")
        temporary_path.replace(destination)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract a loaded Claude Code artifact as standalone HTML."
    )
    parser.add_argument("artifact", help="Claude artifact URL or UUID")
    parser.add_argument("output", type=Path, help="Destination .html file")
    parser.add_argument("--cache-root", action="append", type=Path, default=[])
    parser.add_argument("--since-minutes", type=int, default=120)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        artifact_uuid = parse_artifact_uuid(args.artifact)
        roots = args.cache_root or default_cache_roots()
        frame_url = find_frame_url(artifact_uuid, roots, args.since_minutes)
        payload = authored_html(download_html(frame_url))
        if artifact_uuid.encode("ascii") in payload and b"Page not found" in payload:
            raise RuntimeError("Claude returned a not-found page instead of the artifact.")
        write_atomic(args.output, payload, args.force)
        destination = args.output.expanduser().resolve()
        print(f"Extracted artifact {artifact_uuid}")
        print(f"Output: {destination}")
        print(f"Bytes: {destination.stat().st_size}")
        return 0
    except (FileNotFoundError, FileExistsError, RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
