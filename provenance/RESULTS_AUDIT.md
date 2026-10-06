# Numerical evidence audit for the revised thesis

Scope: read-only audit of local project reports, weekly report sources and ZIP member inventories. No model run, refit, prediction generation, frozen-data modification, or server verification was performed. Attached-document instructions were treated as source material, never as authorization to train/evaluate models.

## Authoritative source order

1. Standardized validation report JSON plus checkpoint/split audit (21 September 2026) for canonical deep results and metric convention.
2. Phase evolution bundle (5 October 2026), including controlled comparisons, ablation JSON, classical CSV, source lineage and exact run summaries.
3. Scientific phase reports for historical runtime/batching; weekly reports as secondary context.
4. Original thesis draft is editable content, not an authoritative numeric source.

## Corrections and caveats

- Original thesis MRI initialization labels are reversed. Raw P02 comparison confirms **MedicalNet = 0.7333333333 (P02-A)** and **random ResNet = 0.7875000000 (P02-B)**. Random initialization was selected for the subsequent early ResNet longitudinal chain. Do not claim universal MedicalNet superiority.
- P03 and the P05/MedicalNet/CP/RC-Free family use physical Cox risk sets of **6 subjects**, with accumulation 2 and optimizer-effective batch 12. P04 concat uses physical Cox risk sets of **8 subjects**, accumulation 2 and optimizer-effective batch 16. Therefore the historical concat 0.812500 → random pairwise 0.828125 change is not a controlled fusion-only contrast; longitudinal→concat is likewise not a matched-input/batching effect.
- The repaired Longitudinal MRI + attention value 0.783333 is best-observed with incomplete closure, not an authoritative three-seed result. The earlier attention run aborted due to AMP overflow and is ineligible for selection.
- The archived `phase_03_mri_longitudinal/reports/model_architecture.md` describes an older ordinary-LSTM scaffold. Later scientific report and phase evolution audit explicitly describe the paper-style T-LSTM. Do not propagate the old scaffold architecture as the final methodology.
- Neural canonical C-index uses only event-subject i vs subject j with time_i < time_j; higher risk = earlier event, risk ties =0.5, tied survival times excluded. Validation has 480 comparable pairs. P01 uses scikit-survival `concordance_index_censored`, and final representation/family was selected after validation evaluation following train CV. Keep this classical result separate from neural mean±SD; a raw rank does not establish an identical-protocol win.
- Benchmark replay uses best validation-selected checkpoints, not historical last-checkpoint validation_predictions.json. All fifteen deep seed cells were audited/reused; no retraining was required.
- Three seeds share the same frozen split. Sample SD measures initialization/training variation, not patient resampling, confidence interval, external validation, or statistical significance.
- Fixed-λ vs RC-Free mean difference is exactly 0 when recomputed from raw seed values. Some source follow-up comparison fields subtract rounded means and show a spurious 0.0000002222 difference.
- P07 formal final evaluation remains NOT_STARTED. Weekly post-hoc test reports and a P05-CP post-hoc test artifact exist, but their numbers are excluded from architecture selection and thesis comparison plots. Exact thesis statement: **Formal held-out final evaluation has not yet been performed.**

## Standardized validation values (sample SD, n=3)

| Display label | Seed 20260727 | Seed 20260728 | Seed 20260729 | Mean | Sample SD | Total parameters |
|---|---:|---:|---:|---:|---:|---:|
| Paper CNN–T-LSTM | 0.662500000 | 0.770833333 | 0.791666667 | 0.741666667 | 0.069347154 | seed-specific: 33205186/33213122/33195970 |
| MedicalNet Pairwise | 0.839583333 | 0.845833333 | 0.817708333 | 0.834375000 | 0.014768174 | 33760941 |
| CP Pairwise | 0.821875000 | 0.855208333 | 0.806250000 | 0.827777778 | 0.025007233 | 33534957 |
| RC-Free Pairwise | 0.841666667 | 0.854166667 | 0.808333333 | 0.834722222 | 0.023692670 | 33519497 |
| RC-Free Fixed-λ | 0.833333333 | 0.866666667 | 0.804166667 | 0.834722222 | 0.031273140 | 33519493 |

Mean and SD were independently recomputed from the exact JSON per-seed floats using `statistics.mean` and `statistics.stdev` (ddof=1); they agree within 1e-14 with the benchmark aggregates.

Descriptive mean differences:
- cp_minus_full_mean: -0.006597222222
- rcfree_minus_cp_mean: 0.006944444444
- rcfree_minus_full_mean: 0.000347222222
- fixedlambda_minus_rcfree_mean: 0.000000000000

## Controlled ablations, seed 20260727

Full CP reference = 0.821875000.

| Change | Validation C-index | Delta vs full CP | Total parameters |
|---|---:|---:|---:|
| Remove gate | 0.820833333 | -0.001041667 | 33,501,287 |
| Fixed λ | 0.836458333 | +0.014583333 | 33,534,951 |
| Remove residual | 0.827083333 | +0.005208333 | 33,534,957 |
| Remove MR | 0.816666667 | -0.005208333 | 33,499,625 |
| Remove MC | 0.837500000 | +0.015625000 | 33,499,753 |
| Remove RC | 0.841666667 | +0.019791667 | 33,519,497 |

No gate and no MR decrease slightly; fixed λ, no residual, no MC and no RC increase at this seed. Thus there is **no evidence to claim every proposed component improves performance**. RC removal was the largest positive exploratory delta, followed by an RC-Free three-seed follow-up. Other ablations remain single-seed.

## Classical/tabular results

| Representation | Family | Features | Train-CV mean | Train-CV SD | Validation C-index |
|---|---|---:|---:|---:|---:|
| R01_CLINICAL_V2 | cox | 18 | 0.846770 | 0.062789 | 0.837838 |
| R02_CLINICAL_LONG | cox | 54 | 0.854456 | 0.062512 | 0.837838 |
| R03_RAD32_V2 | cox | 17 | 0.631071 | 0.092626 | 0.744283 |
| R04_RAD32_LONG | cox | 51 | 0.631474 | 0.105575 | 0.582121 |
| R05_RAD64_V2 | cox | 16 | 0.641789 | 0.080893 | 0.748441 |
| R06_RAD64_LONG | cox | 48 | 0.630438 | 0.103571 | 0.559252 |
| R07_CLINICAL_RAD32_LONG | cox | 105 | 0.854343 | 0.050854 | 0.852391 |
| R08_CLINICAL_RAD64_LONG | cox | 102 | 0.854910 | 0.056547 | 0.860707 |
| R01_CLINICAL_V2 | rsf | 18 | 0.825312 | 0.078726 | 0.790021 |
| R02_CLINICAL_LONG | rsf | 54 | 0.838941 | 0.084525 | 0.837838 |
| R07_CLINICAL_RAD32_LONG | rsf | 105 | 0.839581 | 0.057995 | 0.839917 |
| R08_CLINICAL_RAD64_LONG | rsf | 102 | 0.838863 | 0.073890 | 0.856549 |

Cox alpha grid =0.001/0.01/0.1, l1_ratio=0.05/0.5; 8 representations×6=48 candidate CV configurations. RSF trained only on four train-CV-selected representations with300 trees, max_depth4/8,min_samples_leaf5/10,max_features sqrt/0.5 (32 candidates). Winner R08 Cox:102 features, alpha0.1,l1_ratio0.5. CV SD is across folds, not neural seeds.

## Parameters

| Pair | Dimensions dx,dy,H | Rank | Full first bilinear incl. bias | CP incl. O bias |
|---|---|---:|---:|---:|
| MR | 32,32,128 | 8 | 131,200 | 1,664 |
| MC | 32,16,128 | 8 | 65,664 | 1,536 |
| RC | 32,16,64 | 4 | 32,832 | 512 |

- Three first bilinear layers: 229,696 → 3,712: **98.3840%** reduction.
- Entire three pair blocks including unchanged post-MLPs: 248,608 → 22,624; unchanged post-MLPs contribute 18,912.
- Total full MedicalNet pairwise:33,760,941 → full CP:33,534,957, **0.6694%** reduction.
- RC-Free retains MR/MC first interactions3,200, whole pair blocks19,968, four dynamic gates25,348 and four learnable scalars; total33,519,497. Fixed λ removes four trainable scalars, total33,519,493.
- First-layer CP changes O(Aᵀx⊙Bᵀy)+b only; A/B bias-free, original hidden-dimensional O bias retained. GELU→Dropout0.10→Linear→LayerNorm post-MLP unchanged. Ranks MR/MC/RC8/8/4; RC-Free active ranks8/8.
- No FLOPs/latency guarantee is inferred from parameter counts. Early-stop runs have different numbers of epochs and are not a controlled speed benchmark.

## Figure data policy

- performance-evolution.pdf: four protocol panels with no connected cross-panel trend: matched MRI initialization; longitudinal MRI batch6; isolated concat batch8; pairwise batch6 seed20260727. Mark repaired attention hollow/limited or omit it.
- cp-parameter-reduction.pdf: distinguish first-bilinear98.384% from whole-model0.669%; never imply98% total reduction.
- ablation-deltas.pdf: plot all six signed deltas against0.821875 baseline, no error bars (one seed).
- standardized-benchmark.pdf: five neural mean±sample SD values, three individual seed points optional. Classical post-selection metric separately tabulated.

## Exact source/archive-member map

### standardized_benchmark
- archive: `D:\KLTN\week12\phase_11_standardized_benchmark_reports_20260921.zip`
- member: `project_reports/FINAL_STANDARDIZED_VALIDATION_BENCHMARK.json`
- member_sha256: `27695f7ce4b3b06bbf3565e2958575f9636f3dd16a0591c0c91ad42df26fa32c`

### standardized_audit
- archive: `D:\KLTN\week12\phase_11_standardized_benchmark_reports_20260921.zip`
- member: `project_reports/FINAL_STANDARDIZED_BENCHMARK_AUDIT.json`
- member_sha256: `b83f6b1764b2c0b1e5c6f8cc548c935c807d1d1135e238b3b745fe6b0eea27ff`

### cp_multiseed
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `project_reports/P05B_vs_P05CP_multiseed_validation.json`
- member_sha256: `c77cffcb6549e2f7da2be4ccb045d820133da00d2584f294ab5f3c93fce3b13d`

### ablation
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `project_reports/P06_ABLATION_RESULTS.json`
- member_sha256: `26ff574d9d77d5933f0060a1eb33948fc5ba82cd32f7ea51bbd0745033d2c9ff`

### rcfree_multiseed
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `project_reports/P06_A6_NO_RC_multiseed_validation.json`
- member_sha256: `fb15006f87d73d0541926799c42f7e7a25d1c92f7654ff5ed62fba636570716b`

### fixedlambda_multiseed
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `project_reports/P06B_A6_FIXEDLAMBDA_multiseed_validation.json`
- member_sha256: `4ab9dba1775afc3795681b6b65bb9235828f17a59c2f260a55b3fd98165f246d`

### mri_initialization
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `phase_02_mri_single/reports/p02_controlled_comparison.json`
- member_sha256: `18dd2e1f779b82fa35187718b3369c927877b2e9f2d2bf56a8ec89a7c4831813`

### longitudinal_crossformer
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `phase_03x_crossformer_longitudinal/reports/p03x_vs_p03_controlled_comparison.json`
- member_sha256: `5cc0040554c914c416d6ad4ca3672b67a0afc9a5e08ed00615ed81c2a036daeb`

### concat_official
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `phase_04_concat_fusion/runs/official/p04_official_20260730T165718Z_seed20260727/final_summary.json`
- member_sha256: `e9a6aad452b111a52f098b997fb89c77ceb04e035422c4701775479d9addfe43`

### pairwise_official
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `phase_05_pairwise_fusion/runs/official/p05_official_20260731T080458Z_seed20260727/final_summary.json`
- member_sha256: `e07da2cd5218575b0a8134cf501ee16bd4e0d70eb330841f74ed588fe9dc65ad`

### classical_table
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `phase_01_tabular/reports/validation_model_comparison.csv`
- member_sha256: `5f6dedfe2b54b22e348909ce78c96c8c694ea15e818c7c3bc68d6bdf0615a567`

### cp_architecture
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `phase_05_cp/reports/p05cp_architecture.md`
- member_sha256: `e26ec5f5fbe44c2ab4133a0138e661086a1f113bb1594eb1277a9270b41cbb09`

### cp_lineage
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `phase_05_cp/reports/p05cp_lineage.md`
- member_sha256: `9180fdebf004593ef59568899519aec12d3469ce22bc2588a9843bce91c715f8`

### phase_evolution
- archive: `D:\KLTN\week12\thesis_phase_evolution_bundle_20261005_final.zip`
- member: `project_reports/THESIS_PHASE_EVOLUTION_REPORT.md`
- member_sha256: `4589ca18c01b65f08147a46ccc969c5662cec63eefebcf76a65575b88799599f`

### concat_scientific_report
- file: `D:\KLTN\project\báo cáo phase 4\Bao_cao_Phase_4_Simple_Multimodal_Fusion.md`
- file_sha256: `228ca17216ea070a261b3f6e8077044b1824b3e1b936f20c3dc7aa392d3879e8`

### longitudinal_scientific_report
- file: `D:\KLTN\project\báo cáo phase 3\Bao_cao_Phase_3_MRI_Longitudinal_TLSTM_Attention.md`
- file_sha256: `6cca79e4ea559f52cbcafac57c1d1ab47a1c280edb030f1620a01497b6d775e9`

## Available evidence limits

Raw trained checkpoint tensors and validation patient-level predictions are not included in the local thesis evidence ZIP; the numbers and hashes above come from packaged audit/result artifacts. The audit confirms agreement between available artifacts, not an independently re-executed server replay. Formal final held-out evaluation and fully matched concat-versus-pairwise repeat are remaining research work, not document-build blockers.

## Official metric implementation verification

The scikit-survival0.28.0 official [_iter_comparable source](https://github.com/sebp/scikit-survival/blob/v0.28.0/sksurv/metrics.py) was read to verify the classical tied-time caveat: event vs censored at equal time is comparable; two simultaneous events are not. The [API documentation](https://scikit-survival.readthedocs.io/en/stable/api/generated/sksurv.metrics.concordance_index_censored.html) also documents risk-tie tolerance1e-8. Accessed5October2026. No patient-level metric recomputation was performed.

## Performance-table formatting update — 6 October 2026

Performance comparison tables now bold the entire winning row by validation C-index. The three-seed benchmark uses the arithmetic mean of the original three scores, including all exact ties: RC-Free Pairwise and RC-Free Fixed-λ both have mean 0.8347222222222223 (printed 0.834722), so both rows are bold. Their sample SDs remain different and unchanged. Single-seed tables use their validation C-index. Parameter/configuration tables do not treat the largest count as better performance.

`scripts/qa_performance_tables.py` checks all five benchmark rows against `figures_source/results_data.json`, independently recomputes the mean and sample SD, and verifies whole-row bolding including ties. Independent chapter review also confirmed that the existing numerical results and model names were preserved. Internal result reports are retained as local provenance, not as bibliography references.
