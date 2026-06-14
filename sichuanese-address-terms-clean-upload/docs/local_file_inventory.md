# Local File Inventory

This file records the Sichuanese-related files found on the local machine before pushing this repository.

## Committed Files

### Raw and Processed Data

| Local source | Repository path | Notes |
| --- | --- | --- |
| `C:\Users\13398\Desktop\train_9800.csv` | `data/raw/train_9800.csv` | 9,800 raw candidate rows. |
| `C:\Users\13398\Desktop\WenetSpeech-Chuan文本预览_前100行.tsv` | `data/raw/WenetSpeech-Chuan_preview_first100.tsv` | First 100 WenetSpeech-Chuan text preview rows. |
| `C:\Users\13398\Downloads\train_9800_zh.csv` | `data/processed/train_9800_zh.csv` | 9,810 rows with Mandarin translations. |
| `C:\Users\13398\Downloads\train_9800_zh_pseudo_en.csv` | `data/processed/train_9800_zh_pseudo_en.csv` | 9,810 rows with pseudo-English translations. |

### 150 Address-Term Comparison Data

| Local source | Repository path |
| --- | --- |
| `C:\Users\13398\Downloads\address_terms_150_with_lora_mbart_outputs.csv` | `data/address_terms_150/address_terms_150_with_lora_mbart_outputs.csv` |
| `C:\Users\13398\Downloads\sc_address_terms150_human.xlsx` | `data/address_terms_150/sc_address_terms150_human.xlsx` |
| `C:\Users\13398\Desktop\mbart_150_error_analysis_user_summary_v2.xlsx` | `data/address_terms_150/mbart_150_error_analysis_user_summary_v2.xlsx` |
| `C:\Users\13398\Desktop\mbart_150_error_summary_by_user_labels_v2.csv` | `data/address_terms_150/mbart_150_error_summary_by_user_labels_v2.csv` |
| `C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab\outputs\sichuan_person_terms_report_150.csv` | `data/address_terms_150/sichuan_person_terms_report_150.csv` |
| `C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab\outputs\sichuan_person_terms_report_150_summary.csv` | `data/address_terms_150/sichuan_person_terms_report_150_summary.csv` |
| `C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab\outputs\sichuan_address_terms_report_150_v2.csv` | `data/address_terms_150/sichuan_address_terms_report_150_v2.csv` |
| `C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab\outputs\sichuan_address_terms_report_150_v2_summary.csv` | `data/address_terms_150/sichuan_address_terms_report_150_v2_summary.csv` |
| `C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab\outputs\address_terms_150_model_error_analysis_with_reasons.csv` | `data/address_terms_150/address_terms_150_model_error_analysis_with_reasons.csv` |
| `C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab\outputs\address_terms_150_error_summary.csv` | `data/address_terms_150/address_terms_150_error_summary.csv` |

### Lexicons

| Local source | Repository path |
| --- | --- |
| `C:\Users\13398\Desktop\四川人称称谓候选词典.txt` | `data/lexicons/sichuan_person_address_terms.txt` |
| `C:\Users\13398\Desktop\四川人称称谓候选词典_带次数.csv` | `data/lexicons/sichuan_person_address_terms_with_counts.csv` |
| `C:\Users\13398\Downloads\四川话人称称谓词典_研究候选_JSON版.json` | `data/lexicons/sichuan_person_address_terms_research_candidates.json` |

### mBART Scripts, Notebooks, and Results

| Local source | Repository path |
| --- | --- |
| `C:\Users\13398\Downloads\lora-mbart50.ipynb` | `notebooks/lora-mbart50.ipynb` |
| `C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab\lora_mbart50_new_gold_eval.ipynb` | `notebooks/lora_mbart50_new_gold_eval.ipynb` |
| `C:\Users\13398\Documents\Codex\2026-05-15\files-mentioned-by-the-user-2604mt\*.py` | `scripts/mbart/` |
| `C:\Users\13398\Documents\Codex\2026-05-05\https-huggingface-co-collections-aslp-lab\*.py` | `scripts/data_preparation/` and `scripts/analysis/` |
| `C:\Users\13398\Downloads\lora_mbart_sc_en_cases.csv` | `results/mbart/lora_mbart_sc_en_cases.csv` |
| `C:\Users\13398\Downloads\lora_mbart_sc_en_metrics.csv` | `results/mbart/lora_mbart_sc_en_metrics.csv` |
| `C:\Users\13398\Downloads\lora_mbart_sc_en_predictions.csv` | `results/mbart/lora_mbart_sc_en_predictions.csv` |

## Found But Not Committed

| Local file | Size | Reason |
| --- | ---: | --- |
| `C:\Users\13398\Desktop\WenetSpeech-Chuan-text-only.zip` | 265.6 MB | Over GitHub's normal single-file size limit. |
| `C:\Users\13398\Desktop\filtered_sichuan_person_terms.csv.gz` | 208.0 MB | Over GitHub's normal single-file size limit. |
| `C:\Users\13398\Desktop\filtered_sichuan_person_terms.xlsx` | 123.6 MB | Over GitHub's normal single-file size limit. |

