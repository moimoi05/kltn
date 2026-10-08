# CHANGELOG — 05–08/10/2026

## Hoàn thiện Lời cảm ơn — 08/10/2026

- Viết lại lời cảm ơn theo giọng trang trọng, ấm áp; ghi đúng GS. TS. Nguyễn Linh Trung và Thượng tá, TS. Nguyễn Thành Trung, Phó Chủ nhiệm Khoa Trang bị, Bệnh viện 108.
- Cảm ơn Cử nhân Nguyễn Phương Trang đã hỗ trợ, hướng dẫn và trao đổi; cảm ơn Sepehr Aghajanian đã hồi đáp email về bài báo nền tảng; ghi nhận Lab Avitech đã hỗ trợ tài nguyên máy chủ cho huấn luyện mô hình.
- Giữ lời cảm ơn các thầy cô, những người đóng góp cho ADNI và gia đình. Không đưa địa chỉ email hay nội dung thư riêng vào khóa luận.
- Build đạt 68 trang; chỉ trang 6 thay đổi so với bản phát hành trước và đã được kiểm tra trực quan. 67 trang còn lại giống nhau cả phần chữ lẫn ảnh raster ở mức 97,2 dpi. ZIP giải nén mới được biên dịch độc lập, qua automated QA và tái tạo chính xác text/render của cả 68 trang.


## Rà soát toàn bộ tài liệu tham khảo — 07/10/2026

- Đối chiếu đủ 57 mục với nguồn xuất bản/kho lưu trữ chính thức và ngữ cảnh trích dẫn trong khóa luận; xác nhận tên, tác giả, năm, nơi xuất bản và mức độ liên quan. Cả 57 mục đều được trích dẫn và hỗ trợ nội dung nghiên cứu.
- Sửa metadata đã phát hiện: bổ sung đầy đủ tiêu đề hướng dẫn Petersen; sửa thứ tự/tên tác giả Weiner và hậu tố Clifford R. Jack, Jr.; chuẩn hóa tiêu đề Folstein; bổ sung trang 807–814 cho Nair; sửa thứ tự nhóm ADNI trong Ding.
- Kiểm tra live: 39/39 DOI chuyển hướng HTTP302 tới trang xuất bản, 18/18 URL trực tiếp trả HTTP200. PDF có 57 đích nhúng khớp 57 tài liệu; mọi DOI/URL đều được in rõ và bấm được, không còn nhãn “Liên kết”.
- Dựng lại PDF 68 trang và duyệt trực quan các trang tài liệu tham khảo 61–68. Link được xác minh tại ngày kiểm tra; khả năng truy cập toàn văn vẫn tùy chính sách/trả phí của nhà xuất bản.

## Hiện DOI và URL đầy đủ trong tài liệu tham khảo — 07/10/2026

- Theo góp ý PDF, 39 tài liệu có DOI tiếp tục hiện mã DOI; 18 tài liệu không có DOI nay hiện URL đầy đủ, bấm được thay cho nhãn “Liên kết”.
- Giữ nguyên nội dung, thứ tự, metadata BibTeX và đích của cả 57 tài liệu. Build/QA đạt; PDF có 68 trang, trong đó bibliography tăng từ 7 lên 8 trang do URL hiển thị đầy đủ.

## Bìa và chữ đậm/chữ thường theo mẫu Trang — 07/10/2026

- Đối chiếu PDF cuối và source Nguyễn Phương Trang. Giữ khung kép ở cả ba bìa; logo chỉ ở bìa tiếng Anh đầu tiên. Bỏ dòng mã sinh viên và dòng sinh viên lặp; giữ tên tác giả và tên giảng viên gốc.
- Viết hoa tên đề tài; bìa tiếng Việt dùng bản dịch tương ứng. Chỉ in đậm nhãn Major/Ngành/Supervisor, còn dấu hai chấm, ngành và tên giảng viên dùng Regular; tên trường, tác giả, đề tài, loại khóa luận và năm dùng Semibold.
- Căn giữa tiêu đề hai tóm tắt, cảm ơn và cam đoan; khớp cỡ tiêu đề chương, lề A4 và số La Mã iii của trang tóm tắt. Caption hình/bảng và bibliography dùng Regular13pt; đầu bảng, nhãn cấu trúc và mọi dòng kết quả tốt nhất vẫn đậm.
- Bỏ hai wrapper in đậm trong câu văn Chương2/5, giữ nguyên từng từ và citation. Chapters1/3/4, 57 references, số liệu, 16 hình và source hình không đổi byte.
- PDF vẫn67 trang:13 mở đầu,47 nội dung chính,7 tài liệu tham khảo. Đã duyệt riêng từng trang; QA nguồn/build/font/glyph/link/geometry, bìa và trọng số chữ đều pass. Bằng chứng hiện hành ở `provenance/layout_reference_check.json`, `visual_review.json` và `typography_check.json`.

- Gói source giải nén mới biên dịch độc lập và tái tạo text/render cả67 trang; QA, CRC và checksum PDF trong ZIP được kiểm tra trước khi đồng bộ GitHub.

## Font, mục lục và link tham khảo theo bản Trang — 06/10/2026

- Đối chiếu PDF và source khóa luận Nguyễn Phương Trang; đổi font nội dung sang Libertinus Serif Regular/Italic, Semibold/SemiboldItalic cho chữ đậm, dùng `newtxmath` và Latin Modern cho sans-serif/monospace. Chọn OTF từ TeX distribution; không cần cài font hệ thống. Cả bốn font variant hỗ trợ đầy đủ dấu tiếng Việt và PDF không có missing glyph.
- Mục lục, danh mục hình/bảng và mọi link cùng màu xanh thuần `#0000FF`. Dấu chấm dẫn, số trang và toàn bộ chữ trong hình giữ màu đen.
- Thêm `thesisrefs.bst`, đổi tên từ `unsrtnat` và giữ copyright/license gốc. Rút gọn link hiển thị: 39 mục có DOI bỏ URL trùng; 18 mục còn lại dùng nhãn “Liên kết”. Giữ nguyên byte của `references.bib`, toàn bộ nội dung/thứ tự 57 tài liệu và địa chỉ đích PDF; baseline vẫn là [1].
- Thêm float barrier trước Bảng3.5 để bảng vừa trang sau đổi font; giữ một dòng cho caption và mỗi bước, đủ36 shape. Chapters1/2/4/5, front matter, dữ liệu, hình và source hình không đổi byte. Không chạy thêm training/evaluation.
- Bản cuối67 trang:13 front matter,48 nội dung chính và6 bibliography. Duyệt lại cả67 trang sau đổi font, kiểm tra riêng PDF9/43/62. Font/color/link-target QA và reviewer độc lập đều pass; bằng chứng ở `provenance/typography_check.json`.
- Gói source giải nén mới tái tạo text/render cả67 trang; kiểm tra CRC, checksum PDF và compiled inputs trước khi cập nhật GitHub.

## Rút gọn mục 5.1 và 5.2 — 06/10/2026

- Gộp mục 5.1 thành bốn đoạn thảo luận liền mạch, bỏ bảy tiểu mục. Rút khoảng 71% số từ theo phép đếm khoảng trắng có tính cả LaTeX và caption; giữ Hình 5.1 cùng chú thích.
- Gộp sáu ý ở mục 5.2 thành ba nhóm: dữ liệu/thời điểm dự báo, độ chắc chắn của kết quả, kiểm chứng trên dữ liệu mới/hiệu quả triển khai. Viết lại bằng câu ngắn và từ dễ hiểu hơn; giảm khoảng 30% số từ.
- Giữ nguyên phần mở đầu Chương 5, mục 5.3/5.4, bốn chương trước, 57 references, hình và số liệu. Reviewer độc lập xác nhận các giới hạn khoa học cần thiết vẫn được nêu đầy đủ.
- PDF còn 67 trang: 13 front matter, 47 nội dung chính và 7 bibliography. Kiểm tra 12 trang thay đổi; 55 trang còn lại có render giống hệt bản đã duyệt. Mục lục và danh mục hình đã cập nhật số trang.
- Gói source giải nén mới biên dịch thành công và tái tạo text/render cả 67 trang. QA, CRC và checksum PDF trong ZIP được kiểm tra trước khi đồng bộ GitHub.

## Chỉnh theo ba comment PDF — 06/10/2026

- Hạ nhãn MR/MC sát các mũi tên trong Hình 5.1; khoảng cách từ đáy chữ đến mũi tên còn khoảng 6,36 pt. Thu gọn khoảng trắng của hình.
- Bảng 3.5 dùng hai cột không ngắt dòng; caption và mỗi bước đều nằm trên một dòng, giữ nguyên 36 biểu thức shape và cỡ chữ đọc được.
- Rà đủ 16 hình, bỏ các ghi chú diễn giải ở chân 15 hình; hình evolution vốn không có footer. Thông tin riêng được chuyển vào caption, nội dung trùng được bỏ; trục, giá trị, nhãn nội bộ và marker legends vẫn đầy đủ.
- Kiểm tra trực quan 29 trang thay đổi, tái sử dụng 41 trang có render giống hệt bản đã duyệt; kiểm tra riêng PDF37/41/42/52/54/60 và tám trang thang xám. Bản cuối vẫn 70 trang, toàn bộ chữ trong hình màu đen.
- Reviewer độc lập đối chiếu source với commit d8b7b1c; bibliography và dữ liệu chart đóng băng không đổi byte. Không phát hiện lỗi còn lại.
- ZIP giải nén mới biên dịch thành công bằng script đi kèm; cả 70 trang có text và render giống hệt PDF đã duyệt. Gói source và PDF được kiểm tra CRC/checksum trước khi đồng bộ GitHub.

## Chữ đen, khối 3D và bảng shape — 06/10/2026

- Chuyển toàn bộ chữ của 16 hình sang đen trong PDF, SVG và native drawio; giữ bold/emphasis và màu pastel cho nền/đường nét. Kiểm tra tự động đã phát hiện lỗi trước sửa và pass sau sửa.
- Vẽ MRI/3D encoder bằng khối hộp trong timeline, modality preprocessing và pipeline cuối. Hình CP vẽ tensor trọng số `H×dx×dy` và tổng các tensor rank-one; không vẽ dữ liệu bệnh nhân như đối tượng bị phân rã, không thêm phép dựng tensor/outer-product vào forward CP.
- Bổ sung Bảng 3.1 shape shared MRI encoder, Bảng 3.2 giao diện phase, Bảng 3.3 Paper CNN–PCA–T-LSTM/CrossFormer3D; mở rộng Bảng 3.5 toàn pipeline cuối. Không dùng resizebox hay ảnh chụp bảng.
- Xác minh MRI cuối từ wrapper P05B/config và MONAI1.5.2: input144³, stem stride1, CNN xử lý lần lượt ba visits, stack pooled512 rồi projection128. Shape feature maps là source-derived, không gán log smoke8³/4³ thành trace MRI thật.
- Tích hợp audit từ máy giữ code do người dùng cung cấp: P10 official retuned lấy pre-dropout GAP512, PCA train-only38/69/2 theo seed20260727/28/29, hidden64; CrossFormer stem stride6 và trục channels-last xuyên các stages. Ghi version/commit/config hash và phân biệt source contracts/tests/persisted artifacts với forward hooks trong provenance.
- Tách renderer dùng chung sang `figures_source/scene_renderer.py`; 49 asset/provenance đã duyệt không đổi byte do refactor. Giữ native cuboid stencil editable trong drawio và PDF/SVG vector.
- Bản cuối70 trang:13 front matter,50 nội dung chính,7 bibliography. Giữ57 references, baseline[1], các route trong ngoặc và in đậm winner theo mean; không đổi số liệu thực nghiệm, không training/refit/test.
- Duyệt toàn bộ trang, kiểm tra riêng bảng shape và hình CP/pipeline, chấp nhận tám trang thang xám. ZIP giải nén mới biên dịch độc lập và tái tạo nội dung/ảnh render cả70 trang; CRC và checksum nguồn đóng băng đều pass.

## Mở rộng references và in đậm kết quả — 06/10/2026

- Bỏ hai báo cáo nội bộ khỏi bibliography theo góp ý PDF; kết quả tự nghiên cứu vẫn được dẫn về bảng/phụ lục provenance của source.
- Cố định [1] là Aghajanian et al., *Longitudinal structural MRI-based deep learning and radiomics features for predicting Alzheimer’s disease progression*, baseline trực tiếp để phát triển phương pháp.
- Danh mục cuối có 57 nguồn được trích dẫn: 51 bài tạp chí/hội nghị quốc tế và 6 preprint arXiv ghi rõ trạng thái. Thêm 21 nguồn cho CNN/C3D, LSTM, Transformer/ViT/UNETR/CrossFormer, multimodal/CP, ADNI MRI, neural Cox/Cox-EN/RSF và các thư viện PyTorch, MONAI, NumPy, pandas, scikit-learn, scikit-survival, TorchSurv, Matplotlib.
- Thay bibliography entry tài liệu metric bằng bài JMLR về scikit-survival; chi tiết triển khai 0.28.0 được dẫn bằng footnote tới source cố định theo version.
- Rà soát import/requirements thực tế, loại thư viện cài sẵn trong môi trường khỏi bằng chứng sử dụng. Chương 3 bổ sung mô tả vai trò thư viện; phân biệt TorchSurv nguyên mẫu với Cox/Breslow tự triển khai trong mô hình cuối.
- Chương 2 bổ sung nền tảng Transformer/ViT và ảnh 3D, phân biệt UNETR segmentation với survival task và CrossFormer gốc với bản 3D của project.
- In đậm toàn dòng tốt nhất trong các bảng so sánh hiệu năng. Benchmark dùng mean của ba seed và in đậm cả hai dòng đồng hạng; giữ nguyên score và sample SD.
- Giữ ký hiệu route trong ngoặc. Phiên bản sau cập nhật references có 69 trang: 13 front matter, 49 nội dung chính và 7 bibliography; 16 hình vector. Biên dịch ổn định, không thiếu citation/reference hoặc tràn lề; tất cả 69 trang của phiên bản đó đã được kiểm tra trực quan.

## Cập nhật ký hiệu route — 06/10/2026

- Theo yêu cầu bổ sung, đặt ngoặc quanh các directed route: `(MR→M)`, `(MR→R)`, `(MC→M)`, `(MC→C)`, `(RC→R)` và `(RC→C)`.
- Đồng bộ trong bốn hình full pairwise, gated route, RC-Free routing và overall pipeline; cập nhật cả PDF/SVG/drawio và source sinh hình.
- Công thức, nội dung và caption dùng ký hiệu route tương ứng trong ngoặc; phần cộng trong hình kiến trúc trở thành `M + (MR→M) + (MC→M)`.
- Giữ nguyên mô hình và số liệu; biên dịch lại bản65 trang, kiểm tra bảy trang thay đổi và cập nhật gói source/PDF.

## Tiêu đề và front matter

- Đổi bìa, title pages, macro title, metadata/hyperref, hai abstract và README sang **Longitudinal Learning with Tensor Fusion for Predicting Progression of Alzheimer’s Disease**.
- Giữ thông tin sinh viên, ngành và giảng viên từ source gốc; dùng mẫu khóa luận Nguyễn Phương Trang để đối chiếu cấu trúc bìa và trình bày.
- Xóa trạng thái cũ cho rằng chưa có chương kết quả; cập nhật abstract và cam đoan theo phạm vi validation hiện có.

## Cấu trúc và câu chuyện nghiên cứu

- Giữ năm chương; README cũ ghi sáu chương nhưng `main.tex` thực sự include năm chương. Chương 6 cũ chứa các kế hoạch chưa thực hiện nên không chuyển chúng thành phương pháp/kết quả đã chạy.
- Dẫn từ MRI Only → Longitudinal MRI → Multimodal Concatenation → Dynamic Pairwise Fusion → CP-Factorized Pairwise Fusion → fusion ablation → RC-Free Pairwise Fusion.
- Bổ sung phân biệt research question, hypothesis, controlled comparison và exploratory milestone. Không mô tả CP hoặc RC-Free như lựa chọn đã có từ đầu.
- Dùng tên mô hình mô tả; mã experiment cũ chỉ xuất hiện trong provenance/các báo cáo nguồn.

## Sửa nội dung theo code và báo cáo

- Phân biệt `p=s3` với `L=baseline+18 calendar months`; survival duration tính từ MRI thứ ba nhưng cohort cần không chuyển đổi qua `L`.
- Xác định endpoint thật là ngưỡng MMSE<24 hoặc CDR-global≥1 sau landmark; không mô tả như AD diagnosis đã được thẩm định.
- Nêu clinical nearest-valid ±90 ngày và 294 offsets MMSE/CDR dương đã chấp nhận; không đổi dữ liệu đóng băng hoặc tuyên bố toàn bộ đầu vào có sẵn tại `p`.
- Sửa λ thành scalar học trực tiếp, init0.1, không softplus; identity residual giữ embedding gốc, không có learned identity projection.
- Nêu CP chỉ thay bilinear first layer; bias/output shape/post-MLP được giữ; ranks MR/MC/RC=8/8/4, kiến trúc cuối giữ MR/MC=8/8.
- Làm rõ physical-minibatch Cox risk sets, gradient accumulation, raw log-risk và khác biệt clinical masks/visit masks.
- Sửa nhãn MRI initialization bị đảo trong bản cũ: MedicalNet0.733333, random0.787500.
- Phân biệt concat Cox batch8 với các phase ResNet batch6; không quy mọi delta lịch sử chỉ cho modality/fusion.
- Tính sample SD chính xác; hai RC-Free variants có mean bằng nhau. Tách classical baseline do validation selection và tied-time concordance khác.
- Báo parameter reduction đúng phạm vi: 98.383951% first-layer interaction core, khoảng0.669365% toàn mô hình full→CP.
- Bỏ historical test metrics khỏi các bảng/chart và narrative selection; công bố lịch sử test và trạng thái formal final evaluation chưa chạy.

## Hình và source tham chiếu

Mỗi chương có hình; Methodology chứa nhiều sơ đồ chi tiết nhất. Toàn bộ hình nghiên cứu được dựng mới dưới dạng vector PDF/SVG, giữ editable `.drawio` cho các schematic. Style pastel nhất quán, ký hiệu/chữ vẫn phân biệt khi in grayscale. Không sao chép figure có copyright từ paper.

| New figure | Nội dung |
|---|---|
| mci-progression-timeline.pdf | Ba MRI, prediction reference, eligibility landmark, event/censor |
| fusion-taxonomy.pdf | Các chiến lược fusion và logic dẫn tới framework |
| cohort-construction.pdf | Cohort waterfall899→843→631→536→359 và split |
| modality-preprocessing.pdf | MRI/radiomics/clinical branches và dimensions |
| architecture-evolution.pdf | Tiến trình xây dựng model |
| full-pairwise-graph.pdf | Full reference3pairs/6routes |
| outer-vs-cp.pdf | Full first bilinear layer so với CP weight parameterization |
| gated-residual-route.pdf | Projection, gate, global λ, identity và LayerNorm |
| rc-free-routing.pdf | Ba hàng output và4routes còn hoạt động |
| final-pipeline.pdf | Main architecture: per-visit fusion→threevisits→T-LSTM→attention→Cox |
| temporal-model.pdf | Khoảng visit, hidden states, attention và rawrisk |
| performance-evolution.pdf | Milestones tách theo protocol |
| cp-parameter-reduction.pdf | Interactioncore, fullblocks và wholemodel phạm vi riêng |
| ablation-deltas.pdf | Sáu thay đổi so với fullCP, một seed |
| standardized-benchmark.pdf | Ba seed, mean/sampleSD |
| mri-hub-topology.pdf | MRI-hub giữ đủ3modality, không directRC |

Nguồn hình đã tìm gồm `KLTN/pileline.drawio`, `KLTN/Untitled Diagram.drawio`, `KLTN/pileline.drawio.png`, các hình residual MRI/radiomics/clinical ở root, `KLTN/week7/pileline-Trang-*.drawio.png`, `KLTN/week12/Sơ đồ luồng residual A6 theo M, R, C.png`, và các chart trong báo cáo tuần12. Các hình được redrawn/simplified, sửa routing RC-Free và thống nhất visual style. Mapping chi tiết từng hình tới nguồn nằm trong `figures_source/figure_provenance.json`; data cho chart có archive/member path trong `figures_source/results_data.json`.

## Bảng, typography và bibliography

- Dùng booktabs/tabularx, tên mô hình ngắn, tách bảng classical, MRI milestones, ablation, benchmark, parameters và research questions.
- Không shrink cả bảng bằng resizebox; điều chỉnh chiều cột/font hợp lý và kiểm tra bản PDF thực tế.
- Giữ A4/margins và cỡ chữ13pt từ bản gốc; giảm khoảng trắng đầu chapter, giới hạn TOC tới subsection.
- Sửa metadata của Cox/PCA/Breslow; bổ sung ReLU, Adam và nguồn nghiên cứu của metric; xác minh paper Aghajanian và hai nguồn gated residual/scaling. Danh mục mở rộng cuối cùng và chính sách bỏ báo cáo nội bộ được ghi trong cập nhật references phía trên.
- Chuyển build từ BibLaTeX/Biber sang natbib/BibTeX numeric để source biên dịch được với XeLaTeX hoặc portable Tectonic; DOI/URL vẫn được giữ trong bibliography.

## QA và issues chưa được nghiên cứu giải quyết

- Hoàn thiện float placement: bảng câu hỏi nghiên cứu nằm trước mục tiêu; hình temporal đứng trước Cox objective; các chart kết quả không trôi vào section sau; bảng trả lời RQ và trạng thái formal test nằm chung một trang.
- Đồng nhất trục tensor CP thành `H × dx × dy` và ký hiệu pair feature sau post-MLP thành `E_p` trong sơ đồ gated route.
- Rút chiều cao chart milestones bằng khoảng cách panel, giữ font tối thiểu9.5pt và toàn bộ số liệu; bỏ trang gần trống mà không thu nhỏ chữ.
- Bản cuối có **69 trang tổng cộng**, gồm 13 trang front matter, 49 trang nội dung chính và 7 trang bibliography;16 hình vector theo các chương là1/1/9/4/1.
- Biên dịch bằng Tectonic/XeTeX + BibTeX; không lỗi LaTeX/BibTeX, thiếu references/citations, overfull hoặc missing glyph. Một Underfull hbox nhẹ được kiểm tra trực quan và không ảnh hưởng khả năng đọc.
- Kiểm tra từng trang PDF, bổ sung proof grayscale cho sơ đồ kỹ thuật và cả bốn chart; xác nhận font sử dụng được nhúng,16 PDF/SVG/drawio hợp lệ và10 nguồn chính giữ nguyên checksum.
- Bổ sung script build Windows tự tạo fontconfig khi cần, hướng dẫn biên dịch, QA report và provenance của kiểm tra tích hợp.
- Giải nén ZIP vào thư mục mới rồi biên dịch bằng script đi kèm: cả 69 trang có text và ảnh render trùng bản đã duyệt. Gói cuối kiểm tra CRC, giữ nguyên toàn bộ input đã dùng trong build thử và chứa PDF giống hệt file xuất riêng.

Kết quả kiểm tra source, citation, labels, logs, số trang và kiểm tra trực quan cuối cùng được ghi trong `QUALITY_CHECK.md` và `qa_report.json`. Đây là các giới hạn nghiên cứu còn lại, không phải placeholder trong tài liệu:

- Formal final evaluation chưa thực hiện; lịch sử test cần được công bố và external validation cần thiết.
- Endpoint proxy và cohort điều kiện18tháng chưa tương đương AD diagnosis/prospective baseline cohort.
- Clinical ±90ngày cần kiểm chứng availability theo thời điểm cho triển khai tiến cứu.
- Ba seed trên một split và nhiều lần dùng validation chưa cung cấp bằng chứng statistical superiority.
- Chưa có đồng nhất mọi baseline, missingmodality/external validation, controlledranksweep hoặc latency/memory benchmark.

Source/report gốc và dữ liệu giữ nguyên; không huấn luyện lại và không sửa frozen preprocessing.
