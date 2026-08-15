"""Upload a local image to KIE file storage and print its public URL."""
import base64
import json
import mimetypes
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
KEY = next(
    line.split("=", 1)[1].strip()
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines()
    if line.startswith("KIE_API_KEY=")
)

src = Path(sys.argv[1])
mime = mimetypes.guess_type(src.name)[0] or "image/jpeg"
payload = {
    "base64Data": f"data:{mime};base64,{base64.b64encode(src.read_bytes()).decode()}",
    "uploadPath": "images/glowaroma",
    "fileName": src.name,
}
body = ROOT / "kie_inputs" / f"_upload_{src.stem}.json"
body.write_text(json.dumps(payload), encoding="utf-8")

out = subprocess.run(
    ["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-base64-upload",
     "-H", f"Authorization: Bearer {KEY}", "-H", "Content-Type: application/json",
     "--data-binary", f"@{body}"],
    capture_output=True, text=True,
).stdout
body.unlink(missing_ok=True)

data = json.loads(out)
if not data.get("success", True) and "data" not in data:
    print("ERROR:", out[:400])
    sys.exit(1)
print(data["data"]["downloadUrl"])
