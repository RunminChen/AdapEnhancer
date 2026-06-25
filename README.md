# AdapEnhancer

Adaptive multi-resolution speech enhancement for compact streaming scenarios.

This repository is a lightweight public demo page for AdapEnhancer. Source code,
training scripts, and model checkpoints will be released after paper acceptance.
The current version keeps project notes, presentation metrics, and DNS2020 audio
demo assets for listening and spectrogram comparison.

## Highlights

- Adaptive multi-resolution DPM placement across high-, low-, and bottleneck
  feature resolutions.
- Acoustic-state residual weighting for input-dependent scale contribution.
- Compact speech enhancement target with practical streaming constraints.

## Online Demo

The GitHub Pages demo is prepared under [`docs/`](docs/):

```text
https://runminchen.github.io/AdapEnhancer/
```

The page includes 5 DNS2020 no-reverb examples. Each example provides playable
audio and a spectrogram for AdapEnhancer-B, noisy input, clean reference, and
four Original/AdaMS comparison pairs:

| Track | Description |
|---|---|
| AdapEnhancer-B | Proposed enhanced result |
| Noisy | DNS noisy input |
| Clean | DNS clean reference |
| FastEnhancer-B Original | FastEnhancer-B baseline |
| FastEnhancer-B AdaMS | FastEnhancer-B equipped with AdaMS |
| FSPEN / BSRNN / LiSenNet Original | Original structural designs |
| FSPEN / BSRNN / LiSenNet AdaMS | Corresponding AdaMS variants |

## VoiceBank+DEMAND Comparison

FastEnhancer-B follows the VoiceBank+DEMAND comparison table. AdapEnhancer-B
uses the current local 16 kHz VoiceBank validation log. Only shared verified
metrics are reported here.

| Model | Params (K) | MACs (M) | PESQ | STOI | Note |
|---|---:|---:|---:|---:|---|
| FastEnhancer-B | 92 | 262 | 3.13 | 0.945 | Reported VoiceBank+DEMAND baseline |
| AdapEnhancer-B | 85 | 434 | 3.18 | 0.946 | Current log; best PESQ/STOI: 3.19 / 0.946 |

## DNS2020 No-Reverb Demo Metrics

The audio demo uses matched DNS2020 no-reverb test examples. The summary below
follows the paper's matched DNS2020 no-reverb table. ESTOI is shown as a
percentage.

| Model | Structure | Params (K) | MACs (M) | SI-SDR | ESTOI (%) | PESQ | P.808 | SIG | BAK | OVL |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Noisy | -- | -- | -- | -- | 81.00 | 1.58 | -- | 3.39 | 2.62 | 2.48 |
| FastEnhancer-B | Original | 91 | 262 | 17.20 | 90.70 | 2.75 | 3.97 | 3.43 | 4.11 | 3.20 |
| FastEnhancer-B | AdaMS | 91 | 427 | 17.50 | 91.20 | 2.78 | 4.00 | 3.47 | 4.13 | 3.24 |
| FSPEN | Original | 82 | 64 | 16.20 | 89.20 | 2.56 | 3.86 | 3.38 | 4.09 | 3.13 |
| FSPEN | AdaMS | 102 | 138 | 16.60 | 89.90 | 2.62 | 3.94 | 3.39 | 4.09 | 3.14 |
| BSRNN | Original | 334 | 245 | 17.30 | 90.80 | 2.72 | 3.94 | 3.43 | 4.09 | 3.18 |
| BSRNN | AdaMS | 336 | 608 | 17.50 | 91.10 | 2.75 | 3.97 | 3.45 | 4.11 | 3.21 |
| LiSenNet | Original | 48 | 56 | 16.50 | 89.70 | 2.65 | 3.87 | 3.39 | 4.09 | 3.15 |
| LiSenNet | AdaMS | 43 | 78 | 16.70 | 90.10 | 2.69 | 3.90 | 3.42 | 4.09 | 3.17 |
| AdapEnhancer-B | Proposed | 85 | 434 | 17.60 | 91.60 | 2.88 | 3.99 | 3.46 | 4.11 | 3.22 |

## Demo Samples

| Sample | DNS noise type | Input SNR |
|---|---|---:|
| `fileid_5` | Breath noise | 3 dB |
| `fileid_38` | Baby cry | 12 dB |
| `fileid_88` | Traffic | 11 dB |
| `fileid_161` | Babble | 8 dB |
| `fileid_192` | Vacuum cleaner | 1 dB |

## Repository Layout

```text
AdapEnhancer/
├── README.md
├── docs/
│   ├── index.html
│   └── assets/
│       ├── audio/
│       └── spectrograms/
└── demos/
    └── README.md
```

## Citation

Citation information will be added after the paper is accepted.
