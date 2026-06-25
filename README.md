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

The table follows the VoiceBank+DEMAND metrics used in the comparison figure.
DNSMOS denotes P.808, while SIG/BAK/OVL denote DNSMOS P.835. AdapEnhancer-B
uses our current local 16 kHz VoiceBank validation log. Dashes denote metrics
not available in the current local log.

| Model | Para. (K) | MACs | DNSMOS | SIG | BAK | OVL | SI-SDR | PESQ | STOI | ESTOI | WER |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GTCRN [9] | 24 | 40M | 3.43 | 3.36 | 4.02 | 3.08 | 18.8 | 2.87 | 0.940 | 0.848 | 3.6 |
| LiSenNet-b [11] | 37 | 56M | 3.34 | 3.30 | 3.90 | 2.98 | 13.5 | 3.08 | 0.938 | 0.842 | 3.7 |
| LiSenNet-c [11] | 37 | 56M | 3.42 | 3.34 | 4.03 | 3.07 | 18.5 | 2.98 | 0.941 | 0.851 | 3.4 |
| FSPEN-c [10] | 79 | 64M | 3.40 | 3.33 | 4.00 | 3.05 | 18.4 | 3.00 | 0.942 | 0.850 | 3.6 |
| BSRNN-d [12] | 334 | 245M | 3.44 | 3.36 | 4.00 | 3.07 | 18.9 | 3.06 | 0.942 | 0.855 | 3.4 |
| FastEnhancer-T | 22 | 55M | 3.42 | 3.34 | 4.01 | 3.06 | 18.6 | 2.99 | 0.940 | 0.850 | 3.6 |
| FastEnhancer-B | 92 | 262M | 3.47 | 3.38 | 4.02 | 3.10 | 19.0 | 3.13 | 0.945 | 0.861 | 3.2 |
| FastEnhancer-S | 195 | 664M | 3.49 | 3.40 | 4.03 | 3.12 | 19.2 | 3.19 | 0.947 | 0.866 | 3.2 |
| FastEnhancer-M | 492 | 2.9G | 3.48 | 3.39 | 4.02 | 3.11 | 19.4 | 3.24 | 0.950 | 0.873 | 2.8 |
| FastEnhancer-L | 1105 | 11G | 3.53 | 3.44 | 4.04 | 3.16 | 19.6 | 3.26 | 0.952 | 0.877 | 3.1 |
| AdapEnhancer-B | 85 | 434M | -- | -- | -- | -- | -- | 3.18 | 0.946 | -- | 2.9 |

AdapEnhancer-B best local PESQ/STOI: 3.1854 / 0.9463. The WER shown for
AdapEnhancer-B is 2.9.

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
