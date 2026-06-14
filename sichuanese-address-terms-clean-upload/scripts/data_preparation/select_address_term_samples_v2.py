import csv
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(r"C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab")
TRAIN_CSV = Path(r"C:\Users\13398\Downloads\train_9800.csv")
TEST_CSV = Path(r"C:\Users\13398\Downloads\test_200.csv")
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)

OUT_CSV = OUT_DIR / "sichuan_address_terms_report_150_v2.csv"
OUT_SUMMARY = OUT_DIR / "sichuan_address_terms_report_150_v2_summary.csv"


CATEGORY_TERMS = {
    "kinship": [
        "妈老汉儿", "老汉儿", "老汉", "婆娘", "堂客", "婆姨", "两口子",
        "老婆", "老公", "婆婆", "公公", "嬢嬢", "孃孃", "娘娘",
        "爸爸", "妈妈", "爷爷", "奶奶", "哥哥", "姐姐", "妹妹", "弟弟",
        "大哥", "大姐", "嫂子", "阿姨", "儿子", "女儿", "媳妇", "爸", "妈",
    ],
    "solidarity": [
        "兄弟伙些", "兄弟伙", "哥老倌", "哥佬倌", "哥老官",
        "粉丝朋友", "朋友们", "朋友些", "兄弟", "朋友", "哥们", "姐们",
        "同学", "同事", "老乡", "伙计",
    ],
    "affectionate": [
        "幺妹儿", "幺娃儿", "幺儿", "幺女", "幺妹", "幺娃",
        "女娃儿", "女娃子", "男娃儿", "男娃子", "小娃儿", "小娃",
        "娃儿", "娃娃", "娃子", "妹儿", "妹子", "宝贝", "乖乖",
        "小朋友", "小妹妹", "小姐姐", "小哥哥", "小伙子", "姑娘", "丫头",
    ],
    "hierarchy": [
        "老师傅", "老板娘", "老板儿", "师傅", "师父", "老师", "老板",
        "厨师", "服务员", "医生", "护士", "客户", "客人", "顾客",
        "司机", "主播", "阿姨", "叔叔", "大叔", "大爷", "大妈",
        "嬢嬢", "孃孃", "娘娘", "婆婆", "公公",
    ],
    "insult": [
        "龟儿子", "狗日的", "哈麻批", "瓜娃子", "瓜娃儿", "狗东西",
        "贼娃子", "龟儿", "哈批", "傻子", "疯子", "神经病", "坏人", "瓜娃",
    ],
}


CATEGORY_CN = {
    "kinship": "亲属称谓",
    "solidarity": "亲近/同伴称呼",
    "affectionate": "亲昵称呼",
    "hierarchy": "社会身份/等级称谓",
    "insult": "冒犯/戏谑称谓",
}


def load_data():
    frames = []
    for name, path in [("train_9800", TRAIN_CSV), ("test_200", TEST_CSV)]:
        df = pd.read_csv(path).fillna("")
        df["input_file"] = name
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["text"] = df["text"].astype(str)
    return df


def matched_terms(text, terms):
    return [term for term in terms if term in text]


def score(text, primary, terms):
    length = len(text)
    length_score = 10 if 18 <= length <= 90 else 6 if 10 <= length <= 130 else 1
    variety_score = min(len(terms), 3) * 2
    dialect_score = 5 if primary in {
        "妈老汉儿", "老汉儿", "婆娘", "堂客", "兄弟伙", "兄弟伙些",
        "哥老倌", "幺儿", "幺妹儿", "女娃儿", "娃儿", "师傅",
        "老板儿", "龟儿子", "狗日的", "哈麻批", "瓜娃子",
    } else 0
    direct_address_score = 3 if any(mark in text for mark in ["你", "您", "来", "快", "喊", "问", "说"]) else 0
    return length_score + variety_score + dialect_score + direct_address_score


def main():
    df = load_data()
    selected = []
    used = set()

    for category, terms in CATEGORY_TERMS.items():
        pool = []
        for idx, row in df.iterrows():
            text = row["text"]
            hits = matched_terms(text, terms)
            if not hits:
                continue
            primary = hits[0]
            pool.append({
                "row_idx": idx,
                "category": category,
                "primary_term": primary,
                "all_terms": " ".join(hits),
                "score": score(text, primary, hits),
                "input_file": row["input_file"],
                "source_file": row["source_file"],
                "utt_or_id": row["utt_or_id"],
                "filename": row["filename"],
                "text": text,
                "matched_terms_original": row["matched_terms"],
                "text_length": len(text),
            })

        pool.sort(key=lambda r: (-r["score"], CATEGORY_TERMS[category].index(r["primary_term"]), r["text_length"]))
        per_term = Counter()
        taken = 0

        for row in pool:
            if row["row_idx"] in used:
                continue
            if per_term[row["primary_term"]] >= 5:
                continue
            selected.append(row)
            used.add(row["row_idx"])
            per_term[row["primary_term"]] += 1
            taken += 1
            if taken == 30:
                break

        if taken < 30:
            for row in pool:
                if row["row_idx"] in used:
                    continue
                selected.append(row)
                used.add(row["row_idx"])
                taken += 1
                if taken == 30:
                    break

    out_rows = []
    for i, row in enumerate(selected, start=1):
        out_rows.append({
            "ID": f"ADDR_{i:03d}",
            "四川话原句": row["text"],
            "称谓": row["primary_term"],
            "命中称谓": row["all_terms"],
            "称谓类型": row["category"],
            "称谓类型中文": CATEGORY_CN[row["category"]],
            "模型1输出": "",
            "模型2输出": "",
            "模型3输出": "",
            "称谓翻译结果": "",
            "错误类型": "",
            "分析备注": "",
            "input_file": row["input_file"],
            "utt_or_id": row["utt_or_id"],
            "filename": row["filename"],
            "source_file": row["source_file"],
            "matched_terms_original": row["matched_terms_original"],
            "text_length": row["text_length"],
        })

    out = pd.DataFrame(out_rows)
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)

    summary = []
    for cat in CATEGORY_TERMS:
        sub = out[out["称谓类型"] == cat]
        counts = Counter(sub["称谓"])
        summary.append({
            "称谓类型": cat,
            "称谓类型中文": CATEGORY_CN[cat],
            "条数": len(sub),
            "覆盖称谓数": len(counts),
            "高频称谓": " ".join(f"{k}:{v}" for k, v in counts.most_common(20)),
        })
    pd.DataFrame(summary).to_csv(OUT_SUMMARY, index=False, encoding="utf-8-sig")

    print(f"rows={len(out)}")
    print(out["称谓类型"].value_counts().reindex(CATEGORY_TERMS.keys()).fillna(0).astype(int).to_string())
    print(OUT_CSV)
    print(OUT_SUMMARY)


if __name__ == "__main__":
    main()
