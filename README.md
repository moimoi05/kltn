# Longitudinal Learning with Tensor Fusion for Predicting Progression of Alzheimer’s Disease

Nguyễn Phương Nam — Khóa luận cử nhân, Trí tuệ nhân tạo, UET, 2026.

Đây là bản chỉnh sửa từ source thesis ngày 05/10/2026, giữ nội dung nghiên cứu và bổ sung flow, hình vector, bảng đọc được, đối chiếu code/report và kết quả validation. Không thực hiện thêm preprocessing, training hoặc test evaluation.

Bản PDF hoàn thiện ngày 06/10/2026 có 69 trang tổng cộng, 16 hình vector và 57 tài liệu tham khảo. Gói source đã được giải nén, biên dịch độc lập bằng script đi kèm và đối chiếu toàn bộ trang với PDF đã kiểm tra trực quan. Xem `QUALITY_CHECK.md` để biết phạm vi kiểm chứng và các giới hạn nghiên cứu.

## Cấu trúc năm chương

1. Giới thiệu: vấn đề tiên lượng, mốc dự báo, research gap và năm câu hỏi nghiên cứu.
2. Cơ sở lý thuyết và nghiên cứu liên quan: survival, longitudinal modeling, modalities, fusion, CP và gated residual.
3. Phương pháp: cohort, preprocessing, evolution, full pairwise reference, CP, routes, RC-Free, temporal model và Cox objective.
4. Thực nghiệm, kết quả và phân tích: tiến trình phát triển, đối chứng CP, ablation và benchmark validation ba seed.
5. Thảo luận, kết luận và hướng phát triển: MRI như interaction hub, phạm vi bằng chứng và các bước kiểm chứng tiếp theo.

## Tệp chính

- `main.tex`: entry point; title và PDF metadata dùng một macro `\ThesisTitle`.
- `chapters/`: nội dung năm chương.
- `FrontMatter/`: bìa, tóm tắt Việt/Anh, lời cảm ơn, cam đoan, từ viết tắt.
- `references.bib`: 57 nguồn nghiên cứu quốc tế; bài baseline Aghajanian được cố định ở [1], các nguồn còn lại đánh số theo thứ tự trích dẫn.
- `image/`: logo và 16 hình PDF/SVG vector.
- `figures_source/`: 16 scene `.drawio`, source Python thống nhất, dữ liệu thật của bốn chart và provenance.
- `provenance/`: kiểm chứng literature/method/results, inventory toàn KLTN, catalog và checksum của các nguồn chính.
- `COMPILE.md`, `build.ps1`, `build.sh`, `latexmkrc`: hướng dẫn và cách biên dịch.
- `QUALITY_CHECK.md`, `qa_report.json`: kết quả QA sau biên dịch.
- `CHANGELOG.md`: thay đổi và các giới hạn nghiên cứu còn lại.

## Những phân biệt cần giữ khi chỉnh tiếp

- CP tham số hóa **tensor trọng số bilinear**; không phân rã dữ liệu bệnh nhân.
- RC-Free vẫn giữ MRI/radiomics/clinical; bỏ riêng direct RC và hai routes của nó.
- Dynamic gate là scalar theo patient–visit; λ là scale toàn cục theo route, học được và không ràng buộc dấu.
- Prediction reference `p` là MRI thứ ba; eligibility landmark `L` là baseline + 18 tháng. Endpoint sau `L` là proxy theo MMSE/CDR, duration được tính từ `p`.
- Clinical alignment hồi cứu ±90 ngày không bảo đảm mọi predictor có sẵn đúng lúc `p`.
- Milestones khác protocol không phải ablation đồng nhất. Sample SD của ba seed không phải confidence interval hay biến thiên giữa cohort.
- Không dùng historical test results để chọn architecture. Formal held-out final evaluation has not yet been performed. Lịch sử truy cập test được công bố như một giới hạn.

## References và bảng kết quả — cập nhật 06/10/2026

Danh mục có 51 bài tạp chí/hội nghị và 6 preprint arXiv được ghi rõ trạng thái. Đã bỏ hai báo cáo nội bộ và entry chỉ dẫn tới tài liệu API. CNN/CNN3D, LSTM/T-LSTM, Transformer/ViT/3D UNETR, Med3D và các thư viện thực sự có trong code đều được đối chiếu; mục thư viện ở Chương 3 nêu đúng vai trò của backend nguyên mẫu và pipeline cuối. NiBabel được mô tả trong phương pháp; không tạo một bài công bố không tồn tại chỉ để có citation.

Các bảng so sánh hiệu năng in đậm toàn bộ dòng tốt nhất theo C-index; bảng ba seed dùng mean. Hai dòng RC-Free có mean bằng nhau nên cùng in đậm. Bảng tham số/cấu hình không áp dụng quy tắc “lớn nhất là tốt nhất”. Số liệu thực nghiệm được giữ nguyên.

## Biên dịch và chỉnh hình

Xem `COMPILE.md`. Các hình PDF đã có sẵn nên không cần Python/draw.io để biên dịch LaTeX. Nếu đổi nội dung/diagram, cần kiểm tra lại số trang, font, caption, routing, source data và citation. Không đóng gói hoặc sửa dữ liệu ADNI thô.
