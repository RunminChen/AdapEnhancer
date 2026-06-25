# AdapEnhancer

Adaptive multi-resolution speech enhancement for compact streaming scenarios.

This repository is a lightweight public demo page for AdapEnhancer. Source code,
training scripts, and model checkpoints will be released after paper acceptance.
For now, the repository keeps the project summary, demo placeholders, and metric
tables used for presentation.

## Highlights

- Adaptive multi-resolution DPM placement across high-, low-, and bottleneck
  feature resolutions.
- Acoustic-state residual weighting for input-dependent scale contribution.
- Compact speech enhancement target with practical streaming constraints.

## Demo Status

Audio and spectrogram demos will be organized under [`demos/`](demos/). The
current public version intentionally excludes model weights and inference code.

## VoiceBank+DEMAND Comparison

The following numbers are from the current local VoiceBank+DEMAND evaluation
summary. Higher is better for all metrics.

| Model | SI-SNR | PESQ | STOI (%) | ESTOI (%) | DNSMOS SIG | DNSMOS BAK | DNSMOS OVL | P.808 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Noisy | 8.45 | 1.97 | 92.11 | 78.67 | 3.34 | 3.12 | 2.69 | 3.06 |
| FSPEN | 17.68 | 2.50 | 91.87 | 81.59 | 3.24 | 4.08 | 3.00 | 3.44 |
| BSRNN | 17.76 | 2.32 | 90.59 | 80.41 | 3.26 | 4.07 | 3.02 | 3.45 |
| LiSenNet | 17.96 | 2.28 | 90.97 | 80.33 | 3.23 | 4.10 | 3.00 | 3.44 |
| FastEnhancer-T | 16.99 | 2.51 | 91.66 | 81.08 | 3.19 | 4.06 | 2.95 | 3.40 |
| FastEnhancer-S | 16.76 | 2.40 | 90.96 | 80.12 | 3.20 | 4.06 | 2.96 | 3.43 |
| AdapEnhancer | **19.03** | **2.79** | **93.00** | **84.42** | **3.44** | **4.15** | **3.22** | **3.57** |

> Note: the final repository name, model naming, and full reproducible scripts
> will be updated after paper acceptance.

## Repository Layout

```text
AdapEnhancer/
├── README.md
├── docs/
│   └── index.html
└── demos/
    ├── README.md
    ├── audio/
    └── spectrograms/
```

## Citation

Citation information will be added after the paper is accepted.
