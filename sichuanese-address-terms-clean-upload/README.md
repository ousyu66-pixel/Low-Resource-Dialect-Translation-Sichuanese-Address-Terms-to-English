# Low-Resource Dialect Translation: Sichuanese Address Terms to English

This repository collects the data, lexicons, analysis files, and LoRA-mBART scripts used for a low-resource Sichuanese to English translation project focused on personal pronouns and address terms.

本仓库整理了四川话/川渝口语人称代词、称谓词相关的数据、词表、150 条称谓样本分析，以及 LoRA-mBART 微调和评估代码。

## Repository Layout

| Path | Contents |
| --- | --- |
| `data/raw/` | Raw 9,800-row Sichuanese candidate dataset and WenetSpeech-Chuan preview sample. |
| `data/processed/` | Mandarin and pseudo-English augmented versions of the 9,800-row dataset. |
| `data/address_terms_150/` | 150 address-term comparison samples, human annotation workbook, LoRA-mBART outputs, and error summaries. |
| `data/lexicons/` | Sichuanese personal pronoun and address-term lexicons in TXT, CSV, and JSON formats. |
| `scripts/data_preparation/` | Scripts for extracting WenetSpeech-Chuan text, building lexicons, and selecting report samples. |
| `scripts/analysis/` | Scripts for address-term error analysis and workbook updates. |
| `scripts/mbart/` | Kaggle/Colab-oriented LoRA-mBART training and pivot-translation scripts. |
| `notebooks/` | mBART/LoRA notebooks used during experiments. |
| `results/mbart/` | LoRA-mBART prediction, metric, and case files. |
| `docs/local_file_inventory.md` | Local source inventory and files intentionally omitted from git. |

## Key Data Files

| File | Rows | Notes |
| --- | ---: | --- |
| `data/raw/train_9800.csv` | 9,800 | Raw Sichuanese candidate rows with matched personal/address terms. |
| `data/processed/train_9800_zh.csv` | 9,810 | Sichuanese rows with Mandarin translations. |
| `data/processed/train_9800_zh_pseudo_en.csv` | 9,810 | Sichuanese, Mandarin, and pseudo-English data for pivot experiments. |
| `data/address_terms_150/address_terms_150_with_lora_mbart_outputs.csv` | 150 | 150 address-term samples with LoRA-mBART English predictions. |
| `data/address_terms_150/sichuan_address_terms_report_150_v2.csv` | 150 | Address-term report sample set. |
| `data/address_terms_150/sichuan_person_terms_report_150.csv` | 150 | Personal/address-term report sample set. |
| `data/lexicons/sichuan_person_address_terms_with_counts.csv` | 181 | Candidate lexicon with train/eval occurrence counts. |
| `data/lexicons/sichuan_person_address_terms_research_candidates.json` | 419 entries | Expanded research candidate lexicon. |

## Large Local Files Not Committed

The following local files were found but are not included because they exceed GitHub's normal 100 MB single-file limit or are source archives better stored with Git LFS or release assets:

| Local file | Size | Reason |
| --- | ---: | --- |
| `C:\Users\13398\Desktop\WenetSpeech-Chuan-text-only.zip` | 265.6 MB | Source archive over GitHub single-file limit. |
| `C:\Users\13398\Desktop\filtered_sichuan_person_terms.csv.gz` | 208.0 MB | Large generated corpus extract. |
| `C:\Users\13398\Desktop\filtered_sichuan_person_terms.xlsx` | 123.6 MB | Large workbook over GitHub single-file limit. |

If these files need to be versioned later, use Git LFS or upload them as GitHub release assets.

## Environment

The mBART scripts were written for Kaggle/Colab-style GPU notebooks. Core Python dependencies include:

- `transformers`
- `datasets`
- `accelerate`
- `peft`
- `sacrebleu`
- `sentencepiece`
- `protobuf`
- `torch`
- `pandas`
- `numpy`

