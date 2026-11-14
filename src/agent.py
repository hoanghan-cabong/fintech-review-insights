"""Agent phân loại review: gọi Claude qua Claude Code CLI (`claude -p`), dùng gói Max.

- Chia review thành lô (mặc định 20 review/lô), mỗi lô một lần gọi.
- Đầu ra được ép theo JSON schema; kết quả mỗi lô được lưu cache để chạy lại không tốn thêm.
- Ghi lại thời gian và chi phí API quy đổi (CLI báo `total_cost_usd`) cho phần so sánh chi phí.

Chạy:
  .venv/bin/python src/agent.py --model haiku --prompt v1
  .venv/bin/python src/agent.py --model sonnet --prompt v1
"""
import argparse
import hashlib
import json
import subprocess
import time

from config import DATA, ROOT
from golden import load_set

PRED_DIR = DATA / "preds"
CACHE_DIR = DATA / "cache"
CATS = ["ONBOARD_EKYC", "AUTH_ACCESS", "TXN_FAILURE", "FRAUD_SECURITY", "FEES_LIMITS", "SUPPORT",
        "PROMO_REWARDS", "APP_EXPERIENCE", "NON_ISSUE"]
FLOWS = ["transfer", "payment", "topup_withdraw", "credit_bnpl", "unknown"]

SCHEMA = {
    "type": "object",
    "properties": {"results": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "review_id": {"type": "string"},
            "category": {"type": "string", "enum": CATS},
            "flow": {"type": ["string", "null"], "enum": FLOWS + [None]},
            "severity": {"type": "string", "enum": ["S1", "S2", "S3", "S4"]},
            "social_engineering": {"type": ["boolean", "null"]},
            "evidence": {"type": "string"},
        },
        "required": ["review_id", "category", "flow", "severity", "social_engineering", "evidence"],
    }}},
    "required": ["results"],
}


def call_claude(system: str, batch: list[dict], model: str) -> tuple[list[dict], dict]:
    payload = json.dumps([{"review_id": r["review_id"], "text": r["content"]} for r in batch], ensure_ascii=False)
    cmd = ["claude", "-p", "--model", model, "--tools", "", "--no-session-persistence",
           "--system-prompt", system, "--output-format", "json", "--json-schema", json.dumps(SCHEMA)]
    t0 = time.time()
    proc = subprocess.run(cmd, input=payload, capture_output=True, text=True, timeout=600, cwd=ROOT)
    out = json.loads(proc.stdout)
    if out.get("is_error"):
        raise RuntimeError(out.get("result"))
    data = out.get("structured_output")
    if data is None:  # dự phòng: một số phiên bản CLI trả JSON trong `result`
        text = out["result"]
        data = json.loads(text[text.find("{"): text.rfind("}") + 1])
    meta = {"seconds": round(time.time() - t0, 1), "cost_usd": out.get("total_cost_usd", 0),
            "usage": out.get("usage", {})}
    return data["results"], meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="haiku")
    ap.add_argument("--prompt", default="v1")
    ap.add_argument("--batch", type=int, default=20)
    ap.add_argument("--set", default="dev", choices=["dev", "test"])
    args = ap.parse_args()

    system = (ROOT / "prompts" / f"classifier_{args.prompt}.md").read_text(encoding="utf-8")
    golden = load_set(args.set)
    run = f"agent_{args.prompt}_{args.model}"
    pred_dir = PRED_DIR / "test" if args.set == "test" else PRED_DIR
    cache = CACHE_DIR / (run + ("_test" if args.set == "test" else ""))
    cache.mkdir(parents=True, exist_ok=True)
    pred_dir.mkdir(parents=True, exist_ok=True)

    preds, metas = {}, []

    def run_batch(batch, label):
        key = hashlib.sha1((system + "".join(r["review_id"] for r in batch)).encode()).hexdigest()[:12]
        f = cache / f"{key}.json"
        if f.exists():
            saved = json.loads(f.read_text(encoding="utf-8"))
        else:
            results, meta = call_claude(system, batch, args.model)
            saved = {"results": results, "meta": meta}
            f.write_text(json.dumps(saved, ensure_ascii=False), encoding="utf-8")
            print(f"  {label}: {len(results)}/{len(batch)} review, "
                  f"{meta['seconds']}s, ${meta['cost_usd']:.4f}", flush=True)
        metas.append(saved["meta"])
        ids = {r["review_id"] for r in batch}
        for p in saved["results"]:
            if p["review_id"] in ids:  # bỏ qua review_id do model tự bịa
                preds[p["review_id"]] = p

    for i in range(0, len(golden), args.batch):
        run_batch(golden[i:i + args.batch], f"lô {i // args.batch + 1}")

    # Model đôi khi bỏ sót review trong lô: gọi lại riêng các review bị thiếu (tối đa 2 lần)
    for attempt in (1, 2):
        todo = [r for r in golden if r["review_id"] not in preds]
        if not todo:
            break
        run_batch(todo, f"gọi lại lần {attempt}")

    missing =[r["review_id"] for r in golden if r["review_id"] not in preds]
    with (pred_dir / f"{run}.jsonl").open("w", encoding="utf-8") as fh:
        for r in golden:
            if r["review_id"] in preds:
                fh.write(json.dumps(preds[r["review_id"]], ensure_ascii=False) + "\n")
    summary = {"run": run, "n": len(golden), "missing": missing,
               "seconds": round(sum(m["seconds"] for m in metas), 1),
               "cost_usd": round(sum(m["cost_usd"] for m in metas), 4)}
    (pred_dir / f"{run}.meta.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{run}: {len(preds)}/{len(golden)} review, thiếu {len(missing)}, "
          f"{summary['seconds']}s, ${summary['cost_usd']}")


if __name__ == "__main__":
    main()
