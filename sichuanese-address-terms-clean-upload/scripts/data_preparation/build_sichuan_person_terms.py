import csv
import gzip
import io
import os
import re
import zipfile
from collections import OrderedDict
from pathlib import Path


def add(terms, term, category, note=""):
    if term not in terms:
        terms[term] = {"term": term, "category": category, "note": note}


def build_terms():
    terms = OrderedDict()

    for term in ["我", "我们", "咱", "咱们", "俺", "俺们", "本人", "自己", "自个儿", "各人", "个人"]:
        add(terms, term, "pronoun_first_reflexive", "一/反身人称；各人/个人在川渝口语中可能表示自己")
    for term in ["你", "你们", "您", "您们"]:
        add(terms, term, "pronoun_second", "二人称")
    for term in ["他", "她", "它", "他们", "她们", "它们", "人家", "别人", "大家"]:
        add(terms, term, "pronoun_third_indefinite", "三人称/泛指；人家有歧义")

    dialect_terms = [
        "老子", "老娘", "老汉", "老汉儿", "堂客", "婆娘", "婆姨",
        "幺儿", "幺女", "幺妹", "幺妹儿", "幺娃", "幺娃儿",
        "娃儿", "娃娃", "女娃", "女娃儿", "男娃", "男娃儿", "小娃", "小娃儿", "细娃儿",
        "妹儿", "妹子", "弟娃儿", "哥老倌", "哥佬倌", "哥老官", "姐老倌",
        "娘娘", "嬢嬢", "孃孃", "婆婆", "公公",
        "龟儿", "龟儿子", "瓜娃子", "瓜娃儿", "哈儿",
    ]
    for term in dialect_terms:
        add(terms, term, "sichuan_dialect_address", "川渝口语/方言称谓候选，部分词有贬义或语境歧义")

    kinship_terms = [
        "爸爸", "爸", "妈妈", "妈", "爹", "爹爹", "娘", "爷爷", "奶奶", "外公", "外婆",
        "祖祖", "伯伯", "伯父", "伯母", "叔叔", "叔", "婶婶", "婶儿", "婶子",
        "姑姑", "姑妈", "姨妈", "姨", "阿姨", "舅舅", "舅妈",
        "哥哥", "哥", "姐姐", "姐", "弟弟", "弟", "妹妹", "妹",
        "大哥", "大姐", "小哥", "小哥哥", "小姐", "小姐姐", "小妹", "老妹",
        "嫂子", "嫂嫂", "姐夫", "妹夫", "媳妇", "媳妇儿", "女婿",
        "老婆", "老公", "丈夫", "妻子", "爱人", "对象", "男朋友", "女朋友",
        "儿子", "女儿", "孙子", "孙女",
        "亲戚", "家人", "亲人", "父母", "兄弟", "弟兄", "姐妹", "兄妹", "母子", "父子", "母女", "父女",
    ]
    for term in kinship_terms:
        add(terms, term, "kinship_address", "亲属/拟亲属称谓，短词可能有同形歧义")

    social_terms = [
        "老师", "师傅", "师父", "老板", "老板娘", "医生", "护士", "同学", "同事", "朋友",
        "兄弟伙", "兄弟伙些", "伙计", "客人", "顾客", "游客", "司机", "主播", "粉丝",
        "观众", "网友", "邻居", "服务员", "店员", "厨师", "嬢嬢些",
        "帅哥", "美女", "大叔", "叔叔阿姨", "大爷", "大妈", "老太婆", "老太太",
        "老头", "老头儿", "老爷子", "老婆婆", "老伯", "小伙", "小伙子", "姑娘", "丫头", "宝贝",
    ]
    for term in social_terms:
        add(terms, term, "social_address", "社会身份/泛称，适合宽召回后人工筛")

    return terms


def iter_texts(zip_path):
    eval_names = [
        "eval_asr_easy_text.txt.gz",
        "eval_asr_hard_text.txt.gz",
        "eval_asr_short_text.txt.gz",
        "eval_asr_long_text.txt.gz",
        "eval_tts_test_easy.txt.gz",
        "eval_tts_test_hard.txt.gz",
    ]
    with zipfile.ZipFile(zip_path) as z:
        with z.open("wsc_train_audio_text.tsv.gz") as raw:
            with gzip.GzipFile(fileobj=raw) as gz:
                f = io.TextIOWrapper(gz, encoding="utf-8")
                header = next(f, None)
                for line in f:
                    parts = line.rstrip("\n").split("\t", 2)
                    if len(parts) == 3:
                        yield "train", parts[2]
        for name in eval_names:
            with z.open(name) as raw:
                with gzip.GzipFile(fileobj=raw) as gz:
                    f = io.TextIOWrapper(gz, encoding="utf-8")
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split(maxsplit=1)
                        yield "eval", parts[1] if len(parts) > 1 else parts[0]


def main():
    desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
    zip_path = desktop / "WenetSpeech-Chuan-text-only.zip"
    out_csv = desktop / "四川人称称谓候选词典_带次数.csv"
    out_txt = desktop / "四川人称称谓候选词典.txt"

    terms = build_terms()
    counts = {term: {"train": 0, "eval": 0} for term in terms}

    # Count longer terms first is not required for independent substring counts.
    compiled = [(term, re.compile(re.escape(term))) for term in terms]
    for idx, (split, text) in enumerate(iter_texts(zip_path), start=1):
        for term, pattern in compiled:
            n = len(pattern.findall(text))
            if n:
                counts[term][split] += n
        if idx % 500000 == 0:
            print(f"processed {idx:,} lines", flush=True)

    with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "category", "train_count", "eval_count", "total_count", "note"])
        for term, meta in terms.items():
            train = counts[term]["train"]
            eval_count = counts[term]["eval"]
            writer.writerow([term, meta["category"], train, eval_count, train + eval_count, meta["note"]])

    with out_txt.open("w", encoding="utf-8") as f:
        for term in terms:
            f.write(term + "\n")

    print(out_csv)
    print(out_txt)


if __name__ == "__main__":
    main()
