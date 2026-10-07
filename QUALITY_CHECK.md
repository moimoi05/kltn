# Final thesis QA — 07/10/2026

Reviewed artifact: `Nguyen_Phuong_Nam_Thesis_RCFree_Revised.pdf`.

## Scope and document structure

- [x] Official English title matches the two English covers, both abstracts, title macro, PDF metadata and README: **Longitudinal Learning with Tensor Fusion for Predicting Progression of Alzheimer’s Disease**. The Vietnamese cover uses the equivalent title from `\ThesisTitleVN`; cover titles are uppercase.
- [x] Five chapters, with **67 total PDF pages**: 13 front matter, 47 main content and 7 bibliography. The complete document meets the 70-page ceiling.
- [x] Section5.1 is four connected paragraphs without the seven previous subheadings; Section5.2 groups six limitations into three simpler points. The figure/caption, chapter introduction and Sections5.3/5.4 are retained. An independent read-only review confirmed that the shorter text preserves essential scientific qualifications; measurements are in `provenance/discussion_revision.json`.
- [x] Each chapter has at least one figure; distribution 1/1/9/4/1, total 16. Methodology includes cohort, preprocessing, architecture evolution, full graph, full/CP, gated residual, RC-Free routes, overall pipeline and temporal model.
- [x] Experimental chronology, controlled comparisons and exploratory milestones are distinguished. Historical test scores are excluded from selection tables and charts.

## Scientific and numerical verification

- [x] CP factorizes the **bilinear interaction weight tensor**, retaining the post-MLP; it does not decompose patient observations. Dimensions and ranks match the source implementation.
- [x] RC-Free retains MRI, radiomics and clinical, identity residuals and MR/MC. The direct RC interaction and its two routes are removed; the final model has four directed gates/scales.
- [x] Input-dependent gates, unconstrained global route scales initialized 0.1, directed projections and identity paths are separately described and drawn.
- [x] Third-MRI prediction reference `p` and 18-month eligibility landmark `L` are distinct. The post-L MMSE/CDR progression proxy, retrospective ±90-day clinical matching and prospective-availability limitation are explicit.
- [x] Three-seed means/sample SDs, signed ablation deltas and parameter counts match audited reports. Core reduction is distinguished from whole-model reduction. No statistical superiority or measured speedup is invented.
- [x] Required method citations and direct formula attribution are present. Gated residual/scaling sources are described as inspiration, with the thesis adaptation stated explicitly.
- [x] **Formal held-out final evaluation has not yet been performed.** This research status is stated in the thesis; no new training or final-test run was performed during document editing.

Detailed evidence is in `provenance/LITERATURE_AUDIT.md`, `METHOD_IMPLEMENTATION_AUDIT.md`, `RESULTS_AUDIT.md`, `SCIENTIFIC_REVIEW.md` and `figures_source/results_data.json`.

## Figure style and tensor-shape verification

- [x] All text spans in 16 figure PDFs, all SVG text elements and every labeled native drawio vertex use black. Bold/emphasis and pastel fills/strokes are retained. The style regression check failed on the previous colored text and passed after correction.
- [x] Timeline, modality preprocessing and final pipeline draw volumetric MRI/3D encoders as cuboids. The CP diagram draws a third-order **weight** tensor and rank-one components, with `H×dx×dy` axes and the original efficient forward path/post-MLP.
- [x] Tables3.1/3.2/3.3/3.5 describe final MRI stage maps, phase interfaces, P10/CrossFormer internals and full RC-Free interfaces. Final MRI stem stride1 and sequential visit encoding/pooled512→stack→projection128 match P05B source and recorded MONAI1.5.2 defaults; maps are source-derived, not newly measured hooks.
- [x] The user's remote audit is attributed in `TENSOR_SHAPE_AUDIT.md` and `REMOTE_SHAPE_AUDIT_20261006.md`: P10 MRI128³/channels-last, pre-dropout GAP512, official per-seed PCA38/69/2, hidden64; CrossFormer144³/stride6, channel-first stem followed by channel-last stages. Source contracts/tests and persisted artifact widths are distinguished from forward hooks. Config/version/source commit and config hash are recorded.
- [x] Generator/renderer refactor passed syntax and direct/package-import checks, plus scene-state/export-hash equivalence. No frozen chart-data or bibliography byte changed during this follow-up.

The PDF annotation follow-up additionally checked all 16 figures: explanatory footer notes were removed from 15 figures (architecture evolution had none), with unique scientific information retained in captions. Plot axes, ticks, internal labels and marker legends remain. MR/MC labels in Figure 5.1 sit 6.36 pt above the arrow lines. Table 3.5 has a one-line caption and unbreakable rows; its 36 ordered tensor shapes are unchanged. Independent source review found no unresolved issue; details are in `provenance/pdf_comment_checks.json`.

## Bibliography and comparison-table verification

- [x] 57 unique entries, all used: 51 international journal/conference publications and 6 explicitly labeled arXiv research preprints. No internal-report or software-documentation-only bibliography entry remains.
- [x] Aghajanian et al., *Longitudinal structural MRI-based deep learning and radiomics features for predicting Alzheimer’s disease progression*, is bibliography [1] and explicitly identified as the direct methodological baseline.
- [x] CNN/C3D, LSTM/T-LSTM, Transformer/ViT/3D medical-image Transformer, Med3D and actual library roles have literature attribution. Optional prototype/backbone/background scope is qualified; no nonexistent NiBabel paper was invented.
- [x] Every winner row is bold throughout the performance tables. Benchmark selection uses the mean of three seeds and includes both tied RC-Free rows; the five benchmark scores/means/sample SDs match frozen evidence.
- [x] Reference metadata and all 57 entries' content/order match release613d74d. The renamed `thesisrefs.bst` retains the original `unsrtnat` copyright/license and changes only URL formatting: 39 DOI-bearing entries omit redundant URLs; the other 18 display full clickable URLs. Each entry retains its exact DOI/URL target in the PDF, and the full DOI/URL strings are visible. All reference links use the same blue as the table of contents.

## Build and source verification

- [x] Tectonic 0.17.0+20260731 completed the XeTeX/BibTeX build and stabilized references.
- [x] No LaTeX/BibTeX error, undefined citation/reference, duplicate label, missing image, overfull box, missing glyph or oversized float.
- [x] Three Underfull hbox messages remain (badness1057/4013/1552 in bibliography paragraphs). Their rendered pages were inspected and accepted; there is no overflow, overlap or unreadable spacing. System-font path warnings are portability notices; used PDF fonts are embedded.
- [x] No TODO/FIXME, resizebox or old experiment code as the final narrative name.
- [x] 16 native `.drawio` files and 16 SVG files parse; 16 figure PDFs are single-page vectors. Their minimum label size is 9.5 pt at the supplied 160 mm width. Figures are included at text width without shrinking tables as images.
- [x] Fonts used in extracted PDF text are embedded. No replacement glyph, unresolved `[?]` citation or text outside the page bounds was found across 68 pages.
- [x] Manuscript text matches the Trang reference's Libertinus Serif Regular/Italic and Semibold/SemiboldItalic mapping, with `newtxmath` and Latin Modern defaults. All four Libertinus faces cover the Vietnamese alphabet and accented Unicode range. TOC/list labels and all colored manuscript/link text use exact blue `#0000FF`; navigation dot leaders and page numbers remain black. Embedded figure fonts are unchanged, consistent with the reference's separate illustration fonts. Detailed checks and font checksums are in `provenance/typography_check.json`.
- [x] Checksums of 10 primary original files, including the draft ZIP/PDF and research report archives, remain unchanged.

Build logs are preserved in `provenance/build/`. Current automated findings are in `qa_report.json`; current page geometry and DOI/URL visibility/link checks are in `provenance/pdf_geometry.json` and `provenance/typography_check.json`.

## Reference cover and font-weight verification

- [x] Compared the final Trang PDF rather than relying only on the older source ZIP. All three covers retain its two frame rectangles and line widths; only the first English cover contains the UET logo. The two inner covers omit the student ID and duplicate student row.
- [x] Institutions, author, uppercase thesis title, degree and location/year are Semibold. Major/Ngành and supervisor labels are Semibold; colons, field values and supervisor names are Regular. Nam's original supervisor names are retained.
- [x] Abstracts, acknowledgements and declaration headings are centered Semibold at15.54pt. Chapter labels/titles use26.86/32.22pt; sections/subsections retain18.65/15.54pt. Body text is Regular13pt with selective structured emphasis; two isolated bold prose phrases are now regular without wording changes.
- [x] All16 figure labels and14 table labels are Regular12.95pt, matching the reference13pt setting. Bibliography entries are Regular/Italic13pt. Table headers and best-result rows, including both tied winners, remain bold. Acronym table entries/header are regular.
- [x] A4 margins match the reference (left30mm, right20mm, top20mm, bottom25mm), and the first abstract is numbered iii. TOC chapter entries/page numbers are bold; lower-level entries, leaders and list entries retain the reference weight hierarchy.

Cover comparison and frozen-input hashes are in `provenance/layout_reference_check.json`; current PDF/font and DOI/URL checks are in `provenance/typography_check.json`.

## Page-by-page visual review

- [x] All68 current pages have visual acceptance. Pages1–62 are pixel-identical to previously accepted pages; bibliography pages63–68 were reinspected at full-page scale after displaying full URLs. The comparison and frozen-input checks are in `provenance/visual_reuse_check.json`.
- [x] Covers/front matter, TOC(PDF9), Table3.5/equations(PDF42), benchmark(PDF53) and bibliography(PDF61–68) were inspected at full-page scale. Chapters1/3/4, bibliography metadata, all figure assets and chart data are byte-identical to release1a8dd18. Chapters2/5 preserve all prose and citations, with only two bold wrappers removed. Table3.5's caption and all17 rows fit without shrinking, and all36 tensor shapes are unchanged. Route labels remain parenthesized in diagrams, text, captions and equation indices, including `M + (MR→M) + (MC→M)`.
- [x] Table names and numbers are readable; main model names remain on one line where practical. Captions, margins, page numbers and section transitions are consistent.
- [x] The accepted grayscale review of CP/gate/RC-Free/pipeline drawings and all four result charts on release d254105 PDF37/39/40/41/50/52/54/56 is reused for the byte-identical figure assets. Whole-page renders have changed with the manuscript font and were separately inspected. Labels, arrows, point markers, signed values and error bars preserve meaning without relying on color.
- [x] Final pipeline and routing show all three modalities, no active RC pair and correct128/64/64→256→128→temporal→Cox dimensions. No connector crosses a box interior or clips a label.

The per-page acceptance record and final-PDF checksum are in `provenance/visual_review.json`. Rendered inspection PNGs remain in the local working directory and are not mixed into the thesis source package.

The bibliography-link PDF comment is recorded in `provenance/pdf_comment_checks.json`: entries with DOI show the DOI, the other entries show their full clickable URL, and the generic “Liên kết” label no longer appears.

## Package reproduction

- [x] ZIP extracted into a fresh directory with no previous root-level auxiliary/bibliography build files, then built using the supplied `build.ps1` and portable Tectonic with `FONTCONFIG_FILE` unset. Automatic Windows font configuration succeeded.
- [x] The extracted source passed the same automated source/build checks. All68 rebuilt pages have identical extracted text and pixel-identical renders to the visually accepted PDF.
- [x] Final ZIP CRC checked; compiled inputs are unchanged from the tested extraction. The PDF inside the ZIP is byte-identical to the PDF delivered beside it. Only QA/documentation records were finalized after the reproduction build.

See `provenance/package_build_check.json`. Rebuilt-PDF byte hashes can differ because compilation timestamps change; page text and renders were directly compared and matched.

## Research limitations retained

The endpoint proxy, retrospective cohort/clinical availability, repeated validation selection, three seeds on one split, historical test access and absence of formal final/external evaluation remain disclosed limitations. They are not unresolved formatting placeholders. See Chapter 5 and `CHANGELOG.md`.
