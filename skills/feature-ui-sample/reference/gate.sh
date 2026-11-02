#!/bin/zsh
# Ingredient gate for feature-ui-sample. Usage: zsh gate.sh <samples-dir> [theme-key-prefix]
# Silence per file = pass. Prints line counts at the end.
dir=${1:-design-samples}
cd "$dir" || { echo "no such dir: $dir"; exit 1; }
for f in [0-9]*.html; do
  grep -q 'stroke-dasharray' "$f"          || echo "$f: FAIL no radial chart (stroke-dasharray)"
  grep -q '@keyframes' "$f"                || echo "$f: FAIL no entry motion"
  grep -qE 'pointermove|mousemove' "$f"    || echo "$f: FAIL no cursor interaction"
  grep -q 'data-theme' "$f"                || echo "$f: FAIL no theme toggle"
  grep -q 'prefers-reduced-motion' "$f"    || echo "$f: FAIL no reduced-motion"
  grep -q 'fonts.googleapis.com/css2' "$f" || echo "$f: FAIL no font link"
  grep -q 'id="design-dna"' "$f"           || echo "$f: FAIL no design-dna footer"
  grep -q 'How it would work' "$f"         || echo "$f: FAIL no 'How it would work'"
  grep -q 'id="ideas-next"' "$f"           || echo "$f: FAIL no ideas-next section"
  grep -q 'Ideas not built yet' "$f"       || echo "$f: FAIL no 'Ideas not built yet'"
  grep -qi 'script src=' "$f"              && echo "$f: FAIL external script"
  grep -q 'fetch(' "$f"                    && echo "$f: FAIL fetch"
  for t in --bg --surface --surface-2 --line --ink --muted --accent --accent-2 --good --warn --bad --radius --font-display --font-body --font-mono; do
    c=$(grep -c -- "$t:" "$f"); [[ "$c" -lt 1 ]] && echo "$f: FAIL missing token $t"
  done
  n=$(awk '/<script>/{on=1;c=0;next} /<\/script>/{if(on)print c;on=0} on{c++}' "$f" | sort -n | tail -1)
  [[ -n "$n" && "$n" -gt 40 ]] && echo "$f: WARN script is $n lines (>40)"
  sc=$(grep -c '<script' "$f"); [[ "$sc" -gt 1 ]] && echo "$f: WARN $sc script tags"
  ext=$(grep -oE '(href|src)="https?://[^"]*"' "$f" | grep -vE 'fonts\.(googleapis|gstatic)\.com')
  [[ -n "$ext" ]] && echo "$f: FAIL non-font external: $ext"
  grep -qE '(^|[},; ])(html|body)[^{]*\{[^}]*overflow-x: *hidden' "$f" && echo "$f: WARN page-level overflow-x:hidden (fix the cause; use clip as safety net)"
  ideas=$(awk '/id="ideas-next"/{on=1} on&&/<li/{c++} /<\/footer>/{on=0} END{print c+0}' "$f")
  [[ "$ideas" -lt 6 ]] && echo "$f: WARN only $ideas idea items (want 6-10)"
done
echo "--- line counts"; wc -l [0-9]*.html
