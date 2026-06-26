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

Demo URL: <https://runminchen.github.io/AdapEnhancer/>

The GitHub Pages demo is prepared under [`docs/`](docs/).

The page includes 3 DNS2020 no-reverb examples. Each example provides playable
audio, matched spectrograms, a Noisy / AdapEnhancer-B / Clean reference triplet,
and four Original/AdaMS comparison pairs:

| Track | Description |
|---|---|
| AdapEnhancer-B | Proposed enhanced result |
| Noisy | DNS noisy input |
| Clean | DNS clean reference |
| BSRNN Original / AdaMS | Pairwise comparison |
| FSPEN Original / AdaMS | Pairwise comparison |
| LiSenNet Original / AdaMS | Pairwise comparison |
| FastEnhancer-B Original / AdaMS | Pairwise comparison |

## VoiceBank+DEMAND Comparison

The table follows the VoiceBank+DEMAND metrics used in the comparison figure.
DNSMOS denotes P.808, while SIG/BAK/OVL denote DNSMOS P.835. AdapEnhancer-B
uses the local 16 kHz VoiceBank+DEMAND test evaluation from `scripts/metrics_ns.py`.

| Model | Para. (K) | MACs | DNSMOS | SIG | BAK | OVL | SI-SDR | PESQ | STOI | ESTOI | WER |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GTCRN | 24 | 40M | 3.43 | 3.36 | 4.02 | 3.08 | 18.8 | 2.87 | 0.940 | 0.848 | 3.6 |
| LiSenNet-b | 37 | 56M | 3.34 | 3.30 | 3.90 | 2.98 | 13.5 | 3.08 | 0.938 | 0.842 | 3.7 |
| LiSenNet-c | 37 | 56M | 3.42 | 3.34 | 4.03 | 3.07 | 18.5 | 2.98 | 0.941 | 0.851 | 3.4 |
| FSPEN-c | 79 | 64M | 3.40 | 3.33 | 4.00 | 3.05 | 18.4 | 3.00 | 0.942 | 0.850 | 3.6 |
| BSRNN-d | 334 | 245M | 3.44 | 3.36 | 4.00 | 3.07 | 18.9 | 3.06 | 0.942 | 0.855 | 3.4 |
| FastEnhancer-B | 92 | 262M | 3.47 | 3.38 | 4.02 | 3.10 | 19.0 | 3.13 | 0.945 | 0.861 | 3.2 |
| AdapEnhancer-B | 87.5 | 434M | 3.48 | 3.38 | 4.02 | 3.10 | 19.1 | 3.18 | 0.946 | 0.864 | 2.9 |

AdapEnhancer-B metrics were evaluated with epoch 500. The WER shown for
AdapEnhancer-B is 2.9.

## Demo Samples

| Sample | DNS noise type | Input SNR |
|---|---|---:|
| `fileid_161` | Babble | 8 dB |
| `fileid_192` | Vacuum cleaner | 1 dB |
| `fileid_5` | Breath | 3 dB |

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
