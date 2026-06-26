#!/usr/bin/env python3
"""Build static demo audio, spectrograms, and manifest for GitHub Pages."""

from __future__ import annotations

import csv
import json
import re
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft


REPO = Path(__file__).resolve().parents[1]
FASTENHANCER = Path("/home/cmw/Crm/fastenhancer")
DNS_ROOT = Path("/home/cmw/Crm/data/dns2020_raw/datasets/test_set/synthetic/no_reverb")
TABLE2_WAVS = FASTENHANCER / "eval_outputs/table2_demo_wavs"

SELECTED = [
    {"id": "fileid_5", "noise": "Breath", "label": "Breathing noise"},
    {"id": "fileid_161", "noise": "Babble", "label": "Babble speech noise"},
    {"id": "fileid_192", "noise": "Vacuum cleaner", "label": "Vacuum motor noise"},
]

TRACK_LABELS = {
    "noisy": "Noisy",
    "adapenhancer_b": "AdapEnhancer-B",
    "clean": "Clean",
    "fastenhancer_b_original": "FastEnhancer-B",
    "fastenhancer_b_adams": "FastEnhancer-B AdaMS",
    "bsrnn_original": "BSRNN",
    "bsrnn_adams": "BSRNN AdaMS",
    "fspen_original": "FSPEN",
    "fspen_adams": "FSPEN AdaMS",
    "lisennet_original": "LiSenNet",
    "lisennet_adams": "LiSenNet AdaMS",
}

REFERENCE_KEYS = ["noisy", "adapenhancer_b", "clean"]
PAIR_GROUPS = [
    ("bsrnn", "BSRNN", "bsrnn_original", "bsrnn_adams"),
    ("fspen", "FSPEN", "fspen_original", "fspen_adams"),
    ("lisennet", "LiSenNet", "lisennet_original", "lisennet_adams"),
    (
        "fastenhancer_b_adams",
        "FastEnhancer-B",
        "fastenhancer_b_original",
        "fastenhancer_b_adams",
    ),
]


def read_csv_by_fileid(
    path: Path,
    model: str | None = None,
    testset: str | None = None,
) -> dict[str, dict[str, str]]:
    rows = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            if model is not None and row.get("model") != model:
                continue
            if testset is not None and row.get("testset") != testset:
                continue
            filename = (
                row.get("file_id")
                or row.get("filename")
                or row.get("Filename")
                or row.get("Clean_Filename")
                or ""
            )
            match = re.search(r"fileid_(\d+)", filename)
            if not match:
                continue
            rows[f"fileid_{match.group(1)}"] = row
    return rows


def parse_noisy_rows() -> dict[str, dict[str, object]]:
    rows = {}
    with (FASTENHANCER / "noisynoreverbevaluation_results.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            match = re.search(r"fileid_(\d+)", row["Clean_Filename"])
            if not match:
                continue
            fid = f"fileid_{match.group(1)}"
            source_match = re.search(r"Matched: ([^)]+)", row["Status"])
            source = source_match.group(1) if source_match else ""
            snr_match = re.search(r"_snr(-?\d+)_", source)
            rows[fid] = {
                "source": source,
                "snr": int(snr_match.group(1)) if snr_match else None,
                "pesq": float(row["PESQ"]),
                "stoi": float(row["STOI(%)"]) / 100,
                "sig": float(row["DNSMOS_SIG"]),
                "bak": float(row["DNSMOS_BAK"]),
                "ovl": float(row["DNSMOS_OVL"]),
            }
    return rows


def wav_to_float(path: Path) -> tuple[int, np.ndarray]:
    sr, wav = wavfile.read(path)
    if wav.ndim > 1:
        wav = wav.mean(axis=1)
    if np.issubdtype(wav.dtype, np.integer):
        scale = np.iinfo(wav.dtype).max
        wav = wav.astype(np.float32) / max(scale, 1)
    else:
        wav = wav.astype(np.float32)
    return sr, np.nan_to_num(wav)


def spectrogram_db(path: Path) -> tuple[int, np.ndarray, np.ndarray, np.ndarray]:
    sr, wav = wav_to_float(path)
    freqs, times, spec = stft(
        wav,
        fs=sr,
        window="hann",
        nperseg=512,
        noverlap=384,
        boundary=None,
    )
    db = 20 * np.log10(np.maximum(np.abs(spec), 1e-7))
    vmax = np.percentile(db, 99)
    db = np.clip(db, vmax - 85, vmax)
    return sr, times, freqs, db


def focus_box(origin_path: Path, adams_path: Path, clean_path: Path) -> dict[str, float]:
    sr, times, freqs, origin_db = spectrogram_db(origin_path)
    _, _, _, adams_db = spectrogram_db(adams_path)
    _, _, _, clean_db = spectrogram_db(clean_path)
    rows = min(origin_db.shape[0], adams_db.shape[0], clean_db.shape[0])
    cols = min(origin_db.shape[1], adams_db.shape[1], clean_db.shape[1])
    origin_db = origin_db[:rows, :cols]
    adams_db = adams_db[:rows, :cols]
    clean_db = clean_db[:rows, :cols]
    freqs = freqs[:rows]
    times = times[:cols]

    origin_error = np.abs(origin_db - clean_db)
    adams_error = np.abs(adams_db - clean_db)
    improvement = np.maximum(origin_error - adams_error, 0)

    band = (freqs >= 900) & (freqs <= min(sr / 2, 7600))
    if not np.any(band):
        band = np.ones_like(freqs, dtype=bool)
    # Prefer regions where AdaMS is closer to the clean spectrogram, while
    # avoiding silent margins that can otherwise dominate simple differences.
    clean_band = clean_db[band]
    activity_floor = np.percentile(clean_band, 45)
    activity = clean_band > activity_floor
    weighted = improvement[band] * (0.55 + 0.45 * activity.astype(np.float32))
    energy_t = weighted.mean(axis=0)
    frame_step = max(times[1] - times[0], 1e-3) if len(times) > 1 else 1e-3
    if cols > 8:
        margin = max(4, int(round(0.25 / frame_step))) if len(times) > 1 else 4
        energy_t[:margin] = 0
        energy_t[-margin:] = 0

    win_t = max(10, min(cols, int(round(1.05 / frame_step))))
    kernel = np.ones(win_t) / win_t
    smooth_t = np.convolve(energy_t, kernel, mode="same")
    center_t = int(np.argmax(smooth_t))
    t0 = max(0, center_t - win_t // 2)
    t1 = min(cols - 1, t0 + win_t)
    t0 = max(0, t1 - win_t)

    max_freq = min(sr / 2, freqs[-1])
    candidate_bands = [
        (900, min(2600, max_freq)),
        (2600, min(4600, max_freq)),
        (4600, min(7600, max_freq)),
    ]
    band_scores = []
    for lo, hi in candidate_bands:
        band_mask = (freqs >= lo) & (freqs <= hi)
        if np.any(band_mask):
            score = improvement[band_mask, t0 : t1 + 1].mean()
            band_scores.append((float(score), lo, hi))
    if band_scores:
        _, lo, hi = max(band_scores, key=lambda item: item[0])
        f0 = int(np.searchsorted(freqs, lo, side="left"))
        f1 = int(np.searchsorted(freqs, hi, side="right") - 1)
    else:
        f0 = int(rows * 0.35)
        f1 = int(rows * 0.75)

    duration = max(times[-1], 1e-6)
    top_freq = freqs[-1] if freqs[-1] > 0 else sr / 2
    left = 100 * times[t0] / duration
    width = 100 * max(times[t1] - times[t0], duration * 0.22) / duration
    bottom = 100 * freqs[f0] / top_freq
    height = 100 * max(freqs[f1] - freqs[f0], top_freq * 0.24) / top_freq
    top = 100 - bottom - height

    return {
        "left": round(float(np.clip(left, 5, 76)), 1),
        "top": round(float(np.clip(top, 6, 66)), 1),
        "width": round(float(np.clip(width, 20, 40)), 1),
        "height": round(float(np.clip(height, 22, 42)), 1),
    }


def plot_spectrogram(src: Path, dst: Path, title: str) -> None:
    _sr, times, freqs, db = spectrogram_db(src)
    fig, ax = plt.subplots(figsize=(7.0, 3.1), dpi=150)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#111318")
    extent = [times[0], times[-1], freqs[0] / 1000, freqs[-1] / 1000]
    ax.imshow(db, origin="lower", aspect="auto", extent=extent, cmap="magma")
    ax.set_title(title, fontsize=11, fontweight="bold", pad=6)
    ax.set_xlabel("Time (s)", fontsize=9)
    ax.set_ylabel("Frequency (kHz)", fontsize=9)
    ax.tick_params(axis="both", labelsize=8, length=2)
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("#d6dbe4")
    fig.tight_layout(pad=0.8)
    dst.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dst, bbox_inches="tight")
    plt.close(fig)


def copy_audio(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def find_by_suffix(directory: Path, fid: str) -> Path:
    matches = sorted(directory.glob(f"*{fid}.wav"))
    if not matches:
        raise FileNotFoundError(f"Missing {fid} in {directory}")
    return matches[0]


def metric_float(row: dict[str, str] | None, key: str) -> float | None:
    if not row or row.get(key) in {None, ""}:
        return None
    return float(row[key])


def metrics_from_row(row: dict[str, str] | None) -> dict[str, float]:
    metrics = {}
    for src_key, dst_key, digits in [
        ("pesq", "pesq", 2),
        ("estoi", "estoi", 3),
        ("sisdr", "sisdr", 1),
        ("dnsmos_p808", "dnsmos", 2),
        ("dnsmos_ovr", "dnsmos_ovl", 2),
    ]:
        value = metric_float(row, src_key)
        if value is not None:
            metrics[dst_key] = round(value, digits)
    return metrics


def add_condition(
    sample: dict[str, object],
    key: str,
    src: Path,
    audio_root: Path,
    spec_root: Path,
    metrics: dict[str, float] | None = None,
) -> None:
    fid = str(sample["id"])
    wav_dst = audio_root / fid / f"{key}.wav"
    png_dst = spec_root / fid / f"{key}.png"
    copy_audio(src, wav_dst)
    plot_spectrogram(src, png_dst, TRACK_LABELS[key])
    sample["conditions"].append(
        {
            "key": key,
            "label": TRACK_LABELS[key],
            "audio": str(wav_dst.relative_to(REPO / "docs")),
            "spectrogram": str(png_dst.relative_to(REPO / "docs")),
            "source": src.name,
            "metrics": metrics or {},
        }
    )


def main() -> None:
    noisy_rows = parse_noisy_rows()
    main_rows = {
        model: read_csv_by_fileid(
            FASTENHANCER / "eval_outputs/dns_main_models_nsmetric_details.csv",
            model=model,
            testset="noreverb",
        )
        for model in ["AdapEnhancer"]
    }

    audio_root = REPO / "docs/assets/audio"
    spec_root = REPO / "docs/assets/spectrograms"
    if audio_root.exists():
        shutil.rmtree(audio_root)
    if spec_root.exists():
        shutil.rmtree(spec_root)
    audio_root.mkdir(parents=True, exist_ok=True)
    spec_root.mkdir(parents=True, exist_ok=True)

    manifest = []
    for item in SELECTED:
        fid = item["id"]
        noisy_meta = noisy_rows[fid]
        noisy_src = DNS_ROOT / "noisy" / str(noisy_meta["source"])
        clean_src = DNS_ROOT / "clean" / f"clean_{fid}.wav"
        pair_keys = [key for _, _, origin, adams in PAIR_GROUPS for key in (origin, adams)]
        paths = {
            "noisy": noisy_src,
            "clean": clean_src,
            "adapenhancer_b": TABLE2_WAVS / "adapenhancer_b" / f"{fid}.wav",
            **{key: TABLE2_WAVS / key / f"{fid}.wav" for key in pair_keys},
        }

        noisy_metrics = {
            "pesq": round(float(noisy_meta["pesq"]), 2),
            "stoi": round(float(noisy_meta["stoi"]), 3),
            "dnsmos_ovl": round(float(noisy_meta["ovl"]), 2),
        }
        track_metrics = {
            "noisy": noisy_metrics,
            "adapenhancer_b": metrics_from_row(main_rows["AdapEnhancer"].get(fid)),
            "clean": {},
        }
        for key in pair_keys:
            track_metrics[key] = {}

        sample = {
            "id": fid,
            "noise": item["noise"],
            "label": item["label"],
            "snr": f"{noisy_meta['snr']} dB",
            "reference_keys": REFERENCE_KEYS,
            "metrics": track_metrics,
            "conditions": [],
            "comparison_groups": [],
        }

        for group_id, label, origin_key, adams_key in PAIR_GROUPS:
            sample["comparison_groups"].append(
                {
                    "id": group_id,
                    "label": label,
                    "subtitle": "Original vs AdaMS",
                    "focus": focus_box(paths[origin_key], paths[adams_key], paths["clean"]),
                    "tracks": [
                        {
                            "key": origin_key,
                            "label": "Original",
                            "tag": "Origin",
                            "role": "origin",
                        },
                        {
                            "key": adams_key,
                            "label": "AdaMS",
                            "tag": "AdaMS",
                            "role": "adams",
                        },
                    ],
                }
            )

        for key in [*REFERENCE_KEYS, *pair_keys]:
            add_condition(sample, key, paths[key], audio_root, spec_root, track_metrics[key])
        manifest.append(sample)

    with (REPO / "docs/assets/demo_manifest.json").open("w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print("Selected samples:")
    for sample in manifest:
        n = sample["metrics"]["noisy"]
        a = sample["metrics"]["adapenhancer_b"]
        print(
            f"{sample['id']}: {sample['noise']} SNR {sample['snr']} "
            f"PESQ {n['pesq']} -> {a['pesq']}, OVL {n['dnsmos_ovl']} -> {a['dnsmos_ovl']}"
        )


if __name__ == "__main__":
    main()
