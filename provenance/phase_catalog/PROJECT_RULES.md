# Project Rules

1. `data_alzheimer` is read-only.
2. Do not rerun preprocessing.
3. Do not modify MRI, radiomics, clinical, split, manifest, or freeze data.
4. Do not import code between phases.
5. Do not create a shared runtime package between phases.
6. Code may only be copied as a snapshot/fork with provenance.
7. Cross-phase handoff is only by artifacts with a checksum.
8. Each phase may write only inside its own directory.
9. Do not overwrite previous runs.
10. Do not use test data for tuning.
11. Only `Final Test Evaluation (P07)` may perform final test evaluation.
12. Every phase requires its own `/goal` before implementation.
13. This scaffold does not mean any phase has passed.
14. Do not use ambiguous names such as `final_model_new`, `best2`, `model_v3`, or `test_new`.
15. Internal versioning remains stable: core phases use P00–P07; comparison
    tracks use IDs such as P02D, P03X, P04X, P05B, P05-CP, P05X, P06B, P10
    and P11; baselines/models use B0–B8; ablations use A_DATA, A_TEMPORAL,
    A_FUSION, A_MODALITY; representations use Rxx; and run IDs use timestamp +
    seed + config hash. Human-facing documents should use the descriptive names
    in `PHASE_CATALOG.md`, with the internal ID in parentheses when a file or
    artifact must be traced.
