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

SELECTED = [
    {"id": "fileid_44", "noise": "Birds", "label": "Bird calls, low SNR"},
    {"id": "fileid_110", "noise": "Baby cry", "label": "Baby cry interference"},
    {"id": "fileid_231", "noise": "Vacuum cleaner", "label": "Vacuum motor noise"},
    {"id": "fileid_52", "noise": "Barking", "label": "Barking transient noise"},
    {"id": "fileid_88", "noise": "Traffic", "label": "Traffic background"},
]

TRACKS = {
    "noisy": "Noisy",
    "adapenhancer_b": "AdapEnhancer-B",
    "clean": "Clean",
    "fastenhancer_b_original": "FastEnhancer-B Original",
    "fastenhancer_b_adams": "FastEnhancer-B AdaMS",
}


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
            filename = row.get("filename") or row.get("Filename") or row.get("Clean_Filename") or ""
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


def focus_box(noisy_path: Path, enhanced_path: Path) -> dict[str, float]:
    sr, times, freqs, noisy_db = spectrogram_db(noisy_path)
    _, _, _, enhanced_db = spectrogram_db(enhanced_path)
    rows = min(noisy_db.shape[0], enhanced_db.shape[0])
    cols = min(noisy_db.shape[1], enhanced_db.shape[1])
    noisy_db = noisy_db[:rows, :cols]
    enhanced_db = enhanced_db[:rows, :cols]
    freqs = freqs[:rows]
    times = times[:cols]

    diff = np.maximum(noisy_db - enhanced_db, 0)
    band = (freqs >= 900) & (freqs <= min(sr / 2, 7600))
    if not np.any(band):
        band = np.ones_like(freqs, dtype=bool)
    energy_t = diff[band].mean(axis=0)

    win_t = max(8, min(cols, int(round(0.9 / max(times[1] - times[0], 1e-3)))))
    kernel = np.ones(win_t) / win_t
    smooth_t = np.convolve(energy_t, kernel, mode="same")
    center_t = int(np.argmax(smooth_t))
    t0 = max(0, center_t - win_t // 2)
    t1 = min(cols - 1, t0 + win_t)
    t0 = max(0, t1 - win_t)

    energy_f = diff[:, t0 : t1 + 1].mean(axis=1)
    valid_f = np.flatnonzero(band)
    center_f = valid_f[int(np.argmax(energy_f[band]))]
    win_f = max(18, rows // 4)
    f0 = max(0, center_f - win_f // 2)
    f1 = min(rows - 1, f0 + win_f)
    f0 = max(0, f1 - win_f)

    duration = max(times[-1], 1e-6)
    top_freq = freqs[-1] if freqs[-1] > 0 else sr / 2
    left = 100 * times[t0] / duration
    width = 100 * max(times[t1] - times[t0], duration * 0.18) / duration
    bottom = 100 * freqs[f0] / top_freq
    height = 100 * max(freqs[f1] - freqs[f0], top_freq * 0.24) / top_freq
    top = 100 - bottom - height

    return {
        "left": round(float(np.clip(left, 2, 82)), 1),
        "top": round(float(np.clip(top, 4, 68)), 1),
        "width": round(float(np.clip(width, 16, 42)), 1),
        "height": round(float(np.clip(height, 20, 48)), 1),
    }


def plot_spectrogram(src: Path, dst: Path, title: str, highlight: dict[str, float] | None) -> None:
    sr, times, freqs, db = spectrogram_db(src)
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


def main() -> None:
    noisy_rows = parse_noisy_rows()
    adap_rows = read_csv_by_fileid(
        FASTENHANCER / "eval_outputs/dns_main_models_nsmetric_details.csv",
        model="AdapEnhancer",
        testset="noreverb",
    )
    fast_rows = read_csv_by_fileid(
        FASTENHANCER / "eval_outputs/dns_main_models_nsmetric_details.csv",
        model="FastEnhancer-B",
        testset="noreverb",
    )
    adams_rows = read_csv_by_fileid(FASTENHANCER / "eval_outputs/fastenhancer_b_adams_objective.csv")

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
        adap_src = find_by_suffix(FASTENHANCER / "adapenhancer_b_lsig_adaperb/noreverb", fid)
        fast_src = find_by_suffix(FASTENHANCER / "fast_b/noreverb", fid)
        adams_src = FASTENHANCER / "eval_outputs/fastenhancer_b_adams_noreverb_wavs" / f"{fid}.wav"

        paths = {
            "noisy": noisy_src,
            "adapenhancer_b": adap_src,
            "clean": clean_src,
            "fastenhancer_b_original": fast_src,
            "fastenhancer_b_adams": adams_src,
        }
        focus = focus_box(noisy_src, adap_src)
        sample = {
            "id": fid,
            "noise": item["noise"],
            "label": item["label"],
            "snr": f"{noisy_meta['snr']} dB",
            "focus": focus,
            "metrics": {
                "noisy": {
                    "pesq": round(float(noisy_meta["pesq"]), 2),
                    "stoi": round(float(noisy_meta["stoi"]), 3),
                    "dnsmos_ovl": round(float(noisy_meta["ovl"]), 2),
                },
                "adapenhancer_b": {
                    "pesq": round(float(adap_rows[fid]["pesq"]), 2),
                    "estoi": round(float(adap_rows[fid]["estoi"]), 3),
                    "dnsmos_ovl": round(float(adap_rows[fid]["dnsmos_ovr"]), 2),
                },
                "fastenhancer_b_original": {
                    "pesq": round(float(fast_rows[fid]["pesq"]), 2),
                    "estoi": round(float(fast_rows[fid]["estoi"]), 3),
                    "dnsmos_ovl": round(float(fast_rows[fid]["dnsmos_ovr"]), 2),
                },
                "fastenhancer_b_adams": {
                    "pesq": round(float(adams_rows[fid]["pesq"]), 2),
                    "estoi": round(float(adams_rows[fid]["estoi"]), 3),
                },
            },
            "conditions": [],
        }
        for key, label in TRACKS.items():
            wav_dst = audio_root / fid / f"{key}.wav"
            png_dst = spec_root / fid / f"{key}.png"
            copy_audio(paths[key], wav_dst)
            plot_spectrogram(paths[key], png_dst, label, focus if key in {"noisy", "adapenhancer_b"} else None)
            sample["conditions"].append(
                {
                    "key": key,
                    "label": label,
                    "audio": str(wav_dst.relative_to(REPO / "docs")),
                    "spectrogram": str(png_dst.relative_to(REPO / "docs")),
                    "source": paths[key].name,
                }
            )
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
