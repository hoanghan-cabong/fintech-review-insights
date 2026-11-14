"""Đọc tập đáp án: tập ngẫu nhiên (random) và tập ca khó (hard).

Nếu có data/labels/adjudication.csv (vòng rà soát nhãn, D020), các nhãn đã sửa ở đó
được áp lên trên nhãn gốc. File nhãn gốc không bao giờ bị ghi đè.
"""
import csv

from config import LABEL_DIR

FIELDS = ["category", "severity", "flow", "social_engineering"]


def _complete(r: dict) -> bool:
    if not (r["category"] and r["severity"]):
        return False
    if r["category"] == "TXN_FAILURE" and not r["flow"]:
        return False
    if r["category"] == "FRAUD_SECURITY" and not r["social_engineering"]:
        return False
    return True


def load_adjudication() -> dict[str, dict]:
    """Trả về các review có nhãn bị sửa trong vòng rà soát: review_id -> nhãn mới + lý do."""
    f = LABEL_DIR / "adjudication.csv"
    if not f.exists():
        return {}
    return {r["review_id"]: r for r in csv.DictReader(f.open(encoding="utf-8-sig"))}


def load_golden(apply_adjudication: bool = True) -> list[dict]:
    """Trả về danh sách review kèm nhãn và trường `split` = random | hard."""
    out = []
    for r in csv.DictReader((LABEL_DIR / "random_set_v2.csv").open(encoding="utf-8-sig")):
        out.append({**r, "split": "random"})
    for r in csv.DictReader((LABEL_DIR / "hard_pool.csv").open(encoding="utf-8-sig")):
        # Bỏ các dòng lỡ đánh dấu chọn nhưng chưa gắn nhãn (D018)
        if r["pick"] == "1" and _complete(r):
            out.append({**r, "split": "hard"})
    if apply_adjudication:
        adj = load_adjudication()
        for r in out:
            a = adj.get(r["review_id"])
            if a and _complete(a):
                r.update({k: a[k] for k in FIELDS})
    return out


def load_test(require_complete: bool = True) -> list[dict]:
    """Tập kiểm tra cuối (D021): gắn nhãn trước khi chạy model, chỉ dùng để báo cáo kết quả cuối."""
    rows = [{**r, "split": "test"} for r in csv.DictReader((LABEL_DIR / "test_set.csv").open(encoding="utf-8-sig"))]
    if require_complete:
        todo = [r["review_id"] for r in rows if not _complete(r)]
        if todo:
            raise SystemExit(f"Tập kiểm tra còn {len(todo)} review chưa đủ nhãn, ví dụ {todo[:3]}. "
                             "Gắn nhãn xong rồi mới chạy model.")
    return rows


def load_set(name: str) -> list[dict]:
    return load_test() if name == "test" else load_golden()


if __name__ == "__main__":
    g = load_golden()
    print(len(g), "review:", sum(r["split"] == "random" for r in g), "random,",
          sum(r["split"] == "hard" for r in g), "hard")
