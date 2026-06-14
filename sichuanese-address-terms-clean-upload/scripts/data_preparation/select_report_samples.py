import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(r"C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab")
TRAIN_CSV = Path(r"C:\Users\13398\Downloads\train_9800.csv")
TEST_CSV = Path(r"C:\Users\13398\Downloads\test_200.csv")
DICT_JSON = Path(r"C:\Users\13398\Downloads\四川话人称称谓词典_研究候选_JSON版.json")

OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)
OUT_CSV = OUT_DIR / "sichuan_person_terms_report_150.csv"
OUT_SUMMARY = OUT_DIR / "sichuan_person_terms_report_150_summary.csv"


CATEGORY_ORDER = ["kinship", "solidarity", "affectionate", "hierarchy", "insult"]
TARGET_PER_CATEGORY = {
    "kinship": 30,
    "solidarity": 30,
    "affectionate": 30,
    "hierarchy": 30,
    "insult": 30,
}


SEEDS = {
    "kinship": {
        "老汉儿", "老汉", "婆娘", "堂客", "婆姨", "老婆", "老公", "爸爸", "妈妈", "爸", "妈",
        "爷爷", "奶奶", "外公", "外婆", "公公", "婆婆", "哥哥", "姐姐", "妹妹", "弟弟",
        "大哥", "大姐", "哥", "姐", "弟", "妹", "儿子", "女儿", "媳妇", "媳妇儿", "女婿",
        "亲戚", "家人", "父母", "兄弟", "姐妹", "两口子",
    },
    "solidarity": {
        "兄弟伙", "兄弟伙些", "兄弟", "弟兄", "朋友", "朋友些", "同学", "同事", "伙计",
        "老乡", "哥们", "姐们", "粉丝", "网友", "邻居", "大家", "我们", "咱们",
    },
    "affectionate": {
        "幺儿", "幺女", "幺妹", "幺妹儿", "幺娃", "幺娃儿", "娃儿", "娃娃", "小娃",
        "小娃儿", "女娃", "女娃儿", "男娃", "男娃儿", "妹儿", "妹子", "宝贝", "乖乖",
        "小朋友", "小妹妹", "小哥哥", "小姐姐", "小伙子", "姑娘", "丫头",
    },
    "hierarchy": {
        "师傅", "师父", "老师", "老板", "老板娘", "医生", "护士", "客户", "客人", "顾客",
        "服务员", "店员", "司机", "厨师", "主播", "阿姨", "叔叔", "叔", "大叔", "大爷",
        "大妈", "老爷子", "老太太", "老太婆", "嬢嬢", "孃孃", "娘娘", "哥老倌",
    },
    "insult": {
        "龟儿子", "龟儿", "瓜娃子", "瓜娃儿", "哈儿", "哈麻批", "哈批", "傻子", "疯子",
        "憨包", "宝器", "杂种", "神经病", "狗东西", "坏人",
    },
}


def load_dictionary_terms():
    data = json.loads(DICT_JSON.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    term_to_meta = {}
    for entry in entries:
        term = str(entry.get("term", "")).strip()
        if not term:
            continue
        term_to_meta[term] = entry
    return term_to_meta


def build_category_terms(term_to_meta):
    category_terms = {cat: set(words) for cat, words in SEEDS.items()}
    for term, entry in term_to_meta.items():
        categories = " ".join(map(str, entry.get("categories", [])))
        functions = " ".join(map(str, entry.get("person_function", [])))
        tone = str(entry.get("tone", ""))

        if "evaluative_or_pejorative_address" in functions or "pejorative" in tone or "骂称" in categories:
            category_terms["insult"].add(term)
        if "affectionate" in tone or "娃儿年龄性别称谓" in categories:
            category_terms["affectionate"].add(term)
        if "kinship_term" in functions or "gender_or_spouse_reference" in functions or "亲属" in categories or "配偶" in categories:
            category_terms["kinship"].add(term)
        if "elder_reference_or_honorific" in functions or "长辈" in categories:
            category_terms["hierarchy"].add(term)

    # Keep report categories focused; remove core one-character pronouns from solidarity.
    for generic in ["我", "你", "他", "她", "它", "这个", "那个"]:
        for terms in category_terms.values():
            terms.discard(generic)
    return category_terms


def find_terms(text, terms):
    found = [term for term in terms if term and term in text]
    return sorted(set(found), key=lambda x: (-len(x), x))


def score_row(text, terms):
    length = len(text)
    dialect_bonus = sum(3 for t in terms if t in {"老汉儿", "婆娘", "幺儿", "幺妹儿", "兄弟伙", "龟儿子", "哈麻批", "师傅", "老板"})
    count_bonus = min(len(terms), 4) * 2
    length_score = 8 if 18 <= length <= 90 else 4 if 10 <= length <= 130 else 0
    return dialect_bonus + count_bonus + length_score


def main():
    term_to_meta = load_dictionary_terms()
    category_terms = build_category_terms(term_to_meta)

    frames = []
    for split, path in [("train_9800", TRAIN_CSV), ("test_200", TEST_CSV)]:
        df = pd.read_csv(path).fillna("")
        df["input_file"] = split
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["text"] = df["text"].astype(str)

    candidates = defaultdict(list)
    for idx, row in df.iterrows():
        text = row["text"]
        if not text or len(text) < 2:
            continue
        for cat in CATEGORY_ORDER:
            terms = find_terms(text, category_terms[cat])
            if not terms:
                continue
            candidates[cat].append({
                "row_id": idx,
                "target_category": cat,
                "target_terms": " ".join(terms),
                "input_file": row["input_file"],
                "source_file": row["source_file"],
                "utt_or_id": row["utt_or_id"],
                "filename": row["filename"],
                "text": text,
                "matched_terms_original": row["matched_terms"],
                "text_length": len(text),
                "score": score_row(text, terms),
            })

    selected = []
    used_rows = set()

    # First pass: balanced high-quality rows per category.
    for cat in CATEGORY_ORDER:
        pool = sorted(candidates[cat], key=lambda r: (-r["score"], r["text_length"], str(r["utt_or_id"])))
        term_counts = Counter()
        taken = 0
        for row in pool:
            if row["row_id"] in used_rows:
                continue
            # Encourage term variety: avoid one category being dominated by the same term.
            primary_term = row["target_terms"].split()[0]
            if term_counts[primary_term] >= 5:
                continue
            selected.append(row)
            used_rows.add(row["row_id"])
            term_counts[primary_term] += 1
            taken += 1
            if taken >= TARGET_PER_CATEGORY[cat]:
                break

        # Fill if variety constraint made the category short.
        if taken < TARGET_PER_CATEGORY[cat]:
            for row in pool:
                if row["row_id"] in used_rows:
                    continue
                selected.append(row)
                used_rows.add(row["row_id"])
                taken += 1
                if taken >= TARGET_PER_CATEGORY[cat]:
                    break

    out = pd.DataFrame(selected)
    out = out.drop(columns=["row_id", "score"])
    out.insert(0, "sample_id", [f"SCPR_{i:03d}" for i in range(1, len(out) + 1)])
    out["analysis_note"] = ""
    out["model_1_output"] = ""
    out["model_2_output"] = ""
    out["model_3_output"] = ""
    out["translation_issue"] = ""

    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)

    summary_rows = []
    for cat in CATEGORY_ORDER:
        sub = out[out["target_category"] == cat]
        term_counter = Counter()
        for text in sub["target_terms"]:
            term_counter.update(str(text).split())
        summary_rows.append({
            "target_category": cat,
            "selected_rows": len(sub),
            "top_terms": " ".join([f"{k}:{v}" for k, v in term_counter.most_common(12)]),
        })
    pd.DataFrame(summary_rows).to_csv(OUT_SUMMARY, index=False, encoding="utf-8-sig")

    print(f"selected_rows={len(out)}")
    print(out["target_category"].value_counts().reindex(CATEGORY_ORDER).fillna(0).astype(int).to_string())
    print(OUT_CSV)
    print(OUT_SUMMARY)


if __name__ == "__main__":
    main()
