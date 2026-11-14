"""Chạy agent đã chốt (Opus + prompt v2, D022) trên mẫu lớn để phân tích đối thủ (tuần 4, D023).

Lấy mẫu phân tầng theo app và nhóm sao trong số review >= 5 từ:
- tầng "low" (1–3 sao): tối đa 450 review mỗi app
- tầng "high" (4–5 sao): tối đa 150 review mỗi app
Khi phân tích, mỗi review được gán trọng số = số review của tầng / số review được lấy mẫu,
để kết quả phản ánh đúng phân phối thật.

Chạy song song vài lô một lúc; kết quả từng lô được cache nên dừng giữa chừng thì chạy lại sẽ tiếp tục.
Chạy: .venv/bin/python src/classify_corpus.py
"""
import csv
import hashlib
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from agent import call_claude
from config import CLEAN_DIR, DATA, MIN_WORDS, ROOT, STUDY_APPS

MODEL, PROMPT = "opus", "v2"
CAP = {"low": 450, "high": 150}
SEED, BATCH, WORKERS = 4, 20, 3
OUT_DIR = DATA / "corpus"
CACHE = DATA / "cache" / f"corpus_{PROMPT}_{MODEL}"


def stratum(r):
    return "low" if int(r["score"]) <= 3 else "high"


def build_sample():
    rows = [r for r in csv.DictReader((CLEAN_DIR / "reviews.csv").open(encoding="utf-8"))
            if r["app"] in STUDY_APPS and int(r["n_words"]) >= MIN_WORDS]
    rng = random.Random(SEED)
    sample, weights = [], {}
    for app in STUDY_APPS:
        for st in ("low", "high"):
            pool = [r for r in rows if r["app"] == app and stratum(r) == st]
            pick = pool if len(pool) <= CAP[st] else rng.sample(pool, CAP[st])
            weights[(app, st)] = len(pool) / len(pick) if pick else 0
            sample += [{**r, "stratum": st} for r in pick]
    for r in sample:
        r["weight"] = round(weights[(r["app"], r["stratum"])], 4)
    return sample


def run_batch(system, batch):
    key = hashlib.sha1((system + "".join(r["review_id"] for r in batch)).encode()).hexdigest()[:12]
    f = CACHE / f"{key}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8")), False
    for attempt in range(1, 4):
        try:
            results, meta = call_claude(system, batch, MODEL)
            saved = {"results": results, "meta": meta}
            f.write_text(json.dumps(saved, ensure_ascii=False), encoding="utf-8")
            return saved, True
        except Exception as e:  # lỗi tạm thời, giới hạn tốc độ, JSON hỏng…
            msg = str(e)[:200]
            if "limit" in msg.lower() and attempt == 3:
                raise
            print(f"    lỗi (lần {attempt}): {msg}; thử lại sau {60 * attempt}s", flush=True)
            time.sleep(60 * attempt)
    raise RuntimeError("Lô thất bại sau 3 lần thử")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    sample = build_sample()
    with (OUT_DIR / "sample.csv").open("w", encoding="utf-8", newline="") as f:
        cols = ["review_id", "app", "date", "score", "app_version", "stratum", "weight",
                "has_reply", "reply_hours", "content"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(sample)
    print(f"Mẫu: {len(sample)} review", flush=True)

    system = (ROOT / "prompts" / f"classifier_{PROMPT}.md").read_text(encoding="utf-8")
    preds, metas = {}, []
    t0 = time.time()

    def collect(saved, batch):
        metas.append(saved["meta"])
        ids = {r["review_id"] for r in batch}
        for p in saved["results"]:
            if p["review_id"] in ids:
                preds[p["review_id"]] = p

    for round_ in (1, 2, 3):  # vòng 1: toàn bộ; vòng 2–3: gọi lại review bị model bỏ sót
        todo = [r for r in sample if r["review_id"] not in preds]
        if not todo:
            break
        batches = [todo[i:i + BATCH] for i in range(0, len(todo), BATCH)]
        print(f"Vòng {round_}: {len(todo)} review, {len(batches)} lô", flush=True)
        done = 0
        with ThreadPoolExecutor(WORKERS) as ex:
            futs = {ex.submit(run_batch, system, b): b for b in batches}
            for fut in as_completed(futs):
                saved, fresh = fut.result()
                collect(saved, futs[fut])
                done += 1
                if fresh and done % 10 == 0:
                    print(f"  {done}/{len(batches)} lô · {len(preds)} review · {time.time() - t0:.0f}s", flush=True)

    with (OUT_DIR / f"preds_{PROMPT}_{MODEL}.jsonl").open("w", encoding="utf-8") as f:
        for r in sample:
            if r["review_id"] in preds:
                f.write(json.dumps(preds[r["review_id"]], ensure_ascii=False) + "\n")
    cost = sum(m["cost_usd"] for m in metas)
    summary = {"n_sample": len(sample), "n_pred": len(preds), "wall_seconds": round(time.time() - t0),
               "cost_usd_equiv": round(cost, 2)}
    (OUT_DIR / "run_meta.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
