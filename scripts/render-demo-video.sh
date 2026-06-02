#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK_DIR="${TMPDIR:-/tmp}/riskguard-demo-video"
SLIDE_DIR="$WORK_DIR/slides"
FRAME_DIR="$WORK_DIR/frames"
OUT_DIR="$ROOT_DIR/dist"
OUT_FILE="$OUT_DIR/riskguard-demo.mp4"

CHROME_BIN="${CHROME_BIN:-google-chrome}"

rm -rf "$WORK_DIR"
mkdir -p "$SLIDE_DIR" "$FRAME_DIR" "$OUT_DIR"

write_slide() {
  local index="$1"
  local kicker="$2"
  local title="$3"
  local body="$4"
  local file="$SLIDE_DIR/slide-$index.html"

  cat >"$file" <<EOF
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        width: 1280px;
        height: 720px;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
        background: #f7f8fa;
        color: #121417;
      }
      main {
        width: 1280px;
        height: 720px;
        padding: 72px;
        display: grid;
        align-content: center;
        gap: 30px;
        background: #ffffff;
        border: 24px solid #f7f8fa;
      }
      .kicker {
        margin: 0;
        color: #1f7a5c;
        font-weight: 800;
        font-size: 24px;
        letter-spacing: 0;
        text-transform: uppercase;
      }
      h1 {
        margin: 0;
        max-width: 1040px;
        font-size: 64px;
        line-height: 1.04;
      }
      .body {
        max-width: 1040px;
        color: #56616f;
        font-size: 34px;
        line-height: 1.28;
      }
      .body ul {
        margin: 0;
        padding-left: 36px;
      }
      .body li + li {
        margin-top: 10px;
      }
      code {
        color: #2d4f8f;
        font-weight: 700;
      }
    </style>
  </head>
  <body>
    <main>
      <p class="kicker">$kicker</p>
      <h1>$title</h1>
      <div class="body">$body</div>
    </main>
  </body>
</html>
EOF
}

write_slide "01" "RiskGuard Adapter" "DeFi policy verdict receipts for BNB Chain agents." "<ul><li>BSC testnet deployed</li><li>Two receipt transactions</li><li>Open source + tested</li></ul>"
write_slide "02" "Problem" "Agents can propose financial actions faster than users can review." "<ul><li>Blind trust is risky</li><li>Manual review does not scale</li><li>Policy evidence should exist before execution</li></ul>"
write_slide "03" "Solution" "RiskGuard checks proposed actions against declared policy." "<ul><li>Chain, value, action, token, target and slippage</li><li>Deterministic <code>allow</code> or <code>block</code> receipts</li></ul>"
write_slide "04" "Demo" "One policy-compliant action receives an allow verdict." "<ul><li><code>riskguard validate</code></li><li>Stable proposal, policy, simulation and evidence hashes</li></ul>"
write_slide "05" "Demo" "One policy-violating action receives a block verdict." "<ul><li>Slippage 500 bps exceeds max 100 bps</li><li>Receipt includes concrete reason</li></ul>"
write_slide "06" "Proof" "BSC testnet receipt registry has count 2." "<ul><li>Contract: <code>0x1093...AC1</code></li><li>Allow tx + block tx</li></ul>"
write_slide "07" "Integration" "Manifest-only ERC-8183 evidence payload is implemented." "<ul><li>RiskGuard receipt hash in <code>DeliverableManifest.metadata</code></li><li>No real ERC-8183 settlement claim</li></ul>"
write_slide "08" "Scope" "Small policy-verdict adapter, ready for lightweight integration experiments." "<ul><li>No mainnet funds</li><li>No custody</li><li>No production security claim</li></ul>"

for file in "$SLIDE_DIR"/slide-*.html; do
  base="$(basename "$file" .html)"
  "$CHROME_BIN" \
    --headless \
    --disable-gpu \
    --no-sandbox \
    --window-size=1280,720 \
    --screenshot="$FRAME_DIR/$base.png" \
    "file://$file" >/dev/null 2>&1
done

cat >"$WORK_DIR/concat.txt" <<EOF
file '$FRAME_DIR/slide-01.png'
duration 6
file '$FRAME_DIR/slide-02.png'
duration 6
file '$FRAME_DIR/slide-03.png'
duration 6
file '$FRAME_DIR/slide-04.png'
duration 6
file '$FRAME_DIR/slide-05.png'
duration 6
file '$FRAME_DIR/slide-06.png'
duration 6
file '$FRAME_DIR/slide-07.png'
duration 6
file '$FRAME_DIR/slide-08.png'
duration 6
file '$FRAME_DIR/slide-08.png'
duration 1
EOF

ffmpeg \
  -hide_banner \
  -loglevel error \
  -y \
  -f concat \
  -safe 0 \
  -i "$WORK_DIR/concat.txt" \
  -vf "scale=1280:720,format=yuv420p" \
  -r 30 \
  "$OUT_FILE"

echo "$OUT_FILE"
