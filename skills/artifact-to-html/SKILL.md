---
name: artifact-to-html
description: Extract standalone HTML from an accessible claude.ai/code/artifact link by recovering its loaded frame response from local Chrome or Brave cache. Not for conversation exports.
---

# Artifact to HTML

Convert an accessible `https://claude.ai/code/artifact/<uuid>` page into the authored standalone HTML without rewriting its design or application code.

The user's artifact URL and destination, if supplied, are in: `$ARGUMENTS`

## Workflow

1. Confirm the input is a Claude Code artifact URL containing a UUID and choose a non-conflicting `.html` destination.
2. Open the exact URL in a new tab in the user's existing signed-in Chrome or Brave session. Use browser automation when available; otherwise use permitted OS browser automation.
3. Wait up to 20 seconds and confirm the artifact title replaces the generic Claude loader title. A first request can transiently show `Page not found`; retry the exact URL up to three times before concluding access is unavailable.
4. Run the bundled extractor:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/extract_artifact.py" '<artifact-url>' '<output.html>'
   ```

   The script searches only cache entries containing the supplied UUID, selects the newest matching versioned frame URL, downloads it, removes Claude's outer frame runtime when present, and writes the authored HTML atomically.
5. Verify the output has a meaningful title/content and render it locally in an isolated browser. Confirm that the resulting DOM contains the artifact's expected page content rather than `Claude Artifact` or `Page not found`.
6. Close only the temporary tab created by this workflow and return an absolute path to the HTML file.

## Guardrails

- Do not pass the URL to `run-claude-artifact`; that CLI expects a local `.tsx` or `.jsx` source path.
- Do not use conversation exporters for standalone `/code/artifact/` URLs.
- Never extract browser cookies, Keychain credentials, history, or unrelated cache content. Do not print raw cache records or the recovered frame URL; the bundled script reports only the artifact UUID and output metadata.
- Do not upload client content to a third-party converter unless the user explicitly authorizes that external disclosure.
- Do not overwrite an existing output unless the user requested it or `--force` is explicitly chosen.
- Treat the recovered frame URL as sensitive and temporary; do not include it in the final response.
- The downloaded network response may contain Claude's sandbox wrapper. Removing that wrapper preserves the authored artifact HTML but means the final file is not byte-for-byte identical to the full network response.

## Failure Boundary

If the artifact does not visibly load in the user's browser after three attempts, or no matching cache entry appears, stop. The URL may be incomplete, deleted, expired, or inaccessible to that browser session; an open-source tool cannot bypass Claude's access control. Ask for the complete share URL or viewer access.
