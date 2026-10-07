# Literature audit — final bibliography revision, 6 October 2026

This record describes attribution and source verification; it is not an experimental result. The original 5 October method checks remain applicable, and 21 further publications plus the baseline metadata were checked against primary publisher/conference/preprint sources on 6 October.

## Final bibliography policy

The delivered bibliography contains **57 cited research sources**: 38 BibTeX article entries and 19 inproceedings entries. Of these, 51 are journal/conference publications and 6 are explicitly labeled arXiv research preprints. The six preprints are the two user-specified gated-residual papers, Med3D, Layer Normalization, GELU and MONAI. Their status is not converted into a peer-reviewed journal claim.

The annotated internal standardized-validation report and the phase-evolution report have both been removed from the bibliography and chapter citation calls. Their existing local result/source records remain provenance for the thesis's own data. The documentation-only scikit-survival entry was replaced by its [JMLR library paper](https://jmlr.org/papers/v21/20-729.html). The version-specific metric convention is supported separately by a footnote to the [0.28.0 implementation](https://github.com/sebp/scikit-survival/blob/v0.28.0/sksurv/metrics.py), rather than attributed to the 2020 paper.

The [Aghajanian publisher article](https://link.springer.com/article/10.1186/s13195-025-01827-2) is explicitly identified as the methodological baseline and fixed at bibliography **[1]** through `\nocite` before other citations. All 57 keys are used; no internal report, book, @misc, invented library paper or unused bibliography filler remains.

## New publications and their roles

| Citation key | Role | Primary source |
|---|---|---|
| `lecun1998gradient` | Original CNN background | [Publication](https://doi.org/10.1109/5.726791) |
| `tran2015c3d` | 3D convolutions; video-to-MRI dimensional distinction | [Publication](https://openaccess.thecvf.com/content_iccv_2015/html/Tran_Learning_Spatiotemporal_Features_ICCV_2015_paper.html) |
| `hochreiter1997lstm` | Original LSTM background | [Publication](https://doi.org/10.1162/neco.1997.9.8.1735) |
| `vaswani2017attention` | Transformer background | [Publication](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) |
| `dosovitskiy2021vit` | Original Vision Transformer background | [Publication](https://arxiv.org/abs/2010.11929) |
| `wang2022crossformer` | CrossFormer foundation; project uses a 3D adaptation | [Publication](https://arxiv.org/abs/2108.00154) |
| `hatamizadeh2022unetr` | 3D medical-image Transformer background; not an evaluated thesis model | [Publication](https://openaccess.thecvf.com/content/WACV2022/html/Hatamizadeh_UNETR_Transformers_for_3D_Medical_Image_Segmentation_WACV_2022_paper.html) |
| `paszke2019pytorch` | Actual deep-learning implementation library | [Publication](https://proceedings.neurips.cc/paper_files/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html) |
| `cardoso2022monai` | Actual MONAI ResNet implementation; explicitly labeled preprint | [Publication](https://arxiv.org/abs/2211.02701) |
| `harris2020numpy` | Array processing in project and preprocessing code | [Publication](https://doi.org/10.1038/s41586-020-2649-2) |
| `mckinney2010pandas` | Manifest and tabular-data processing | [Publication](https://doi.org/10.25080/Majora-92bf1922-00a) |
| `pedregosa2011sklearn` | Train-only scaling/PCA and classical pipeline | [Publication](https://jmlr.org/papers/v12/pedregosa11a.html) |
| `polsterl2020sksurv` | Classical survival library; version-specific metric details separately footnoted | [Publication](https://jmlr.org/papers/v21/20-729.html) |
| `monod2024torchsurv` | Optional prototype survival backend; final pairwise loss is project implementation | [Publication](https://doi.org/10.21105/joss.07341) |
| `hunter2007matplotlib` | MRI preprocessing quality-control plotting | [Publication](https://doi.org/10.1109/MCSE.2007.55) |
| `simon2011coxnet` | Regularized Cox classical baseline | [Publication](https://doi.org/10.18637/jss.v039.i05) |
| `ishwaran2008rsf` | Random survival forest baseline | [Publication](https://doi.org/10.1214/08-AOAS169) |
| `katzman2018deepsurv` | Neural Cox background | [Publication](https://doi.org/10.1186/s12874-018-0482-1) |
| `jack2008adnimri` | ADNI MRI acquisition/methods background | [Publication](https://doi.org/10.1002/jmri.21049) |
| `baltrusaitis2019multimodal` | Multimodal fusion taxonomy | [Publication](https://doi.org/10.1109/TPAMI.2018.2798607) |
| `carroll1970candecomp` | Original CANDECOMP background | [Publication](https://doi.org/10.1007/BF02310791) |

## Attribution boundaries retained

- The user-specified [Ryumina et al.](https://arxiv.org/html/2607.14702v2) motivates input-dependent residual gates, while [Liu et al.](https://arxiv.org/html/2606.11645v1) uses a fixed residual scale. The thesis's learnable, unconstrained route-specific scale and pairwise residual equation are its own adaptation.
- CNN/C3D and LSTM/T-LSTM foundations are cited where introduced. C3D's video axes are distinguished from the three spatial MRI axes. CrossFormer is cited as the foundation of the project's 3D comparator. UNETR is related background for 3D medical-image Transformers, not a claimed evaluated survival model.
- PyTorch, MONAI, NumPy, pandas, scikit-learn, scikit-survival, PyRadiomics and the relevant survival-baseline sources are linked to their actual method roles. Matplotlib is evidenced in preprocessing QC code. TorchSurv is an optional prototype backend; the final P05B-derived training objective is implemented in project code.
- NiBabel appears in actual NIfTI preprocessing code and is named in the method. Its official citation is a software release rather than a standalone journal paper, so no unrelated paper is substituted. Utility dependencies such as PyYAML/tqdm/pytest are recorded in the source inventory without padding the bibliography.
- The PCA journal metadata, Cox pages excluding discussion, Breslow 1974 ties paper, original ReLU and Adam/AdamW references are retained from the earlier audit.
- Related works distinguish survival, fixed-horizon prediction, cognitive-score regression and diagnostic classification. No ranking is inferred across incompatible study protocols.

`bibliography_verification_20261006.json` records the 57 entries, primary links, publication status and revision scope. `library_source_inventory.json` records direct code imports and requirements, excluding installed `site-packages`, virtual environments and bytecode caches. Duplicate archive/checkout hits are evidence locations, not independent executions. `literature_source_manifest.json` retains the original local-source hashes. Original research figures were redrawn rather than copied from papers.

## Exhaustive reference check — 7 October 2026

All **57** bibliography entries were checked against the primary publisher, conference or repository record and against the thesis passages that cite them. The audit confirmed the article title, author metadata, publication year/venue and DOI or canonical URL; all 57 references are cited and each supports the thesis's AD/MCI context, ADNI/MRI data, radiomics, multimodal/tensor methods, longitudinal or survival methods, model foundations, or implementation. The six arXiv items are explicitly labeled as preprints; the two gated-residual papers are described as architecture inspiration, not as clinical AD evidence. No unrelated or uncited reference remains.

The source contains 39 DOI-bearing entries and 18 entries with a direct URL but no DOI. On the audit date, all 39 DOI resolver requests returned HTTP 302 with a destination, and all 18 direct URLs returned HTTP 200. The compiled bibliography contains 87 PDF link annotations representing exactly 57 unique targets; each target matches its reference's DOI or direct URL, every target is visibly printed, and no generic “Liên kết” label remains. Some publisher landing pages respond to scripted requests with automated-access or subscription controls; that does not break DOI resolution, but it also cannot guarantee permanent uptime or free full-text access.

Metadata corrections applied after the primary-source comparison:

- [2] now includes the full Mild Cognitive Impairment guideline title and subtitle.
- [3], [5] and [45] render Clifford R. Jack's suffix as “Jr.” in the correct position. [5] also uses the verified author list, including Paul M. Thompson and the Alzheimer's Disease Neuroimaging Initiative, and removes the erroneous Jennifer Salazar name.
- [23] includes the verified proceedings pages 807–814.
- [30] uses the exact quoted “Mini-mental state” title.
- [41] places the Alzheimer's Disease Neuroimaging Initiative in the verified author order.

The current title and author output was visually inspected across bibliography pages 61–68. The PDF has 68 pages; all 57 printed DOI/URL strings are visible and clickable.
