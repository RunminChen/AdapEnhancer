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

The page includes 5 DNS2020 no-reverb examples. Each example provides playable
audio and a spectrogram for AdapEnhancer-B, noisy input, clean reference, and
one FastEnhancer-B Original/AdaMS comparison pair:

| Track | Description |
|---|---|
| AdapEnhancer-B | Proposed enhanced result |
| Noisy | DNS noisy input |
| Clean | DNS clean reference |
| FastEnhancer-B Original | FastEnhancer-B baseline |
| FastEnhancer-B AdaMS | FastEnhancer-B equipped with AdaMS |

## VoiceBank+DEMAND Comparison

The table follows the VoiceBank+DEMAND metrics used in the comparison figure.
DNSMOS denotes P.808, while SIG/BAK/OVL denote DNSMOS P.835. AdapEnhancer-B
uses our current local 16 kHz VoiceBank validation log. Dashes denote metrics
not available in the current local log.

| Model | Para. (K) | MACs | DNSMOS | SIG | BAK | OVL | SI-SDR | PESQ | STOI | ESTOI | WER |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FastEnhancer-B | 92 | 262M | 3.47 | 3.38 | 4.02 | 3.10 | 19.0 | 3.13 | 0.945 | 0.861 | 3.2 |
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
