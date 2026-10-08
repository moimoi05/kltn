# Scientific and requirement review

## Current integrated review — 8 October 2026

The current artifact has 66 total pages: 13 front-matter pages, 46 main-content pages and 7 bibliography pages. All pages are accepted: 32 are pixel/text-identical to the prior accepted PDF, and 34 changed pages were inspected. All 54 retained references are cited and retain verified metadata, with 37 visible DOI identifiers and 17 full URLs targeting the matching entries. The preceding three-dimensional CP/pipeline and grayscale figure reviews remain applicable because all 16 figure assets are byte-identical.

All 16 scientific figures use black text in PDF/SVG/native drawio, with volumetric MRI and CP weight tensors drawn as cuboids. Source-derived final ResNet maps use MONAI1.5.2 stem stride1 at144³ and sequential visit processing, pooled512→stack→projection128. The earlier shape audit's wording corrections were integrated: PCA produces16, radiomics MLP produces64, and pooled512 vectors are stacked before MRI projection.

The user's remote audit provides the CNN–PCA–T-LSTM Adaptation's per-seed PCA38/69/2, pre-dropout GAP512, hidden64 and channels-last128³ CNN; CrossFormer source contracts/shape tests provide the144³/stride6 stem and its permutation to channels-last stages. These are attributed to supplied remote evidence, with exact configuration/version/hash identifiers in REMOTE_SHAPE_AUDIT_20261006.md. Neither this editor nor the remote audit claimed a new forward-hook measurement. Distinct CrossFormer fusion internals are not assigned the final ResNet bottlenecks.

All frozen chart/ablation/three-seed validation arrays and parameter counts are unchanged. The new user-reported common-seed scores are checked for transcription, arithmetic, table coverage and column-specific maximum emphasis. RC-Free is selected by validation and structural simplicity, with higher full-CP post-hoc test and lower MedicalNet validation SD stated honestly. No statistical stability or superiority is inferred from a single-seed split gap. The baseline comparison is against the local adaptation.

Current source/build/style/font/geometry/original-source checks pass. All manuscript models have descriptive names. The title/relevance/link audit is recorded in `LITERATURE_AUDIT.md` and `bibliography_verification_20261006.json`; its live-routing date remains 7 October. Fresh-package reproduction of all66 page texts/renders is recorded in `package_build_check.json`. Independent scientific review findings were resolved as documented below.

## Earlier independent reviews

Reviewed 5 October 2026. Scope was read-only review of the full user request, Chapters 1–5, English/Vietnamese abstracts, current figure-source semantics, methodology/results/literature evidence audits and `figures_source/results_data.json`. Project data and model code were not changed; no training, refit or prediction run was performed.

## Disposition

No unresolved substantive scientific or numerical accuracy issue was found in the completed chapter source. One actionable formula typo was reported: Chapter 2's routing equation used literal `sum` instead of `\sum`. The corrected source was subsequently verified. PDF rendering, table/float layout and page-by-page visual review remain separate integrated checks.

## Verified content

- **Endpoint/time semantics:** eligibility landmark is baseline + 18 calendar months; model origin is third MRI `p <= L`; duration is `(outcome_date-p)/365.25`. The score-defined post-L MMSE/CDR endpoint is qualified as a progression proxy. Conditioning on no early conversion through L is disclosed rather than represented as universally prospective prognostic validation.
- **Clinical availability:** retrospective nearest-valid ±90-day matching is stated. The 294 positive MMSE/CDR offsets are described as offsets, not patients. The thesis does not claim all clinical predictors preceded p or that split/train-only preprocessing proves strict temporal availability.
- **Implemented architecture:** CP parameterizes the first bilinear weight tensor and retains the post-MLP. MR/MC/RC input dimensions/ranks are 32×32/8, 32×16/8 and 32×16/4. Gates are input-dependent per-patient/visit/route scalars; global lambdas are unconstrained, initialized 0.1. Identity residuals use original modality embeddings without a learned identity projection. RC-Free keeps MRI, radiomics and clinical and only removes the direct RC branch and two corresponding routes. Final dimensions 128/64/64 → concat256 → readout128 → T-LSTM/attention/Cox are consistent.
- **Chronology/protocol:** concat precedes pairwise, which precedes CP and ablation/RC-Free. MRI random/pretrained labels are correctly 0.787500/0.733333. Concat physical Cox batch8 is distinguished from batch6 MRI/pairwise runs. Limited repaired-attention provenance and single-seed ablations are explicitly bounded.
- **Results/uncertainty:** all five three-seed means and sample SDs were independently recomputed from the numerical JSON; discrepancies are floating-point roundoff only. Signed ablation deltas and model/core parameter counts match the evidence. Independently calculated reductions are 98.3839509613% for first bilinear layers and 0.6693652289% for the whole model. RC-Free and Fixed-lambda means are equal. No population confidence interval, significance, universal component benefit or measured speedup is inferred from these artifacts.
- **Test policy:** historical test access is disclosed; post-hoc test scores are named in current result tables; charts remain validation-only and test is excluded from selection. The exact formal-final-evaluation status is stated honestly.
- **Literature attribution:** the two gated-residual papers are cited as inspiration rather than exact sources of the thesis formula; fixed-alpha versus learned route-scale adaptation is distinguished. The direct baseline's 228 participants and CNN/T-LSTM/attention/survival scope were additionally checked against the [official publisher article](https://link.springer.com/article/10.1186/s13195-025-01827-2).

## Integrated checks completed, 6 October 2026

The parent completed the integrated checks: all 69 final PDF pages were visually inspected, including the final pipeline, full/CP block, gate anatomy, RC-Free routing and protocol-separated charts. Every chapter has a rendered figure (1/1/9/4/1); all citations/references and image paths resolve. The PDF contains 49 main-content pages and 69 total pages, including front matter and bibliography. Physical figure fonts are at least 9.5 pt; grayscale proofs preserve the interpretation of routes and results. See `../QUALITY_CHECK.md`, `visual_review.json` and `artifact_checks.json` for the build and rendering evidence. Frozen research data were not altered and no final test evaluation was run.

## Figure visual follow-up

All 16 original-resolution PNG renders in `thesis_revision_work/figure_qa/` were visually inspected: timeline, taxonomy, cohort, modality preprocessing, architecture evolution, full pairwise graph, outer-product/CP block, gate anatomy, RC-Free routing, final pipeline, temporal model, performance evolution, parameter reduction, ablation deltas, standardized benchmark and MRI-hub topology. No substantive content error, unreadable figure text, clipped glyphs, text overlap or connector crossing a box interior was found. Topology, dimensions, gate/residual behavior, time semantics and chart numerical values match the reviewed source/evidence.

The small consistency recommendation was resolved: the CP legend now uses `H × dx × dy` and `o ⊗ a ⊗ b`, matching Chapter 3. The gated-route figure uses `E_p` for the post-MLP pair feature, consistent with the text. Integrated float placement and physical-size review are complete; no unresolved document or scientific correction remains.

## Independent bibliography/table review — 6 October 2026

The final 69-page contact sequence was visually inspected; the benchmark page and first/last bibliography pages were additionally inspected at full-page scale. Integrated build, figure/font, original-source and package reproduction evidence is recorded in `../QUALITY_CHECK.md` and the JSON QA records.

## Results rewrite review — 8 October 2026

A delegated read-only scientific reviewer checked the revised Chapters4/5 and abstracts. All common-seed numbers, gains, gaps and preserved three-seed statistics were consistent. Corrections separated the residual post-hoc test drop from validation-based selection, included all variants with smaller split gaps, and required new independent data rather than a fresh split of used participants. Descriptive naming, post-hoc scope and local-adaptation comparison boundaries were accepted. No new model execution was performed during document editing.

Final read-only review of the actual Git release diff found no remaining actionable correctness or security issue. The numerical QA script is correctly limited to document transcription/arithmetic, and the final selection, descriptive names, post-hoc test and local baseline comparison statements are consistent.
