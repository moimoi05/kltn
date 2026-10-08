# Longitudinal Learning with Tensor Fusion for Predicting Progression of Alzheimer’s Disease

Nguyễn Phương Nam — Khóa luận cử nhân, Trí tuệ nhân tạo, UET, 2026.

Bản chỉnh sửa ngày08/10/2026 trình bày RC-Free Pairwise Fusion là kiến trúc chính, với bảng validation/test cùng seed20260727, ablation từng thành phần và benchmark validation ba seed. Mọi mô hình trong PDF dùng tên dễ nhận biết. Biên tập tài liệu không chạy lại mô hình hay thay đổi dữ liệu ADNI.

## Kết quả và phạm vi bằng chứng

RC-Free đạt validation0,841667 và test hậu nghiệm0,875000 ở seed20260727; mean validation ba seed là0,834722±0,023693. Mô hình được chọn theo validation và cấu trúc gọn. CP đầy đủ có test hậu nghiệm cao hơn; chênh lệch test–validation không chứng minh độ ổn định. Bảng tăng C-index so với CNN–PCA–T-LSTM là so với bản adaptation trên cohort hiện tại.

Các số test do người dùng cung cấp từ báo cáo Codex trên máy chủ được lưu trong provenance/common_seed_evaluation_20261008.json/.csv. Chúng đã được kiểm tra về chép số, tính chênh lệch, mức tăng và in đậm theo cột; chưa tái tính từ dự đoán từng người tại môi trường biên tập. Test từng được truy cập nên các điểm này là hậu nghiệm, không phải đánh giá độc lập cuối cùng. Benchmark nhiều seed giữ nguyên nguồn validation đóng băng cũ.

## Cấu trúc và tệp chính

Năm chương gồm giới thiệu; cơ sở lý thuyết và nghiên cứu liên quan; phương pháp; thực nghiệm/kết quả/ablation; thảo luận/kết luận/hướng phát triển. PDF có66 trang,16 hình vector và54 tài liệu tham khảo được trích dẫn, gồm48 bài tạp chí/hội nghị và6 preprint được ghi rõ. Bài baseline Aghajanian ở[1].

- main.tex và chapters/, FrontMatter/: nguồn LaTeX.
- references.bib và thesisrefs.bst: metadata đã kiểm chứng;37 mục hiển thị DOI và17 mục hiển thị URL đầy đủ.
- image/ và figures_source/:16 bộ PDF/SVG/drawio; bốn chart giữ validation và số tham số từ báo cáo đã đóng băng.
- provenance/: nguồn số liệu, audit khoa học, font/link, kiểm tra từng trang và build gói độc lập.
- scripts/qa_thesis.py: kiểm tra source/build, kết quả, ablation và hình.
- build.ps1, build.sh, COMPILE.md: cách biên dịch từ gói sạch.
- QUALITY_CHECK.md, qa_report.json, CHANGELOG.md: phạm vi QA và thay đổi.

## Trình bày và phương pháp

Bìa, chữ đậm/chữ thường và font theo bản cuối của Nguyễn Phương Trang; bìa không ghi mã sinh viên. Nội dung dùng Libertinus Serif, chữ đậm Semibold và newtxmath; caption/bibliography13pt thường. Liên kết/mục lục xanh#0000FF, leaders và số trang đen. Các bảng một seed in đậm ô C-index cao nhất từng cột, benchmark ba seed in đậm cả hai dòng đồng hạng theo mean. Mũi tên↑ nghĩa là chỉ số càng cao càng tốt.

CP tham số hóa tensor trọng số, không phân rã dữ liệu người bệnh; lợi ích98,384% chỉ áp dụng ba lớp song tuyến đầu tiên, còn toàn mạng giảm0,669%. RC-Free giữ cả ba encoder, chỉ bỏ pair RC và hai route. Gate phụ thuộc đầu vào;λ là scale học được theo route. Prediction reference p là MRI thứ ba và eligibility landmark L là baseline+18 tháng; endpoint MMSE/CDR và ghép ngày hồi cứu có giới hạn tiến cứu. Ba seed chung split không phải ba cohort độc lập; SD không phải khoảng tin cậy.

Xem QUALITY_CHECK.md để biết trạng thái PDF và kiểm chứng gói. Các hình đã có sẵn nên không cần công cụ dựng hình để biên dịch. Gói không chứa dữ liệu MRI thô hay checkpoint mô hình.
