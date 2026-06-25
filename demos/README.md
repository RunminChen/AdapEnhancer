# DNS2020 Demo Assets

The public demo uses 5 matched DNS2020 no-reverb examples. Audio and
spectrogram files are stored in [`docs/assets/`](../docs/assets/) so they can be
served directly by GitHub Pages.

## Samples

| Sample | Noise type | Input SNR |
|---|---|---:|
| `fileid_5` | Breath noise | 3 dB |
| `fileid_38` | Baby cry | 12 dB |
| `fileid_88` | Traffic | 11 dB |
| `fileid_161` | Babble | 8 dB |
| `fileid_192` | Vacuum cleaner | 1 dB |

## Tracks

Every sample contains the following playable tracks and matching STFT
spectrograms:

| Track key | Display name |
|---|---|
| `adapenhancer_b` | AdapEnhancer-B |
| `noisy` | Noisy |
| `clean` | Clean |
| `fastenhancer_b_original` | FastEnhancer-B Original |
| `fastenhancer_b_adams` | FastEnhancer-B AdaMS |

Path pattern:

```text
docs/assets/audio/<sample>/<track-key>.wav
docs/assets/spectrograms/<sample>/<track-key>.png
```

The machine-readable listing is available at
[`docs/assets/demo_manifest.json`](../docs/assets/demo_manifest.json).
