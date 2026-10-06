# Phase catalog — tên hiển thị, mục đích và thí nghiệm

Đây là danh sách đọc chính của project. `ID` và `Folder` là định danh kỹ thuật;
`Tên hiển thị` là tên nên dùng trong báo cáo, slide và trao đổi hằng ngày.

## Luồng nghiên cứu chính

```text
Data Audit
  → Tabular Baselines
  → MRI Only
  → Longitudinal MRI
  → Multimodal Concatenation
  → Dynamic Pairwise Fusion
  → Fusion Ablations
  → Final Test Evaluation
```

Các track CrossFormer, MedicalNet, CP-factorized, paper adaptation và benchmark
là nhánh so sánh/audit; chúng không thay đổi ID lịch sử của luồng chính.

## Danh sách phase/track

| Tên hiển thị | ID | Folder | Mục đích | Thực nghiệm chính | Trạng thái hiện tại |
|---|---|---|---|---|---|
| **Data Audit** | P00 | `phase_00_audit` | Kiểm tra dữ liệu và môi trường trước modeling. | Audit freeze, schema, outcome, split, leakage và environment; không train model. | PASS |
| **Tabular Baselines** | P01 | `phase_01_tabular` | Đo tín hiệu survival cơ bản từ clinical/radiomics. | Clinical + missingness mask và radiomics PCA (`bin32/bin64`); visit cuối vs 3 visits; Cox elastic-net và RSF. | PASS; R08 Cox validation C-index `0.860707` |
| **MRI Only** | P02 | `phase_02_mri_single` | Đo khả năng dự báo từ một MRI visit cuối. | 3D ResNet-18, visit 2; controlled `MedicalNet` vs `random initialization`; P02-C GroupNorm chỉ là optional preparation. | Có official P02-A/P02-B evidence; manifest phase còn `IN_PROGRESS` |
| **MRI Only — CrossFormer** | P02-D | `phase_02d_crossformer_single` | So sánh backbone nhẹ hơn với MRI-only ResNet. | CrossFormer3D Tiny vs P02-B ResNet-18, chỉ thay backbone, giữ input/head/protocol. | Official closure; validation best `0.764583` |
| **Longitudinal MRI** | P03 | `phase_03_mri_longitudinal` | Kiểm tra lợi ích của chuỗi 3 MRI và thời gian giữa visits. | Shared ResNet-18 → paper-style T-LSTM → Cox; thử final hidden và masked temporal attention. | T-LSTM official PASS; attention repaired run có provenance limited |
| **Longitudinal MRI — CrossFormer** | P03-X | `phase_03x_crossformer_longitudinal` | Đo ảnh hưởng của backbone CrossFormer trong bài toán longitudinal. | Thay shared ResNet bằng shared CrossFormer3D; giữ T-LSTM, attention, loss, sampler và protocol cố định. | Protocol-fixed official closure; validation best `0.725000` |
| **Multimodal Concatenation** | P04 | `phase_04_concat_fusion` | Làm baseline cộng trực tiếp ba modality. | MRI + radiomics + clinical (value/mask) → fixed concatenation → T-LSTM/attention → Cox; không có pairwise interaction. | Official evidence PASS; validation best `0.812500` |
| **Multimodal Concatenation — CrossFormer** | P04-X | `phase_04x_crossformer_concat` | Kiểm tra CrossFormer có thay đổi kết quả của simple concat không. | Giữ fusion/protocol P04, thay MRI ResNet bằng CrossFormer3D; so sánh matched với P04/P03-X. | Official closure; validation best `0.806250` |
| **Dynamic Pairwise Fusion** | P05 | `phase_05_pairwise_fusion` | Kiểm tra tương tác giữa từng cặp modality có tốt hơn concat không. | MR/MC/RC low-rank outer products, directed projections, dynamic gates, learnable lambdas, modality-centered residual, T-LSTM/attention/Cox. | Official evidence PASS; validation best `0.828125` |
| **Pairwise Fusion — MedicalNet** | P05B | `phase_05b_pairwise_medicalnet` | Đánh giá pretraining MRI trên cùng kiến trúc pairwise. | Giữ toàn bộ P05, chỉ strict-load MedicalNet cho MRI encoder và fine-tune đầy đủ; có validation multi-seed. | Official evidence PASS; 3-seed mean `0.834375` |
| **Pairwise Fusion — CP-Factorized** | P05-CP | `phase_05_cp` | Giảm kích thước pairwise bilinear mà vẫn giữ protocol. | Thay phép biến đổi pairwise đầu tiên bằng CP factorization, ranks MR/MC/RC = `8/8/4`; so sánh với P05B. | Validation multi-seed complete; mean `0.827778` |
| **Pairwise Fusion — CrossFormer** | P05-X | `phase_05x_crossformer_pairwise` | So sánh các thiết kế pairwise trên backbone CrossFormer. | XA static pairwise, XB dynamic pairwise, XC dynamic pairwise + gated residual; cùng data/protocol P04-X. | XA/XB/XC official closures; best lần lượt `0.804167/0.825000/0.830208` |
| **Fusion Ablations** | P06 | `phase_06_ablation` | Xác định thành phần nào thực sự cần trong P05-CP. | A1 bỏ dynamic gate; A2 fixed lambda; A3 bỏ identity residual; A4/A5/A6 bỏ lần lượt MR/MC/RC; A0 là full reference. | Hoàn tất cho seed `20260727`; validation-only |
| **RC-Free Fixed-Lambda** | P06B / B1 | `phase_06b_targeted` | Kiểm tra bản rút gọn A6 khi cố định lambda. | A6 bỏ RC + giữ MR/MC + 4 dynamic gates + identity residual; fixed lambda `0.1`; chạy 3 seeds. | Validation complete; mean `0.834722`; không test |
| **Final Test Evaluation** | P07 | `phase_07_final_evaluation` | Đánh giá một checkpoint đã khóa trên test đúng một lần, có ledger. | Chọn final model sau validation, khóa checkpoint/config, ghi test-use ledger và tạo prediction/metric cuối. | Scaffold `NOT_STARTED`; không gán report post-hoc bên ngoài vào P07 |
| **Paper CNN–PCA–T-LSTM Adaptation** | P10 | `phase_10_paper_cnn_tlstm_reproduction` | Có baseline tham chiếu từ kiến trúc paper, không tuyên bố exact reproduction. | CNN 3D visit 2 → embedding 3 visits → train-only PCA99 → paper T-LSTM + attention; 3 seeds. | Adaptation complete; mean validation `0.741667` |
| **Standardized Validation Benchmark** | P11 | `phase_11_standardized_benchmark` | Chuẩn hóa so sánh các run đã tồn tại, không tạo architecture mới. | Audit split/preprocessing/checkpoint/test-lock; replay/recompute validation cho P10, P05B, P05-CP, A6, B1 và giữ P01-R08 làm classical comparator. | COMPLETE; không train và không tính test metric |

## Cách gọi ngắn nên dùng

| Không nên dùng trong trao đổi | Nên dùng |
|---|---|
| Phase 1 | **Tabular Baselines** |
| Phase 2 | **MRI Only** |
| Phase 3 | **Longitudinal MRI** |
| Phase 4 | **Multimodal Concatenation** |
| Phase 5 | **Dynamic Pairwise Fusion** |
| Phase 6 | **Fusion Ablations** |
| Phase 7 | **Final Test Evaluation** |
| Phase 2D/3X/4X/5X | Gọi theo tên track CrossFormer ở bảng trên |

Khi cần truy xuất file hoặc chạy script, dùng thêm ID kỹ thuật trong ngoặc, ví dụ
`MRI Only (P02)` hoặc `Pairwise Fusion — MedicalNet (P05B)`.

## Ghi chú provenance

- Tên hiển thị không thay thế `P00–P07`, `P02-D`, `P03-X`, `P04-X`, `P05B`,
  `P05-CP`, `P05-X`, `P06B`, `P10` và `P11` trong code/checkpoint.
- Một số `phase_manifest.json` được tạo ở giai đoạn scaffold nên trạng thái của
  manifest có thể cũ hơn closure/report mới nhất. Catalog này ghi trạng thái theo
  evidence hiện có trong repository.
- Frozen data vẫn read-only; test chỉ thuộc **Final Test Evaluation (P07)**
  theo policy. Benchmark P11 chỉ dùng metadata/fingerprint và validation.
