#!/usr/bin/env bash
# createTask -> poll -> download, via curl (node fetch flakes on this network)
set -u
KEY=$(grep KIE_API_KEY "$(dirname "$0")/.env" | cut -d= -f2 | tr -d '\r')
MODEL="$1"; INPUT="$2"; OUT="$3"

TASK=$(curl -s -X POST "https://api.kie.ai/api/v1/jobs/createTask" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"input\":$(cat "$INPUT")}" \
  | py -c "import sys,json; print(json.load(sys.stdin)['data']['taskId'])")
[ -z "$TASK" ] && { echo "no taskId"; exit 2; }
echo "task=$TASK -> $OUT"

for i in $(seq 1 90); do
  sleep 5
  RESP=$(curl -s -H "Authorization: Bearer $KEY" "https://api.kie.ai/api/v1/jobs/recordInfo?taskId=$TASK")
  STATE=$(echo "$RESP" | py -c "import sys,json; print(json.load(sys.stdin)['data']['state'])" 2>/dev/null)
  case "$STATE" in
    success)
      URL=$(echo "$RESP" | py -c "import sys,json; d=json.load(sys.stdin); print(json.loads(d['data']['resultJson'])['resultUrls'][0])")
      CR=$(echo "$RESP" | py -c "import sys,json; print(json.load(sys.stdin)['data'].get('creditsConsumed'))")
      curl -s -o "$OUT" "$URL" && echo "saved $OUT (credits: $CR)"
      exit 0 ;;
    fail)
      echo "FAILED: $(echo "$RESP" | py -c "import sys,json; d=json.load(sys.stdin)['data']; print(d.get('failCode'), d.get('failMsg'))")"
      exit 3 ;;
    *) printf "[%s] %s " "$i" "$STATE" ;;
  esac
done
echo "TIMEOUT"; exit 4
