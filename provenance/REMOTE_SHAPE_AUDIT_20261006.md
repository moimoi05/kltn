# Remote tensor-shape evidence — 6 October 2026

The user supplied this source/config/artifact audit from the machine holding the model code. This document records that evidence and its qualifications. The local thesis editor did not inspect the remote checkout, execute the models, rerun tests or collect new forward hooks. No training, PCA refit or test evaluation was performed for this document revision.

## Paper CNN–PCA–T-LSTM–Attention: official P10 retuned runs

| Configuration | Supplied value |
|---|---|
| Experiment | P10A-RETUNED-PAPER-CNN-PCA-TLSTM-ATTENTION |
| Protocol | p10a-retuned-v1 |
| Source commit | 5e7eff571ec18cb5fa11e66bfe449d2045c486c6 |
| CNN runtime | TensorFlow 2.17.1; Keras 3.15.1; Python 3.11.15 |
| T-LSTM runtime | PyTorch 2.6.0+cu124; Python 3.11.15 |
| Scientific CNN input | [N,128,128,128,1], channels-last [N,D,H,W,C] |
| Extracted embedding | 512, taken at GlobalAveragePooling before dropout |
| PCA | Separately fit on each seed's training embeddings; centered; 99% explained variance; no scaling/whitening |
| Selected T-LSTM hidden size | 64, selected with train-only Optuna |
| Selected learning rate | 0.000224618961659 |
| Training minibatch | 16 subjects |
| Sequence length | 3 visits |

N denotes the batch of MRI volumes passed to the CNN; B denotes a subject batch in the longitudinal model. Full-cohort B=251 training / B=54 validation should not be mistaken for the training minibatch16. The [32,32,32,1] input in a parameter-count architecture audit is a reduced audit input, not the scientific input.

| CNN operation | Output shape |
|---|---|
| MRI input | [N,128,128,128,1] |
| Conv3D7³, stride2 | [N,64,64,64,64] |
| MaxPool3³, stride2 | [N,32,32,32,64] |
| Residual stage1 | [N,32,32,32,64] |
| Stage2 | [N,16,16,16,128] |
| Stage3 | [N,8,8,8,256] |
| Stage4 | [N,4,4,4,512] |
| Global average pooling — P10 embedding extraction point | [N,512] |
| Dropout0.45 — standalone CNN path | [N,512] |
| Dense risk — standalone CNN path | [N,1] |

P10 uses the pre-dropout pooled embedding, not the CNN Dense risk. Supplied source references:

- phase_10_paper_cnn_tlstm_reproduction/external/original_CNN_TLSTM/model.py:23
- phase_10_paper_cnn_tlstm_reproduction/src/p10_paper_reproduction/cnn/embedding_extractor.py:11

### Official seed-specific PCA artifacts

| Seed | Input width | PCA K | Retained explained variance | Train array | Validation array |
|---|---:|---:|---:|---|---|
| 20260727 | 512 | 38 | 0.9901210439 | [753,38] | [162,38] |
| 20260728 | 512 | 69 | 0.9900956005 | [753,69] | [162,69] |
| 20260729 | 512 | 2 | 0.9947040587 | [753,2] | [162,2] |

There is no single shared PCA width across the three official seeds. The old p10_pca_audit.md pilot512→4 does not describe these official runs. Official pre-PCA NPZ arrays are [753,512] training and [162,512] validation. The extractor asserts an embedding width of512 at runtime.

| Longitudinal operation | Shape |
|---|---|
| CNN embeddings | [N,512] |
| Group three visits by RID | [B,3,512] |
| Apply seed-specific PCA | [B,3,K], K∈{38,69,2} |
| T-LSTM input | [B,3,K] |
| T-LSTM hidden sequence | [B,3,64] |
| Last hidden / last cell | [B,64] each |
| Attention projection + tanh | [B,3,64] |
| Attention scores | [B,3,1] |
| Attention weights | [B,3,1] |
| Attention weighted context | [B,64] |
| Linear risk | [B,1] |
| Squeezed raw risk | [B] |
| Timestamp / sequence mask | [B,3] each |

Supplied source/config references:

- phase_10_paper_cnn_tlstm_reproduction/src/p10_paper_reproduction/tlstm/original_tlstm_wrapper.py:34
- phase_10_paper_cnn_tlstm_reproduction/src/p10_paper_reproduction/data/longitudinal_dataset.py:39
- phase_10_paper_cnn_tlstm_reproduction/artifacts/manifests/p10a_retuned_tlstm_selected_hyperparameters.json:1

The CNN feature-map shapes are derived from source convolution/pool/residual strides. The embedding and PCA widths are supported by persisted NPZ/manifests; hidden64 is supported by the selected-hyperparameter and T-LSTM reports. This is not a new forward-hook trace.

## CrossFormer3D Tiny: canonical P02-D

| Configuration | Supplied value |
|---|---|
| MRI input | [B,1,144,144,144] |
| Input axis order | [B,C,D,H,W] |
| Stem branches | kernel5/7/9, stride6, 16 channels per branch |
| Stage widths | [64,128,256,512] |
| Stage depths | [2,2,2,2] |
| Attention heads | [2,4,8,16] |
| Group edges | [4,3,3,3] |
| Backbone parameters | 9,790,708 |
| Full P02-D parameters | 9,856,501 |
| Runtime | PyTorch 2.6.0+cu124; Python 3.11.15 |
| Resolved config SHA256 | 0f29e1fc9c2337f39909cf723d0c3e5edb5cc9201e2165c5d0894f6f32c6f5bc |

| Operation | Output shape | Axis order |
|---|---|---|
| MRI input | [B,1,144,144,144] | B,C,D,H,W |
| Branch kernel5 | [B,16,24,24,24] | B,C,D,H,W |
| Branch kernel7 | [B,16,24,24,24] | B,C,D,H,W |
| Branch kernel9 | [B,16,24,24,24] | B,C,D,H,W |
| Concatenate branches | [B,48,24,24,24] | B,C,D,H,W |
| 1×1 projection | [B,64,24,24,24] | B,C,D,H,W |
| Permute + LayerNorm + GELU | [B,24,24,24,64] | B,D,H,W,C |
| Stage1, two blocks | [B,24,24,24,64] | B,D,H,W,C |
| Patch Merge1 | [B,12,12,12,128] | B,D,H,W,C |
| Stage2, two blocks | [B,12,12,12,128] | B,D,H,W,C |
| Patch Merge2 | [B,6,6,6,256] | B,D,H,W,C |
| Stage3, two blocks | [B,6,6,6,256] | B,D,H,W,C |
| Patch Merge3 | [B,3,3,3,512] | B,D,H,W,C |
| Stage4, two blocks | [B,3,3,3,512] | B,D,H,W,C |
| Final LayerNorm | [B,3,3,3,512] | B,D,H,W,C |
| Masked spatial pooling | [B,512] | B,F |
| Identity adapter | [B,512] | B,F |
| Head Linear512→128, GELU, Dropout0.30 | [B,128] | B,F |
| Head Linear128→1 | [B,1] | B,F |
| Squeeze raw risk | [B] | B |

Supplied source references:

- phase_02d_crossformer_single/src/p02d_crossformer/cross_scale_stem.py:38
- phase_02d_crossformer_single/src/p02d_crossformer/crossformer3d_tiny.py:23
- phase_02d_crossformer_single/src/p02d_crossformer/patch_merge_3d.py:17
- phase_02d_crossformer_single/src/p02d_crossformer/survival_head.py:7

For longitudinal CrossFormer, the supplied audit identifies input [B,3,1,144,144,144] and pooled visit sequence [B,3,512]. P03-X applies temporal projection [B,3,128], T-LSTM [B,3,128], temporal attention and raw risk [B]. P04-X/P05-X use the same pooled backbone width512 before their respective concat/pairwise branches. The remote audit does not supply every internal fusion-node shape for P05-XA/XB/XC; do not assign the final ResNet M32/R32/C16 bottlenecks to those distinct variants.

No saved CrossFormer forward-hook log was supplied. Its shape evidence is the source contract plus official_stage_shapes, stem tests at144³, hierarchy-shape tests and backbone-output tests for [B,512]. Persisted parameter/config artifacts identify the canonical variant; they are not an activation-hook measurement.

## Thesis integration boundaries

Chapter3 includes the verified encoder and temporal interfaces, with explicit axis order and evidence qualification. Chapter4 identifies the exact seed↔PCA mapping and pre-dropout extraction point while preserving all frozen experimental scores. The audit does not change the final RC-Free architecture, its144³ input, MONAI stem stride1, its128-wide temporal state or the final-test status.
