import argparse
import csv
import gzip
import io
import json
import sys
import time
import zipfile
from pathlib import Path

import requests


BASE = "https://huggingface.co/datasets/ASLP-lab"

TRAIN_URL = f"{BASE}/WSC-Train/resolve/main/wsc_metadata.jsonl"

EVAL_FILES = [
    ("WSC-Eval-ASR/Easy/text", "eval_asr_easy_text.txt.gz"),
    ("WSC-Eval-ASR/Easy/wav.scp", "eval_asr_easy_wav.scp.gz"),
    ("WSC-Eval-ASR/Hard/text", "eval_asr_hard_text.txt.gz"),
    ("WSC-Eval-ASR/Hard/wav.scp", "eval_asr_hard_wav.scp.gz"),
    ("WSC-Eval-ASR/Short/text", "eval_asr_short_text.txt.gz"),
    ("WSC-Eval-ASR/Short/wav.scp", "eval_asr_short_wav.scp.gz"),
    ("WSC-Eval-ASR/Long/text", "eval_asr_long_text.txt.gz"),
    ("WSC-Eval-ASR/Long/wav.scp", "eval_asr_long_wav.scp.gz"),
    ("WSC-Eval-TTS/test_easy.txt", "eval_tts_test_easy.txt.gz"),
    ("WSC-Eval-TTS/test_hard.txt", "eval_tts_test_hard.txt.gz"),
]


def log(message):
    print(message, flush=True)


def request_stream(url):
    response = requests.get(url, stream=True, timeout=(30, 120))
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response


def download_train_text(work_dir):
    target = work_dir / "wsc_train_audio_text.tsv.gz"
    log("Downloading WSC-Train metadata and extracting audio/text columns...")
    response = request_stream(TRAIN_URL)
    if response is None:
        raise RuntimeError("WSC-Train metadata file was not found")

    rows = 0
    started = time.time()
    bytes_in = 0
    with gzip.open(target, "wt", encoding="utf-8", newline="") as gz:
        writer = csv.writer(gz, delimiter="\t", lineterminator="\n")
        writer.writerow(["utt", "filename", "text"])
        for raw_line in response.iter_lines(chunk_size=1024 * 1024, decode_unicode=False):
            if not raw_line:
                continue
            bytes_in += len(raw_line)
            try:
                item = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            utt = item.get("utt") or item.get("utt_id") or item.get("audio_id") or ""
            filename = item.get("filename") or item.get("wav_utt_id") or item.get("source_audio_path") or ""
            text = item.get("text") or item.get("rover_result") or ""
            writer.writerow([utt, filename, text])
            rows += 1
            if rows % 200000 == 0:
                elapsed = max(time.time() - started, 1)
                mb = bytes_in / 1024 / 1024
                log(f"  train rows: {rows:,}, downloaded: {mb:.1f} MiB, speed: {mb / elapsed:.1f} MiB/s")

    log(f"Finished WSC-Train text rows: {rows:,}")
    return target


def download_text_file(path, output_name, work_dir):
    url = f"{BASE}/WSC-Eval/resolve/main/{path}"
    target = work_dir / output_name
    response = request_stream(url)
    if response is None:
        log(f"Skipping missing file: {path}")
        return None

    log(f"Downloading {path}...")
    with gzip.open(target, "wb") as gz:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                gz.write(chunk)
    return target


def add_readme(work_dir):
    readme = work_dir / "README.txt"
    readme.write_text(
        "\n".join(
            [
                "WenetSpeech-Chuan text-only export",
                "",
                "Files:",
                "- wsc_train_audio_text.tsv.gz: WSC-Train columns: utt, filename, text.",
                "- eval_asr_*_text.txt.gz: WSC-Eval ASR text files, format: audio_id text.",
                "- eval_asr_*_wav.scp.gz: WSC-Eval ASR audio path maps, format: audio_id path.",
                "- eval_tts_*.txt.gz: WSC-Eval TTS text files from the dataset repository.",
                "",
                "All .gz files are line-oriented and can be streamed without loading the whole file into memory.",
                "Source: https://huggingface.co/collections/ASLP-lab/wenetspeech-chuan",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return readme


def create_zip(files, zip_path):
    log(f"Creating ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for file_path in files:
            archive.write(file_path, arcname=file_path.name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--desktop", required=True)
    parser.add_argument("--skip-train", action="store_true")
    args = parser.parse_args()

    desktop = Path(args.desktop).expanduser().resolve()
    work_dir = desktop / "WenetSpeech-Chuan-text-only-work"
    zip_path = desktop / "WenetSpeech-Chuan-text-only.zip"
    work_dir.mkdir(parents=True, exist_ok=True)

    files = []
    if not args.skip_train:
        files.append(download_train_text(work_dir))

    for path, output_name in EVAL_FILES:
        downloaded = download_text_file(path, output_name, work_dir)
        if downloaded is not None:
            files.append(downloaded)

    files.append(add_readme(work_dir))
    create_zip(files, zip_path)
    size_mb = zip_path.stat().st_size / 1024 / 1024
    log(f"Done: {zip_path} ({size_mb:.1f} MiB)")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log(f"ERROR: {exc}")
        sys.exit(1)
