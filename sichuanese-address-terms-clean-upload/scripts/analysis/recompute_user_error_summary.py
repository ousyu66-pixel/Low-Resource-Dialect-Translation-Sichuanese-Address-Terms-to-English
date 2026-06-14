from pathlib import Path

import pandas as pd


DESKTOP = Path(r"C:\Users\13398\Desktop")
INPUT_XLSX = DESKTOP / "mbart_150_error_analysis_with_reasons.xlsx"
OUT_XLSX = DESKTOP / "mbart_150_error_analysis_user_summary_v2.xlsx"
OUT_CSV = DESKTOP / "mbart_150_error_summary_by_user_labels_v2.csv"

LABELS = ["Preserved", "Omitted", "Literalized", "Other"]
TYPE_ORDER = ["kinship", "solidarity", "affectionate", "hierarchy", "insult"]


def normalize_label(value):
    text = "" if pd.isna(value) else str(value).strip()
    lower = text.lower()
    mapping = {
        "preserved": "Preserved",
        "preserve": "Preserved",
        "保留": "Preserved",
        "omitted": "Omitted",
        "omit": "Omitted",
        "省略": "Omitted",
        "literalized": "Literalized",
        "literalised": "Literalized",
        "literal": "Literalized",
        "字面化": "Literalized",
        "直译": "Literalized",
        "other": "Other",
        "其他": "Other",
        "mistranslated": "Other",
        "wrong": "Other",
    }
    return mapping.get(lower, text)


def main():
    xls = pd.ExcelFile(INPUT_XLSX)
    rows = pd.read_excel(INPUT_XLSX, sheet_name="row_analysis")

    if "人工复核" in rows.columns and rows["人工复核"].notna().any():
        label_col = "人工复核"
    elif "user_label" in rows.columns and rows["user_label"].notna().any():
        label_col = "user_label"
    else:
        label_col = "error_label"

    rows["final_error_label"] = rows[label_col].apply(normalize_label)

    invalid = sorted(set(rows["final_error_label"].dropna()) - set(LABELS))
    if invalid:
        print("WARNING invalid labels:", invalid)

    summary = (
        rows.pivot_table(index="称谓类型", columns="final_error_label", values="ID", aggfunc="count", fill_value=0)
        .reindex(TYPE_ORDER)
        .fillna(0)
        .astype(int)
    )
    for label in LABELS:
        if label not in summary.columns:
            summary[label] = 0
    summary = summary[LABELS]
    summary.loc["TOTAL"] = summary.sum(axis=0)

    term_summary = (
        rows.pivot_table(index=["称谓类型", "称谓"], columns="final_error_label", values="ID", aggfunc="count", fill_value=0)
        .reset_index()
    )
    for label in LABELS:
        if label not in term_summary.columns:
            term_summary[label] = 0
    term_summary["条数"] = term_summary[LABELS].sum(axis=1)
    term_summary = term_summary[["称谓类型", "称谓", "条数"] + LABELS]

    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
        summary.reset_index().rename(columns={"称谓类型": "Type"}).to_excel(writer, sheet_name="summary_matrix", index=False)
        term_summary.to_excel(writer, sheet_name="term_summary", index=False)
        rows.to_excel(writer, sheet_name="row_analysis", index=False)
        wb = writer.book
        for ws in wb.worksheets:
            ws.freeze_panes = "A2"
            for col in ws.columns:
                max_len = min(max(len(str(cell.value)) if cell.value is not None else 0 for cell in col), 80)
                ws.column_dimensions[col[0].column_letter].width = max(12, max_len + 2)

    summary.to_csv(OUT_CSV, encoding="utf-8-sig")
    print("label_col:", label_col)
    print(OUT_XLSX)
    print(OUT_CSV)
    print(summary)


if __name__ == "__main__":
    main()
