from pathlib import Path

import pandas as pd


ROOT = Path(r"C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab")
INPUT_XLSX = ROOT / "outputs" / "address_terms_150_model_error_analysis.xlsx"
OUT_XLSX = ROOT / "outputs" / "address_terms_150_model_error_analysis_with_reasons.xlsx"
OUT_CSV = ROOT / "outputs" / "address_terms_150_model_error_analysis_with_reasons.csv"


def clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def reason(row):
    label = clean(row["error_label"])
    term = clean(row["称谓"])
    gold = clean(row["en_gold_human"])
    pred = clean(row["pred_english_lora_mbart"])
    rendering = clean(row["model_address_rendering"])
    term_type = clean(row["称谓类型"])

    if label == "Preserved":
        if rendering:
            return (
                f"模型译文中出现了“{rendering}”，与人工标注“{gold}”相同或属于可接受近义译法；"
                f"因此判断为保留了“{term}”的主要称谓/语用功能。"
            )
        return (
            f"模型译文虽然没有逐字对应“{term}”，但整体上保留了人工标注“{gold}”所表示的称谓意义。"
        )

    if label == "Omitted":
        return (
            f"人工标注认为“{term}”应体现为“{gold}”，但模型译文中没有明显对应的人称称谓或近义表达；"
            "因此判断为称谓被省略。"
        )

    if label == "Literalized":
        if rendering:
            return (
                f"模型把“{term}”翻成了“{rendering}”，更像按词面或构词成分直译；"
                f"但人工标注期望的是“{gold}”这类语用意义，因此判断为字面化翻译。"
            )
        return (
            f"模型译法偏向字面直译，没有表达人工标注“{gold}”对应的称谓语用意义。"
        )

    if label == "Other":
        if rendering:
            return (
                f"模型译文中出现了“{rendering}”，说明它没有完全省略称谓；"
                f"但该表达与人工标注“{gold}”不一致，属于称谓类别、人物关系、性别/身份或情感色彩发生偏移。"
            )
        return (
            f"模型输出与人工标注“{gold}”不匹配，但错误不属于明确省略或字面化；"
            "因此暂归为其他类型，建议人工复核。"
        )

    return "未识别的标签，建议人工复核。"


def main():
    summary = pd.read_excel(INPUT_XLSX, sheet_name="summary_matrix")
    term_summary = pd.read_excel(INPUT_XLSX, sheet_name="term_summary")
    rows = pd.read_excel(INPUT_XLSX, sheet_name="row_analysis")

    rows["标注理由"] = rows.apply(reason, axis=1)
    rows["人工复核"] = ""

    rows.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="summary_matrix", index=False)
        term_summary.to_excel(writer, sheet_name="term_summary", index=False)
        rows.to_excel(writer, sheet_name="row_analysis", index=False)
        wb = writer.book
        for ws in wb.worksheets:
            ws.freeze_panes = "A2"
            for col in ws.columns:
                max_len = min(max(len(str(cell.value)) if cell.value is not None else 0 for cell in col), 90)
                ws.column_dimensions[col[0].column_letter].width = max(12, max_len + 2)

    print(OUT_XLSX)
    print(OUT_CSV)
    print(rows[["ID", "称谓", "en_gold_human", "model_address_rendering", "error_label", "标注理由"]].head(12).to_string(index=False))


if __name__ == "__main__":
    main()
