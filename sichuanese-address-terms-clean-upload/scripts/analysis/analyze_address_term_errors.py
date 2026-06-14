import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(r"C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab")
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)

HUMAN_XLSX = Path(r"C:\Users\13398\Downloads\sc_address_terms150_human.xlsx")
MODEL_CSV = Path(r"C:\Users\13398\Downloads\address_terms_150_with_lora_mbart_outputs.csv")

OUT_XLSX = OUT_DIR / "address_terms_150_model_error_analysis.xlsx"
OUT_CSV = OUT_DIR / "address_terms_150_model_error_analysis.csv"
OUT_SUMMARY = OUT_DIR / "address_terms_150_error_summary.csv"


def norm(text):
    text = "" if pd.isna(text) else str(text).lower()
    text = text.replace("’", "'")
    text = re.sub(r"[^a-z0-9'\s/-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_gold(gold):
    gold = "" if pd.isna(gold) else str(gold).strip()
    parts = re.split(r"[/;,]| or | and ", gold, flags=re.I)
    return [norm(p) for p in parts if norm(p) and norm(p) != "-"]


SYNONYMS = {
    "parents": ["parents", "parent", "mother and father", "mom and dad", "mum and dad", "father and mother"],
    "dad": ["dad", "father", "daddy", "papa", "old man"],
    "mom": ["mom", "mother", "mum", "mommy", "mama"],
    "wife": ["wife", "spouse"],
    "mother-in-law": ["mother in law", "mother-in-law"],
    "granny": ["granny", "grandma", "grandmother"],
    "dude": ["dude", "bro", "brother", "buddy", "man", "guy"],
    "bro": ["bro", "brother", "buddy", "dude", "man"],
    "guys": ["guys", "dudes", "friends", "folks", "everyone", "you guys"],
    "fans": ["fans", "fan"],
    "fan": ["fan", "fans"],
    "friends": ["friends", "friend"],
    "relationship": ["relationship", "girlfriend", "boyfriend", "dating", "friends"],
    "kids": ["kids", "children"],
    "children": ["children", "kids"],
    "children kids": ["children", "kids"],
    "children/ kids": ["children", "kids"],
    "kid": ["kid", "child"],
    "child": ["child", "kid"],
    "sweetie": ["sweetie", "baby", "dear", "darling", "honey"],
    "girl": ["girl", "young girl"],
    "young girl": ["young girl", "girl"],
    "girls": ["girls", "girl"],
    "boy": ["boy"],
    "teacher": ["teacher", "professor"],
    "mr": ["mr", "mister"],
    "boss": ["boss", "owner", "manager"],
    "driver": ["driver"],
    "auntie": ["auntie", "aunt"],
    "uncle": ["uncle"],
    "old man": ["old man", "elderly man", "senior"],
    "elderly": ["elderly", "senior", "old man"],
    "senior": ["senior", "elderly", "old man"],
    "master": ["master", "sifu", "teacher"],
    "sifu": ["sifu", "master"],
    "cook": ["cook", "chef"],
    "sir": ["sir"],
    "bastard": ["bastard", "son of a bitch", "son of bitch", "jerk", "asshole"],
    "moron": ["moron", "dumb", "idiot", "fool"],
    "dumb": ["dumb", "moron", "idiot", "fool", "silly"],
    "nuts": ["nuts", "crazy", "mad", "insane", "psycho"],
    "bad men": ["bad men", "bad man", "bad people", "bad person"],
    "sneaky": ["sneaky", "thief"],
    "thief": ["thief", "sneaky"],
}

LITERAL_PATTERNS = [
    "turtle", "turtle son", "little turtle", "cuckoo", "dog day", "god of dogs",
    "dog's day", "dog son", "thief's daughter", "old man's eggs",
]

PERSON_TERM_PATTERNS = [
    "grandmother", "grandma", "granny", "old lady", "old woman", "mother", "mom",
    "father", "dad", "aunt", "auntie", "uncle", "teacher", "master", "brother",
    "sister", "girl", "woman", "man", "friend", "friends", "boss", "owner",
    "driver", "cook", "chef", "kid", "child", "children", "boy", "fan", "fans",
]

TERM_HINTS = {
    "妈老汉儿": ["parents", "mother and father", "mom and dad", "father and mother"],
    "老汉儿": ["dad", "father", "old man"],
    "老汉": ["dad", "father", "old man"],
    "婆娘": ["wife", "woman", "girl", "bitch"],
    "堂客": ["wife", "home", "married woman"],
    "老婆": ["wife"],
    "婆婆": ["mother-in-law", "grandma", "granny", "grandmother"],
    "爸爸": ["dad", "father"],
    "妈妈": ["mom", "mother"],
    "兄弟伙": ["dude", "bro", "brother", "buddy", "guy"],
    "兄弟伙些": ["dudes", "guys", "brothers", "buddies"],
    "哥老倌": ["bro", "dude", "man"],
    "粉丝朋友": ["fans", "fan friend", "fans friends"],
    "朋友们": ["friends", "guys", "folks"],
    "兄弟": ["brother", "bro", "dude", "man"],
    "朋友": ["friend", "friends", "relationship"],
    "哥们": ["bro", "dude", "guy", "man"],
    "小朋友": ["kids", "children", "child"],
    "幺妹儿": ["yaomei", "girl", "young girl"],
    "女娃儿": ["girl", "young girl"],
    "幺儿": ["kid", "sweetie", "baby", "son"],
    "娃儿": ["child", "kid", "children"],
    "女娃子": ["girl", "young girl"],
    "小娃儿": ["kid", "child"],
    "老板儿": ["boss", "owner"],
    "老板": ["boss", "owner"],
    "老板娘": ["boss", "landlady", "owner"],
    "师傅": ["master", "sifu", "cook", "chef", "sir"],
    "老师傅": ["master", "sifu", "cook", "chef", "sir"],
    "老师": ["teacher"],
    "司机": ["driver"],
    "阿姨": ["auntie", "aunt"],
    "叔叔": ["uncle"],
    "大爷": ["old man", "elderly", "senior"],
    "龟儿子": ["bastard", "turtle"],
    "龟儿": ["bastard", "turtle"],
    "瓜娃子": ["moron", "dumb", "fool", "cuckoo"],
    "狗日的": ["bastard", "dog day", "son of a bitch"],
    "贼娃子": ["thief", "sneaky"],
    "傻子": ["moron", "dumb", "fool"],
    "疯子": ["nuts", "crazy"],
    "神经病": ["nuts", "crazy", "psycho"],
    "坏人": ["bad men", "bad people"],
    "狗东西": ["son of a bitch", "dog"],
}


def contains_any(pred_norm, phrases):
    for phrase in phrases:
        phrase_norm = norm(phrase)
        if not phrase_norm:
            continue
        if re.search(rf"\b{re.escape(phrase_norm)}\b", pred_norm):
            return phrase
        if phrase_norm in pred_norm:
            return phrase
    return ""


def gold_phrases(gold):
    phrases = []
    for part in split_gold(gold):
        phrases.append(part)
        phrases.extend(SYNONYMS.get(part, []))
    # Special handling for unnormalized raw labels.
    raw = norm(gold)
    if "children" in raw and "kids" in raw:
        phrases.extend(["children", "kids", "child", "kid"])
    if "dude" in raw or "bro" in raw or "guys" in raw:
        phrases.extend(["dude", "bro", "brother", "buddy", "guy", "guys", "dudes"])
    if "cook" in raw or "sir" in raw:
        phrases.extend(["cook", "chef", "sir"])
    if "master" in raw or "sifu" in raw:
        phrases.extend(["master", "sifu"])
    if "moron" in raw or "dumb" in raw:
        phrases.extend(["moron", "dumb", "idiot", "fool"])
    if "elderly" in raw or "senior" in raw:
        phrases.extend(["elderly", "senior", "old man"])
    return list(dict.fromkeys([p for p in phrases if p]))


def classify(row):
    term = str(row["称谓"])
    gold = str(row["en_gold_human"])
    pred = str(row["pred_english_lora_mbart"])
    pn = norm(pred)

    phrases = gold_phrases(gold)
    hit = contains_any(pn, phrases)
    if hit:
        return "Preserved", hit, "matches human target or accepted synonym"

    literal = contains_any(pn, LITERAL_PATTERNS)
    if literal:
        return "Literalized", literal, "literal/morpheme-based rendering rather than pragmatic meaning"

    term_hint = contains_any(pn, TERM_HINTS.get(term, []))
    if term_hint:
        # If it is not the human label but still a plausible address rendering, keep it as Other.
        return "Other", term_hint, "different plausible or shifted rendering; check manually"

    wrong_person_term = contains_any(pn, PERSON_TERM_PATTERNS)
    if wrong_person_term:
        return "Other", wrong_person_term, "wrong or shifted person/address rendering"

    return "Omitted", "", "no clear English rendering of the target address term"


def main():
    human = pd.read_excel(HUMAN_XLSX)
    model = pd.read_csv(MODEL_CSV)
    merged = human.merge(model[["ID", "pred_english_lora_mbart"]], on="ID", how="left")

    labels = []
    renderings = []
    notes = []
    for _, row in merged.iterrows():
        label, rendering, note = classify(row)
        labels.append(label)
        renderings.append(rendering)
        notes.append(note)

    merged["model_address_rendering"] = renderings
    merged["error_label"] = labels
    merged["auto_note"] = notes

    cols = [
        "ID", "四川话原句", "称谓", "en_gold_human", "pred_english_lora_mbart",
        "model_address_rendering", "error_label", "称谓类型", "称谓类型中文", "auto_note",
    ]
    analysis = merged[cols].copy()

    summary = (
        analysis.pivot_table(index="称谓类型", columns="error_label", values="ID", aggfunc="count", fill_value=0)
        .reindex(index=["kinship", "solidarity", "affectionate", "hierarchy", "insult"])
    )
    for col in ["Preserved", "Omitted", "Literalized", "Other"]:
        if col not in summary.columns:
            summary[col] = 0
    summary = summary[["Preserved", "Omitted", "Literalized", "Other"]]
    summary.loc["TOTAL"] = summary.sum(axis=0)

    term_summary_rows = []
    for (term_type, term), sub in analysis.groupby(["称谓类型", "称谓"], sort=False):
        labels_count = Counter(sub["error_label"])
        render_counts = Counter([x for x in sub["model_address_rendering"].fillna("").astype(str) if x.strip()])
        term_summary_rows.append({
            "称谓类型": term_type,
            "称谓": term,
            "人工目标译法": " | ".join(sorted(set(sub["en_gold_human"].astype(str)))),
            "条数": len(sub),
            "Preserved": labels_count.get("Preserved", 0),
            "Omitted": labels_count.get("Omitted", 0),
            "Literalized": labels_count.get("Literalized", 0),
            "Other": labels_count.get("Other", 0),
            "模型常见译法": "; ".join(f"{k}:{v}" for k, v in render_counts.most_common(8)) or "(no clear rendering)",
        })
    term_summary = pd.DataFrame(term_summary_rows)

    analysis.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    summary.to_csv(OUT_SUMMARY, encoding="utf-8-sig")

    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
        summary.reset_index().rename(columns={"称谓类型": "Type"}).to_excel(writer, sheet_name="summary_matrix", index=False)
        term_summary.to_excel(writer, sheet_name="term_summary", index=False)
        analysis.to_excel(writer, sheet_name="row_analysis", index=False)
        wb = writer.book
        for ws in wb.worksheets:
            ws.freeze_panes = "A2"
            for col in ws.columns:
                max_len = min(max(len(str(cell.value)) if cell.value is not None else 0 for cell in col), 70)
                ws.column_dimensions[col[0].column_letter].width = max(12, max_len + 2)

    print(OUT_XLSX)
    print(OUT_CSV)
    print(OUT_SUMMARY)
    print(summary)
    print(term_summary.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
