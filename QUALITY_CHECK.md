# Thesis QA — 8 October 2026

Reviewed PDF: Nguyen_Phuong_Nam_Thesis_RCFree_Revised.pdf.

## Current document

- [x] Five chapters,66 total pages:13 front matter,46 main-content and7 bibliography;16 figures (1/1/9/4/1) and54 cited research sources.
- [x] Results/Discussion and abstracts/method/intro agree on validation-based selection of RC-Free Pairwise Fusion and post-hoc test scope. Descriptive names are used throughout the PDF; no phase/variant codes are printed.
- [x] All22 common-seed models are represented in MRI, fusion, baseline-comparison and ablation tables. C-index↑ means larger is better. Highest Val/Test cells are bold by column; both tied three-seed mean winners are bold by row.
- [x] RC-Free has common-seed validation0.841667/test0.875000; full CP has higher post-hoc test0.884470. Selection and conclusion do not claim universal test superiority or statistical stability.
- [x] Gains+0.179167 validation/+0.337121 test are against the local CNN–PCA–T-LSTM Adaptation on the same split, not the original paper's published cohort/result.

## Evidence and numerical checks

- [x] common_seed_evaluation_20261008.json/.csv accurately transcribes the user-provided remote report: seed20260727, selected epochs, Val/Test,480/528 comparable pairs and reported PASS status.
- [x] qa_common_seed_tables.py checks table coverage, scores, displayed epochs, signed gains/deltas/gaps and per-column maxima. This verifies arithmetic/transcription, not remote execution; the new report did not provide patient predictions or checkpoint/log hashes for local recomputation.
- [x] Frozen three-seed validation, all ablation/chart data and parameter counts remain unchanged. qa_performance_tables.py verifies the5 benchmark rows, exact mean/sampleSD and tied mean emphasis.
- [x] Controlled ablation changes one component relative to full CP; broader MRI→concat→pairwise milestones are kept separate because protocols differ. Fixed-λ on full CP and Fixed-λ on RC-Free are distinct named variants.
- [x] |Test−Val| is descriptive, not a stability statistic. SD across3 seeds on one split is not a confidence interval. Tests are post-hoc because the split was historically accessed; no independent final evaluation is claimed.
- [x] CP factorizes the bilinear weight tensor while retaining post-MLP. The98.384% reduction applies to the first three bilinear layers; whole-model reduction is0.669%. No measured speedup is invented.
- [x] A delegated read-only reviewer checked Chapters4/5 and abstracts; the residual-test/selection ambiguity, complete gap comparison and independent-data wording were corrected.

## Layout, references and source

- [x] All66 pages accepted:32 match the previously accepted PDF exactly in text and97.2dpi render;34 changed pages were inspected. Baseline comparison and ablation were also checked at full-page scale. Abstract keywords and the final reference fit without a separate nearly empty page.
- [x] Bìa/frame/logo/uppercase title, regular field values, Semibold labels and centered date/author signature preserve accepted formatting. Libertinus Serif Regular/Italic/Semibold, newtxmath,13pt body/caption/bibliography and A4 margins are retained. Bibliography item spacing is2.5pt to keep its last entry together.
- [x] Four Libertinus variants cover Vietnamese; all used fonts are embedded. Links/navigation are blue#0000FF, leaders and page numbers black. All16 byte-identical vector figure assets retain black text and valid PDF/SVG/drawio sources; accepted grayscale proofs remain applicable.
- [x] All54 retained reference metadata records match the previously verified bibliography. Baseline stays[1]; all37 DOI identifiers and17 full URLs are visibly printed and target the matching entries. No generic link label remains. Live-routing verification is dated7 October; this edit does not claim another network audit or permanent uptime.
- [x] Current build passes with no undefined citation/reference, LaTeX/BibTeX error, missing glyph/image, overfull box, duplicate label or oversized float. Three underfull bibliography warnings were visually inspected and accepted.
- [x] Ten original input/report files are unchanged. The package contains no raw MRI data or model checkpoint. Current evidence is in qa_report.json, provenance/artifact_checks.json, typography_check.json and visual_review.json.

## Package and Git release

- [x] Fresh ZIP extraction builds with supplied script and reproduces all66 page texts/renders.
- [x] ZIP CRC, embedded/delivered PDF identity and compiled-input hash stability pass.
- [x] Exact Git overlay, diff/whitespace/secret review and all114 indexed release-file identity checks pass before push.
