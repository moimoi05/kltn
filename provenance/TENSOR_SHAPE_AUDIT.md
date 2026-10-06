# Tensor-shape audit — 6 October 2026

Read-only scientific evidence audit, followed by documentation updates. No model, data, training or preprocessing was changed by this audit. Neither `D:/KLTN/.codegraph` nor `D:/KLTN/project/.codegraph` exists. Local ZIPs were inspected in memory, including nested P03 ZIPs. No PyTorch/MONAI installation or forward run was performed. Additional remote source/artifact findings were supplied by the user and are attributed separately below.

## Conclusion

The final RC-Free step-by-step interface table is supported by the actual P05B source and the controlled CP → P06/A6 → P06B lineage. Internal ResNet maps are **derived from the source/configuration**, because the actual wrapper and the recorded MONAI 1.5.2 runtime identify all spatial settings. They are not new hook measurements. The user's subsequent remote source/artifact audit also supplies the official P10 per-seed PCA dimensions and hidden size, plus the P02-D CrossFormer channel-layout transitions. These findings are recorded in [REMOTE_SHAPE_AUDIT_20261006.md](REMOTE_SHAPE_AUDIT_20261006.md). The local auditor did not execute remote hooks or independently verify the remote commit/source files.

## Authority and evidence

- **B**: `D:/KLTN/phase_05b_pairwise_medicalnet_source.zip`. Prefix: `phase_05b_pairwise_medicalnet/`.
  - `configs/p05b_common.yaml`: frozen inputs lines 10–27; encoder/fusion/temporal dimensions lines 68–148.
  - `src/p05b_pairwise_medicalnet/mri_encoder.py`: exact `resnet18` constructor lines 49–54; per-visit sequential encoding and projection lines 107–122.
  - Actual `clinical_encoder.py`, `radiomics_encoder.py`, `low_rank_projection.py`, `dynamic_gate.py`, `dynamic_pairwise_fusion.py`, `tlstm.py`, `tlstm_cell.py`, `temporal_attention.py`, `survival_head.py` establish the other interfaces.
  - `artifacts/manifests/p05b_architecture_manifest.json`: authoritative frozen inputs and all component dimensions.
  - `reports/phase_05b_preparation_summary.json`: runtime MONAI **1.5.2**.
  - `reports/p05b_end_to_end_flow_audit.json`: authoritative real MRI `[B,3,1,144,144,144]`; synthetic diagnostic interfaces agree with the source, but its synthetic MRI is **8³**. `p05b_dataset_inspection.md` uses a **4³** smoke placeholder. Neither is a measured real-volume feature-map trace.
- **E**: `D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip`.
  - `phase_00_audit/reports/training_data_schema_v1.md`: bin64 PCA has 16 columns; bin32 PCA has 17; scaled radiomics 104.
  - `phase_04_concat_fusion/reports/p04_architecture.md`.
  - `phase_05_cp/reports/p05cp_architecture.md` and `p05cp_lineage.md`: only first pair interaction transforms change; all other interfaces retained.
  - `project_reports/P06_A6_NO_RC_multiseed_validation.md`: MR/MC rank 8/8 remain, RC removed; temporal stack unchanged.
  - `phase_06b_targeted/reports/p06b_lineage.md`: same RC-Free interfaces; learnable lambdas replaced by fixed 0.1.
  - `phase_04x_crossformer_concat/reports/p04x_architecture_audit.md`: CrossFormer spatial stages, final channels512, matching modality/readout interfaces.
- **R**: `D:/KLTN/project/phase3 fix-20260730T142818Z-1-001.zip`, inner member `phase3 fix/phase_03_tlstm_attention_amp_repaired_green_bundle_p03_tlstm_attn_amp_repaired_one_epoch_20260730T141622Z_seed20260727.zip`. Actual `src/p03_mri_longitudinal/model.py`, `tlstm.py`, `tlstm_cell.py`, `config.py` and the pilot `resolved_architecture.json` / `resolved_config.yaml` verify the P03 T-LSTM/attention interfaces. This is a source/interface qualification artifact, not evidence of a fully closed formal scientific run.
- **M**: official version-pinned MONAI source, accessed 6 October 2026: [MONAI 1.5.2 resnet.py](https://raw.githubusercontent.com/Project-MONAI/MONAI/1.5.2/monai/networks/nets/resnet.py). Constructor defaults: stride1 stem, kernel7, padding3, max-pool kernel3/stride2/padding1, stage widths64/128/256/512; `resnet18` uses two basic blocks per stage. The project invokes `resnet18`, **not** `ResNetFeatures` (the latter explicitly sets stem stride2).
- **U**: remote audit supplied by the user on 6 October 2026, transcribed and qualified in `REMOTE_SHAPE_AUDIT_20261006.md`. P10 official retuned seed20260727/28/29 uses PCA widths38/69/2 and T-LSTM hidden64. P02-D CrossFormer accepts channel-first MRI144³ and permutes its projected stem to `[B,D,H,W,C]`. This is reported source/contract/test and persisted-artifact evidence, not a newly executed forward-hook trace.

## Proposed final-step table

Use `B` for subject batch, `T=3` for visits, and channel-first MRI `[B,T,C,D,H,W]`. Batch size is not part of the architectural feature width: physical training batch is6, but inference/validation batch can vary. All visit operations share weights and preserve `[B,T]` until temporal aggregation.

| Step | Shape / transition | Evidence |
|---|---|---|
| Model-ready MRI | `[B,3,1,144,144,144]` | B config/manifest; E lineage |
| One selected visit into shared CNN | `[B,1,144,144,144]` | B `mri_encoder.py` |
| CNN pooled vectors, all visits | `[B,3,512]` | B sequence encoder |
| MRI projection | `[B,3,512] → [B,3,128]` | B Linear512→128 |
| Radiomics preparation | 107 features/image →104 after three train-constant removals →PCA99 **16**; assembled input `[B,3,16]` | E schema and methods audit |
| Radiomics MLP | `[B,3,16] → [B,3,128] → [B,3,64]` | B encoder; E CP lineage |
| Clinical values and observedness mask | `[B,3,9]` each; concat `[B,3,18]` | B clinical source/manifest |
| Clinical MLP | `[B,3,18] → [B,3,64] → [B,3,64]` | B clinical encoder |
| Low modality projections | M:128→32, R:64→32, C:64→16; `[B,3,32]`, `[B,3,32]`, `[B,3,16]` | B low projections; E controlled lineage |
| CP MR and MC rank-space | two factor outputs `[B,3,8]`; Hadamard result `[B,3,8]` for **each** pair | E CP architecture; P06/A6 definition |
| CP hidden →pair embedding | MR/MC: `[B,3,8] → [B,3,128] → [B,3,64]` | E CP architecture |
| Directed projected pairs | `(MR→M)`, `(MC→M)`: `[B,3,128]`; `(MR→R)`, `(MC→C)`: `[B,3,64]` | B directed adapters; E RC-Free lineage |
| Four dynamic gates | each `[B,3,1]`; gate input256 for M targets,128 for R/C targets; hidden32 | B gate source; E active-route definition |
| Route lambda | each scalar shape `[]`, global learnable; broadcast across B,T,features. P06B uses fixed scalar0.1 | B lambdas / E P06B |
| Centered residual outputs | M `[B,3,128]`, R/C `[B,3,64]` | B residuals; E RC-Free lineage |
| Fusion concat and readout | `[B,3,256] → [B,3,128]` | B fusion source |
| Time intervals and sequence mask | each `[B,3]`; at each visit slice `[B,1]` | B model and T-LSTM source |
| T-LSTM hidden sequence | `[B,3,128]`; hidden/cell at a visit `[B,128]` | B T-LSTM source |
| Temporal score and weights | score MLP `[B,3,128] → [B,3,64] → [B,3,1]`; squeeze scores/weights `[B,3]` | B attention source |
| Attention pooled patient vector | `[B,128]` | B weighted sum across T |
| Cox head and risk | `[B,128] → [B,64] → [B,1]`; squeeze raw log-risk `[B]` | B survival head |

For a compact thesis table, group the two radiomics rows and the two clinical rows; group the gate/lambda rows and time/mask rows. If including CNN internals, put those in a separate short encoder table rather than widening the overall table.

## Source-derived MRI stage table

At one visit (channel-first, B subjects), exact P05B wrapper + MONAI1.5.2 defaults imply:

| Operation | Output |
|---|---|
| Input | `[B,1,144,144,144]` |
| Stem Conv3D7³ / stride1 / padding3, BN, ReLU | `[B,64,144,144,144]` |
| MaxPool3D3³ / stride2 / padding1 | `[B,64,72,72,72]` |
| Stage1, two basic blocks, width64 / stride1 | `[B,64,72,72,72]` |
| Stage2, width128, first block stride2 | `[B,128,36,36,36]` |
| Stage3, width256, first block stride2 | `[B,256,18,18,18]` |
| Stage4, width512, first block stride2 | `[B,512,9,9,9]` |
| Adaptive global average pool | `[B,512,1,1,1]` |
| Flatten | `[B,512]` |
| Stack pooled vectors from three sequential visits | `[B,3,512]` |
| Shared Linear512→128, GELU, Dropout0.20, LN | `[B,3,128]` |

These dimensions follow the usual convolution/pool floor formula. Do not copy the baseline screenshot's128³ or stem stride2. MedicalNet loading changes parameter values and initializes target-only shortcut-B states deterministically; it does not change stride/padding/kernel configuration. CP lineage declares the MRI module unchanged, so this is the justified source-derived final encoder table; an actual server hook trace would strengthen the record.

## CP 3D figure and factor dimensions

Draw the **bilinear interaction weight tensor**, not an MRI or patient feature tensor. Use the thesis axis order and a cuboid labeled `W ∈ R^(h × d_x × d_y)`, with indices `W[s,i,j]`, and three factor matrices / rank-one component axes. A reconstruction `Σ_q o_q ∘ a_q ∘ b_q` explains the third order while the computation `u=Aᵀx`, `v=Bᵀy`, `q=u⊙v`, `hidden=Oq+b` explains the efficient forward path. Here `h` is the hidden-output width, not an MRI spatial dimension.

| Pair | Conceptual W cuboid | Rank | Conceptual A / B / O | Rank activation | Hidden / output |
|---|---|---:|---|---|---|
| MR |128×32×32|8|32×8 /32×8 /128×8|`[B,T,8]`|128 /64|
| MC |128×32×16|8|32×8 /16×8 /128×8|`[B,T,8]`|128 /64|
| RC (full CP reference only) |64×32×16|4|32×4 /16×4 /64×4|`[B,T,4]`|64 /32|

PyTorch stores `nn.Linear` weights as `[out,in]`: A/B are `[Q,d_x]`, `[Q,d_y]`, O is `[h,Q]`. A/B are bias-free; O retains hidden bias `[h]`. The full first Linear stores `[h,d_x*d_y]`, equivalently the conceptual 3D W. CP forward does **not** instantiate W, an outer product or its flatten activation. RC-Free has only MR/MC. Drawing W/reconstruction is a mathematical illustration, not an extra executed operation.

## Historical phase interfaces and the user's remote evidence

| Phase | Supported interface | Qualification |
|---|---|---|
| P02 MRI-only | one visit `[B,1,144³] →512 →128 →1 →risk[B]` | E `monai_backbone.md`; shortcut-A MedicalNet-compatible settings differ from P05B shortcutB. Do not copy internal map settings from P05B without the P02 constructor. |
| P03 T-LSTM | three MRI→512→128→T-LSTM128→last-valid hidden128→Cox64→1 | Actual nested R model/config validates dimensions; its attention variant instead pools with128→64→1 scores. |
| P04 concat | M128/R64/C64→concat256→128→T-LSTM128→attention→Cox[B] | Direct E architecture, no CP or pairwise tensor. |
| P05/P05B full pairwise | low M32/R32/C16; MR outer32×32→flat1024→128→64; MC32×16→512→128→64; RC32×16→512→64→32; six routes; same concat256→128 temporal/readout | B actual source; E architecture equivalence. |
| P05-CP | same outputs as full P05B; rank MR/MC8, RC4; no outer activation | E architecture/lineage. |
| P06/A6 RC-Free | final table above; MR/MC8; four gates/scales; three modalities remain | E A6 multi-seed definition. |
| P06B/B1 | same tensor interfaces as P06/A6 | Four learnable lambdas replaced by fixed0.1 only. |
| P02-D CrossFormer MRI-only | channel-first `[B,1,144,144,144]`; three stem branches each `[B,16,24,24,24]`→channel concat `[B,48,24,24,24]`→1×1 projection `[B,64,24,24,24]`→permute `[B,24,24,24,64]`; stages24³/64→12³/128→6³/256→3³/512 | U source/contracts/tests plus persisted artifacts; internal stages use `[B,D,H,W,C]` after the stem permutation. No new forward-hook measurement. |
| P04-X CrossFormer concat | stages recorded as spatial24³/ch64→12³/ch128→6³/ch256→3³/ch512; pooled512→128; same M/R/C concat256→128 and temporal/head as P04 | E direct architecture plus the same CrossFormer design family identified by U. The explicit U axis-layout audit is P02-D; do not claim a separate P04-X measured hook trace. |
| P05-XA/B/C | CrossFormer stages retained; pairwise fusion is a different common-width design; common M/R/C128, base concat384, pair output128, fusion output128 | E matched protocol table; do not assign final ResNet MR32/R32/C16 topology to this branch. A per-node activation table still needs full actual code. |
| P10 official retuned paper adaptation | TensorFlow channels-last volume batch `[N,128,128,128,1]`, CNN stem stride2; pre-dropout global-average-pooling512; longitudinal subject batch `[B,3,512]`→train-only PCA99 `[B,3,K]`→T-LSTM hidden64 | U gives K=38/69/2 for official seed20260727/28/29 respectively. The original paper's unspecified selected hyperparameter remains distinct from this project's identified retuned configuration. Do not assign final144³ inputs or hidden128 to P10. |

The loose `D:/KLTN/project/src/models/full_model.py`, `configs/default.yaml`, `tests/test_shapes.py` describe an **obsolete prototype**: MRI128³, radiomics150, clinical20, embeddings512 each, pair512²→32², concat1536, recurrent hidden256. They are not the final trained lineage. Likewise E `phase_03_mri_longitudinal/reports/model_architecture.md` describes the archived learned-time-embedding standard-LSTM design `[B,3,144]`; the nested repaired ZIP explicitly marks this model archived and supplies paper-style T-LSTM without a learned time embedding.

## Remote audit qualification

The user supplied the requested P10 seed-specific PCA widths and selected hidden size, and the CrossFormer stem/stage layout audit. The details and exact source/config/version/hash identifiers supplied by the user belong in `REMOTE_SHAPE_AUDIT_20261006.md`; they are not a claim that this local session inspected those remote files or ran those tests/hooks. The evidence method is a remote **source/contract/test and persisted-artifact audit**, with no new forward hooks. It is sufficient to document those configured interfaces while keeping that method qualification visible.

No architecture, PCA fit, training result, checkpoint selection or test evaluation was changed. If future work needs measured shapes, run a separate read-only synthetic eval trace on the exact named model/config; an8³ or4³ smoke trace must not be described as the configured144³ encoder trace.

All conclusions above refer to evidence already archived, not new training results or prospective availability guarantees.
