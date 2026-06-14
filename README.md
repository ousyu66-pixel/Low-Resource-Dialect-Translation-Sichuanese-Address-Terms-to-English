# Low-Resource Dialect Translation: Sichuanese Address Terms to English

This repository contains datasets, scripts, notebooks, and evaluation results for a research project on **Sichuanese-to-English machine translation in a low-resource setting**, with a particular focus on the translation of **personal reference and address terms**.

The project investigates how multilingual machine translation systems handle culturally and pragmatically rich Sichuanese expressions, especially address terms that convey kinship, solidarity, affection, hierarchy, and insult.

---

## Project Overview

Machine Translation (MT) systems have achieved strong performance across many language pairs, but dialect translation remains challenging due to limited parallel corpora, non-standard orthography, and culturally specific expressions.

This project focuses on:

* Sichuanese-to-English machine translation
* Low-resource dialect translation
* Translation of personal reference and address terms
* Pragmatic meaning preservation
* Automatic and human evaluation of MT outputs

The study combines automatic evaluation metrics with qualitative error analysis to examine whether machine translation systems preserve the social and interpersonal meanings encoded in Sichuanese address terms.

---

## Dataset

The dataset was derived from the **WenetSpeech-Chuan+** corpus and further processed for address-term-focused machine translation research.

### Raw Data

| File                                              | Description                             |
| ------------------------------------------------- | --------------------------------------- |
| `data/raw/train_9800.csv`                         | Main Sichuanese dataset (9,800 samples) |
| `data/raw/WenetSpeech-Chuan_preview_first100.tsv` | Preview subset from WenetSpeech-Chuan+  |

### Processed Data

| File                                         | Description                                                     |
| -------------------------------------------- | --------------------------------------------------------------- |
| `data/processed/train_9800_zh.csv`           | Sichuanese–Mandarin dataset                                     |
| `data/processed/train_9800_zh_pseudo_en.csv` | Sichuanese–Mandarin–pseudo-English dataset used for MT training |
| `data/processed/test_200.csv                 |test csv
| `data/processed/golden_manually_200_en.csv   |used for personal address analysis

### Address-Term Evaluation Data

| File                                                                             | Description                                       |
| -------------------------------------------------------------------------------- | ------------------------------------------------- |
| `data/address_terms_150/address_terms_150_with_lora_mbart_outputs.csv`           | 150 address-term examples with LoRA-mBART outputs |
| `data/address_terms_150/sc_address_terms150_human.xlsx`                          | Human evaluation workbook                         |
| `data/address_terms_150/sichuan_address_terms_report_150_v2.csv`                 | Address-term evaluation dataset                   |
| `data/address_terms_150/sichuan_person_terms_report_150.csv`                     | Personal reference term evaluation dataset        |
| `data/address_terms_150/address_terms_150_error_summary.csv`                     | Error summary statistics                          |
| `data/address_terms_150/address_terms_150_model_error_analysis_with_reasons.csv` | Detailed error analysis                           |
| `data/address_terms_150/mbart_150_error_summary_by_user_labels_v2.csv`           | Human-labelled error summary                      |
| `data/address_terms_150/sichuan_address_terms_report_150_v2_summary.csv`         | Summary statistics                                |
| `data/address_terms_150/sichuan_person_terms_report_150_summary.csv`             | Summary statistics                                |

### Lexicons

| File                                                                  | Description                         |
| --------------------------------------------------------------------- | ----------------------------------- |
| `data/lexicons/sichuan_person_address_terms.txt`                      | Sichuanese address-term lexicon     |
| `data/lexicons/sichuan_person_address_terms_with_counts.csv`          | Address terms with frequency counts |
| `data/lexicons/sichuan_person_address_terms_research_candidates.json` | Candidate address-term inventory    |

---

## Models

The full project evaluates multilingual machine translation systems under both baseline and fine-tuned settings.

### mBART-50

Model:

```text
facebook/mbart-large-50-many-to-many-mmt
```

Experiments included:

* Baseline mBART-50
* LoRA Fine-Tuned mBART-50

Resources currently included in this repository:

* Training notebooks
* Fine-tuning scripts
* Evaluation scripts
* Prediction outputs
* Metric files
* Human error analysis

### NLLB-200

Model:

```text
facebook/nllb-200-distilled-600M
```

Experiments discussed in the accompanying report include:

* Baseline NLLB-200
* LoRA Fine-Tuned NLLB-200

Associated scripts and outputs are maintained as part of the complete project workflow.

---

## Evaluation

### Automatic Metrics

Translation quality is evaluated using:

* BLEU
* chrF

### Human Error Analysis

A manually curated subset of 150 Sichuanese utterances containing address terms was evaluated through qualitative error analysis.

Error categories include:

* Preserved
* Omitted
* Literalized
* Other

The analysis focuses on whether social and pragmatic meanings are preserved rather than solely on sentence-level similarity.

---

## Repository Structure

```text
.
├── data
│   ├── address_terms_150
│   ├── lexicons
│   ├── processed
│   └── raw
│
├── docs
│   └── local_file_inventory.md
│
├── notebooks
│   ├── lora-mbart50.ipynb
│   └── lora_mbart50_new_gold_eval.ipynb
│
├── results
│   └── mbart
│       ├── lora_mbart_sc_en_cases.csv
│       ├── lora_mbart_sc_en_metrics.csv
│       └── lora_mbart_sc_en_predictions.csv
│
├── scripts
│   ├── analysis
│   ├── data_preparation
│   └── mbart
│
├── requirements.txt
└── README.md
```

---

## Results

The repository includes LoRA-mBART prediction outputs and evaluation files:

* `results/mbart/lora_mbart_sc_en_predictions.csv`
* `results/mbart/lora_mbart_sc_en_metrics.csv`
* `results/mbart/lora_mbart_sc_en_cases.csv`

Additional analyses are available in the address-term evaluation datasets and summary reports.

---

## Requirements

Recommended environment:

* Python 3.10+
* PyTorch
* Transformers
* PEFT
* Datasets
* Pandas
* NumPy
* SacreBLEU

Install dependencies:

```bash
pip install -r requirements.txt
```

---

This project uses data derived from the WenetSpeech-Chuan+ corpus and was completed as part of a research project on low-resource dialect machine translation.
