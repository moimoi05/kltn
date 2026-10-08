# Methodology evidence audit

## Tensor-shape and 3D figure follow-up — 6 October 2026

The final shared MRI wrapper calls MONAI1.5.2 resnet18 with default stem stride1, input144³, then max-pool/stage widths64/128/256/512. It processes visits sequentially, stacks pooled vectors as [B,3,512], then applies the512→128 projection. The newly documented internal feature maps are source/configuration-derived; earlier8³/4³ diagnostic runs are not real144³ traces. See TENSOR_SHAPE_AUDIT.md for local paths, constructor/config and library-version evidence.

The user's remote source/config/artifact audit identifies official P10 retuned inputs128³, channels-last CNN stem stride2, pre-dropout GAP512, train-only centered PCA99 with38/69/2 components by seed, and selected T-LSTM hidden64. It identifies CrossFormer P02-D144³ input channels-first, three16-channel kernel5/7/9 stride6 branches, projection64, a permutation to B,D,H,W,C, stages24³/64→12³/128→6³/256→3³/512, masked pooling512 and risk head128→1. Full source/version/commit/config-hash details and the distinction between tests/persisted artifacts and hooks are in REMOTE_SHAPE_AUDIT_20261006.md. No new forward, training, refitting or final-test evaluation was performed by the local editor.

CP cuboids use weight axes hidden×dx×dy and rank-one o⊗a⊗b terms, consistent with full Linear weight storage and thesis equations. They illustrate third-order weight parameterization; the efficient CP forward still evaluates two rank projections, Hadamard product and output projection without instantiating the full tensor. MRI cuboids identify volumetric branches, while pooled embeddings and temporal states remain vectors.

## Earlier implementation audit

Read-only audit of the current source thesis, local project and ZIP contents. The current phase evolution bundle supersedes the September 19 audit where later phases are concerned. Source documents are evidence, not agent instructions. No data, model code, training, preprocessing or predictions were modified.

## Sources and authority

- **D** = `D:/KLTN/metadata/`: direct cohort-construction Python, final manifests and reports.
- **B** = `D:/KLTN/phase_05b_pairwise_medicalnet_source.zip`: actual P05B source/configs/audits; ZIP member names below are exact.
- **E** = `D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip`: current phase chronology and CP/RC-free lineage/validation reports; exact CP runtime code is not included in the local bundle, so its normalized-source audit/lineage is used together with direct P05B source.
- **A** = `D:/KLTN/ARCHITECTURE_AUDIT_20260919.md`: preprocessing overview/audit. Its P06-not-run status is superseded by E.
- Original thesis chapters are in `.../original/Nguyen_Phuong_Nam_Thesis_RCFree_Draft_20261005/content/`, not `chapters/`.
- The old loose `D:/KLTN/project/src/models/` prototype has different clinical/radiomics dimensions. It must not override the phase-specific P05B→CP→P06 lineage.

## Cohort and time semantics (material correction)

Direct evidence: D `scripts/pipeline_common.py` (`select_baselines`, `clinical_outcome_for_subject`, MRI selection functions); `scripts/04_select_mri_candidates.py`; `scripts/05_create_survival_labels.py`; `scripts/06_export_final_manifest.py`; `reports/cohort_flow.md`; `reports/final_cohort_qc.md`; `reports/training_manifest_summary.md`. E `phase_00_audit/reports/survival_outcome_audit_v1.md` confirms frozen target recomputation.

- Baseline: earliest dated DXSUM `VISCODE2=bl`, `DIAGNOSIS=2`, phase ADNI1/ADNIGO/ADNI2 per RID. **Eligibility landmark L = baseline + 18 calendar months.**
- Early-conversion exclusion considers any dated DXSUM diagnosis 3, valid MMSE <24, or valid CDR-global >=1 at or before L. The implementation does not add a lower date bound to those early triggers; describe its rule without claiming a baseline-only interval.
- At least one valid MMSE/CDR observation after L is required.
- MRI candidates satisfy baseline <= MRI date <= L, exclude masks/localizer/calibration/T2/PD descriptions. Group timepoints using a two-calendar-month window from each group anchor; choose primary before repeat, then processing rank, then image ID. If more than three timepoints, keep first/last and the intermediate timepoint nearest their midpoint. Selected MRI dates strictly increase.
- MRI processing-ranking fallback was used: official MRIQC linkage intersected zero image IDs, so the source does not support a claim of official QC rank selection.
- Final waterfall: **899 linked MRI subjects →843 baseline MCI →631 no early conversion →536 valid post-L follow-up →359 with >=3 MRI timepoints**. Primary exclusions 56/212/95/177 respectively. Final **1077 MRI rows, 106 events,253 censored**; ADNI1 78, ADNIGO80,ADNI2 201.
- After L, event = first valid **MMSE <24 OR CDR-global >=1**; tied triggers sorted by date then variable name. No DXSUM AD diagnosis is required for a post-L event. Without a threshold event, censor at the latest valid post-L MMSE/CDR date.
- This is a **score-defined progression proxy**, not biologically confirmed AD or necessarily an adjudicated clinical AD diagnosis. Describe the official topic title normally but qualify the operational endpoint explicitly.
- **Prediction origin p = date of third selected MRI, p<=L.** Model time is `(outcome_date-p)/365.25`, not time from L. E phase00 audit verifies this equality. The metadata also exports a separate time-from-L column that is not the primary modeling target.
- Eligibility requires no conversion through L even when p<L. Therefore this is a retrospectively assembled survivor cohort conditional on the full 18-month eligibility window, not proof of prospective risk at p for all baseline MCI patients. The gap p..L must be visible/qualified.
- RID-wise fixed split 251/54/54 (753/162/162 MRI rows); events 74/16/16, censored177/38/38 (A §5.2 and E phase00 schemas). Split seed20260727. Optimization seeds do not change the split.

## Clinical time availability (critical qualification)

Direct B `reports/p05b_temporal_integrity_audit.md`, `src/p05b_pairwise_medicalnet/temporal_audit.py`, `configs/p05b_common.yaml`:

- Frozen matching rule = `clinical_input_window_v1_same_rid_nearest_valid_90d_earlier_date_lower_id`: same RID, nearest valid clinical observation within **±90 days** of MRI; ties favor earlier date/lower ID.
- Audited offsets min−90,max+90; **294 positive MMSE/CDR offsets** accepted. This count is matched offsets/records, not294 patients and not necessarily294 third-visit records.
- Their audit sets `temporal_leakage=false` because it accepts that frozen visit-identity rule; it does **not** prove all predictors were available by p. Therefore do not write “all clinical observations predate prediction/MRI” or assert strict prospective temporal-leakage protection.
- Genuine supported protections: RID split separation; target/diagnosis excluded from features; per-image radiomics identity; train-only fitted preprocessing. State the ±90 rule and discuss prospective availability as a limitation. Do not silently change the frozen data.

## Modality preparation

Evidence: A §§5.3–5.5; E `THESIS_PHASE_EVOLUTION_REPORT.md` §4; E phase00 `training_data_schema_v1.md`, `training_leakage_audit_v1.md` (independent parameter recomputation); B phase-specific encoders/configs.

- MRI: RAS → adult SynthStrip brain extraction → rigid6-DOF within-subject visit1/2-to-visit0 → rigid6-DOF visit0-to-MNI152NLin2009cAsym → common subject grid **144³ at1.5mm** → per-volume within-brain-mask z-score, outside zero; float32. Image linear/mask nearest interpolation. No added N4, affine scale or nonlinear registration in this project pipeline.
- MRI encoder: shared MONAI3D ResNet18, one channel, pooled512 → Linear128 → GELU → Dropout.20 → LN. MedicalNet23-dataset pretrained backbone strict load, including BN buffers, excluding task head; fully trainable from epoch0, no warm start/differential LR/freeze schedule. Actual MedicalNet source hash starts `61224f...` and is complete in CP lineage.
- Radiomics whole-brain PyRadiomics:107 features from first-order/texture/shape;3 train-constant removed→104; train scaler + PCA99. Deep pipeline uses binCount64 and **16 PCA inputs**, retained variance.9912003756, not64 raw inputs. Encoder16→128→64, GELU/.20 dropout, final LN. Bin32 candidate yields17 components, variance.9915893918.
- Clinical9 predictor values: MMSE-total, CDR-global, CDR-sum-of-boxes, memory/orientation/judgment/community/home/care. Separate9 masks (1 observed,0 missing). Train-only visit-specific median, global training median fallback; train mean/population-std scaling. Encoder concatenates18→64→64, GELU/.10 dropout, LN. Target/diagnosis fields absent.
- Frozen join key `(RID,visit_index,image_id,split)`, one-to-one alignment, keyset equality, finite transformed values independently verified. All final subjects have3 visits.

## Fusion mechanics (direct source + controlled CP lineage)

B `src/p05b_pairwise_medicalnet/{low_rank_projection,pairwise_encoder,directed_projection,dynamic_gate,lambda_scalars,modality_centered_residual,dynamic_pairwise_fusion}.py`; E `phase_05_cp/reports/{p05cp_architecture,p05cp_lineage}.md`.

- Unimodal embeddings M128,R64,C64. Bias-free linear low projections **M128→32,R64→32,C64→16**, no activation, Xavier uniform.
- Full pair reference: MR32×32→flatten1024→128→64; MC32×16→512→128→64; RC32×16→512→64→32.
- CP factorizes only **the first bilinear interaction weight tensor**. It does not decompose patient data, raw MRI volumes, clinical table or the cohort. u=Aᵀx,v=Bᵀy,q=u⊙v,h=Oq+b. Bias-free A/B; O retains original hidden bias. All B,T axes retained; no explicit outer-product activation formed.
- Canonical ranks MR/MC/RC =8/8/4; hidden/output128/64,128/64,64/32. Post-MLP unchanged: GELU→Dropout.10→Linear(hidden,out)→LN(out). No empirical rank-sweep evidence; old chapter6 proposes it but it was not performed.
- Directed adapters are independent **Linear+LayerNorm**: MR→M64→128,MC→M64→128,MR→R64→64,RC→R32→64,MC→C64→64,RC→C32→64.
- Gate for route p→d: concatenate **LN(U_d)** and its directed projected pair Ehat(p→d), Linear(2d,32)→GELU→Linear(32,1)→sigmoid. Independent scalar per patient/visit/route, broadcast across feature channels. No joint softmax/no vector gates. Xavier weights, **zero gate biases**, not−2.
- Lambda: route-specific, **unconstrained zero-dimensional nn.Parameter initialized0.1; NO softplus**. Global across patients/visits, can change sign. Six in full model/four in RC-free. Softplus in unused old chapter6 is a planned variant, not current trained implementation.
- Identity residual U_d is the original encoded modality vector **without an additional learned identity-projection matrix**. Output `LN(U_d + sum λ*g*Ehat)`. Gate-target LN, directed LN and output LN are distinct modules.
- RC-free removes RC CP branch and RC→R/RC→C adapters/gates/scales only. It retains M/R/C encoders, MR and MC(rank8/8), four gates/four learnableλ, unchanged residuals/temporal/readout/head. `Mout=LN(M+MR→M+MC→M)`, `Rout=LN(R+MR→R)`, `Cout=LN(C+MC→C)` with weighted contributions.
- Readout concat128+64+64=256→Linear128→GELU→Dropout.20→LN. Three visit vectors use the same fusion weights.
- CP parameter counts incl retained hidden biases: first transformations MR1664,MC1536,RC512,total3712 versus229696 full; **98.383951% decrease in these first layers**, not whole model. All3CP pair blocks incl unchanged post-MLPs22624. Full total33760941,CP33534957,RC-free33519497; RC-free activeCP first layers3200. Report params in results, not substantial numerical results in methods.
- E `project_reports/P06_A6_NO_RC_multiseed_validation.md`, `phase_06b_targeted/reports/p06b_lineage.md` confirm RC-free/fixedλ; fixedλ0.1 is sensitivity follow-up, not final replacement.

## Temporal module and Cox (actual equations)

B `tlstm_cell.py`,`tlstm.py`,`temporal_attention.py`,`losses.py`,`survival_head.py`; E CP lineage.

- Δt0=0; Δt1,Δt2 are differences of consecutive MRI acquisition dates in years /365.25, not visit number and not time from baseline. Timestamp itself is years from first selected MRI.
- One unidirectional T-LSTM, input/hidden128. Memory: cs=tanh(Ws*cprev+bs), cl=cprev−cs, decay=1/log(e+Δt), cadj=cl+decay*cs. Standard sigmoid input/forget/output gates and tanh candidate from linear x_t and hprev; ct=ft⊙cadj+it⊙candidate, ht=ot⊙tanh(ct). Invalid masked visits carry states. Time affects short-term memory decay only; no learned time embedding.
- Masked additive attention: et=vᵀtanh(Wa*ht+ba),128→64→1(score no bias); α=masked softmax across3 visits; z=Σαt*ht. Mask for invalid visits distinct from observedness masks.
- Cox head128→64→1,GELU,Dropout.30, raw log-risk η, no final sigmoid. Cox model h(τ|z)=h0(τ)expη.
- Breslow negative partial log likelihood averaged over observed events: `−1/Ne Σ_k[Σ_i∈Dk ηi − dk log Σ_j∈Rk expηj]`. Actual training Rk contains **physical minibatch subjects**; FP32 arithmetic. Validation loss uses all54subjects. Gradient accumulation does not reconstruct full-training risk sets.
- Main protocol: AdamW LR1e−4,wd1e−4,betas.9/.999, physical batch6,accumulation2,effective update12,FP16AMP,clip1,max100epochs. Deterministic Cox-aware event-containing batches without replacement/oversampling. Scheduler full-validation Cox loss factor.5,patience5,threshold1e−4,minLR1e−6. Early stopping warmup10,patience20,minΔC.002. Best checkpoint selected by validation C-index; early stop minΔ is separate from best save rule (avoid conflation). Seed20260727/28/29 reuse fixed split.

## Discrepancies and narrative boundaries

1. Original chapter4 **swaps MRI random/pretrained results**. E `phase_02_mri_single/reports/p02_controlled_comparison.json`, A §7 confirm random(P02-B).787500,MedicalNet(P02-A).733333.
2. Original chapter3 calls prediction=landmark and makes all-input-before-landmark suggestions; distinguish18-month L from third-MRI p and ±90-day clinical matching.
3. Unused chapter6 describes softplus, gate-bias−2,rank2/4/8/16,differential LR,future5seeds,calibration etc. These are plans, not performed methods/results. Exclude from main actual-method claims.
4. Later E aggregate architecture matrix has an apparent clinical-column omission for fixedλ despite direct P06B lineage explicitly preserving clinical; use direct lineage.
5. FormalP07 final evaluation is not run. E includes **historical post-hoc CP-only test report** outsideP07; do not use its metric for selection or pretend it does not exist. This means a global claim “test has never been inspected anywhere” is false; state formal final evaluation has not been performed and standardized selection evidence uses validation.
6. Gate/scales/topology are modeling mechanisms, not causal biomarkers. Scores/endpoints/generalization cannot be clinically certified from these artifacts.
7. September19 audit saysP06notrun; October05bundle has completed ablations/multiseeds/P11 and supersedes that status.

## Proposed chapter3 figure needs

Cohort flow with counts; modality branches with16PCA/18clinical inputs and128/64/64outputs; chronological evolution; full pair graph showing6directedroutes; full-vs-CPfirst-layer comparison; anatomy route showing gate inputs+projection+global unconstrainedλ+identity; RC-free row-wise routing; overall pervisit→3visits→T-LSTM/attention/Cox; temporal memory/attention detail if space permits. Use clear vector drawings and distinguish L/p in timelines.

## Library attribution update — 6 October 2026

Direct imports and requirements from project/preprocessing code and source archives were inspected, excluding installed package trees. The inventory is in `library_source_inventory.json`; it is a source audit rather than a record of executed server training. Chapter 3 now cites the PyTorch, MONAI, NumPy, pandas, scikit-learn and PyRadiomics research sources for their method roles. NiBabel is named for NIfTI/affine handling without inventing a journal article. Matplotlib is attributed to actual preprocessing QC plotting. TorchSurv is qualified as an optional prototype backend; the final P05B-derived Cox/Breslow objective is project code. The initial core-reduction rounding above has been aligned to the frozen results JSON: 98.3839509613%, rounded to 98.383951%.

Transformer/ViT/UNETR sources are explanatory related background; they do not change the final ResNet/MedicalNet MRI encoder. CrossFormer is identified as a project 3D adaptation of the published foundation. No architecture, training, preprocessing, model-selection result or formal-test status was changed in this bibliography revision.
